import sqlite3
import pandas as pd
import glob

padrao_busca = r"C:\dados_rfb\03_sqlite_file\*.db"
arquivos_db = glob.glob(padrao_busca)

if not arquivos_db:
    raise FileNotFoundError("Nenhum banco de dados foi encontrado na pasta 03_sqlite_file.")

caminho_banco = arquivos_db[0] # Pega o arquivo encontrado
print(f"Conectado ao banco: {caminho_banco}\n")

conexao = sqlite3.connect(caminho_banco)

print("--- LISTA OFICIAL DE NATUREZAS JURÍDICAS ---")
query_naturezas = "SELECT codigo, descricao FROM natureza ORDER BY codigo"
df_naturezas = pd.read_sql_query(query_naturezas, conexao)

print(df_naturezas.to_string(index=False))
print("\n" + "="*60 + "\n")

