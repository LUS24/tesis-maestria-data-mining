"""Figuras de la corrección IX.1.1.

Lee las tablas generadas por los scripts de análisis y escribe figuras nuevas
en `figuras/`. No modifica figuras históricas del manuscrito.

Uso:
    uv run --project codigo_experimentos --no-sync --frozen \
      python analisis-valoracion-jurado/correccion-01-analisis-estadistico/src/make_figures.py
"""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

BASE = Path(__file__).resolve().parents[3]
OUT = BASE / "analisis-valoracion-jurado" / "correccion-01-analisis-estadistico"
DATOS = OUT / "datos"
SALIDAS = OUT / "salidas"
FIGURAS = OUT / "figuras"
FIGURAS.mkdir(parents=True, exist_ok=True)

ESTRATEGIAS = [
    "llm_responses_no_rag",
    "llm_responses_base_rag",
    "llm_responses_agentic_rag",
]
ESTRATEGIA_LABEL = {
    "llm_responses_no_rag": "Sin RAG",
    "llm_responses_base_rag": "RAG básico",
    "llm_responses_agentic_rag": "Agentic-RAG",
}
MODELOS = ["gpt-5-nano", "gpt-5-mini", "gpt-5"]
MODELO_COLOR = {
    "gpt-5-nano": "#56B4E9",
    "gpt-5-mini": "#CC79A7",
    "gpt-5": "#D55E00",
}
MODELO_MARKER = {"gpt-5-nano": "o", "gpt-5-mini": "s", "gpt-5": "^"}
SCENARIO_COLOR = {
    "principal_cero_no_sustantivas": "#0072B2",
    "observado_jueces_rubric": "#E69F00",
    "exclusion_no_sustantivas": "#009E73",
    "solo_fallos_tecnicos_cero": "#CC79A7",
}
SCENARIO_LABEL = {
    "principal_cero_no_sustantivas": "Principal: no sustantivas = 0",
    "observado_jueces_rubric": "Observado (rúbrica)",
    "exclusion_no_sustantivas": "Exclusión",
    "solo_fallos_tecnicos_cero": "Solo fallos técnicos = 0",
}
RUBRICA = [0.0, 0.25, 0.5, 0.75, 1.0]
RUBRICA_COLOR = {
    0.0: "#D55E00",
    0.25: "#E69F00",
    0.5: "#F0E442",
    0.75: "#56B4E9",
    1.0: "#0072B2",
}

plt.rcParams.update(
    {
        "figure.dpi": 130,
        "savefig.dpi": 300,
        "savefig.bbox": "tight",
        "font.size": 10,
        "axes.titlesize": 11,
        "axes.labelsize": 10,
        "xtick.labelsize": 9,
        "ytick.labelsize": 9,
        "legend.fontsize": 8,
        "figure.constrained_layout.use": True,
    }
)


def save(fig: plt.Figure, stem: str) -> None:
    fig.savefig(FIGURAS / f"{stem}.pdf")
    fig.savefig(FIGURAS / f"{stem}.png")
    plt.close(fig)
    print(f"  ✓ {stem}.pdf / .png")


def cell_label(estrategia: str, modelo: str, short: bool = False) -> str:
    e = ESTRATEGIA_LABEL[estrategia].replace("RAG básico", "RAG bás.") if short else ESTRATEGIA_LABEL[estrategia]
    return f"{e}\n{modelo}"


