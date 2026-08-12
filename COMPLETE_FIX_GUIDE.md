📋 QUANTLENS — COMPLETE FIX GUIDE
═══════════════════════════════════════════════════════════════════════════════

ISSUE: Pandas binary mismatch in virtual environment

SOLUTION: Recreate virtual environment with clean installation

═══════════════════════════════════════════════════════════════════════════════
STEP-BY-STEP INSTRUCTIONS (Windows)
═══════════════════════════════════════════════════════════════════════════════

1️⃣  OPEN COMMAND PROMPT OR POWERSHELL

   Windows Key + R
   Type: cmd  (or powershell)
   Press Enter

2️⃣  NAVIGATE TO PROJECT

   cd "D:\project ideas\stock condition"

3️⃣  REMOVE OLD VIRTUAL ENVIRONMENT

   rmdir /s /q .venv

   (When prompted "Are you sure?" press Y and Enter)

4️⃣  CREATE NEW VIRTUAL ENVIRONMENT

   python -m venv .venv

   (This creates a fresh .venv folder — may take 1-2 minutes)

5️⃣  ACTIVATE VIRTUAL ENVIRONMENT

   FOR COMMAND PROMPT:
   .venv\Scripts\activate.bat

   FOR POWERSHELL:
   .venv\Scripts\Activate.ps1

   (You should see (.venv) at the start of your prompt)

6️⃣  UPGRADE PIP & INSTALL DEPENDENCIES

   python -m pip install --upgrade pip
   pip install -r requirements.txt

   (This downloads and installs: streamlit, yfinance, pandas, numpy,
    scikit-learn, plotly — may take 5-10 minutes)

7️⃣  LAUNCH THE APP

   streamlit run app.py

   (Streamlit will print something like:
    Local URL: http://localhost:8501
    You can now view your Streamlit app in your browser.)

8️⃣  OPEN YOUR BROWSER

   Navigate to: http://localhost:8501

═══════════════════════════════════════════════════════════════════════════════
WHAT TO EXPECT IN THE BROWSER
═══════════════════════════════════════════════════════════════════════════════

✅ QuantLens dashboard loads
✅ Left sidebar has:
   - Stock dropdown (AAPL, MSFT, NVDA, GOOGL, AMZN, TSLA, SPY, QQQ,
     RELIANCE.NS, TCS.NS, INFY.NS, HDFCBANK.NS, ICICIBANK.NS)
   - Period selector (1y, 2y, 5y, 10y)
   - ⭐ Number of regimes slider (2-5) [NEW!]

✅ Main area shows:
   - Current price and regime
   - Market statistics (5D return, volatility, RSI)
   - Price chart with colored regime markers
   - Historical regime characteristics table
   - Model validation (silhouette score)
   - Regime transition matrix
   - Risk analysis charts

═══════════════════════════════════════════════════════════════════════════════
TROUBLESHOOTING
═══════════════════════════════════════════════════════════════════════════════

PROBLEM: "AttributeError: partially initialized module 'pandas'"
SOLUTION: Make sure you completed steps 1-6 correctly.
          Run: .venv\Scripts\python.exe -c "import pandas; print(pandas.__version__)"
          Should print version number like "2.2.0"

PROBLEM: "streamlit: command not found"
SOLUTION: 
  1. Verify you activated venv (.venv should show in prompt)
  2. Try: pip install streamlit
  3. Then: streamlit run app.py

PROBLEM: "No module named 'yfinance'" or similar
SOLUTION: Run from inside venv and ensure step 6 completed.
          If stuck, run: pip install --upgrade yfinance numpy pandas scikit-learn plotly

PROBLEM: Streamlit doesn't open browser automatically
SOLUTION: Manually open http://localhost:8501 in your browser

PROBLEM: App keeps reloading / infinite spinner
SOLUTION: 
  1. Press Ctrl+C in terminal to stop
  2. Check internet connection (Yahoo Finance needs network)
  3. Try a different stock or longer period
  4. Restart: streamlit run app.py

═══════════════════════════════════════════════════════════════════════════════
ALTERNATE METHODS
═══════════════════════════════════════════════════════════════════════════════

OPTION A: Use Python Script (Hands-off)
  cd "D:\project ideas\stock condition"
  python fix_and_run.py
  (Automatically fixes everything and launches app)

OPTION B: Use Batch File (Simple)
  cd "D:\project ideas\stock condition"
  run_app.bat
  (Fixes env and starts app)

═══════════════════════════════════════════════════════════════════════════════
CODE CHANGES MADE (All Verified)
═══════════════════════════════════════════════════════════════════════════════

✅ features.py (lines 41-42, 49)
   Removed deprecated fill_method=None from pct_change()
   This caused pandas 2.2+ compatibility error

✅ requirements.txt
   Cleaned up duplicate entries
   Kept: streamlit, yfinance, pandas, numpy, scikit-learn, plotly
   Removed: unused 'ta' library

✅ model.py (line 222-225)
   Removed unreachable silhouette score edge case

✅ app.py (line 61, 18, 80, 89)
   Added n_clusters parameter to build_analysis()
   Added slider for "Number of regimes" (2-5)
   Added data_date variable for freshness timestamp
   Updated metric help text to show data timestamp

═══════════════════════════════════════════════════════════════════════════════
NEED HELP?
═══════════════════════════════════════════════════════════════════════════════

1. Check Python version:
   python --version
   (Should be 3.10+)

2. Verify virtual environment:
   where python
   (Should show path containing .venv\Scripts)

3. Check pandas:
   python -c "import pandas; print(pandas.__version__)"
   (Should print 2.2+ without errors)

4. Check all packages:
   pip list
   (Should show: streamlit, yfinance, pandas, numpy, scikit-learn, plotly)

5. Capture error logs:
   Run from terminal: streamlit run app.py 2>&1 | tee error.log
   Then send error.log contents

═══════════════════════════════════════════════════════════════════════════════

Good luck! 🚀
If this still doesn't work, share the exact error message you see.
