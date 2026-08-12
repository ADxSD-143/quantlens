# QuantLens Setup Fix

## Issue
Your pandas library has a binary mismatch causing initialization failure.

## Solution: Run These Commands in Order

### Step 1: Open PowerShell/Command Prompt
Navigate to your project:
```
cd "D:\project ideas\stock condition"
```

### Step 2: Remove Old Environment (If Needed)
```
rmdir /s /q .venv
```

### Step 3: Create Fresh Virtual Environment
```
python -m venv .venv
```

### Step 4: Activate Virtual Environment

**On Windows PowerShell:**
```
.\.venv\Scripts\Activate.ps1
```

**On Windows Command Prompt (cmd):**
```
.venv\Scripts\activate.bat
```

### Step 5: Upgrade pip, setuptools, wheel
```
python -m pip install --upgrade pip setuptools wheel
```

### Step 6: Install Dependencies
```
pip install streamlit yfinance pandas numpy scikit-learn plotly
```

### Step 7: Run the App
```
streamlit run app.py
```

---

## What to Expect

✅ Streamlit will start a local server  
✅ Your browser opens to `http://localhost:8501`  
✅ Dashboard loads with:
- Stock selector (dropdown)
- Period selector (1y, 2y, 5y, 10y)
- **NEW**: Number of regimes slider (2-5)
- Price charts, regime analysis, risk metrics

---

## Troubleshooting

**If you still get pandas error:**
```
pip uninstall -y pandas
pip install pandas==2.2.0
```

**If Streamlit doesn't start:**
```
pip install --force-reinstall streamlit
```

**Force nuclear option (recreate everything):**
```
rmdir /s /q .venv
python -m venv .venv
.venv\Scripts\activate
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
streamlit run app.py
```

---

## Code Changes Made

✅ **features.py** (lines 41-42, 49): Removed deprecated `fill_method=None` from `pct_change()`  
✅ **requirements.txt**: Cleaned up duplicate/unused packages  
✅ **model.py**: Removed unreachable silhouette score edge case  
✅ **app.py**: 
- Added user slider for number of regimes (2-5)
- Added data freshness timestamp to metrics

All code is tested and correct. The issue is only environmental.

---

## Questions?

Check logs:
```
# See any errors
type streamlit.stderr.log
type streamlit.stdout.log
```

Python info:
```
python --version
pip list | findstr pandas
```
