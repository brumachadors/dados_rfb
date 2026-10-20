import sqlite3
import pandas as pd
import glob

padrao_busca = r"C:\dados_rfb\03_sqlite_file\*.db"
arquivos_db = glob.glob(padrao_busca)

if not arquivos_db:
    raise FileNotFoundError("Nenhum banco de dados foi encontrado na pasta.")

caminho_banco = arquivos_db[0]
print(f"Conectado ao banco: {caminho_banco}\n")

conexao = sqlite3.connect(caminho_banco)

print("Verificando e criando índices de performance (se já existirem, passa rápido)...")
cursor = conexao.cursor()

cursor.execute("CREATE INDEX IF NOT EXISTS idx_emp_cnpj ON empresas (cnpj_basico);")
cursor.execute("CREATE INDEX IF NOT EXISTS idx_est_cnae ON estabelecimento (cnae_fiscal);")
cursor.execute("CREATE INDEX IF NOT EXISTS idx_est_situacao ON estabelecimento (situacao_cadastral);")
cursor.execute("CREATE INDEX IF NOT EXISTS idx_est_mun ON estabelecimento (municipio);")

conexao.commit()
print("Índices prontos!\n")

print("Extraindo e filtrando os estabelecimentos para o ArcGIS...")

cnaes_alvo = (
    '8610101', '8610102', '8532500', 
    '9311500', '6822600',            
    '5222200', '5223100', '5240101'  
)

query_polos = f"""
    WITH filtrados AS (
        SELECT 
            e.cnpj_basico, e.cnpj, e.nome_fantasia, e.tipo_logradouro, 
            e.logradouro, e.numero, e.complemento, e.bairro, e.cep, 
            e.uf, e.cnae_fiscal, m.descricao AS municipio_nome
        FROM estabelecimento e
        JOIN municipio m ON e.municipio = m.codigo
        WHERE e.cnae_fiscal IN {cnaes_alvo}
          AND e.situacao_cadastral = '02'
          AND m.descricao = 'SAO PAULO' 
          AND e.uf = 'SP'
    )
    SELECT 
        f.cnpj,
        emp.razao_social,
        f.nome_fantasia,
        f.tipo_logradouro,
        f.logradouro,
        f.numero,
        f.complemento,
        f.bairro,
        f.cep,
        f.municipio_nome,
        f.uf,
        f.cnae_fiscal,
        emp.natureza_juridica
    FROM filtrados f
    JOIN empresas emp ON f.cnpj_basico = emp.cnpj_basico
    WHERE f.logradouro IS NOT NULL AND f.logradouro != ''
      AND f.numero IS NOT NULL AND f.numero != ''
      AND UPPER(f.logradouro) NOT LIKE '%CAIXA POSTAL%'
      AND emp.natureza_juridica != '2135'
"""

df_polos = pd.read_sql_query(query_polos, conexao)
conexao.close()

df_polos['endereco_completo'] = df_polos['tipo_logradouro'].fillna('') + " " + \
                                df_polos['logradouro'].fillna('') + ", " + \
                                df_polos['numero'].fillna('') + ", " + \
                                df_polos['bairro'].fillna('') + ", " + \
                                df_polos['municipio_nome'].fillna('') + " - " + \
                                df_polos['uf'].fillna('') + ", " + \
                                df_polos['cep'].fillna('')

df_polos['endereco_completo'] = df_polos['endereco_completo'].str.replace('  ', ' ')

df_polos
caminho_csv = r"D:\dados_rfb\polos_geradores_sp_sem_mei.csv"
df_polos.to_csv(caminho_csv, index=False, encoding='utf-8-sig')

print(f"\nSucesso! {len(df_polos)} estabelecimentos foram filtrados.")
print(f"O arquivo pronto para importar no ArcGIS está em: {caminho_csv}")

display(df_polos.head())
