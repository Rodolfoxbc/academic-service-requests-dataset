import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.stats import chi2_contingency

from config import FIGURES_DIR, TABLES_DIR, UNDESIRABLE_STATES
from fetch_data import ensure_dataset
from validate_data import load_and_validate_data


def _prepare():
    ensure_dataset()
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    TABLES_DIR.mkdir(parents=True, exist_ok=True)


def _save(df, name):
    df.to_csv(TABLES_DIR / name, index=False)


def _label_horizontal(ax, containers):
    xmax = ax.get_xlim()[1]
    for container in containers:
        for bar in container:
            value = bar.get_width()
            ax.text(value + xmax * 0.01,
                    bar.get_y() + bar.get_height() / 2,
                    f"{int(round(value)):,}",
                    va="center", ha="left", fontsize=9)


def _request_type_figure(data, title, filename):
    plot = data.sort_values("TOTAL_BOTH", ascending=True)
    y = np.arange(len(plot))
    h = 0.36
    fig, ax = plt.subplots(figsize=(12, max(3.8, 0.78 * len(plot) + 1.8)))
    b1 = ax.barh(y - h / 2, plot["PERIOD_1"], height=h, label="PERIOD_1")
    b2 = ax.barh(y + h / 2, plot["PERIOD_2"], height=h, label="PERIOD_2")
    ax.set_yticks(y)
    ax.set_yticklabels(plot.index)
    ax.set_xlabel("Number of requests")
    ax.set_ylabel("Request type")
    ax.set_title(title)
    ax.legend()
    xmax = max(plot["PERIOD_1"].max(), plot["PERIOD_2"].max())
    ax.set_xlim(0, xmax * 1.18)
    _label_horizontal(ax, [b1, b2])
    fig.tight_layout()
    fig.savefig(FIGURES_DIR / filename, dpi=300, bbox_inches="tight")
    plt.close(fig)


