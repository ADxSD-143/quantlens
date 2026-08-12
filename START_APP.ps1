# QuantLens Startup Script
cd "D:\project ideas\stock condition"

Write-Host "`n" -ForegroundColor Cyan
Write-Host "╔════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║     QUANTLENS — Starting App          ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host "`n"

# Verify venv exists
if (-not (Test-Path ".venv\Scripts\streamlit.exe")) {
    Write-Host "❌ Virtual environment not found!" -ForegroundColor Red
    Write-Host "   Creating venv..." -ForegroundColor Yellow
    python -m venv .venv
}

Write-Host "✅ Virtual environment found" -ForegroundColor Green
Write-Host "`n"

# Check if streamlit is installed
Write-Host "🔍 Checking dependencies..." -ForegroundColor Cyan
.venv\Scripts\python.exe -c "import streamlit; print(f'✅ Streamlit {streamlit.__version__}')" 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "⚠️  Streamlit missing, installing..." -ForegroundColor Yellow
    .venv\Scripts\pip.exe install -q streamlit yfinance pandas numpy scikit-learn plotly
}

Write-Host "`n"
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host "🚀 Launching QuantLens on http://localhost:8501" -ForegroundColor Green
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host "`n"

# Run streamlit
.venv\Scripts\streamlit.exe run app.py

Write-Host "`n❌ App stopped" -ForegroundColor Red
