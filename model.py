"""Unsupervised market-regime discovery with StandardScaler and K-Means.

The model groups observed feature patterns into recurring historical states. It
does not estimate or predict a stock's future price direction.
"""

from __future__ import annotations

import os
from dataclasses import dataclass

import numpy as np
import pandas as pd

# The project's Windows Python runtime does not expose the retired ``wmic``
# command that joblib otherwise uses to detect physical CPU cores.
os.environ.setdefault("LOKY_MAX_CPU_COUNT", str(os.cpu_count() or 1))

from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler

from features import CLUSTER_FEATURES


REGIME_COLORS = ("#18a999", "#f4a261", "#e63946", "#7b2cbf", "#277da1")


@dataclass
class RegimeAnalysis:
    """Fitted clustering objects and labelled observations for one security."""

    data: pd.DataFrame
    summary: pd.DataFrame
    scaler: StandardScaler
    model: KMeans
    feature_columns: list[str]
    current_regime: str
    current_risk_band: str
    current_description: str
    silhouette_score: float
    silhouette_interpretation: str
    transition_matrix: pd.DataFrame


def _assign_risk_bands(summary: pd.DataFrame) -> pd.Series:
    """Rank clusters by realized volatility to derive relative risk bands."""
    risk_order = summary["Annualized_Volatility"].rank(method="first", ascending=True)
    count = len(summary)
    risk_bands: list[str] = []
    for rank in risk_order:
        if count == 1:
            risk_bands.append("Typical risk")
        elif rank == 1:
            risk_bands.append("Lower risk")
        elif rank == count:
            risk_bands.append("Elevated risk")
        else:
            risk_bands.append("Moderate risk")
    return pd.Series(risk_bands, index=summary.index, dtype="object")


def _cluster_return_profile(average_daily_return: float) -> str:
    """Map observed return direction to a descriptive profile."""
    if average_daily_return <= -0.0015:
        return "Downside"
    if average_daily_return < 0:
        return "Defensive Down"
    if average_daily_return < 0.00075:
        return "Range-Bound"
    return "Upside"


def _cluster_regime_name(return_profile: str, risk_band: str) -> str:
    """Build a human-readable regime name without overstating model certainty."""
    if return_profile == "Upside":
        if risk_band == "Lower risk":
            return "Stable Up"
        if risk_band == "Elevated risk":
            return "High-Volatility Up"
        return "Momentum Up"
    if return_profile == "Downside":
        if risk_band == "Lower risk":
            return "Defensive Pullback"
        if risk_band == "Elevated risk":
            return "High-Pressure Down"
        return "Downside Pressure"
    if return_profile == "Defensive Down":
        if risk_band == "Lower risk":
            return "Defensive Drift"
        if risk_band == "Elevated risk":
            return "Volatile Drift"
        return "Soft Pullback"
    if risk_band == "Lower risk":
        return "Calm Range"
    if risk_band == "Elevated risk":
        return "High-Volatility Range"
    return "Transitional Range"


def _make_unique_names(names: list[str]) -> list[str]:
    """Ensure regime names stay unique even if two clusters map to one label."""
    counts: dict[str, int] = {}
    unique_names: list[str] = []
    for name in names:
        counts[name] = counts.get(name, 0) + 1
        occurrence = counts[name]
        unique_names.append(name if occurrence == 1 else f"{name} {occurrence}")
    return unique_names


def _describe_cluster(summary: pd.DataFrame) -> pd.Series:
    """Summarize each cluster in interview-friendly plain language."""
    descriptions = (
        summary["Return Profile"]
        + " regime with "
        + summary["Risk Band"].str.lower()
        + ", average daily return "
        + summary["Average_Daily_Return"].map(lambda value: f"{value:.2%}")
        + ", and annualized volatility "
        + summary["Annualized_Volatility"].map(lambda value: f"{value:.1%}")
        + "."
    )
    return descriptions.astype("object")


def _silhouette_interpretation(score: float) -> str:
    """Translate the silhouette score into a concise cluster-quality label."""
    if not np.isfinite(score):
        return "Silhouette score unavailable"
    if score >= 0.5:
        return "Well-separated regimes"
    if score >= 0.25:
        return "Moderately separated regimes"
    if score >= 0.1:
        return "Weakly separated regimes"
    return "Highly overlapping regimes"


