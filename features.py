"""Feature engineering and non-predictive risk calculations for QuantLens."""

from __future__ import annotations

import numpy as np
import pandas as pd


CLUSTER_FEATURES = [
    "Return 1D",
    "Return 5D",
    "Volatility 20D",
    "RSI 14",
    "MA Spread",
    "Volume Ratio",
]


def calculate_rsi(close: pd.Series, window: int = 14) -> pd.Series:
    """Calculate Wilder's Relative Strength Index."""
    change = close.diff()
    gains = change.clip(lower=0)
    losses = -change.clip(upper=0)
    average_gain = gains.ewm(alpha=1 / window, adjust=False, min_periods=window).mean()
    average_loss = losses.ewm(alpha=1 / window, adjust=False, min_periods=window).mean()
    relative_strength = average_gain / average_loss.replace(0, np.nan)
    rsi = 100 - (100 / (1 + relative_strength))
    rsi = rsi.mask((average_loss == 0) & (average_gain > 0), 100)
    return rsi.mask((average_gain == 0) & (average_loss > 0), 0)


def add_market_features(history: pd.DataFrame) -> pd.DataFrame:
    """Add return, volatility, momentum, trend, volume, and drawdown features."""
    if "Close" not in history.columns:
        raise ValueError("Price history must include a Close column.")

    frame = history.copy()
    close = frame["Close"].astype(float)
    volume = frame["Volume"].astype(float)

    frame["Return 1D"] = close.pct_change()
    frame["Return 5D"] = close.pct_change(5)
    frame["Log Return"] = np.log(close / close.shift(1))
    frame["Volatility 20D"] = frame["Return 1D"].rolling(20).std() * np.sqrt(252)
    frame["RSI 14"] = calculate_rsi(close)
    frame["MA 20"] = close.rolling(20).mean()
    frame["MA 50"] = close.rolling(50).mean()
    frame["MA Spread"] = (frame["MA 20"] / frame["MA 50"]) - 1
    frame["Momentum 20D"] = close.pct_change(20)
    frame["Volume MA 20"] = volume.rolling(20).mean()
    frame["Volume Ratio"] = volume / frame["Volume MA 20"].replace(0, np.nan)
    frame["Rolling Peak"] = close.cummax()
    frame["Drawdown"] = (close / frame["Rolling Peak"]) - 1
    return frame


def calculate_risk_metrics(data: pd.DataFrame) -> dict[str, float]:
    """Return annualized whole-sample metrics; they describe history, not forecasts."""
    returns = data["Return 1D"].dropna()
    if returns.empty:
        raise ValueError("At least two price observations are required for risk metrics.")

    annualized_return = (1 + returns).prod() ** (252 / len(returns)) - 1
    annualized_volatility = returns.std(ddof=1) * np.sqrt(252)
    sharpe = (
        (returns.mean() / returns.std(ddof=1)) * np.sqrt(252)
        if returns.std(ddof=1) > 0
        else np.nan
    )
    return {
        "Annualized Return": annualized_return,
        "Annualized Volatility": annualized_volatility,
        "Sharpe Ratio": sharpe,
        "Max Drawdown": data["Drawdown"].min(),
    }
