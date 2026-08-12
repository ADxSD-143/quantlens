# QuantLens: ML Market Regime & Risk Analyzer

[![Streamlit App](https://img.shields.io/badge/Streamlit-1.40+-FF4B4B?style=flat-square&logo=streamlit)](https://streamlit.io)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python)](https://www.python.org)
[![License MIT](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)

An unsupervised ML system that discovers recurring market regimes from historical price data and quantifies their risk characteristics and transition behavior.

## 🎯 Project Overview

**QuantLens** uses K-Means clustering on engineered market features to identify distinct market regimes (e.g., "Stable Up", "High-Volatility Range", "Downside Pressure"). For each regime, it calculates:
- **Risk Metrics**: Volatility, Sharpe Ratio, Max Drawdown
- **Return Characteristics**: Daily/annualized returns, trend
- **Transition Probabilities**: How likely regimes follow one another

This is **descriptive historical analysis**, not a price prediction system.

---

## 🏗️ Architecture

```
Live Market Data (Yahoo Finance)
           ↓
    data.py: Multi-market support (US + India)
           ↓
  features.py: 6 engineered features
               • Return 1D, Return 5D
               • Volatility 20D
               • RSI 14
               • MA Spread (20/50)
               • Volume Ratio
           ↓
    model.py: StandardScaler → K-Means → Regime Discovery
              • Configurable clusters (2–5)
              • Silhouette score validation
              • Regime naming (human-readable)
              • Transition matrix (empirical)
           ↓
     eda.py: Plotly visualizations
           ↓
    app.py: Interactive Streamlit Dashboard
```

---

## ✨ Key Features

### 📊 Interactive Dashboard
- **Stock Selector**: 13 US & Indian stocks (AAPL, MSFT, NVDA, RELIANCE.NS, TCS.NS, etc.)
- **Period Selector**: 1y, 2y, 5y, 10y historical data
- **Regime Slider**: Discover 2–5 market clusters dynamically
- **Real-time Metrics**: Current price, regime, 5D return, volatility, RSI

### 🤖 Unsupervised ML
- **K-Means Clustering**: Identifies recurring market patterns
- **Feature Engineering**: Returns, volatility, momentum, trend, volume
- **Standardized Scaling**: Handles different feature scales
- **Silhouette Validation**: Quantifies cluster separation quality

### 📈 Risk Analytics
- **Regime Characteristics**: Volatility, returns, Sharpe ratio per cluster
- **Risk Bands**: "Lower risk", "Moderate risk", "Elevated risk"
- **Transition Matrix**: Row-normalized probabilities (t → t+1)
- **Drawdown Analysis**: Historical peak-to-trough movements

### 💡 Explainability
- **Regime Names**: "Stable Up", "Downside Pressure", "Calm Range", etc.
- **Plain English Descriptions**: "Upside regime with elevated risk, average daily return +0.05%, volatility 18.5%"
- **No Black Boxes**: Every metric is interpretable and financial standards-compliant

---

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- pip / conda

### Installation

```bash
# Clone repository
git clone https://github.com/yourusername/quantlens.git
cd quantlens

# Create virtual environment
python -m venv .venv

# Activate (Windows)
.venv\Scripts\activate.bat

# Activate (macOS/Linux)
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Run the App

```bash
streamlit run app.py
```

Open browser to **`http://localhost:8501`**

---

## 📋 Requirements

```
streamlit>=1.40
yfinance>=0.2.54
pandas>=2.2
numpy>=1.26
scikit-learn>=1.5
plotly>=5.24
```

---

## 📁 Project Structure

```
quantlens/
├── app.py              # Streamlit dashboard
├── data.py             # Yahoo Finance data fetching
├── features.py         # Feature engineering & risk metrics
├── model.py            # K-Means & regime discovery
├── eda.py              # Plotly visualizations
├── requirements.txt    # Dependencies
├── README.md           # This file
└── .gitignore          # Git ignore rules
```

---

## 🔍 How It Works

### 1. Data Acquisition
- Fetches daily OHLCV (Open, High, Low, Close, Volume) from Yahoo Finance
- Supports US stocks (AAPL, MSFT, NVDA, etc.) and Indian stocks (RELIANCE.NS, TCS.NS, etc.)
- Auto-adjusted for splits/dividends

### 2. Feature Engineering
Six behavioral features capture different market dimensions:
```python
Return 1D        → Daily momentum
Return 5D        → 5-day momentum
Volatility 20D   → Short-term risk
RSI 14           → Momentum oscillator (Wilder's smoothing)
MA Spread        → Trend (20/50 moving average ratio)
Volume Ratio     → Participation relative to 20-day average
```

### 3. Standardization & Clustering
- StandardScaler normalizes all features (different scales: RSI 0–100, returns %, volume units)
- K-Means with 25 initializations finds stable clusters
- Silhouette score validates cluster quality (higher = better separation)

### 4. Regime Characterization
For each cluster:
- Calculate mean/median of returns, volatility, RSI, MA spread, volume
- Rank by realized annualized volatility → risk bands
- Combine return profile + risk band → regime name
- Compute transition probabilities empirically

### 5. Dashboard Visualization
- Price timeline with color-coded regime markers
- Regime risk comparison (bar chart)
- Historical drawdown (area chart)
- Silhouette score interpretation
- Regime transition matrix (heatmap-style table)

---

## 📊 Example Usage

```python
from data import load_price_history, SUPPORTED_TICKERS
from features import add_market_features
from model import fit_regime_model

# Load data
ticker = "AAPL"
prices = load_price_history(ticker, period="5y")

# Engineer features
features = add_market_features(prices)

# Discover regimes
analysis = fit_regime_model(features, n_clusters=3)

# Access results
print(f"Current regime: {analysis.current_regime}")
print(f"Silhouette score: {analysis.silhouette_score:.3f}")
print(f"Transition matrix:\n{analysis.transition_matrix}")
```

---

## 🔬 Technical Highlights

### Correct Financial Formulas
- **Sharpe Ratio**: (daily return mean ÷ daily volatility) × √252
- **Annualized Volatility**: daily std × √252
- **CAGR**: (ending / beginning) ^ (252 / trading days) - 1
- **Drawdown**: (current / historical peak) - 1

### Robust ML Practices
- **Silhouette Score**: Quantifies cluster quality
- **Multiple Initializations**: K-Means n_init=25 reduces local minima
- **Reproducibility**: Fixed random_state=42
- **Type Hints**: PEP 484 compliance
- **Edge Case Handling**: NaN/Inf filtering, zero-division checks

### Clean Code
- Modular architecture (data → features → model → viz → UI)
- Comprehensive docstrings
- Error messages guide users
- No magic numbers (or documented if necessary)

---

## 🎓 Interview Talking Points

### Problem Statement
> "I built an unsupervised ML system to discover recurring market regimes from historical price data. The goal: understand *what states* the market enters, not *predict future prices*."

### Approach
> "I engineered six interpretable features (returns, volatility, RSI, trend, volume), standardized them, and used K-Means clustering. Each regime is characterized by risk metrics and transition probabilities."

### Key Decision: Why K-Means?
> "K-Means is fast, interpretable, and the silhouette score gives me a quality metric. For this historical analysis, it's appropriate. If I added predictive capability, I'd consider HMM or regime-switching models."

### Honesty About Limitations
> "QuantLens is descriptive, not predictive. It tells you what happened historically, not what will happen. This is an important distinction for financial analysis."

### Next Steps
> "The natural extension is backtesting: if I used these regime signals for risk management, what would historical returns look like? I'd implement walk-forward validation to avoid look-ahead bias."

---

## 📈 Example Output

**Current Market State (AAPL, 5y)**
```
Current Price: $195.34
Change: +1.23% vs previous close

Current Regime: Stable Up · Lower risk
Description: Upside regime with lower risk, average daily return +0.08%, 
             and annualized volatility 15.2%.

Silhouette Score: 0.387
Interpretation: Moderately separated regimes

Regime Characteristics:
┌──────────────────────────────────────────────────────┐
│ Regime             │ Volatility │ Avg Return │ Count │
├──────────────────────────────────────────────────────┤
│ Stable Up          │ 15.2%      │ +0.08%     │ 847   │
│ Momentum Up        │ 22.5%      │ +0.12%     │ 423   │
│ High-Volatility Up │ 35.8%      │ +0.11%     │ 156   │
└──────────────────────────────────────────────────────┘

Transition Matrix:
                    Stable Up  Momentum Up  High-Vol Up
Stable Up           78.5%      18.2%        3.3%
Momentum Up         12.4%      72.1%        15.5%
High-Volatility Up  8.1%       22.3%        69.6%
```

---

## 🧪 Testing & Validation

Currently, the project includes:
- ✅ Data validation (Yahoo Finance, column checks)
- ✅ Input validation (ticker, period, cluster count)
- ✅ Mathematical validation (Silhouette score, NaN checks)

Future improvements:
- Unit tests for RSI calculation, feature engineering
- Integration tests for end-to-end pipeline
- Backtesting module with walk-forward validation

---

## 🤝 Contributing

Contributions welcome! Areas for improvement:
1. Unit test suite
2. Backtesting framework (walk-forward validation)
3. Predictive regime transitions (HMM, Markov switching)
4. More technical indicators
5. Portfolio-level regime analysis
6. Export to CSV/Excel

---

## 📝 License

MIT License — See [LICENSE](LICENSE) for details.

---

## 🔗 Links

- **GitHub**: [github.com/yourusername/quantlens](https://github.com/yourusername/quantlens)
- **LinkedIn**: [Post link]
- **Live Demo**: [Streamlit Cloud link if deployed]

---

## 👤 Author

**Your Name**
- GitHub: [@yourusername](https://github.com/yourusername)
- LinkedIn: [linkedin.com/in/yourprofile](https://linkedin.com/in/yourprofile)
- Email: your.email@example.com

---

## 📞 Support

Found a bug or have a feature request? Open an issue on GitHub!

---

## 🙏 Acknowledgments

- Yahoo Finance for market data
- Scikit-learn for K-Means clustering
- Streamlit for interactive dashboards
- Plotly for beautiful charts

---

**Last Updated**: August 2024
**Version**: 1.0.0
