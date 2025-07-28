import json
import os
from typing import List

import requests
from tqdm import tqdm

import config


def fetch_empenhos_mes(ano: int, mes: int, unidade_gestora: str, session: requests.Session) -> List[dict]:
    """Coleta lista de empenhos para um mes especifico."""
    ano_mes = f"{ano}{mes:02d}"
    page = 0
    resultados: List[dict] = []

    while True:
        params = {
            "unidades_gestoras": unidade_gestora,
            "page": page,
            "size": config.PAGE_SIZE,
            "ano_mes": ano_mes,
        }
        resp = session.get(config.BASE_URL, params=params, timeout=30)
        resp.raise_for_status()
        dados = resp.json()

        # Tentamos suportar diferentes formatos de retorno
        itens = dados.get("content") or dados.get("data") or dados
        if not itens:
            break
        resultados.extend(itens)

        # Verifica se existe próxima página
        if dados.get("last") or len(itens) < config.PAGE_SIZE:
            break
        page += 1

    return resultados


def coletar_empenhos_ano():
    os.makedirs(config.OUTPUT_DIR, exist_ok=True)
    session = requests.Session()
    todos: List[dict] = []

    for mes in tqdm(range(1, 13), desc="Meses"):
        itens = fetch_empenhos_mes(config.ANO, mes, config.UNIDADE_GESTORA, session)
        todos.extend(itens)

    caminho = os.path.join(config.OUTPUT_DIR, f"empenhos_{config.ANO}.json")
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(todos, f, ensure_ascii=False, indent=2)

    print(f"Total de empenhos coletados: {len(todos)}")
    print(f"Arquivo salvo em: {caminho}")


if __name__ == "__main__":
    coletar_empenhos_ano()