def fig_cell_means() -> None:
    cells = pd.read_csv(SALIDAS / "10_resumen_celdas_escenarios.csv")
    df = cells[cells["escenario"] == "principal_cero_no_sustantivas"].copy()
    fig, ax = plt.subplots(figsize=(10.5, 5.2))
    x = np.arange(len(ESTRATEGIAS))
    width = 0.24
    for j, modelo in enumerate(MODELOS):
        sub = df[df["modelo"] == modelo].set_index("estrategia").loc[ESTRATEGIAS]
        means = sub["media"].to_numpy()
        lower = sub["media_ic95_inf"].to_numpy()
        upper = sub["media_ic95_sup"].to_numpy()
        ax.bar(
            x + (j - 1) * width,
            means,
            width,
            label=modelo,
            color=MODELO_COLOR[modelo],
            alpha=0.88,
            edgecolor="black",
            linewidth=0.4,
        )
        ax.errorbar(
            x + (j - 1) * width,
            means,
            yerr=[means - lower, upper - means],
            fmt="none",
            ecolor="black",
            capsize=3,
            linewidth=0.9,
        )
    ax.set_xticks(x)
    ax.set_xticklabels([ESTRATEGIA_LABEL[e] for e in ESTRATEGIAS])
    ax.set_ylabel("Media de respuesta correcta (0–1)")
    ax.set_ylim(0, 1)
    ax.axhline(0.75, color="gray", linestyle="--", linewidth=0.8)
    ax.text(2.45, 0.76, "umbral 0,75", ha="right", va="bottom", fontsize=8, color="gray")
    ax.legend(title="Modelo del especialista", ncol=3, loc="upper left")
    ax.set_title("Escenario principal: respuestas no sustantivas imputadas a 0")
    save(fig, "01_medias_por_celda_principal")


def fig_interaction() -> None:
    pred = pd.read_csv(SALIDAS / "22_modelo_predicciones_celdas.csv")
    df = pred[pred["escenario"] == "principal_cero_no_sustantivas"].copy()
    df["estrategia"] = df["cell"].str.split("|", regex=False).str[0]
    df["modelo"] = df["cell"].str.split("|", regex=False).str[1]
    fig, ax = plt.subplots(figsize=(8.2, 5.2))
    x = np.arange(len(ESTRATEGIAS))
    for modelo in MODELOS:
        sub = df[df["modelo"] == modelo].set_index("cell")
        vals = []
        lo = []
        hi = []
        for estrategia in ESTRATEGIAS:
            row = sub.loc[f"{['Sin RAG', 'RAG basico', 'Agentic-RAG'][ESTRATEGIAS.index(estrategia)]}|{modelo}"]
            vals.append(float(row["p_ge_075"]))
            lo.append(float(row["p_ge_075_ic95_inf"]))
            hi.append(float(row["p_ge_075_ic95_sup"]))
        vals = np.array(vals)
        lo = np.array(lo)
        hi = np.array(hi)
        ax.plot(x, vals, marker=MODELO_MARKER[modelo], color=MODELO_COLOR[modelo], label=modelo, linewidth=1.8)
        ax.fill_between(x, lo, hi, color=MODELO_COLOR[modelo], alpha=0.16, linewidth=0)
    ax.set_xticks(x)
    ax.set_xticklabels([ESTRATEGIA_LABEL[e] for e in ESTRATEGIAS])
    ax.set_ylabel("P(respuesta correcta ≥ 0,75)")
    ax.set_ylim(0, 1)
    ax.legend(title="Modelo del especialista")
    ax.set_title("Interacción estrategia × modelo (predicción del modelo ordinal)")
    save(fig, "02_interaccion_prob_ge_075")


def fig_forest() -> None:
    effects = pd.read_csv(SALIDAS / "24_efectos_simples_probabilidad.csv")
    df = effects[effects["escenario"] == "principal_cero_no_sustantivas"].copy()
    fig, axes = plt.subplots(1, 2, figsize=(13, 6.2), sharex=True)
    panels = [
        ("estrategia_dentro_de_modelo", "Estrategia dentro de cada modelo"),
        ("modelo_dentro_de_estrategia", "Modelo dentro de cada estrategia"),
    ]
    for ax, (family, title) in zip(axes, panels):
        sub = df[df["familia"] == family].copy()
        sub["label"] = sub["bloque"] + "\n" + sub["comparacion"].str.replace("llm_responses_", "", regex=False)
        sub = sub.iloc[::-1].reset_index(drop=True)
        y = np.arange(len(sub))
        x = sub["diferencia_esperada_plugin"].to_numpy()
        lo = sub["diferencia_esperada_ic95_inf"].to_numpy()
        hi = sub["diferencia_esperada_ic95_sup"].to_numpy()
        colors = [MODELO_COLOR.get(m, "#0072B2") for m in sub["bloque"]]
        if family == "modelo_dentro_de_estrategia":
            colors = ["#0072B2"] * len(sub)
        ax.errorbar(
            x,
            y,
            xerr=[x - lo, hi - x],
            fmt="o",
            color="black",
            ecolor="black",
            capsize=3,
            markersize=5,
            linewidth=0.9,
        )
        ax.scatter(x, y, c=colors, s=38, zorder=3, edgecolor="black", linewidth=0.3)
        ax.axvline(0, color="gray", linestyle="--", linewidth=0.8)
        ax.set_yticks(y)
        ax.set_yticklabels(sub["label"], fontsize=7.5)
        ax.set_xlabel("Diferencia de media esperada (IC 95%)")
        ax.set_title(title)
        ax.grid(axis="x", color="#DDDDDD", linewidth=0.5)
    fig.suptitle("Efectos simples bajo el escenario principal", fontsize=12)
    save(fig, "03_efectos_simples_probabilidad")


