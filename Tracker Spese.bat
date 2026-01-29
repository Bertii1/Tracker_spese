@echo off
cd /d "%~dp0"

if not exist "venv" (
    echo Primo avvio - installazione in corso...
    python -m venv venv
    call venv\Scripts\activate.bat
    pip install flask
    echo Installazione completata!
) else (
    call venv\Scripts\activate.bat
)

start http://127.0.0.1:5000
python app.py
