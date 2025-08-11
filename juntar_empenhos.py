import os
import json
from pathlib import Path

# Caminho da pasta com os arquivos JSON
PASTA = "saida_manual_navegador"
CAMINHO_COMPLETO = Path(PASTA)
ARQUIVO_SAIDA = "empenhos_merged.json"

def juntar_empenhos(pasta: Path, arquivo_saida: str):
    empenhos = []

    for arquivo in sorted(pasta.glob("*.json")):
        try:
            with open(arquivo, "r", encoding="utf-8") as f:
                dados = json.load(f)
                empenhos_parciais = dados.get("_embedded", {}).get("empenhos", [])
                empenhos.extend(empenhos_parciais)
        except Exception as e:
            print(f"Erro ao processar {arquivo.name}: {e}")

    with open(arquivo_saida, "w", encoding="utf-8") as f:
        json.dump(empenhos, f, ensure_ascii=False, indent=2)

    print(f"Arquivo final gerado: {arquivo_saida} ({len(empenhos)} empenhos)")

if __name__ == "__main__":
    juntar_empenhos(CAMINHO_COMPLETO, ARQUIVO_SAIDA)