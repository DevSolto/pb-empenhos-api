import subprocess
import sys
import shlex

def run(cmd):
    print(f"→ {cmd}")
    try:
        # Usa shell=False no Windows e POSIX; shlex.split para segurança
        subprocess.run(shlex.split(cmd), check=True)
    except subprocess.CalledProcessError as e:
        print(f"Erro executando: {cmd}\n{e}")
        sys.exit(e.returncode)

if __name__ == "__main__":
    # 1) Coleta por navegador (salva em ./saida_manual_navegador)
    run("python main.py")

    # 2) Junta tudo em empenhos_merged.json
    run("python juntar_empenhos.py")

    # 3) Pega os detalhes dos empenhos
    run("python detalhes.py")

    print("✅ Pipeline finalizado com sucesso!")
