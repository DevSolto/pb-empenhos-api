import json
import csv
from pathlib import Path

# Caminhos
ARQUIVO_JSON = "empenhos_merged.json"
ARQUIVO_CSV = "empenhos_merged.csv"

# Campos que vamos exportar
CAMPOS = [
    "codigo_unidade_gestora",
    "codigo_unidade_orcamentaria",
    "numero_empenho",
    "classificacao",
    "data_empenho",
    "codigo_credor",
    "nome_credor",
    "valor_contratado",
    "valor_pago"
]

def json_para_csv(json_path: str, csv_path: str):
    with open(json_path, "r", encoding="utf-8") as f:
        empenhos = json.load(f)

    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CAMPOS, delimiter=";")
        writer.writeheader()
        for item in empenhos:
            item["codigo_credor"] = f"'{item.get('codigo_credor', '')}"
            item["numero_empenho"] = f"'{item.get('numero_empenho', '')}"
            writer.writerow({campo: item.get(campo, "") for campo in CAMPOS})

    print(f"Arquivo CSV gerado: {csv_path}")

if __name__ == "__main__":
    json_para_csv(ARQUIVO_JSON, ARQUIVO_CSV)