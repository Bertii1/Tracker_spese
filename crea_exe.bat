@echo off
cd /d "%~dp0"

echo ========================================
echo   Creazione eseguibile Tracker Spese
echo ========================================
echo.

if not exist "venv" (
    echo Creazione ambiente virtuale...
    python -m venv venv
)

call venv\Scripts\activate.bat

echo Installazione dipendenze...
pip install flask pyinstaller

echo.
echo Creazione eseguibile...
pyinstaller --noconfirm --onedir --console ^
    --name "Tracker Spese" ^
    --add-data "templates;templates" ^
    --add-data "static;static" ^
    --add-data "data;data" ^
    app.py

echo.
echo ========================================
echo   Fatto!
echo   L'eseguibile si trova in:
echo   dist\Tracker Spese\Tracker Spese.exe
echo ========================================
echo.
pause