def main():
    _prepare()
    df, validation = load_and_validate_data()
    df["IS_UNDESIRABLE"] = df["CURRENT_STATE"].isin(UNDESIRABLE_STATES)

    _save(pd.DataFrame([{"criterion": k, "value": v} for k, v in validation.items()]),
          "validation_summary.csv")

    # Overall volume
    period = df.groupby("PERIOD", as_index=False)["TOTAL"].sum().rename(
        columns={"TOTAL": "TOTAL_REQUESTS"})
    p1 = int(period.loc[period["PERIOD"] == "PERIOD_1", "TOTAL_REQUESTS"].iloc[0])
    p2 = int(period.loc[period["PERIOD"] == "PERIOD_2", "TOTAL_REQUESTS"].iloc[0])
    period["ABSOLUTE_CHANGE"] = [np.nan, p2 - p1]
    period["PERCENTAGE_CHANGE"] = [np.nan, (p2 - p1) / p1 * 100]
    _save(period, "table_08_requests_by_period.csv")

    fig, ax = plt.subplots(figsize=(7, 5))
    bars = ax.bar(period["PERIOD"], period["TOTAL_REQUESTS"])
    ax.set_xlabel("Period")
    ax.set_ylabel("Number of requests")
    ax.set_title("Academic service requests by period")
    for bar in bars:
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height(),
                f"{int(bar.get_height()):,}", ha="center", va="bottom")
    fig.tight_layout()
    fig.savefig(FIGURES_DIR / "figure_01_requests_by_period.png", dpi=300, bbox_inches="tight")
    plt.close(fig)

    # Campus volume
    campus = df.groupby(["CAMPUS", "PERIOD"])["TOTAL"].sum().unstack(fill_value=0)
    campus = campus.reindex(columns=["PERIOD_1", "PERIOD_2"])
    campus["ABSOLUTE_CHANGE"] = campus["PERIOD_2"] - campus["PERIOD_1"]
    campus["PERCENTAGE_CHANGE"] = campus["ABSOLUTE_CHANGE"] / campus["PERIOD_1"] * 100
    _save(campus.reset_index(), "table_09_requests_by_campus.csv")

    ax = campus[["PERIOD_1", "PERIOD_2"]].plot(kind="bar", figsize=(8, 5))
    ax.set_xlabel("Campus")
    ax.set_ylabel("Number of requests")
    ax.set_title("Academic service requests by campus and period")
    ax.legend(title="")
    fig = ax.get_figure()
    fig.tight_layout()
    fig.savefig(FIGURES_DIR / "figure_02_requests_by_campus.png", dpi=300, bbox_inches="tight")
    plt.close(fig)

    # Request types and revised Figure 3
    req = df.groupby(["TYPE_REQUEST", "PERIOD"])["TOTAL"].sum().unstack(fill_value=0)
    req = req.reindex(columns=["PERIOD_1", "PERIOD_2"])
    req["TOTAL_BOTH"] = req["PERIOD_1"] + req["PERIOD_2"]
    top10 = req.sort_values("TOTAL_BOTH", ascending=False).head(10).copy()
    top10["ABSOLUTE_CHANGE"] = top10["PERIOD_2"] - top10["PERIOD_1"]
    top10["PERCENTAGE_CHANGE"] = top10["ABSOLUTE_CHANGE"] / top10["PERIOD_1"] * 100
    _save(top10.reset_index(), "table_10_top_request_types.csv")
    _request_type_figure(top10.iloc[:2],
                         "Two dominant academic service-request types",
                         "figure_03a_dominant_request_types.png")
    _request_type_figure(top10.iloc[2:],
                         "Remaining eight most frequent academic service-request types",
                         "figure_03b_remaining_request_types.png")

    # Workflow states
    states = df.groupby(["CURRENT_STATE", "PERIOD"])["TOTAL"].sum().unstack(fill_value=0)
    states = states.reindex(columns=["PERIOD_1", "PERIOD_2"])
    states["ABSOLUTE_CHANGE"] = states["PERIOD_2"] - states["PERIOD_1"]
    states["PERCENTAGE_CHANGE"] = np.where(
        states["PERIOD_1"] != 0,
        states["ABSOLUTE_CHANGE"] / states["PERIOD_1"] * 100,
        np.nan)
    _save(states.reset_index(), "table_11_workflow_states.csv")

    # Undesirable-state summary
    und = df.groupby(["PERIOD", "IS_UNDESIRABLE"])["TOTAL"].sum().unstack(fill_value=0)
    und = und.rename(columns={False: "OTHER_REQUESTS", True: "UNDESIRABLE_REQUESTS"})
    und["TOTAL_REQUESTS"] = und["OTHER_REQUESTS"] + und["UNDESIRABLE_REQUESTS"]
    und["UNDESIRABLE_RATE"] = und["UNDESIRABLE_REQUESTS"] / und["TOTAL_REQUESTS"] * 100
    _save(und.reset_index(), "table_12_undesirable_rate_by_period.csv")

    rates = und.loc[["PERIOD_1", "PERIOD_2"], "UNDESIRABLE_RATE"]
    fig, ax = plt.subplots(figsize=(7, 5))
    bars = ax.bar(rates.index, rates.values)
    ax.set_xlabel("Period")
    ax.set_ylabel("Undesirable workflow-state rate (%)")
    ax.set_title("Undesirable workflow-state rate by period")
    ax.set_ylim(0, max(rates.values) * 1.18)
    for bar, value in zip(bars, rates.values):
        ax.text(bar.get_x() + bar.get_width()/2, value, f"{value:.2f}%",
                ha="center", va="bottom")
    fig.tight_layout()
    fig.savefig(FIGURES_DIR / "figure_04_undesirable_rate.png", dpi=300, bbox_inches="tight")
    plt.close(fig)

    # Individual undesirable states
    selected = [s for s in UNDESIRABLE_STATES if s in states.index]
    undes_states = states.loc[selected].copy()
    _save(undes_states.reset_index(), "table_13_undesirable_states.csv")
    plot = undes_states[["PERIOD_1", "PERIOD_2"]].sort_values("PERIOD_1", ascending=True)
    ax = plot.plot(kind="barh", figsize=(10, 5))
    ax.set_xlabel("Number of requests")
    ax.set_ylabel("Workflow state")
    ax.set_title("Undesirable workflow states by period")
    ax.legend(title="")
    xmax = max(plot["PERIOD_1"].max(), plot["PERIOD_2"].max())
    ax.set_xlim(0, xmax * 1.17)
    _label_horizontal(ax, ax.containers)
    fig = ax.get_figure()
    fig.tight_layout()
    fig.savefig(FIGURES_DIR / "figure_05_undesirable_states.png", dpi=300, bbox_inches="tight")
    plt.close(fig)

    # Campus undesirable rates and heatmap
    ct = df.groupby(["PERIOD", "CAMPUS"])["TOTAL"].sum().rename("TOTAL_REQUESTS")
    cb = df[df["IS_UNDESIRABLE"]].groupby(["PERIOD", "CAMPUS"])["TOTAL"].sum().rename(
        "UNDESIRABLE_REQUESTS")
    cr = pd.concat([ct, cb], axis=1).fillna(0)
    cr["RATE"] = cr["UNDESIRABLE_REQUESTS"] / cr["TOTAL_REQUESTS"] * 100
    _save(cr.reset_index(), "table_14_undesirable_rates_by_campus.csv")

    heat = cr["RATE"].unstack("PERIOD").reindex(columns=["PERIOD_1", "PERIOD_2"])
    fig, ax = plt.subplots(figsize=(7, 4))
    image = ax.imshow(heat.values, aspect="auto")
    ax.set_xticks(np.arange(len(heat.columns)))
    ax.set_xticklabels(heat.columns)
    ax.set_yticks(np.arange(len(heat.index)))
    ax.set_yticklabels(heat.index)
    ax.set_xlabel("Period")
    ax.set_ylabel("Campus")
    ax.set_title("Undesirable workflow-state rate by campus")
    for i in range(heat.shape[0]):
        for j in range(heat.shape[1]):
            ax.text(j, i, f"{heat.iloc[i,j]:.2f}%", ha="center", va="center")
    fig.colorbar(image, ax=ax, label="Rate (%)")
    fig.tight_layout()
    fig.savefig(FIGURES_DIR / "figure_06_undesirable_rate_heatmap.png",
                dpi=300, bbox_inches="tight")
    plt.close(fig)

    # Request-type-specific rates and standardization
    tt = df.groupby(["TYPE_REQUEST", "PERIOD"])["TOTAL"].sum().rename("TOTAL_REQUESTS")
    tb = df[df["IS_UNDESIRABLE"]].groupby(["TYPE_REQUEST", "PERIOD"])["TOTAL"].sum().rename(
        "UNDESIRABLE_REQUESTS")
    tr = pd.concat([tt, tb], axis=1).fillna(0)
    tr["UNDESIRABLE_RATE"] = tr["UNDESIRABLE_REQUESTS"] / tr["TOTAL_REQUESTS"] * 100
    _save(tr.reset_index(), "request_type_undesirable_rates.csv")

    rw = tr["UNDESIRABLE_RATE"].unstack("PERIOD").reindex(
        columns=["PERIOD_1", "PERIOD_2"])
    rw["RATE_CHANGE_PP"] = rw["PERIOD_2"] - rw["PERIOD_1"]
    _save(rw.reset_index(), "request_type_undesirable_rate_changes.csv")

    pooled = df.groupby("TYPE_REQUEST")["TOTAL"].sum() / df["TOTAL"].sum()
    standardized = []
    for period_name in ["PERIOD_1", "PERIOD_2"]:
        period_rates = tr["UNDESIRABLE_RATE"].unstack("PERIOD")[period_name] / 100
        value = float((period_rates * pooled).sum() * 100)
        standardized.append({"PERIOD": period_name,
                             "STANDARDIZED_UNDESIRABLE_RATE": value})
    _save(pd.DataFrame(standardized), "standardized_undesirable_rates.csv")

    # Illustrative Pearson chi-square and Cramer's V
    contingency = np.array([
        [und.loc["PERIOD_1", "UNDESIRABLE_REQUESTS"],
         und.loc["PERIOD_1", "OTHER_REQUESTS"]],
        [und.loc["PERIOD_2", "UNDESIRABLE_REQUESTS"],
         und.loc["PERIOD_2", "OTHER_REQUESTS"]]], dtype=float)
    chi2, p_value, dof, _ = chi2_contingency(contingency, correction=False)
    cramers_v = float(np.sqrt(chi2 / contingency.sum()))
    _save(pd.DataFrame([{
        "test": "Pearson chi-squared test of independence",
        "chi_square": float(chi2),
        "degrees_of_freedom": int(dof),
        "p_value": float(p_value),
        "cramers_v": cramers_v}]), "illustrative_chi_square_cramers_v.csv")

    print("Analysis completed successfully.")
    print(f"Validated rows: {validation['rows']}")
    print(f"Represented requests: {validation['sum_total']:,}")
    print("Standardized undesirable rates: " +
          ", ".join(f"{x['PERIOD']}={x['STANDARDIZED_UNDESIRABLE_RATE']:.2f}%"
                    for x in standardized))
    print(f"Chi-square={chi2:.2f}, p={p_value:.3e}, Cramer's V={cramers_v:.3f}")


if __name__ == "__main__":
    main()
