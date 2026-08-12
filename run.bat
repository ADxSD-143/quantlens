@echo off
setlocal enabledelayedexpansion

cls
echo.
echo ╔════════════════════════════════════════════════════════╗
echo ║          QUANTLENS - Starting Application             ║
echo ╚════════════════════════════════════════════════════════╝
echo.

cd /d "D:\project ideas\stock condition"

REM Check if venv exists
if not exist ".venv\Scripts\streamlit.exe" (
    echo [!] Virtual environment not found. Creating...
    python -m venv .venv
    echo [+] Created .venv
)

echo [+] Checking dependencies...
.venv\Scripts\pip.exe install -q streamlit yfinance pandas numpy scikit-learn plotly 2>nul

echo [+] Starting Streamlit...
echo.
echo ════════════════════════════════════════════════════════
echo Open your browser to: http://localhost:8501
echo ════════════════════════════════════════════════════════
echo.

.venv\Scripts\streamlit.exe run app.py

pause
