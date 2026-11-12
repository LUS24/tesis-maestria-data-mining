"""Valida y resume la revisión manual ciega de IX.1.2.

Uso:
    uv run --project codigo_experimentos --no-sync --frozen \
      python analisis-valoracion-jurado/correccion-02-diagnostico-gpt-5-nano/src/validar_revision_manual.py

Requiere que `revision_manual/plantilla_resultados.csv` esté completa.
No modifica la plantilla ni el paquete ciego.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

BASE = Path(__file__).resolve().parents[3]
OUT = BASE / "analisis-valoracion-jurado" / "correccion-02-diagnostico-gpt-5-nano"
REVISION = OUT / "revision_manual"
SALIDAS = OUT / "salidas"

CATEGORIAS = {
    "sustantiva",
    "vacia",
    "solo_espacios",
    "abstencion_explicita",
    "error_explicito",
    "truncada",
    "indeterminada",
}


def main() -> None:
    template_path = REVISION / "plantilla_resultados.csv"
    mapping_path = SALIDAS / "mapa_revision_ciega.csv"

    if not template_path.exists() or not mapping_path.exists():
        raise SystemExit("Faltan la plantilla o el mapa de revisión.")

    template = pd.read_csv(template_path, dtype=str, keep_default_na=False, encoding="utf-8")
    mapping = pd.read_csv(mapping_path, dtype=str, keep_default_na=False, encoding="utf-8")

    required = {"review_id", "categoria_revisada", "justificacion", "revisor", "fecha"}
    missing = required - set(template.columns)
    if missing:
        raise SystemExit(f"Faltan columnas en la plantilla: {sorted(missing)}")

    template["categoria_revisada"] = template["categoria_revisada"].str.strip()
    template["justificacion"] = template["justificacion"].str.strip()

    invalid = template[
        (~template["categoria_revisada"].isin(CATEGORIAS))
        & (template["categoria_revisada"] != "")
    ]
    incomplete = template[template["categoria_revisada"] == ""]

    print(f"Filas en la plantilla: {len(template)}")
    print(f"Filas completas: {len(template) - len(incomplete)}")
    print(f"Filas sin categoría: {len(incomplete)}")
    print(f"Categorías inválidas: {len(invalid)}")

    if len(invalid):
        print("\nCategorías inválidas:")
        print(invalid[["review_id", "categoria_revisada"]].to_string(index=False))

    if len(incomplete):
        print("\nFilas pendientes:")
        print(incomplete[["review_id"]].to_string(index=False))
        print("\nCompleta la plantilla antes de generar el resumen definitivo.")
        return

    merged = template.merge(mapping, on="review_id", how="left", validate="one_to_one")
    if merged["obs_id"].isna().any():
        raise SystemExit("Hay review_id sin correspondencia en el mapa.")

    merged["coincide"] = merged["categoria_revisada"] == merged["categoria"]
    agreement = float(merged["coincide"].mean())
    confusion = pd.crosstab(
        merged["categoria"],
        merged["categoria_revisada"],
        rownames=["categoria_automatica"],
        colnames=["categoria_revisada"],
    )

    summary = (
        merged.groupby(["categoria", "categoria_revisada"], dropna=False)
        .size()
        .reset_index(name="n")
        .rename(columns={"categoria": "categoria_automatica"})
    )
    summary["coincide"] = summary["categoria_automatica"] == summary["categoria_revisada"]
    summary.to_csv(SALIDAS / "revision_manual_resumen.csv", index=False, encoding="utf-8")

    discrepancies = merged[~merged["coincide"]][
        [
            "review_id",
            "obs_id",
            "estrategia",
            "modelo",
            "categoria",
            "subcategoria",
            "categoria_revisada",
            "justificacion",
            "respuesta_obtenida",
        ]
    ]
    discrepancies.to_csv(
        SALIDAS / "revision_manual_discrepancias.csv", index=False, encoding="utf-8"
    )

    print(f"\nAcuerdo automático–manual: {agreement:.1%}")
    print("\nMatriz de confusión:")
    print(confusion.to_string())
    print("\nDiscrepancias:", len(discrepancies))
    print("Resumen:", SALIDAS / "revision_manual_resumen.csv")
    print("Discrepancias:", SALIDAS / "revision_manual_discrepancias.csv")


if __name__ == "__main__":
    main()
