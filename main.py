import pyautogui
import pyperclip
import time
import json
import os

# Configurações
ANO = 2024
UNIDADE_GESTORA = "201157"
PAGE_SIZE = 50
OUTPUT_DIR = "201157-saida_manual_navegador"
DELAY_ABA = 4
DELAY_ENTRE_ITERACOES = 3

os.makedirs(OUTPUT_DIR, exist_ok=True)

def montar_url(ano, mes, page, ug, size):
    ano_mes = f"{ano}{mes:02d}"
    return f"https://sagrescidadao.tce.pb.gov.br/api/municipal/despesas/funcoes/empenhos?unidades_gestoras={ug}&page={page}&size={size}&ano_mes={ano_mes}"

def abrir_url_no_navegador(url):
    pyautogui.hotkey("ctrl", "t")
    time.sleep(1)
    pyperclip.copy(url)
    pyautogui.hotkey("ctrl", "v")
    time.sleep(1)
    pyautogui.press("enter")
    time.sleep(DELAY_ABA)

def copiar_conteudo_pagina():
    pyautogui.hotkey("ctrl", "a")
    time.sleep(0.5)
    pyautogui.hotkey("ctrl", "c")
    time.sleep(1)
    return pyperclip.paste()

def fechar_aba():
    pyautogui.hotkey("ctrl", "w")
    time.sleep(0.5)

# Execução
for mes in range(12, 13):  # ajuste aqui se quiser só o mês 6, por exemplo: range(6, 7)
    pagina = 1
    time.sleep(DELAY_ENTRE_ITERACOES)
    while True:
        url = montar_url(ANO, mes, pagina, UNIDADE_GESTORA, PAGE_SIZE)
        print(f"Abrindo: {url}")
        abrir_url_no_navegador(url)

        conteudo = copiar_conteudo_pagina()
        fechar_aba()

        try:
            dados = json.loads(conteudo)
            empenhos = dados.get("_embedded", {}).get("empenhos", [])
            if dados.get("count", 0) == 0 or not empenhos:
                print(f"Fim dos dados para {mes:02d}")
                break
        except Exception as e:
            print(f"Erro ao interpretar JSON: {e}")
            break

        filename = f"{OUTPUT_DIR}/empenhos_{ANO}{mes:02d}_p{pagina}.json"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(conteudo)
        print(f"Salvo: {filename}")
        pagina += 1
