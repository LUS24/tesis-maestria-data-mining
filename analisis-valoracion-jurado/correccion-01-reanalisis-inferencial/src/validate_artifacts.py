"""Valida los artefactos de la corrección IX.1.1.

No modifica fuentes. Comprueba dimensiones, unicidad, cobertura de escenarios
y que las entradas sigan teniendo los hashes registrados. Si una entrada
cambió —por ejemplo, porque se completó la plantilla manual— lo reporta como
advertencia, no como fallo.

Uso:
    uv run --project codigo_experimentos --no-sync --frozen \
      python analisis-valoracion-jurado/correccion-01-reanalisis-inferencial/src/validate_artifacts.py
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pandas as pd

BASE = Path(__file__).resolve().parents[3]
OUT = BASE / "analisis-valoracion-jurado" / "correccion-01-reanalisis-inferencial"
DATOS = OUT / "datos"
SALIDAS = OUT / "salidas"

ESTRATEGIAS = [
    "llm_responses_no_rag",
    "llm_responses_base_rag",
    "llm_responses_agentic_rag",
]
MODELOS = ["gpt-5-nano", "gpt-5-mini", "gpt-5"]
SCENARIOS = [
    "principal_cero_no_sustantivas",
    "observado_jueces_rubric",
    "exclusion_no_sustantivas",
    "solo_fallos_tecnicos_cero",
]


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def check(name: str, condition: bool, detail: str, errors: list[str]) -> None:
    status = "OK" if condition else "FALLA"
    print(f"[{status}] {name}: {detail}")
    if not condition:
        errors.append(f"{name}: {detail}")


def main() -> None:
    errors: list[str] = []
    warnings: list[str] = []

    wide = pd.read_csv(DATOS / "01_wide_711.csv")
    long = pd.read_csv(DATOS / "02_long_2133.csv")
    cells = pd.read_csv(SALIDAS / "10_resumen_celdas_escenarios.csv")
    friedman = pd.read_csv(SALIDAS / "11_friedman.csv")
    wilcoxon = pd.read_csv(SALIDAS / "12_wilcoxon_posthoc.csv")
    models = pd.read_csv(SALIDAS / "20_modelo_interaccion.csv")
    coefs = pd.read_csv(SALIDAS / "21_modelo_coeficientes.csv")
    preds = pd.read_csv(SALIDAS / "22_modelo_predicciones_celdas.csv")
    latent = pd.read_csv(SALIDAS / "23_efectos_simples_latentes.csv")
    prob = pd.read_csv(SALIDAS / "24_efectos_simples_probabilidad.csv")
    judges = pd.read_csv(SALIDAS / "25_modelo_por_juez.csv")

    check("Base ancha", len(wide) == 711, f"{len(wide)} filas", errors)
    check("Base larga", len(long) == 2133, f"{len(long)} filas", errors)
    check("Unidades", wide["obs_id"].nunique() == 79, f"{wide['obs_id'].nunique()} unidades", errors)
    check("Casos", wide["caso_id"].nunique() == 25, f"{wide['caso_id'].nunique()} casos", errors)
    check("Celdas", wide.groupby(["estrategia", "modelo"]).ngroups == 9, "9 celdas", errors)
    check(
        "Observaciones únicas",
        len(wide.drop_duplicates(["obs_id", "estrategia", "modelo"])) == 711,
        "711 combinaciones unidad-celda",
        errors,
    )
    check(
        "Evaluaciones juez-observación únicas",
        len(long.drop_duplicates(["obs_id", "estrategia", "modelo", "juez"])) == 2133,
        "2.133 combinaciones",
        errors,
    )
    check(
        "Tres jueces por observación",
        (long.groupby(["obs_id", "estrategia", "modelo"])["juez"].nunique() == 3).all(),
        "todas las observaciones tienen 3 jueces",
        errors,
    )
    check(
        "Puntaje principal completo",
        wide["score_principal_prom"].notna().all(),
        f"{wide['score_principal_prom'].isna().sum()} nulos",
        errors,
    )
    check(
        "Categorías no sustantivas",
        int(wide["es_no_sustantiva"].sum()) == int((wide["categoria_final"] != "sustantiva").sum()),
        f"{int(wide['es_no_sustantiva'].sum())} no sustantivas",
        errors,
    )

    check(
        "Escenarios en descriptivos",
        set(cells["escenario"]) == set(SCENARIOS),
        f"{sorted(set(cells['escenario']))}",
        errors,
    )
    check(
        "Filas por escenario",
        all((cells["escenario"] == s).sum() == 9 for s in SCENARIOS),
        "9 celdas por escenario",
        errors,
    )
    check(
        "Filas de Friedman",
        len(friedman) == 24,
        f"{len(friedman)} pruebas (6 por escenario)",
        errors,
    )
    check(
        "Comparaciones Wilcoxon",
        len(wilcoxon) == 72,
        f"{len(wilcoxon)} comparaciones (18 por escenario)",
        errors,
    )
    check(
        "Modelos por escenario",
        len(models) == 4 and set(models["escenario"]) == set(SCENARIOS),
        f"{len(models)} modelos",
        errors,
    )
    check(
        "Coeficientes",
        len(coefs) == 4 * 14,
        f"{len(coefs)} filas (14 parámetros por escenario)",
        errors,
    )
    check(
        "Predicciones",
        len(preds) == 4 * 9,
        f"{len(preds)} filas (9 celdas por escenario)",
        errors,
    )
    check(
        "Efectos latentes",
        len(latent) == 4 * 18,
        f"{len(latent)} filas (18 contrastes por escenario)",
        errors,
    )
    check(
        "Efectos de probabilidad",
        len(prob) == 4 * 18,
        f"{len(prob)} filas (18 contrastes por escenario)",
        errors,
    )
    check(
        "Modelos por juez",
        judges["juez"].nunique() == 3 and len(judges) == 27,
        f"{judges['juez'].nunique()} jueces, {len(judges)} filas",
        errors,
    )
    check(
        "Convergencia principal",
        int(models.loc[models["escenario"] == "principal_cero_no_sustantivas", "convergencia"].iloc[0]) == 0,
        "convergencia 0",
        errors,
    )
    check(
        "Interacción principal",
        float(models.loc[models["escenario"] == "principal_cero_no_sustantivas", "p_interaccion"].iloc[0]) < 0.001,
        "p < 0,001",
        errors,
    )

    # Hashes de entradas.
    manifest_path = DATOS / "00_manifiesto_entradas.csv"
    if manifest_path.exists():
        manifest = pd.read_csv(manifest_path)
        for _, row in manifest.iterrows():
            path = BASE / row["archivo"]
            if not path.exists():
                warnings.append(f"Entrada ausente: {row['archivo']}")
                continue
            current = sha256(path)
            if current != row["sha256"]:
                warnings.append(
                    f"Entrada modificada desde la construcción: {row['archivo']}"
                )

    manual_status_path = DATOS / "00_estado_revision_manual.json"
    if manual_status_path.exists():
        manual_status = json.loads(manual_status_path.read_text(encoding="utf-8"))
        if not manual_status.get("completa", False):
            warnings.append(
                "La revisión manual no está completa; el análisis usa clasificación automática."
            )

    # Manifiesto de salidas.
    output_rows = []
    for path in sorted(SALIDAS.glob("*")):
        if path.is_file() and not path.name.endswith(".log"):
            output_rows.append(
                {
                    "archivo": str(path.relative_to(BASE)),
                    "sha256": sha256(path),
                    "bytes": path.stat().st_size,
                }
            )
    pd.DataFrame(output_rows).to_csv(
        SALIDAS / "36_manifiesto_salidas.csv", index=False, encoding="utf-8"
    )

    summary = {
        "errores": errors,
        "advertencias": warnings,
        "n_wide": len(wide),
        "n_long": len(long),
        "n_no_sustantivas": int(wide["es_no_sustantiva"].sum()),
        "n_celdas": int(wide.groupby(["estrategia", "modelo"]).ngroups),
        "revision_manual_completa": (
            json.loads(manual_status_path.read_text(encoding="utf-8")).get("completa", False)
            if manual_status_path.exists()
            else None
        ),
    }
    (SALIDAS / "37_validacion_artefactos.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    print("\nAdvertencias:")
    for warning in warnings:
        print(" -", warning)
    print("\nErrores:")
    for error in errors:
        print(" -", error)
    if errors:
        raise SystemExit(f"{len(errors)} controles fallaron")
    print("\nTodos los controles pasaron.")


if __name__ == "__main__":
    main()
