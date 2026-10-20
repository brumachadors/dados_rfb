# !pip install rfbpy
from rfbpy import RFBData

diretorio_base = r"C:\dados_rfb"

rfb = RFBData(
    processing_dir=diretorio_base,
    month="2026-09"
)
print("Checando arquivos de Setembro de 2026 no servidor da RFB...\n")
rfb.check()