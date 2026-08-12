#!/usr/bin/env python3
"""
QuantLens Environment Fixer
Automatically fixes pandas/environment issues and launches the app.
"""

import subprocess
import sys
import os
import shutil
from pathlib import Path

PROJECT_DIR = Path(__file__).parent
VENV_DIR = PROJECT_DIR / ".venv"

def run_cmd(cmd, description):
    """Run command and return success status."""
    print(f"\n{'='*60}")
    print(f"▶ {description}")
    print(f"{'='*60}")
    print(f"Command: {cmd}\n")
    
    try:
        result = subprocess.run(cmd, shell=True, cwd=PROJECT_DIR)
        if result.returncode == 0:
            print(f"✅ {description} — SUCCESS\n")
            return True
        else:
            print(f"❌ {description} — FAILED (code {result.returncode})\n")
            return False
    except Exception as e:
        print(f"❌ {description} — ERROR: {e}\n")
        return False

def main():
    os.chdir(PROJECT_DIR)
    print(f"\n🔧 QuantLens Environment Fixer")
    print(f"📂 Project: {PROJECT_DIR}\n")
    
    # Step 1: Check if venv exists
    if VENV_DIR.exists():
        print(f"ℹ️  Virtual environment found at {VENV_DIR}")
        response = input("Recreate venv? (y/n) [default: y]: ").strip().lower()
        if response != "n":
            print(f"\n🗑️  Removing old venv...")
            shutil.rmtree(VENV_DIR, ignore_errors=True)
            print(f"✅ Removed\n")
    
    # Step 2: Create venv
    if not VENV_DIR.exists():
        if not run_cmd(f"{sys.executable} -m venv .venv", "Creating virtual environment"):
            print("❌ Failed to create venv. Exiting.")
            sys.exit(1)
    
    # Detect pip executable
    pip_exe = VENV_DIR / ("Scripts" if sys.platform == "win32" else "bin") / ("pip.exe" if sys.platform == "win32" else "pip")
    python_exe = VENV_DIR / ("Scripts" if sys.platform == "win32" else "bin") / ("python.exe" if sys.platform == "win32" else "python")
    
    print(f"🔍 Using Python: {python_exe}")
    print(f"🔍 Using pip: {pip_exe}\n")
    
    # Step 3: Upgrade pip
    run_cmd(f"{pip_exe} install --upgrade pip setuptools wheel", "Upgrading pip, setuptools, wheel")
    
    # Step 4: Install dependencies
    deps = [
        "streamlit>=1.40",
        "yfinance>=0.2.54",
        "pandas>=2.2",
        "numpy>=1.26",
        "scikit-learn>=1.5",
        "plotly>=5.24"
    ]
    
    for dep in deps:
        run_cmd(f"{pip_exe} install --upgrade {dep}", f"Installing {dep}")
    
    # Step 5: Verify imports
    print(f"\n{'='*60}")
    print("✅ Verifying imports...")
    print(f"{'='*60}\n")
    
    try:
        import pandas
        print(f"✅ pandas {pandas.__version__} OK")
    except Exception as e:
        print(f"❌ pandas import failed: {e}")
    
    try:
        import streamlit
        print(f"✅ streamlit {streamlit.__version__} OK")
    except Exception as e:
        print(f"❌ streamlit import failed: {e}")
    
    try:
        import sklearn
        print(f"✅ scikit-learn {sklearn.__version__} OK")
    except Exception as e:
        print(f"❌ scikit-learn import failed: {e}")
    
    try:
        import plotly
        print(f"✅ plotly {plotly.__version__} OK")
    except Exception as e:
        print(f"❌ plotly import failed: {e}")
    
    # Step 6: Launch app
    print(f"\n{'='*60}")
    print("🚀 Launching QuantLens App...")
    print(f"{'='*60}\n")
    
    streamlit_exe = VENV_DIR / ("Scripts" if sys.platform == "win32" else "bin") / ("streamlit.exe" if sys.platform == "win32" else "streamlit")
    
    if streamlit_exe.exists():
        os.system(f"{streamlit_exe} run app.py")
    else:
        print(f"❌ streamlit not found at {streamlit_exe}")
        print(f"Trying alternative: {pip_exe} -m streamlit run app.py")
        os.system(f"{pip_exe} -m streamlit run app.py")

if __name__ == "__main__":
    main()
