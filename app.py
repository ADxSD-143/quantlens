"""QuantLens — ML Market Regime & Risk Analyzer."""

from __future__ import annotations

import numpy as np
import streamlit as st

from data import SUPPORTED_TICKERS, get_currency, load_price_history
from eda import build_drawdown_figure, build_price_regime_figure, build_regime_risk_figure
from features import add_market_features, calculate_risk_metrics
from model import fit_regime_model, get_regime_colors


st.set_page_config(page_title="QuantLens", page_icon="◉", layout="wide")


@st.cache_data(ttl=900, show_spinner=False)
def build_analysis(ticker: str, period: str, n_clusters: int):
    """Download, engineer features, and discover historical regimes."""
    prices = load_price_history(ticker, period)
    features = add_market_features(prices)
    analysis = fit_regime_model(features, n_clusters=n_clusters)
    return (
        analysis.data,
        analysis.summary,
        analysis.current_regime,
        analysis.current_risk_band,
        analysis.current_description,
        analysis.silhouette_score,
        analysis.silhouette_interpretation,
        analysis.transition_matrix,
    )


def format_percent(value: float, decimals: int = 1) -> str:
    """Render a percentage while retaining an unavailable-data marker."""
    return "—" if not np.isfinite(value) else f"{value:.{decimals}%}"


def regime_icon(risk_band: str) -> str:
    """Choose a visual indicator for a historical risk band."""
    if risk_band == "Lower risk":
        return "🟢"
    if risk_band == "Elevated risk":
        return "🔴"
    return "🟡"


st.title("QUANTLENS")
st.caption("ML Market Regime & Risk Analyzer")

with st.sidebar:
    st.header("Analysis settings")
    ticker = st.selectbox(
        "Stock",
        options=list(SUPPORTED_TICKERS),
        index=0,
        format_func=lambda symbol: f"{symbol} — {SUPPORTED_TICKERS[symbol]}",
    )
    period = st.selectbox("Period", options=["1y", "2y", "5y", "10y"], index=2)
    n_regimes = st.slider("Number of regimes", min_value=2, max_value=5, value=3)
    st.caption("Data: Yahoo Finance · Interval: daily")
    st.divider()
    st.caption(
        "QuantLens uses unsupervised clustering to describe recurring historical market states. "
        "It does not predict whether a price will rise or fall."
    )

try:
    with st.spinner("Loading market history and identifying observed regimes..."):
        (
            labelled_data,
            regime_summary,
            current_regime,
            current_risk_band,
            current_description,
            silhouette,
            silhouette_interpretation,
            transition_matrix,
        ) = build_analysis(ticker, period, n_regimes)

    latest = labelled_data.dropna(subset=["Close"]).iloc[-1]
    previous_close = labelled_data["Close"].iloc[-2]
    one_day_change = (latest["Close"] / previous_close) - 1
    currency_symbol, currency_code = get_currency(ticker)
    regime_colors = get_regime_colors(regime_summary)
    risk_metrics = calculate_risk_metrics(labelled_data)
    characteristic = current_description
    data_date = latest.name.strftime("%d %b %Y, %H:%M")

    first, second = st.columns(2)
    first.metric(
        "Current Price",
        f"{currency_symbol}{latest['Close']:,.2f}",
        f"{one_day_change:+.2%} vs previous close",
        help=f"Adjusted closing price in {currency_code} as of {data_date}.",
    )
    second.metric(
        "Current Regime",
        f"{regime_icon(current_risk_band)} {current_regime} · {current_risk_band}",
        characteristic,
        help="Risk bands compare each cluster's observed volatility within the selected historical period.",
    )

    st.divider()
    st.subheader("Market Statistics")
    metric_one, metric_two, metric_three = st.columns(3)
    metric_one.metric("5D Return", format_percent(float(latest["Return 5D"]), 2))
    metric_two.metric("Volatility (20D)", format_percent(float(latest["Volatility 20D"]), 1))
    metric_three.metric("RSI (14)", f"{latest['RSI 14']:.1f}")

    st.divider()
    st.subheader("Regime Analysis")
    st.plotly_chart(
        build_price_regime_figure(labelled_data, ticker, currency_symbol, regime_colors),
        use_container_width=True,
    )
    st.caption(
        "Each coloured point is assigned to the closest cluster based on standardized return, volatility, "
        "RSI, moving-average spread, and volume features. Cluster IDs are descriptive labels, not forecasts."
    )

    chart_column, table_column = st.columns((1, 1))
    with chart_column:
        st.plotly_chart(build_regime_risk_figure(regime_summary, regime_colors), use_container_width=True)
    with table_column:
        st.markdown("##### Historical regime characteristics")
        display_summary = regime_summary[
            [
                "Regime",
                "Risk Band",
                "Observations",
                "Average_Daily_Return",
                "Annualized_Volatility",
                "Maximum_Drawdown",
            ]
        ].rename(
            columns={
                "Average_Daily_Return": "Avg daily return",
                "Annualized_Volatility": "Ann. volatility",
                "Maximum_Drawdown": "Max drawdown",
            }
        )
        st.dataframe(
            display_summary.style.format(
                {
                    "Avg daily return": "{:.2%}",
                    "Ann. volatility": "{:.1%}",
                    "Max drawdown": "{:.1%}",
                }
            ),
            use_container_width=True,
            hide_index=True,
        )

    st.divider()
    st.subheader("Model Validation")

    validation_one, validation_two = st.columns(2)

    with validation_one:
        st.metric("Silhouette Score", f"{silhouette:.3f}")
        st.caption(silhouette_interpretation)

    with validation_two:
        st.markdown("##### What this means")
        st.caption(
            "Silhouette score measures how well-separated the discovered "
            "market regimes are. Higher values indicate cleaner separation."
        )

    st.markdown("##### Regime Transition Matrix")
    st.caption("Probability of moving from the current regime to another regime on the next trading day.")

    st.dataframe(
        transition_matrix.style.format("{:.1%}"),
        use_container_width=True,
    )

    st.divider()
    st.subheader("Risk Analysis")

    risk_one, risk_two, risk_three = st.columns(3)
    risk_one.metric("Max Drawdown", format_percent(float(risk_metrics["Max Drawdown"]), 1))
    risk_two.metric("Sharpe (0% RF)", f"{risk_metrics['Sharpe Ratio']:.2f}")
    risk_three.metric("Annualized Volatility", format_percent(float(risk_metrics["Annualized Volatility"]), 1))
    st.plotly_chart(build_drawdown_figure(labelled_data), use_container_width=True)

    with st.expander("Methodology and limitations"):
        st.markdown(
            "- Yahoo Finance adjusted daily OHLCV data is transformed into return, volatility, RSI, "
            "trend, and volume features.\n"
            f"- A `StandardScaler` normalizes feature scales before `KMeans` groups similar historical days "
            f"into {n_regimes} clusters.\n"
            "- Regime risk bands are assigned by comparing each cluster's realized annualized volatility.\n"
            "- Results describe the selected history only and are not investment advice or a prediction."
        )
except Exception as error:
    st.error(str(error))
    st.info("Try a longer period, then refresh. Yahoo Finance availability can vary by ticker.")
