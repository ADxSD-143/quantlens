"""Yahoo Finance data access for QuantLens."""

from __future__ import annotations

from pathlib import Path
from tempfile import gettempdir

import pandas as pd
import yfinance as yf
import yfinance.cache as yf_cache


SUPPORTED_TICKERS: dict[str, str] = {
    "AAPL": "Apple (US)",
    "MSFT": "Microsoft (US)",
    "NVDA": "NVIDIA (US)",
    "GOOGL": "Alphabet (US)",
    "AMZN": "Amazon (US)",
    "TSLA": "Tesla (US)",
    "SPY": "SPDR S&P 500 ETF (US)",
    "QQQ": "Invesco QQQ ETF (US)",
    "RELIANCE.NS": "Reliance Industries (India)",
    "TCS.NS": "Tata Consultancy Services (India)",
    "INFY.NS": "Infosys (India)",
    "HDFCBANK.NS": "HDFC Bank (India)",
    "ICICIBANK.NS": "ICICI Bank (India)",
}


def get_currency(ticker: str) -> tuple[str, str]:
    """Return the display currency symbol and ISO currency for a ticker."""
    return ("₹", "INR") if ticker.upper().endswith(".NS") else ("$", "USD")


def _flatten_columns(data: pd.DataFrame, ticker: str) -> pd.DataFrame:
    """Make yfinance's single-ticker output use simple OHLCV columns."""
    if not isinstance(data.columns, pd.MultiIndex):
        return data

    ticker_level = data.columns.get_level_values(-1)
    if ticker in ticker_level:
        return data.xs(ticker, axis=1, level=-1, drop_level=True)

    flattened = data.copy()
    flattened.columns = flattened.columns.get_level_values(0)
    return flattened


def _configure_yfinance_cache() -> None:
    """Keep Yahoo Finance's small cookie cache outside the source tree."""
    cache_path = Path(gettempdir()) / "quantlens-yfinance"
    yf_cache.set_cache_location(str(cache_path))


def load_price_history(ticker: str, period: str = "5y") -> pd.DataFrame:
    """Load adjusted daily OHLCV data for one security from Yahoo Finance."""
    symbol = ticker.strip().upper()
    if not symbol:
        raise ValueError("Choose or enter a valid ticker symbol.")

    _configure_yfinance_cache()
    history = yf.download(
        symbol,
        period=period,
        interval="1d",
        auto_adjust=True,
        progress=False,
        threads=False,
    )
    history = _flatten_columns(history, symbol)
    if history.empty:
        raise ValueError(f"Yahoo Finance returned no daily data for {symbol}.")

    required_columns = {"Close", "High", "Low", "Open", "Volume"}
    missing_columns = required_columns.difference(history.columns)
    if missing_columns:
        names = ", ".join(sorted(missing_columns))
        raise ValueError(f"The downloaded data is missing required columns: {names}.")

    history.index = pd.to_datetime(history.index)
    history.index.name = "Date"
    return history.sort_index().dropna(subset=["Close"])
