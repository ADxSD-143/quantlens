# QuantLens

### ML Market Regime & Risk Analyzer

QuantLens is a machine-learning based quantitative finance project that analyzes historical stock-market data and identifies recurring market regimes using unsupervised learning.

Instead of predicting stock prices directly, QuantLens uses **K-Means clustering** to discover different market states based on returns, volatility, RSI, momentum, trend, and volume.

## Features

- Live historical market data using Yahoo Finance
- Configurable stock and analysis period
- Quantitative feature engineering
- K-Means based market-regime detection
- StandardScaler feature normalization
- Silhouette Score for cluster validation
- Regime transition matrix
- Volatility and drawdown analysis
- Sharpe Ratio
- Interactive Streamlit dashboard

## ML Pipeline

```text
Yahoo Finance
      ↓
OHLCV Data
      ↓
Feature Engineering
      ↓
StandardScaler
      ↓
K-Means Clustering
      ↓
Market Regimes
      ↓
Risk & Transition Analysis
      ↓
Streamlit Dashboard

Features Used
Daily Return
5-Day Return
20-Day Volatility
RSI
Momentum
Moving Average Spread
Volume Ratio
Drawdown
Tech Stack
Python
Pandas
NumPy
Scikit-learn
yfinance
Plotly
Streamlit
Project Structure
quantlens/
├── app.py
├── data.py
├── features.py
├── model.py
├── eda.py
├── fix_and_run.py
├── run.bat
├── requirements.txt
├── README.md
├── LICENSE
└── .gitignore
Run Locally
git clone https://github.com/ADxSD-143/quantlens.git
cd quantlens

python -m venv .venv
.venv\Scripts\activate

pip install -r requirements.txt

streamlit run app.py
Important

QuantLens is a research and educational project. The discovered regimes describe historical market behavior and are not guaranteed predictions or financial advice.

Author

Aditya Narayan Laha
B.Tech CSE — IIIT Bhubaneswar
