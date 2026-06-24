"""Generate all figures for Ch.8 (Evaluación y Resultados) of the thesis.

Uses a colorblind-friendly palette (IBM Design / Wong 2011).
Outputs PDF figures to ../media/ for Typst inclusion.
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# ──────────────────── Paths ────────────────────
SCRIPT_DIR = Path(__file__).resolve().parent
ROOT = SCRIPT_DIR.parent.parent.parent  # repo root (manuscrito/codigo-helpers/generacion_diagramas_y_figs/ -> ../../.. = repo root)
DATA_DIR = ROOT / "codigo_experimentos" / "part_i"
JUDGE_DIR = ROOT / "codigo_experimentos" / "part_h_1"
COST_DIR = ROOT / "codigo_experimentos" / "part_i"
OUT_DIR = ROOT / "manuscrito" / "media"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# ──────────────────── Colorblind-safe palette (Wong 2011) ────────────────────
CB_BLUE = "#0072B2"
CB_ORANGE = "#E69F00"
CB_GREEN = "#009E73"
CB_RED = "#D55E00"
CB_PURPLE = "#CC79A7"
CB_CYAN = "#56B4E9"
CB_YELLOW = "#F0E442"
CB_BLACK = "#000000"

STRATEGY_COLORS = {
    "llm_responses_no_rag": CB_ORANGE,
    "llm_responses_base_rag": CB_BLUE,
    "llm_responses_agentic_rag": CB_GREEN,
}
STRATEGY_LABELS = {
    "llm_responses_no_rag": "Sin RAG",
    "llm_responses_base_rag": "RAG básico",
    "llm_responses_agentic_rag": "Agentic-RAG",
}
MODEL_COLORS = {
    "gpt-5-nano": CB_CYAN,
    "gpt-5-mini": CB_PURPLE,
    "gpt-5": CB_RED,
}
MODEL_MARKERS = {
    "gpt-5-nano": "o",
    "gpt-5-mini": "s",
    "gpt-5": "^",
}

ESTRATEGIAS = ["llm_responses_no_rag", "llm_responses_base_rag", "llm_responses_agentic_rag"]
MODELOS = ["gpt-5-nano", "gpt-5-mini", "gpt-5"]

VR_LABELS = {
    "respuesta_correcta_avg": "Respuesta correcta (avg jueces)",
    "token_f1": "Token F1",
    "rouge_l": "ROUGE-L",
    "sbert_similarity_spanish": "SBERT Similarity (español)",
    "bertscore": "BERTScore",
    "precision_legal_avg": "Precisión legal (avg jueces)",
}
VR_SELECCIONADAS = list(VR_LABELS.keys())

RUBRICA_VALORES = [0.0, 0.25, 0.5, 0.75, 1.0]

JUDGE_LABELS = {
    "grok_4_1_fast_free": "Grok",
    "openrouter_deepseek_deepseek-chat-v3-1": "DeepSeek",
    "openrouter_moonshotai_kimi-k2-0905": "Kimi K2",
}

# ──────────────────── Global matplotlib config  ────────────────────
plt.rcParams.update({
    "figure.dpi": 150,
    "savefig.dpi": 300,
    "savefig.bbox": "tight",
    "font.size": 13,
    "axes.titlesize": 14,
    "axes.labelsize": 13,
    "xtick.labelsize": 12,
    "ytick.labelsize": 12,
    "legend.fontsize": 11,
    "figure.constrained_layout.use": True,
})


# ──────────────────── Data loading ────────────────────
def load_metrics() -> pd.DataFrame:
    df = pd.read_csv(DATA_DIR / "combined_metrics_for_analysis.csv")
    return df


def load_judge() -> pd.DataFrame:
    df = pd.read_csv(JUDGE_DIR / "final_judge_results.csv")
    return df


def load_costs() -> pd.DataFrame:
    df = pd.read_csv(COST_DIR / "metadata_tokens_cost_cleaned.csv")
    # Compute total cost including retrieval
    df["retrieval_total_price"] = pd.to_numeric(df["retrieval_total_price"], errors="coerce").fillna(0)
    df["total_price"] = pd.to_numeric(df["total_price"], errors="coerce").fillna(0)
    df["costo_total"] = df["total_price"] + df["retrieval_total_price"]
    return df


# ──────────────────── Figure 1: Boxplots by strategy × model ────────────────────
def fig_boxplots_by_strategy(df: pd.DataFrame):
    """Boxplots of VR metrics grouped by retrieval strategy."""
    n_vr = len(VR_SELECCIONADAS)
    n_cols = 3
    n_rows = (n_vr + n_cols - 1) // n_cols
    fig, axes = plt.subplots(n_rows, n_cols, figsize=(14, 4.5 * n_rows))
    axes = axes.flatten()

    for i, metrica in enumerate(VR_SELECCIONADAS):
        ax = axes[i]
        data_by_strat = []
        for est in ESTRATEGIAS:
            vals = df.loc[df["estrategia"] == est, metrica].dropna().values
            data_by_strat.append(vals)

        bp = ax.boxplot(
            data_by_strat,
            tick_labels=[STRATEGY_LABELS[e] for e in ESTRATEGIAS],
            patch_artist=True,
            widths=0.6,
            medianprops=dict(color=CB_BLACK, linewidth=1.5),
        )
        for patch, est in zip(bp["boxes"], ESTRATEGIAS):
            patch.set_facecolor(STRATEGY_COLORS[est])
            patch.set_alpha(0.7)

        # Add means as diamonds
        means = [d.mean() for d in data_by_strat]
        ax.scatter(range(1, len(means) + 1), means, color=CB_RED, marker="D", s=35, zorder=5, label="Media")

        ax.set_title(VR_LABELS.get(metrica, metrica))
        ax.set_ylabel("Score")
        if i == 0:
            ax.legend(loc="lower right", fontsize=8)

    # Hide unused axes
    for j in range(i + 1, len(axes)):
        axes[j].set_visible(False)

    fig.suptitle("Distribución de métricas por estrategia de recuperación", fontsize=13, y=1.01)
    fig.savefig(OUT_DIR / "boxplots_por_estrategia.pdf")
    plt.close(fig)
    print("  ✓ boxplots_por_estrategia.pdf")


# ──────────────────── Figure 2: Interaction plots (strategy × model) ────────────────────
def fig_interaction_plots(df: pd.DataFrame):
    """Interaction line plots: model lines across strategies with 95% CI."""
    n_vr = len(VR_SELECCIONADAS)
    n_cols = 3
    n_rows = (n_vr + n_cols - 1) // n_cols
    fig, axes = plt.subplots(n_rows, n_cols, figsize=(15, 5 * n_rows))
    axes = axes.flatten()

    for i, metrica in enumerate(VR_SELECCIONADAS):
        ax = axes[i]
        for modelo in MODELOS:
            means, cis = [], []
            for est in ESTRATEGIAS:
                vals = df.loc[
                    (df["estrategia"] == est) & (df["id_modelo_especialista"] == modelo), metrica
                ].dropna().values
                m = vals.mean() if len(vals) > 0 else np.nan
                se = vals.std() / np.sqrt(len(vals)) if len(vals) > 1 else 0
                means.append(m)
                cis.append(1.96 * se)

            x_pos = np.arange(len(ESTRATEGIAS))
            ax.errorbar(
                x_pos, means, yerr=cis,
                marker=MODEL_MARKERS[modelo], capsize=4, capthick=1.2,
                linewidth=2, color=MODEL_COLORS[modelo], label=modelo,
                markersize=7,
            )

        ax.set_xticks(range(len(ESTRATEGIAS)))
        ax.set_xticklabels([STRATEGY_LABELS[e] for e in ESTRATEGIAS], fontsize=8)
        ax.set_title(VR_LABELS.get(metrica, metrica))
        ax.set_ylabel("Media ± IC 95%")
        if i == 0:
            ax.legend(loc="best", fontsize=8)

    for j in range(i + 1, len(axes)):
        axes[j].set_visible(False)

    fig.suptitle("Interacción modelo × estrategia de recuperación", fontsize=13, y=1.01)
    fig.savefig(OUT_DIR / "interaccion_modelo_estrategia.pdf")
    plt.close(fig)
    print("  ✓ interaccion_modelo_estrategia.pdf")


# ──────────────────── Figure 3: Cost-performance scatter ────────────────────
def fig_cost_performance(df_metrics: pd.DataFrame, df_cost: pd.DataFrame):
    """Scatter plots of mean cost vs mean performance for each VR.

    Each point = one modelo × estrategia combination (9 total).
    Color = strategy, marker = model → all 9 combos visually distinct.
    """
    # Compute mean cost per combination
    cost_agg = (
        df_cost.groupby(["estrategia", "id_modelo_especialista"])["costo_total"]
        .mean()
        .reset_index()
        .rename(columns={"costo_total": "costo_medio"})
    )

    # Compute mean performance per combination
    perf_agg = (
        df_metrics.groupby(["estrategia", "id_modelo_especialista"])[VR_SELECCIONADAS]
        .mean()
        .reset_index()
    )

    merged = perf_agg.merge(cost_agg, on=["estrategia", "id_modelo_especialista"], how="left")

    # Debug: print combinations present
    print(f"  Combinaciones en merged: {len(merged)} (esperadas: 9)")
    for _, row in merged.iterrows():
        print(f"    {row['estrategia']} × {row['id_modelo_especialista']}: costo={row['costo_medio']:.5f}")

    n_vr = len(VR_SELECCIONADAS)
    n_cols = 3
    n_rows = (n_vr + n_cols - 1) // n_cols
    fig, axes = plt.subplots(n_rows, n_cols, figsize=(18, 5.5 * n_rows))
    axes = axes.flatten()

    for i, metrica in enumerate(VR_SELECCIONADAS):
        ax = axes[i]
        for _, row in merged.iterrows():
            est = row["estrategia"]
            modelo = row["id_modelo_especialista"]
            costo = row["costo_medio"]
            perf = row[metrica]
            if pd.isna(costo) or pd.isna(perf):
                print(f"    ⚠ Omitido por NaN: {est} × {modelo} en {metrica}")
                continue

            # Color = strategy, Marker = model → 3×3 = 9 unique visual combos
            ax.scatter(
                costo, perf,
                color=STRATEGY_COLORS.get(est, CB_BLACK),
                marker=MODEL_MARKERS.get(modelo, "o"),
                s=160, edgecolors=CB_BLACK, linewidth=0.8, zorder=5,
            )

        ax.set_xlabel("Costo medio (USD)", fontsize=13)
        ax.set_ylabel(VR_LABELS.get(metrica, metrica), fontsize=13)
        ax.set_title(VR_LABELS.get(metrica, metrica), fontsize=14)
        ax.tick_params(labelsize=11)

    # Shared legend: model markers + strategy colors
    from matplotlib.lines import Line2D
    legend_elements = []
    # Strategy legend (colored squares)
    for est in ESTRATEGIAS:
        legend_elements.append(
            Line2D([0], [0], marker="s", color="w",
                   markerfacecolor=STRATEGY_COLORS[est], markersize=12,
                   markeredgecolor=CB_BLACK, markeredgewidth=0.8,
                   label=STRATEGY_LABELS[est])
        )
    # Model legend (black markers)
    for modelo in MODELOS:
        legend_elements.append(
            Line2D([0], [0], marker=MODEL_MARKERS[modelo], color="w",
                   markerfacecolor=CB_BLACK, markersize=12,
                   markeredgecolor=CB_BLACK, markeredgewidth=0.8,
                   label=modelo)
        )
    axes[0].legend(handles=legend_elements, loc="best", fontsize=10,
                   title="Estrategia (color)  /  Modelo (forma)", title_fontsize=10)

    for j in range(i + 1, len(axes)):
        axes[j].set_visible(False)

    fig.suptitle("Relación costo-desempeño para respuesta_correcta_avg y las cinco métricas complementarias.\nCada punto representa una combinación modelo × estrategia",
                 fontsize=15, y=1.02)
    fig.savefig(OUT_DIR / "costo_desempenio.pdf")
    plt.close(fig)
    print("  ✓ costo_desempenio.pdf")


# ──────────────────── Figure 4: Efficiency bars ────────────────────
def fig_efficiency_bars(df_metrics: pd.DataFrame, df_cost: pd.DataFrame):
    """Efficiency index (performance / normalized cost) per configuration."""
    cost_agg = (
        df_cost.groupby(["estrategia", "id_modelo_especialista"])["costo_total"]
        .mean()
        .reset_index()
        .rename(columns={"costo_total": "costo_medio"})
    )
    perf_agg = (
        df_metrics.groupby(["estrategia", "id_modelo_especialista"])[VR_SELECCIONADAS]
        .mean()
        .reset_index()
    )
    merged = perf_agg.merge(cost_agg, on=["estrategia", "id_modelo_especialista"], how="left")

    c_min = merged["costo_medio"].min()
    c_max = merged["costo_medio"].max()
    merged["costo_norm"] = ((merged["costo_medio"] - c_min) / (c_max - c_min)).clip(lower=0.01)

    metrica = "respuesta_correcta_avg"
    merged["eficiencia"] = merged[metrica] / merged["costo_norm"]
    merged = merged.sort_values("eficiencia", ascending=True)

    fig, ax = plt.subplots(figsize=(10, 6))
    labels = [
        f"{STRATEGY_LABELS[r['estrategia']]}\n{r['id_modelo_especialista']}"
        for _, r in merged.iterrows()
    ]
    colors = [MODEL_COLORS.get(r["id_modelo_especialista"], CB_BLACK) for _, r in merged.iterrows()]
    hatches = []
    for _, r in merged.iterrows():
        if r["estrategia"] == "llm_responses_agentic_rag":
            hatches.append("//")
        elif r["estrategia"] == "llm_responses_base_rag":
            hatches.append("\\\\")
        else:
            hatches.append("")

    bars = ax.barh(range(len(merged)), merged["eficiencia"].values, color=colors, alpha=0.8, edgecolor=CB_BLACK, linewidth=0.5)
    for bar, h in zip(bars, hatches):
        bar.set_hatch(h)

    ax.set_yticks(range(len(merged)))
    ax.set_yticklabels(labels, fontsize=8)
    ax.set_xlabel("Índice de eficiencia (desempeño / costo normalizado)")
    ax.set_title(f"Eficiencia: {VR_LABELS[metrica]}")
    fig.savefig(OUT_DIR / "eficiencia_costo.pdf")
    plt.close(fig)
    print("  ✓ eficiencia_costo.pdf")


# ──────────────────── Figure 5: Judge score distribution heatmap ────────────────────
def fig_judge_heatmap(df_judge: pd.DataFrame):
    """Heatmap of score distribution proportions by judge."""
    rubricas = ["score_respuesta_correcta", "score_precision_legal"]
    jueces = sorted(df_judge["modelo_juez"].unique())

    fig, axes = plt.subplots(1, 2, figsize=(14, 4))
    for idx, rubrica in enumerate(rubricas):
        ax = axes[idx]

        matrix = np.zeros((len(jueces), len(RUBRICA_VALORES)))
        for i, juez in enumerate(jueces):
            scores = df_judge.loc[df_judge["modelo_juez"] == juez, rubrica].dropna()
            total = len(scores)
            for j, s in enumerate(RUBRICA_VALORES):
                count = (scores == s).sum()
                matrix[i, j] = count / total if total > 0 else 0

        im = ax.imshow(matrix, cmap="Blues", aspect="auto", vmin=0, vmax=matrix.max())
        ax.set_xticks(range(len(RUBRICA_VALORES)))
        ax.set_xticklabels([f"{s:.2f}" for s in RUBRICA_VALORES])
        ax.set_yticks(range(len(jueces)))
        ax.set_yticklabels([JUDGE_LABELS.get(j, j) for j in jueces], fontsize=9)

        for i in range(len(jueces)):
            for j in range(len(RUBRICA_VALORES)):
                color = "white" if matrix[i, j] > 0.3 else CB_BLACK
                ax.text(j, i, f"{matrix[i, j]:.2f}", ha="center", va="center", fontsize=9, color=color)

        plt.colorbar(im, ax=ax, label="Proporción", shrink=0.8)
        rubrica_label = rubrica.replace("score_", "").replace("_", " ").title()
        ax.set_title(f"Distribución: {rubrica_label}")
        ax.set_xlabel("Puntaje")

    fig.suptitle("Distribución de puntajes por juez", fontsize=13, y=1.03)
    fig.savefig(OUT_DIR / "heatmap_jueces.pdf")
    plt.close(fig)
    print("  ✓ heatmap_jueces.pdf")


# ──────────────────── Figure 6: Krippendorff alpha by system ────────────────────
def fig_krippendorff_alpha():
    """Bar chart of Krippendorff alpha values per system and rubric."""
    # Hardcoded from notebook 06 results
    data = {
        "sistema": ["agentic_rag", "base_rag", "no_rag", "agentic_rag", "base_rag", "no_rag"],
        "rubrica": [
            "respuesta_correcta", "respuesta_correcta", "respuesta_correcta",
            "precision_legal", "precision_legal", "precision_legal",
        ],
        "alpha": [0.8693, 0.8219, 0.6979, 0.7550, 0.6389, 0.6211],
    }
    df = pd.DataFrame(data)

    rubricas = ["respuesta_correcta", "precision_legal"]
    sistemas = ["agentic_rag", "base_rag", "no_rag"]
    sistemas_labels = ["Agentic-RAG", "RAG básico", "Sin RAG"]

    fig, ax = plt.subplots(figsize=(9, 5))
    x = np.arange(len(sistemas))
    width = 0.35
    rubrica_colors = [CB_BLUE, CB_ORANGE]

    for i, rubrica in enumerate(rubricas):
        subset = df[df["rubrica"] == rubrica]
        alphas = [subset.loc[subset["sistema"] == s, "alpha"].values[0] for s in sistemas]
        bars = ax.bar(x + i * width, alphas, width, label=rubrica.replace("_", " ").title(),
                      color=rubrica_colors[i], alpha=0.85, edgecolor=CB_BLACK, linewidth=0.5)
        for bar, a in zip(bars, alphas):
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.01,
                    f"{a:.3f}", ha="center", va="bottom", fontsize=8)

    ax.axhline(y=0.800, color=CB_GREEN, linestyle="--", alpha=0.8, linewidth=1.5, label="α = 0.800 (bueno)")
    ax.axhline(y=0.667, color=CB_RED, linestyle="--", alpha=0.8, linewidth=1.5, label="α = 0.667 (aceptable)")

    ax.set_xticks(x + width / 2)
    ax.set_xticklabels(sistemas_labels)
    ax.set_ylabel("α de Krippendorff (ordinal)")
    ax.set_ylim([0, 1.05])
    ax.set_title("Acuerdo inter-juez por sistema de recuperación")
    ax.legend(loc="lower left", fontsize=8)
    fig.savefig(OUT_DIR / "krippendorff_alpha_por_sistema.pdf")
    plt.close(fig)
    print("  ✓ krippendorff_alpha_por_sistema.pdf")


# ──────────────────── Figure 7: Summary table (medians + IQR) ────────────────────
def fig_summary_table(df: pd.DataFrame):
    """Generate a table figure with medians and IQR for all 9 configurations."""
    rows = []
    for est in ESTRATEGIAS:
        for modelo in MODELOS:
            subset = df[(df["estrategia"] == est) & (df["id_modelo_especialista"] == modelo)]
            row = {"Estrategia": STRATEGY_LABELS[est], "Modelo": modelo}
            for metrica in VR_SELECCIONADAS:
                vals = subset[metrica].dropna()
                if len(vals) > 0:
                    med = vals.median()
                    q1 = vals.quantile(0.25)
                    q3 = vals.quantile(0.75)
                    row[metrica] = f"{med:.3f} [{q1:.3f}–{q3:.3f}]"
                else:
                    row[metrica] = "—"
            rows.append(row)

    df_table = pd.DataFrame(rows)
    df_table.to_csv(OUT_DIR / "tabla_resumen_medianas_iqr.csv", index=False)

    # Also render as a figure
    col_labels = ["Estrategia", "Modelo"] + [VR_LABELS.get(m, m)[:18] for m in VR_SELECCIONADAS]
    cell_text = df_table.values.tolist()

    fig, ax = plt.subplots(figsize=(20, 5))
    ax.axis("off")
    table = ax.table(
        cellText=cell_text,
        colLabels=col_labels,
        loc="center",
        cellLoc="center",
    )
    table.auto_set_font_size(False)
    table.set_fontsize(7)
    table.scale(1, 1.4)

    # Color header
    for j in range(len(col_labels)):
        table[0, j].set_facecolor(CB_BLUE)
        table[0, j].set_text_props(color="white", fontweight="bold")

    # Alternate row colors
    for i in range(1, len(cell_text) + 1):
        for j in range(len(col_labels)):
            if i % 2 == 0:
                table[i, j].set_facecolor("#f0f0f0")

    fig.suptitle("Medianas [IQR] por configuración", fontsize=12, y=0.95)
    fig.savefig(OUT_DIR / "tabla_resumen_medianas_iqr.pdf")
    plt.close(fig)
    print("  ✓ tabla_resumen_medianas_iqr.pdf + .csv")


# ──────────────────── Figure 8: Cost bars by configuration ────────────────────
def fig_cost_bars(df_cost: pd.DataFrame):
    """Grouped bar chart of mean cost by model × strategy."""
    fig, ax = plt.subplots(figsize=(12, 6.5))
    x = np.arange(len(ESTRATEGIAS))
    width = 0.25

    for i, modelo in enumerate(MODELOS):
        means = []
        for est in ESTRATEGIAS:
            vals = df_cost.loc[
                (df_cost["estrategia"] == est) & (df_cost["id_modelo_especialista"] == modelo),
                "costo_total",
            ].dropna()
            means.append(vals.mean() if len(vals) > 0 else 0)

        bars = ax.bar(
            x + i * width, means, width,
            label=modelo, color=MODEL_COLORS[modelo], alpha=0.85,
            edgecolor=CB_BLACK, linewidth=0.8,
        )
        for bar, m in zip(bars, means):
            if m > 0:
                ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.0005,
                        f"${m:.4f}", ha="center", va="bottom", fontsize=11, rotation=45)

    ax.set_xticks(x + width)
    ax.set_xticklabels([STRATEGY_LABELS[e] for e in ESTRATEGIAS], fontsize=13)
    ax.set_ylabel("Costo medio por consulta (USD)", fontsize=14)
    ax.set_title("Costo medio por consulta (USD) para cada combinación modelo", fontsize=15)
    ax.legend(loc="upper left", fontsize=12)
    ax.tick_params(labelsize=12)
    fig.savefig(OUT_DIR / "costos_por_configuracion.pdf")
    plt.close(fig)
    print("  ✓ costos_por_configuracion.pdf")


# ──────────────────── Main ────────────────────
def main():
    print("Cargando datos...")
    df_metrics = load_metrics()
    df_judge = load_judge()
    df_cost = load_costs()

    print(f"  Métricas: {len(df_metrics)} filas")
    print(f"  Jueces:   {len(df_judge)} filas")
    print(f"  Costos:   {len(df_cost)} filas")

    print("\nGenerando figuras...")
    fig_boxplots_by_strategy(df_metrics)
    fig_interaction_plots(df_metrics)
    fig_cost_performance(df_metrics, df_cost)
    fig_efficiency_bars(df_metrics, df_cost)
    fig_judge_heatmap(df_judge)
    fig_krippendorff_alpha()
    fig_summary_table(df_metrics)
    fig_cost_bars(df_cost)

    print(f"\n✓ Todas las figuras guardadas en: {OUT_DIR}")


if __name__ == "__main__":
    main()