def _build_regime_summary(labelled_data: pd.DataFrame) -> pd.DataFrame:
    """Summarize observed return and risk characteristics per discovered state."""
    grouped = labelled_data.dropna(subset=["Cluster"]).groupby("Cluster", observed=True)
    summary = grouped.agg(
        Observations=("Return 1D", "size"),
        Average_Daily_Return=("Return 1D", "mean"),
        Average_5D_Return=("Return 5D", "mean"),
        Annualized_Return=("Return 1D", lambda values: values.mean() * 252),
        Annualized_Volatility=("Return 1D", lambda values: values.std(ddof=1) * np.sqrt(252)),
        Average_RSI=("RSI 14", "mean"),
        Average_MA_Spread=("MA Spread", "mean"),
        Average_Volume_Ratio=("Volume Ratio", "mean"),
        Maximum_Drawdown=("Drawdown", "min"),
    ).reset_index()

    daily_volatility = grouped["Return 1D"].std(ddof=1)
    mean_return = grouped["Return 1D"].mean()
    summary["Sharpe (0% RF)"] = summary["Cluster"].map(
        (mean_return / daily_volatility.replace(0, np.nan)) * np.sqrt(252)
    )
    summary["Share of History"] = summary["Observations"] / summary["Observations"].sum()
    summary["Risk Band"] = _assign_risk_bands(summary)
    summary["Return Profile"] = summary["Average_Daily_Return"].map(_cluster_return_profile)
    summary["Regime"] = _make_unique_names(
        [
            _cluster_regime_name(return_profile, risk_band)
            for return_profile, risk_band in zip(summary["Return Profile"], summary["Risk Band"], strict=False)
        ]
    )
    summary["Historical Characteristic"] = np.where(
        summary["Average_Daily_Return"] > 0,
        "positive average return",
        np.where(summary["Average_Daily_Return"] < 0, "negative average return", "flat average return"),
    )
    summary["Description"] = _describe_cluster(summary)
    return summary.sort_values("Cluster").reset_index(drop=True)


def _build_transition_matrix(labelled_data: pd.DataFrame, summary: pd.DataFrame) -> pd.DataFrame:
    """Calculate row-normalized transition probabilities between observed regimes."""
    observed = labelled_data.dropna(subset=["Cluster"]).copy()
    observed["Next Cluster"] = observed["Cluster"].shift(-1)
    transitions = observed.dropna(subset=["Next Cluster"]).copy()

    cluster_order = summary["Cluster"].astype(int).tolist()
    regime_names = summary.set_index("Cluster")["Regime"].to_dict()
    if transitions.empty:
        return pd.DataFrame(index=summary["Regime"], columns=summary["Regime"], dtype=float)

    counts = pd.crosstab(
        transitions["Cluster"].astype(int),
        transitions["Next Cluster"].astype(int),
        dropna=False,
    ).reindex(index=cluster_order, columns=cluster_order, fill_value=0)
    probabilities = counts.div(counts.sum(axis=1).replace(0, np.nan), axis=0)
    probabilities.index = [regime_names[int(cluster)] for cluster in probabilities.index]
    probabilities.columns = [regime_names[int(cluster)] for cluster in probabilities.columns]
    return probabilities


def fit_regime_model(data: pd.DataFrame, n_clusters: int = 3) -> RegimeAnalysis:
    """Standardize selected features, discover historical regimes, and summarize them."""
    if n_clusters < 2:
        raise ValueError("At least two clusters are needed to compare market regimes.")

    missing = set(CLUSTER_FEATURES).difference(data.columns)
    if missing:
        raise ValueError(f"Missing clustering features: {', '.join(sorted(missing))}.")

    complete = data.replace([np.inf, -np.inf], np.nan).dropna(subset=CLUSTER_FEATURES).copy()
    minimum_rows = max(80, n_clusters * 20)
    if len(complete) < minimum_rows:
        raise ValueError(
            f"Need at least {minimum_rows} complete daily observations for {n_clusters} regimes; "
            "select a longer history."
        )

    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(complete[CLUSTER_FEATURES])
    estimator = KMeans(n_clusters=n_clusters, n_init=25, random_state=42)
    complete["Cluster"] = estimator.fit_predict(scaled_features)

    silhouette = float(silhouette_score(scaled_features, complete["Cluster"]))

    labelled = data.copy()
    labelled["Cluster"] = pd.Series(pd.NA, index=labelled.index, dtype="Int64")
    labelled.loc[complete.index, "Cluster"] = complete["Cluster"].astype("Int64")

    summary = _build_regime_summary(labelled)
    summary_by_cluster = summary.set_index("Cluster")
    labelled["Regime"] = labelled["Cluster"].map(summary_by_cluster["Regime"])
    labelled["Risk Band"] = labelled["Cluster"].map(summary_by_cluster["Risk Band"])
    labelled["Historical Characteristic"] = labelled["Cluster"].map(
        summary_by_cluster["Historical Characteristic"]
    )
    labelled["Regime Description"] = labelled["Cluster"].map(summary_by_cluster["Description"])

    current = labelled.dropna(subset=CLUSTER_FEATURES).iloc[-1]
    current_cluster = int(current["Cluster"])
    current_regime = str(summary_by_cluster.loc[current_cluster, "Regime"])
    current_risk_band = str(summary_by_cluster.loc[current_cluster, "Risk Band"])
    current_description = str(summary_by_cluster.loc[current_cluster, "Description"])

    return RegimeAnalysis(
        data=labelled,
        summary=summary,
        scaler=scaler,
        model=estimator,
        feature_columns=CLUSTER_FEATURES.copy(),
        current_regime=current_regime,
        current_risk_band=current_risk_band,
        current_description=current_description,
        silhouette_score=silhouette,
        silhouette_interpretation=_silhouette_interpretation(silhouette),
        transition_matrix=_build_transition_matrix(labelled, summary),
    )


def get_regime_colors(summary: pd.DataFrame) -> dict[str, str]:
    """Provide stable dashboard colours keyed by human-readable regime names."""
    return {
        row.Regime: REGIME_COLORS[int(row.Cluster) % len(REGIME_COLORS)]
        for row in summary.itertuples(index=False)
    }
