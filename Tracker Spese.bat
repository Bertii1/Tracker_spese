@echo off
cd /d "%~dp0"

if not exist "venv" (
    echo Primo avvio - installazione in corso...
    echo Attendere qualche minuto...
    python -m venv venv
    call venv\Scripts\activate.bat
    pip install flask
    echo.
    echo Installazione completata!
    echo.
) else (
    call venv\Scripts\activate.bat
)

python app.py
