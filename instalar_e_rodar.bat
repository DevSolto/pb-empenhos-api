@echo off
setlocal
REM Cria venv
python -m venv venv
if errorlevel 1 (
  echo [ERRO] Nao foi possivel criar o venv. Verifique o Python no PATH.
  pause
  exit /b 1
)

call venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt

REM Executa o pipeline
python run_pipeline.py

echo.
echo [OK] Concluido. Pressione uma tecla para sair.
pause