def fig_scenarios() -> None:
    cells = pd.read_csv(SALIDAS / "10_resumen_celdas_escenarios.csv")
    order = [(e, m) for e in ESTRATEGIAS for m in MODELOS]
    labels = [cell_label(e, m, short=True) for e, m in order]
    fig, ax = plt.subplots(figsize=(13, 5.8))
    x = np.arange(len(order))
    for scenario in [
        "principal_cero_no_sustantivas",
        "observado_jueces_rubric",
        "exclusion_no_sustantivas",
        "solo_fallos_tecnicos_cero",
    ]:
        sub = cells[cells["escenario"] == scenario].set_index(["estrategia", "modelo"])
        vals = np.array([float(sub.loc[key, "media"]) for key in order])
        lo = np.array([float(sub.loc[key, "media_ic95_inf"]) for key in order])
        hi = np.array([float(sub.loc[key, "media_ic95_sup"]) for key in order])
        ax.plot(
            x,
            vals,
            marker="o",
            markersize=5,
            linewidth=1.4,
            color=SCENARIO_COLOR[scenario],
            label=SCENARIO_LABEL[scenario],
        )
        ax.fill_between(x, lo, hi, color=SCENARIO_COLOR[scenario], alpha=0.10, linewidth=0)
    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=45, ha="right", fontsize=8)
    ax.set_ylabel("Media de respuesta correcta (0–1)")
    ax.set_ylim(0, 1)
    ax.legend(ncol=2, fontsize=8, loc="upper left")
    ax.set_title("Sensibilidad al tratamiento de las respuestas no sustantivas")
    save(fig, "04_sensibilidad_escenarios")


def fig_score_distribution() -> None:
    long = pd.read_csv(DATOS / "02_long_2133.csv")
    long["estrategia_label"] = long["estrategia"].map(ESTRATEGIA_LABEL)
    long["cell"] = long["estrategia_label"] + "\n" + long["modelo"]
    order = [f"{ESTRATEGIA_LABEL[e]}\n{m}" for e in ESTRATEGIAS for m in MODELOS]
    tab = pd.crosstab(long["cell"], long["score_principal"], normalize="index").reindex(order).fillna(0)
    fig, ax = plt.subplots(figsize=(12, 5.5))
    bottom = np.zeros(len(tab))
    for value in RUBRICA:
        vals = tab.get(value, pd.Series(0, index=tab.index)).to_numpy()
        ax.bar(
            np.arange(len(tab)),
            vals,
            bottom=bottom,
            color=RUBRICA_COLOR[value],
            edgecolor="white",
            linewidth=0.4,
            label=f"{value:.2f}",
        )
        bottom += vals
    ax.set_xticks(np.arange(len(tab)))
    ax.set_xticklabels(tab.index, rotation=45, ha="right", fontsize=8)
    ax.set_ylabel("Proporción de evaluaciones")
    ax.set_ylim(0, 1)
    ax.legend(title="Puntaje", ncol=5, loc="upper center", bbox_to_anchor=(0.5, -0.22))
    ax.set_title("Distribución del puntaje bajo el escenario principal (juez-observación)")
    save(fig, "05_distribucion_puntajes_principal")


def main() -> None:
    fig_cell_means()
    fig_interaction()
    fig_forest()
    fig_scenarios()
    fig_score_distribution()
    print(f"Figuras en: {FIGURAS}")


if __name__ == "__main__":
    main()
