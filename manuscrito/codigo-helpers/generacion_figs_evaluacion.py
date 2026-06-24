"""
Genera las figuras de análisis exploratorio para el capítulo de Evaluación:
  - spearman_correlacion_completa.pdf : matriz de correlación de Spearman 15×15
  - biplot_pca_suplementarias.pdf     : biplot PCA con variables agénticas suplementarias

Uso:
  cd codigo_experimentos/
  uv run python ../manuscrito/codigo-helpers/generacion_figs_evaluacion.py

Requiere que los datos procesados estén en part_i/:
  - metric_comparison_source_data_cleaned.csv
  - final_judge_results.csv
"""

import polars as pl
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from pathlib import Path

# ── Configuración ──────────────────────────────────────────────
plt.rcParams.update({"figure.dpi": 150, "figure.figsize": (12, 8)})

DATA_DIR = Path("part_i")
MEDIA_DIR = Path("../manuscrito/media")

# ── Carga de datos ─────────────────────────────────────────────
df_metrics = pl.read_csv(DATA_DIR / "metric_comparison_source_data_cleaned.csv")
df_judge = pl.read_csv(DATA_DIR / "final_judge_results.csv")

df_wide = df_metrics.pivot(
    on="metrica",
    index=["nro_pregunta", "nro_subpregunta", "estrategia", "id_modelo_especialista"],
    values="valor",
)

METRICAS_TRADICIONALES = [
    "token_f1", "jaccard_similarity", "levenshtein_similarity",
    "character_error_rate", "bleu", "rouge_1", "rouge_2", "rouge_l",
    "sbert_similarity_multilingual", "sbert_similarity_spanish",
    "bertscore", "length_ratio", "word_count_ratio",
]

# ── Imputación de scores de jueces a valores de rúbrica ────────
RUBRICA_VALORES = [0.0, 0.25, 0.5, 0.75, 1.0]
_rubrica_arr = np.array(RUBRICA_VALORES)


def impute_to_rubrica(value: float) -> float:
    """Redondea al valor de rúbrica más cercano; empates → el mayor."""
    dists = np.abs(_rubrica_arr - value)
    min_dist = dists.min()
    candidates = _rubrica_arr[dists == min_dist]
    return float(candidates.max())


JUDGE_SCORES = ["score_respuesta_correcta", "score_precision_legal"]
df_judge_clean = df_judge.with_columns([
    pl.col(sc).map_elements(
        lambda v: impute_to_rubrica(v) if v not in RUBRICA_VALORES else v,
        return_dtype=pl.Float64,
    ).alias(sc) for sc in JUDGE_SCORES
])

# ── Promedio de scores por juez → variables agénticas ──────────
df_judge_avg = df_judge_clean.group_by(
    ["numero_pregunta", "numero_subpregunta", "sistema", "modelo_respuesta"]
).agg(
    pl.col("score_respuesta_correcta").mean().alias("respuesta_correcta_avg"),
    pl.col("score_precision_legal").mean().alias("precision_legal_avg"),
)

# ── Unión con métricas tradicionales ───────────────────────────
df_combined = df_wide.join(
    df_judge_avg,
    left_on=["nro_pregunta", "nro_subpregunta", "estrategia", "id_modelo_especialista"],
    right_on=["numero_pregunta", "numero_subpregunta", "sistema", "modelo_respuesta"],
    how="left",
)

# ═══════════════════════════════════════════════════════════════
# FIGURA 1: Matriz de correlación de Spearman (15×15)
# ═══════════════════════════════════════════════════════════════
TODAS_LAS_METRICAS = METRICAS_TRADICIONALES + [
    "respuesta_correcta_avg", "precision_legal_avg"
]

all_data = df_combined.select(TODAS_LAS_METRICAS).to_numpy()
n_all = len(TODAS_LAS_METRICAS)

spearman_all = np.zeros((n_all, n_all))
for i in range(n_all):
    for j in range(n_all):
        mask = ~np.isnan(all_data[:, i]) & ~np.isnan(all_data[:, j])
        if mask.sum() > 2:
            rho, _ = stats.spearmanr(all_data[mask, i], all_data[mask, j])
            spearman_all[i, j] = rho
        else:
            spearman_all[i, j] = np.nan

SHORT_LABELS = [
    "token_f1", "jaccard", "levenshtein", "CER", "bleu",
    "rouge_1", "rouge_2", "rouge_l",
    "sbert_multi", "sbert_es", "bertscore",
    "length_ratio", "word_count",
    "resp_correcta", "prec_legal",
]

fig, ax = plt.subplots(figsize=(22, 20))
im = ax.imshow(spearman_all, cmap="RdBu_r", vmin=-1, vmax=1, aspect="auto")
ax.set_xticks(range(n_all))
ax.set_yticks(range(n_all))
ax.set_xticklabels(SHORT_LABELS, rotation=45, ha="right", fontsize=16)
ax.set_yticklabels(SHORT_LABELS, fontsize=16)

for i in range(n_all):
    for j in range(n_all):
        val = spearman_all[i, j]
        if not np.isnan(val):
            color = "white" if abs(val) > 0.6 else "black"
            ax.text(j, i, f"{val:.2f}", ha="center", va="center",
                    fontsize=14, color=color,
                    fontweight="bold" if abs(val) > 0.85 else "normal")

