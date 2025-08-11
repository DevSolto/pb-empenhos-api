import pyautogui
import pyperclip
import time
import json
import os
import csv
from datetime import datetime

time.sleep(2)  # Espera inicial

# ========= Configurações =========
ARQUIVO_ENTRADA = "empenhos_merged.json"
ARQUIVO_CSV = "detalhes.csv"
OUTPUT_DIR = "saida_detalhes"
PAGE_WAIT = 5

os.makedirs(OUTPUT_DIR, exist_ok=True)

CAMPOS = [
    "exercicio", "codigo_unidade_gestora", "codigo_unidade_orcamentaria",
    "nome_unidade_orcamentaria", "numero_empenho", "data_empenho", "codigo_elemento",
    "nome_elemento_despesa", "codigo_funcao", "nome_funcao", "codigo_sub_funcao",
    "nome_sub_funcao", "codigo_programa", "nome_programa", "codigo_acao", "nome_acao",
    "nome_credor", "codigo_credor", "historico", "valor_contratado", "valor_realizado", "valor_pago"
]

# ========= Utilitários =========
def montar_url(empenho):
    ano_mes = empenho['data_empenho'].replace("-", "")[:6]
    return (
        f"https://sagrescidadao.tce.pb.gov.br/api/municipal/despesas/funcoes/empenhos/"
        f"{empenho['numero_empenho']}?unidades_gestoras={empenho['codigo_unidade_gestora']}"
        f"&codigo_unidade_orcamentaria={empenho['codigo_unidade_orcamentaria']}"
        f"&ano_mes={ano_mes}"
    )

def abrir_url_no_navegador(url):
    pyautogui.hotkey("ctrl", "t")
    time.sleep(1)
    pyperclip.copy(url)
    pyautogui.hotkey("ctrl", "v")
    time.sleep(1)
    pyautogui.press("enter")
    time.sleep(PAGE_WAIT)

def copiar_conteudo_pagina():
    pyautogui.hotkey("ctrl", "a")
    time.sleep(0.5)
    pyautogui.hotkey("ctrl", "c")
    time.sleep(1)
    return pyperclip.paste()

def fechar_aba():
    pyautogui.hotkey("ctrl", "w")
    time.sleep(0.5)

def salvar_json(data, path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# ========= Carregar dados =========
with open(ARQUIVO_ENTRADA, "r", encoding="utf-8") as f:
    empenhos = json.load(f)

vistos = set()
empenhos_alvo = []
for e in empenhos:
    ano_mes = e['data_empenho'].replace("-", "")[:6]
    chave = (e['numero_empenho'], e['codigo_unidade_gestora'], e['codigo_unidade_orcamentaria'], ano_mes)
    if chave not in vistos:
        vistos.add(chave)
        empenhos_alvo.append(e)

total = len(empenhos_alvo)
print(f"🚀 Iniciando coleta dos detalhes ({total} itens) — {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")

linhas_csv = []
ok_count = 0
err_count = 0

for i, empenho in enumerate(empenhos_alvo, start=1):
    url = montar_url(empenho)
    print(f"[{i}/{total}] Acessando {url}")
    try:
        abrir_url_no_navegador(url)
        conteudo = copiar_conteudo_pagina()
        fechar_aba()

        if not conteudo.strip().startswith("{"):
            err_count += 1
            print(f"Conteúdo inesperado para {url}")
            continue

        dados = json.loads(conteudo)
        empenho_detalhado = dados.get("_embedded", {}).get("empenho", {}) or dados

        linhas_csv.append({campo: empenho_detalhado.get(campo, "") for campo in CAMPOS})

        filename = f"{OUTPUT_DIR}/detalhe_{empenho['numero_empenho']}.json"
        salvar_json(empenho_detalhado, filename)
        ok_count += 1

    except Exception as e:
        err_count += 1
        print(f"Erro no item {i}/{total}: {e}")
        continue

# ========= Gerar CSV =========
with open(ARQUIVO_CSV, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=CAMPOS, delimiter=";")
    writer.writeheader()
    for linha in linhas_csv:
        if linha.get("codigo_credor"):
            linha["codigo_credor"] = f"'{linha['codigo_credor']}"
        if linha.get("numero_empenho"):
            linha["numero_empenho"] = f"'{linha['numero_empenho']}"
        writer.writerow(linha)

print(f"✅ Finalizado {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
print(f"Total: {total} | OK: {ok_count} | Erros: {err_count}")
print(f"Arquivo CSV gerado: {ARQUIVO_CSV}")
