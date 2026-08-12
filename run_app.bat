@echo off
cd /d "D:\project ideas\stock condition"

echo.
echo ========================================
echo Fixing Pandas Environment...
echo ========================================
echo.

REM Reinstall pandas and numpy
".venv\Scripts\pip.exe" install --force-reinstall --no-cache-dir pandas numpy scikit-learn plotly yfinance streamlit

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ERROR: Reinstall failed. Attempting full venv recreation...
    rmdir /s /q .venv
    python -m venv .venv
    ".venv\Scripts\pip.exe" install --upgrade pip setuptools wheel
    ".venv\Scripts\pip.exe" install -r requirements.txt
)

echo.
echo ========================================
echo Starting QuantLens App...
echo ========================================
echo.

".venv\Scripts\streamlit.exe" run app.py

pause