# Líneas divisorias de clústeres
for boundary in [7.5, 10.5, 12.5]:
    ax.axhline(y=boundary, color="gray", linewidth=1.5, linestyle="--", alpha=0.5)
    ax.axvline(x=boundary, color="gray", linewidth=1.5, linestyle="--", alpha=0.5)

cbar = plt.colorbar(im, ax=ax, label="Spearman ρ", shrink=0.8)
cbar.ax.yaxis.label.set_size(17)
ax.set_title(
    "Matriz de Correlación de Spearman — Métricas Textuales + Evaluación Agéntica",
    fontsize=20,
)
plt.tight_layout()
fig.savefig(MEDIA_DIR / "spearman_correlacion_completa.pdf",
            bbox_inches="tight", dpi=150)
plt.close()
print("✓ spearman_correlacion_completa.pdf")

# ═══════════════════════════════════════════════════════════════
# FIGURA 2: Biplot PCA con variables suplementarias
# ═══════════════════════════════════════════════════════════════
pca_data = df_wide.select(METRICAS_TRADICIONALES).drop_nulls().to_numpy()

scaler = StandardScaler()
pca_data_scaled = scaler.fit_transform(pca_data)

pca = PCA()
pca.fit(pca_data_scaled)
pca_scores = pca.transform(pca_data_scaled)

var_explained = pca.explained_variance_ratio_
loadings = pca.components_[:2].T  # (13 métricas, 2 componentes)

# ── Variables suplementarias ───────────────────────────────────
SUPP_VARS = ["respuesta_correcta_avg", "precision_legal_avg"]
align_cols = METRICAS_TRADICIONALES + SUPP_VARS
aligned_data = df_combined.select(align_cols).drop_nulls().to_numpy()

trad_data_aligned = aligned_data[:, :len(METRICAS_TRADICIONALES)]
supp_data_aligned = aligned_data[:, len(METRICAS_TRADICIONALES):]

trad_scaled_aligned = scaler.transform(trad_data_aligned)
scores_aligned = pca.transform(trad_scaled_aligned)

# Coordenadas suplementarias = correlación de Pearson(score PC, var supl.)
supp_coords = np.zeros((len(SUPP_VARS), 2))
for s_idx in range(len(SUPP_VARS)):
    for pc_idx in range(2):
        r, _ = stats.pearsonr(
            scores_aligned[:, pc_idx], supp_data_aligned[:, s_idx]
        )
        supp_coords[s_idx, pc_idx] = r

# ── Biplot ─────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(10, 10))

# Métricas tradicionales (azul)
for i, metrica in enumerate(METRICAS_TRADICIONALES):
    x, y = loadings[i, 0], loadings[i, 1]
    ax.annotate("", xy=(x, y), xytext=(0, 0),
                arrowprops=dict(arrowstyle="->", color="#1f77b4", lw=2.0))
    short = SHORT_LABELS[i]
    offset_x = 0.025 * (1 if x >= 0 else -1)
    offset_y = 0.025 * (1 if y >= 0 else -1)
    ax.text(x + offset_x, y + offset_y, short, fontsize=13,
            color="#1f77b4", ha="center", va="center")

# Variables suplementarias (rojo, negrita)
SUPP_SHORT = ["resp_correcta\n(agéntica)", "prec_legal\n(agéntica)"]
for s_idx, s_name in enumerate(SUPP_VARS):
    sx, sy = supp_coords[s_idx, 0], supp_coords[s_idx, 1]
    ax.annotate("", xy=(sx, sy), xytext=(0, 0),
                arrowprops=dict(arrowstyle="->", color="#d62728", lw=3.5))
    ax.text(sx + 0.025, sy + 0.025, SUPP_SHORT[s_idx], fontsize=14,
            color="#d62728", fontweight="bold", ha="center", va="center")

# Decoraciones
R = 0.6
circle = plt.Circle((0, 0), R, fill=False, color="gray",
                    linestyle="--", alpha=0.3)
ax.add_patch(circle)
ax.axhline(0, color="gray", linewidth=0.5)
ax.axvline(0, color="gray", linewidth=0.5)
ax.set_xlim(-R - 0.1, R + 0.1)
ax.set_ylim(-R - 0.1, R + 0.1)
ax.set_aspect("equal")
ax.set_xlabel(f"PC1 ({var_explained[0]:.1%} varianza)", fontsize=16)
ax.set_ylabel(f"PC2 ({var_explained[1]:.1%} varianza)", fontsize=16)
ax.set_title(
    "Biplot PCA — Métricas Textuales (azul) + Variables Agénticas Suplementarias (rojo)",
    fontsize=18,
)

from matplotlib.lines import Line2D
legend_elements = [
    Line2D([0], [0], color="#1f77b4", lw=2,
           label="Métricas textuales (activas)"),
    Line2D([0], [0], color="#d62728", lw=2,
           label="Variables agénticas (suplementarias)"),
]
ax.legend(handles=legend_elements, loc="lower right", fontsize=15)

plt.tight_layout()
fig.savefig(MEDIA_DIR / "biplot_pca_suplementarias.pdf",
            bbox_inches="tight", dpi=150)
plt.close()
print("✓ biplot_pca_suplementarias.pdf")

print("\nFiguras guardadas en", MEDIA_DIR.resolve())
