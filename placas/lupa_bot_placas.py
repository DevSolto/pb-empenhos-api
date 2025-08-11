import pyautogui
import pyperclip
import time
import re
import csv
import os

# Lista de placas a consultar
placas = [
    "QSE6662", "QSE6G62", "QSF2743", "QSF5809", "QXF0I85", "RLQ1D50", "RLQ1050", "RLQ1D50",
    "RLW6A83", "RLW8672", "RLW8G72", "RLX0D19", "RLX0D19", "RLX4A36", "RLX4A46", "RLX7I97",
    "RUN9129", "RUN9I29", "SDI8J58", "SKU9F88", "SKV9F88", "SKX4C74", "SKX7A83", "SKX7B03",
    "SKX7B83", "SLC8C19", "SLD4J42", "SLD6G90", "SLF9G19", "SLF9G49", "TOT5D69", "TOX8J45",
    "TOX8J55", "TOZ7B70"
]


# Função para extrair os dados da página
def extrair_dados(texto):
    dados = {}

    match_modelo = re.search(r'Marca/Modelo\s+(.+)', texto)
    if match_modelo:
        dados["marca_modelo"] = match_modelo.group(1).strip()

    match_placa = re.search(r'Placa\s+([A-Z0-9]{7})', texto)
    if match_placa:
        dados["placa"] = match_placa.group(1)

    match_chassi = re.search(r'Chassi\s+(\w+)', texto)
    if match_chassi:
        dados["chassi"] = match_chassi.group(1)

    match_ano = re.search(r'Ano Fabricação/Modelo\s+(\d{4})/(\d{4})', texto)
    if match_ano:
        dados["ano_fabricacao"] = match_ano.group(1)
        dados["ano_modelo"] = match_ano.group(2)

    return dados

# Nome do arquivo de saída
arquivo_csv = "placas_consultadas.csv"

# Cria ou sobrescreve o arquivo CSV
with open(arquivo_csv, mode="w", newline="", encoding="utf-8") as csvfile:
    campos = ["placa", "marca_modelo", "chassi", "ano_fabricacao", "ano_modelo"]
    writer = csv.DictWriter(csvfile, fieldnames=campos, delimiter=";")
    writer.writeheader()

    # Loop pelas placas
    for i, placa in enumerate(placas, start=1):
        print(f"[{i}/{len(placas)}] Consultando placa: {placa}")

        time.sleep(3)  # Aguarda o carregamento do ambiente
        # Abrir nova aba
        pyautogui.hotkey("ctrl", "t")
        time.sleep(1)

        # Acessar o site
        pyperclip.copy("https://www.lupaveicular.com")
        pyautogui.hotkey("ctrl", "v")
        time.sleep(1)
        pyautogui.press("enter")
        time.sleep(6)

        # Navegar até o input
        for _ in range(7):
            pyautogui.press("tab")
            time.sleep(0.2)

        # Colar placa e buscar
        pyperclip.copy(placa)
        pyautogui.hotkey("ctrl", "v")
        time.sleep(0.5)
        pyautogui.press("enter")
        time.sleep(10)

        # Copiar conteúdo
        pyautogui.hotkey("ctrl", "a")
        pyautogui.hotkey("ctrl", "c")
        time.sleep(0.5)
        conteudo = pyperclip.paste()

        if "Não foi possível carregar as informações" in conteudo:
            continue


        # Fechar aba
        pyautogui.hotkey("ctrl", "w")

        # Extrair e salvar
        dados = extrair_dados(conteudo)
        if not dados.get("placa"):
            continue
        writer.writerow({
            "placa": dados.get("placa", ""),
            "marca_modelo": dados.get("marca_modelo", ""),
            "chassi": dados.get("chassi", ""),
            "ano_fabricacao": dados.get("ano_fabricacao", ""),
            "ano_modelo": dados.get("ano_modelo", ""),
        })
        print("→ Salvo com sucesso:", dados)
