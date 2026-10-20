from rfbpy import RFBData

diretorio_base = r"D:\dados_rfb"

rfb = RFBData(
    processing_dir=diretorio_base,
    month="2026-09"
)

print("download e montagem do banco")
resultado = rfb.run(destination="sqlite")

caminho_banco = resultado.load.path
print(f"sucesso em: {caminho_banco}")