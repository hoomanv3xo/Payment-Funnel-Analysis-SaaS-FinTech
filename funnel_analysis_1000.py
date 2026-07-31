"""
Order Funnel Analysis — 1,000-subscription version
-----------------------------------------------------
Same logic as the original funnel_analysis.py, with defaults pointed
at the 1,000-row synthetic dataset instead of the 50-row sample.

Inputs : funnel_stage_counts_1000.csv, funnel_clean_export_1000.csv
Outputs: funnel_chart_1000.png, dropoff_chart_1000.png, simulation results (printed)
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

STAGE_ORDER = ["PaymentWidgetOpened", "PaymentEntered", "PaymentSubmitted",
               "PaymentSuccess", "Complete"]

# ------------------------------------------------------------------
# 1. LOAD
# ------------------------------------------------------------------
def load_data(stage_counts_path="funnel_stage_counts_1000.csv",
              orders_path="funnel_clean_export_1000.csv"):
    stages = pd.read_csv(stage_counts_path)
    orders = pd.read_csv(orders_path)
    return stages, orders


# ------------------------------------------------------------------
# 2. FUNNEL METRICS: conversion & drop-off at each step
# ------------------------------------------------------------------
def compute_funnel_metrics(stages: pd.DataFrame) -> pd.DataFrame:
    """Given cumulative counts per stage, compute step-over-step
    conversion rate and drop-off (both count and %)."""
    df = stages.sort_values("stage_id").reset_index(drop=True).copy()
    df["step_conversion_rate"] = df["orders_reaching_stage"] / df["orders_reaching_stage"].shift(1)
    df.loc[0, "step_conversion_rate"] = 1.0
    df["dropoff_count"] = df["orders_reaching_stage"].shift(1) - df["orders_reaching_stage"]
    df.loc[0, "dropoff_count"] = 0
    df["dropoff_pct"] = 1 - df["step_conversion_rate"]
    df["overall_conversion_from_start"] = df["orders_reaching_stage"] / df["orders_reaching_stage"].iloc[0]
    return df


# ------------------------------------------------------------------
# 3. VISUALIZATION
# ------------------------------------------------------------------
def plot_funnel(metrics: pd.DataFrame, out_path="funnel_chart_1000.png"):
    fig, ax = plt.subplots(figsize=(8, 5))
    y = np.arange(len(metrics))
    ax.barh(y, metrics["orders_reaching_stage"], color="#2E5EAA")
    ax.set_yticks(y)
    ax.set_yticklabels(metrics["stage_name"])
    ax.invert_yaxis()
    ax.set_xlabel("Orders reaching stage")
    ax.set_title("Order Funnel: Orders Reaching Each Payment Stage (n=1,000)")
    for i, v in enumerate(metrics["orders_reaching_stage"]):
        pct = metrics["overall_conversion_from_start"].iloc[i] * 100
        ax.text(v + 5, i, f"{int(v)}  ({pct:.0f}% of started orders)", va="center")
    ax.set_xlim(0, metrics["orders_reaching_stage"].max() * 1.25)
    plt.tight_layout()
    plt.savefig(out_path, dpi=150)
    plt.close()


def plot_dropoff(metrics: pd.DataFrame, out_path="dropoff_chart_1000.png"):
    fig, ax = plt.subplots(figsize=(8, 5))
    steps = [f"{a} → {b}" for a, b in zip(metrics["stage_name"], metrics["stage_name"].shift(-1))][:-1]
    dropoff_pct = (metrics["dropoff_pct"].shift(-1) * 100)[:-1]
    colors = ["#D64545" if v == dropoff_pct.max() else "#8CA6C8" for v in dropoff_pct]
    ax.bar(steps, dropoff_pct, color=colors)
    ax.set_ylabel("% of orders lost at this step")
    ax.set_title("Where Orders Fall Out of the Funnel (n=1,000)")
    plt.xticks(rotation=20, ha="right")
    for i, v in enumerate(dropoff_pct):
        ax.text(i, v + 0.5, f"{v:.1f}%", ha="center")
    plt.tight_layout()
    plt.savefig(out_path, dpi=150)
    plt.close()


# ------------------------------------------------------------------
# 4. WHAT-IF SIMULATION
# ------------------------------------------------------------------
def simulate_improvement(metrics: pd.DataFrame, orders: pd.DataFrame,
                          step_index: int, improvement_pp: float,
                          n_sims: int = 5000, seed: int = 42) -> dict:
    """
    Simulate raising the conversion rate of ONE funnel step by
    `improvement_pp` percentage points (e.g. 10 = +10pp) and
    propagate the effect through the rest of the funnel.

    Uses a binomial draw at each downstream step (Monte Carlo) so we
    can report a confidence range, not just a point estimate. At
    n=1,000 starting orders the resulting CIs are much tighter than
    the 50-row version -- a good sanity check that the effect is real
    and not just small-sample noise.
    """
    rng = np.random.default_rng(seed)
    base_rates = metrics["step_conversion_rate"].values.copy()
    new_rates = base_rates.copy()
    new_rates[step_index] = min(1.0, base_rates[step_index] + improvement_pp / 100)

    start_orders = metrics["orders_reaching_stage"].iloc[0]
    completions_base, completions_new = [], []

    for _ in range(n_sims):
        n_base, n_new = start_orders, start_orders
        for r_base, r_new in zip(base_rates[1:], new_rates[1:]):
            n_base = rng.binomial(int(round(n_base)), min(r_base, 1.0)) if n_base > 0 else 0
            n_new = rng.binomial(int(round(n_new)), min(r_new, 1.0)) if n_new > 0 else 0
        completions_base.append(n_base)
        completions_new.append(n_new)

    completions_base = np.array(completions_base)
    completions_new = np.array(completions_new)

    avg_revenue_per_completed_order = orders.loc[orders["is_completed_order"] == 1, "revenue"].mean()

    result = {
        "step_improved": metrics["stage_name"].iloc[step_index],
        "improvement_pp": improvement_pp,
        "baseline_completions_mean": completions_base.mean(),
        "baseline_completions_ci95": np.percentile(completions_base, [2.5, 97.5]),
        "simulated_completions_mean": completions_new.mean(),
        "simulated_completions_ci95": np.percentile(completions_new, [2.5, 97.5]),
        "expected_extra_completions": completions_new.mean() - completions_base.mean(),
        "avg_revenue_per_completed_order": avg_revenue_per_completed_order,
        "expected_revenue_lift": (completions_new.mean() - completions_base.mean()) * avg_revenue_per_completed_order,
    }
    return result


def find_best_opportunity(metrics: pd.DataFrame, orders: pd.DataFrame,
                           improvement_pp: float = 10.0) -> pd.DataFrame:
    """Run the same simulated improvement at every step and rank
    steps by expected revenue lift -- identifies where a fixed
    product investment (e.g. +10pp conversion) pays off the most."""
    rows = []
    for i in range(1, len(metrics)):  # skip step 0 (nothing upstream of first stage)
        res = simulate_improvement(metrics, orders, i, improvement_pp)
        rows.append(res)
    ranked = pd.DataFrame(rows).sort_values("expected_revenue_lift", ascending=False)
    return ranked


# ------------------------------------------------------------------
# 5. MAIN
# ------------------------------------------------------------------
if __name__ == "__main__":
    stages, orders = load_data()
    metrics = compute_funnel_metrics(stages)
    print("\n=== FUNNEL METRICS (n=1,000) ===")
    print(metrics.to_string(index=False))

    plot_funnel(metrics)
    plot_dropoff(metrics)

    print("\n=== BIGGEST DROP-OFF STEP ===")
    worst_step = metrics["dropoff_pct"].iloc[1:].idxmax()
    print(f"{metrics['stage_name'].iloc[worst_step-1]} -> {metrics['stage_name'].iloc[worst_step]}: "
          f"{metrics['dropoff_pct'].iloc[worst_step]*100:.1f}% of orders lost")

    print("\n=== SIMULATION: +10pp conversion at every step, ranked by revenue lift ===")
    ranked = find_best_opportunity(metrics, orders, improvement_pp=10.0)
    print(ranked[["step_improved", "expected_extra_completions",
                  "baseline_completions_ci95", "simulated_completions_ci95",
                  "expected_revenue_lift"]]
          .round(2).to_string(index=False))
