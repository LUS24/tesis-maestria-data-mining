import polars as pl
import numpy as np
from scipy import stats
import krippendorff
from pathlib import Path
from itertools import combinations

DATA_DIR = Path("part_i")
df_judge = pl.read_csv(DATA_DIR / "final_judge_results.csv")

JUECES = sorted(df_judge["modelo_juez"].unique().to_list())
SISTEMAS = sorted(df_judge["sistema"].unique().to_list())
RUBRICAS = ["score_respuesta_correcta", "score_precision_legal"]
RUBRICA_VALORES = [0.0, 0.25, 0.5, 0.75, 1.0]
_rubrica_arr = np.array(RUBRICA_VALORES)

def impute_to_rubrica(value):
    dists = np.abs(_rubrica_arr - value)
    min_dist = dists.min()
    candidates = _rubrica_arr[dists == min_dist]
    return float(candidates.max())

df_judge_clean = df_judge.with_columns([
    pl.col(sc).map_elements(
        lambda v: impute_to_rubrica(v) if v not in RUBRICA_VALORES else v,
        return_dtype=pl.Float64,
    ).alias(sc) for sc in RUBRICAS
])

print("=" * 60)
print("SPEARMAN CORRELATIONS")
print("=" * 60)
for rubrica in RUBRICAS:
    print(f"\nRubrica: {rubrica}")
    df_pivot = df_judge.select([
        "numero_pregunta", "numero_subpregunta", "sistema", "modelo_respuesta",
        "modelo_juez", rubrica
    ]).pivot(on="modelo_juez",
        index=["numero_pregunta", "numero_subpregunta", "sistema", "modelo_respuesta"],
        values=rubrica)
    for j1, j2 in combinations(JUECES, 2):
        if j1 in df_pivot.columns and j2 in df_pivot.columns:
            valid = df_pivot.select([j1, j2]).drop_nulls()
            if len(valid) > 2:
                vals1 = valid[j1].to_numpy()
                vals2 = valid[j2].to_numpy()
                rho, p = stats.spearmanr(vals1, vals2)
                print(f"  {j1[:25]} <> {j2[:25]}: rho={rho:.4f}, p={p:.2e}")

print("\n" + "=" * 60)
print("KRIPPENDORFF ALPHA GLOBAL")
print("=" * 60)
for rubrica in RUBRICAS:
    df_pivot = df_judge.select([
        "numero_pregunta", "numero_subpregunta", "sistema", "modelo_respuesta",
        "modelo_juez", rubrica
    ]).pivot(on="modelo_juez",
        index=["numero_pregunta", "numero_subpregunta", "sistema", "modelo_respuesta"],
        values=rubrica)
    judge_cols = [c for c in df_pivot.columns if c in JUECES]
    reliability_data = [df_pivot[j].to_numpy().astype(float) for j in judge_cols]
    reliability_matrix = np.array(reliability_data)
    alpha_ord = krippendorff.alpha(reliability_data=reliability_matrix, level_of_measurement="ordinal")
    alpha_nom = krippendorff.alpha(reliability_data=reliability_matrix, level_of_measurement="nominal")
    alpha_int = krippendorff.alpha(reliability_data=reliability_matrix, level_of_measurement="interval")
    print(f"{rubrica}: ord={alpha_ord:.4f}, nom={alpha_nom:.4f}, int={alpha_int:.4f}")

print("\n" + "=" * 60)
print("ALPHA POR SISTEMA")
print("=" * 60)
for rubrica in RUBRICAS:
    df_pivot_full = df_judge.select([
        "numero_pregunta", "numero_subpregunta", "sistema", "modelo_respuesta",
        "modelo_juez", rubrica
    ]).pivot(on="modelo_juez",
        index=["numero_pregunta", "numero_subpregunta", "sistema", "modelo_respuesta"],
        values=rubrica)
    judge_cols = [c for c in df_pivot_full.columns if c in JUECES]
    for sistema in SISTEMAS:
        subset = df_pivot_full.filter(pl.col("sistema") == sistema)
        if len(subset) > 5:
            rel_data = [subset[j].to_numpy().astype(float) for j in judge_cols]
            rel_matrix = np.array(rel_data)
            alpha_val = krippendorff.alpha(reliability_data=rel_matrix, level_of_measurement="ordinal")
            print(f"  {rubrica} | {sistema.replace('llm_responses_', '')}: alpha={alpha_val:.4f}")

print("\n" + "=" * 60)
print("CHI-SQUARED HOMOGENEITY")
print("=" * 60)
for rubrica in RUBRICAS:
    all_scores = sorted(df_judge_clean[rubrica].drop_nulls().unique().to_list())
    contingency = []
    for juez in JUECES:
        scores = df_judge_clean.filter(pl.col("modelo_juez") == juez)[rubrica].drop_nulls()
        row = [(scores == s).sum() for s in all_scores]
        contingency.append(row)
    contingency = np.array(contingency)
    chi2, p, dof, expected = stats.chi2_contingency(contingency)
    n_cells_low = (expected < 5).sum()
    pct_low = 100 * n_cells_low / expected.size
    print(f"{rubrica}: chi2={chi2:.4f}, df={dof}, p={p:.6f}, sig={p < 0.05}, cells_low={pct_low:.1f}%")

print("\n" + "=" * 60)
print("BIAS (MEDIA POR JUEZ)")
print("=" * 60)
for rubrica in RUBRICAS:
    print(f"\n{rubrica}:")
    for juez in JUECES:
        scores = df_judge_clean.filter(pl.col("modelo_juez") == juez)[rubrica].drop_nulls().to_numpy()
        media = scores.mean()
        std = scores.std()
        cv = (std / media * 100) if media != 0 else float("nan")
        print(f"  {juez[:35]:<35} media={media:.4f} std={std:.4f} cv={cv:.1f}%")

print("\n" + "=" * 60)
print("DISCORDANCIA")
print("=" * 60)
for rubrica in RUBRICAS:
    df_pivot = df_judge.select([
        "numero_pregunta", "numero_subpregunta", "sistema", "modelo_respuesta",
        "modelo_juez", rubrica
    ]).pivot(on="modelo_juez",
        index=["numero_pregunta", "numero_subpregunta", "sistema", "modelo_respuesta"],
        values=rubrica)
    judge_cols = [c for c in df_pivot.columns if c in JUECES]
    scores_matrix = df_pivot.select(judge_cols).to_numpy().astype(float)
    std_vals = np.nanstd(scores_matrix, axis=1)
    range_vals = np.nanmax(scores_matrix, axis=1) - np.nanmin(scores_matrix, axis=1)
    print(f"{rubrica}:")
    print(f"  Media std: {np.nanmean(std_vals):.4f}")
    print(f"  Mediana std: {np.nanmedian(std_vals):.4f}")
    print(f"  Max std: {np.nanmax(std_vals):.4f}")
    print(f"  % std>1: {100 * np.mean(std_vals > 1):.1f}%")
    print(f"  % rango>=3: {100 * np.mean(range_vals >= 3):.1f}%")
