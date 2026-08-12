"""Plotly visualizations used by the QuantLens Streamlit dashboard."""

from __future__ import annotations

import pandas as pd
import plotly.graph_objects as go


def build_price_regime_figure(
    data: pd.DataFrame,
    ticker: str,
    currency_symbol: str,
    regime_colors: dict[str, str],
) -> go.Figure:
    """Plot the price history with each discovered regime shown as coloured markers."""
    figure = go.Figure()
    figure.add_trace(
        go.Scatter(
            x=data.index,
            y=data["Close"],
            mode="lines",
            name="Close",
            line={"color": "#aab7c4", "width": 1.5},
            hovertemplate="%{x|%d %b %Y}<br>Close: %{y:,.2f}<extra></extra>",
        )
    )

    for regime, color in regime_colors.items():
        observations = data[data["Regime"] == regime]
        if observations.empty:
            continue
        figure.add_trace(
            go.Scatter(
                x=observations.index,
                y=observations["Close"],
                mode="markers",
                name=regime,
                marker={"color": color, "size": 6, "opacity": 0.82},
                customdata=observations[["Risk Band", "Historical Characteristic"]],
                hovertemplate=(
                    "%{x|%d %b %Y}<br>Close: %{y:,.2f}<br>%{fullData.name}"
                    "<br>%{customdata[0]} · %{customdata[1]}<extra></extra>"
                ),
            )
        )

    figure.update_layout(
        title=f"{ticker}: price timeline and historical regimes",
        yaxis_title=f"Price ({currency_symbol})",
        hovermode="x unified",
        legend_title="Observed state",
        margin={"l": 10, "r": 10, "t": 50, "b": 10},
        template="plotly_white",
    )
    return figure


def build_regime_risk_figure(summary: pd.DataFrame, regime_colors: dict[str, str]) -> go.Figure:
    """Compare the historical annualized volatility of each discovered regime."""
    colors = [regime_colors[regime] for regime in summary["Regime"]]
    figure = go.Figure(
        go.Bar(
            x=summary["Regime"],
            y=summary["Annualized_Volatility"],
            marker_color=colors,
            customdata=summary[["Average_Daily_Return", "Maximum_Drawdown", "Risk Band"]],
            hovertemplate=(
                "%{x}<br>Annualized volatility: %{y:.1%}"
                "<br>Average daily return: %{customdata[0]:.2%}"
                "<br>Maximum drawdown: %{customdata[1]:.1%}"
                "<br>%{customdata[2]}<extra></extra>"
            ),
        )
    )
    figure.update_layout(
        title="Historical risk by regime",
        yaxis_title="Annualized volatility",
        xaxis_title=None,
        showlegend=False,
        margin={"l": 10, "r": 10, "t": 50, "b": 10},
        template="plotly_white",
    )
    figure.update_yaxes(tickformat=".0%")
    return figure


def build_drawdown_figure(data: pd.DataFrame) -> go.Figure:
    """Plot running drawdown from the historical peak."""
    figure = go.Figure(
        go.Scatter(
            x=data.index,
            y=data["Drawdown"],
            mode="lines",
            fill="tozeroy",
            line={"color": "#e63946", "width": 1.5},
            fillcolor="rgba(230, 57, 70, 0.18)",
            hovertemplate="%{x|%d %b %Y}<br>Drawdown: %{y:.1%}<extra></extra>",
        )
    )
    figure.update_layout(
        title="Historical drawdown from prior peak",
        yaxis_title="Drawdown",
        hovermode="x unified",
        margin={"l": 10, "r": 10, "t": 50, "b": 10},
        template="plotly_white",
    )
    figure.update_yaxes(tickformat=".0%")
    return figure
