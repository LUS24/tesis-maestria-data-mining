"""Valida y resume la revisión manual ciega de IX.1.2.

Uso:
    uv run --project codigo_experimentos --no-sync --frozen \
      python analisis-valoracion-jurado/correccion-02-diagnostico-gpt-5-nano/src/validar_revision_manual.py

Requiere que `revision_manual/plantilla_resultados.csv` esté completa.
No modifica la plantilla ni el paquete ciego.
"""

from __future__ import annotations

from pathlib import Path
import sys

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
    template_path = Path(sys.argv[1]) if len(sys.argv) > 1 else REVISION / "plantilla_resultados.csv"
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
    template["revisor"] = template["revisor"].str.strip()
    template["fecha"] = template["fecha"].str.strip()

    invalid = template[
        (~template["categoria_revisada"].isin(CATEGORIAS))
        & (template["categoria_revisada"] != "")
    ]
    incomplete = template[template["categoria_revisada"] == ""]
    blank_justification = template[template["justificacion"] == ""]
    blank_reviewer = template[template["revisor"] == ""]
    blank_date = template[template["fecha"] == ""]
    invalid_date = template[
        (template["fecha"] != "")
        & (~template["fecha"].str.match(r"^\d{4}-\d{2}-\d{2}$"))
    ]

    print(f"Filas en la plantilla: {len(template)}")
    print(f"Filas con categoría: {len(template) - len(incomplete)}")
    print(f"Filas sin categoría: {len(incomplete)}")
    print(f"Categorías inválidas: {len(invalid)}")
    print(f"Justificaciones vacías: {len(blank_justification)}")
    print(f"Revisores vacíos: {len(blank_reviewer)}")
    print(f"Fechas vacías: {len(blank_date)}")
    print(f"Fechas con formato distinto de AAAA-MM-DD: {len(invalid_date)}")

    if len(invalid):
        print("\nCategorías inválidas:")
        print(invalid[["review_id", "categoria_revisada"]].to_string(index=False))

    if len(blank_justification):
        print("\nFilas con justificación vacía:")
        print(blank_justification[["review_id", "categoria_revisada"]].to_string(index=False))

    if len(blank_reviewer) or len(blank_date) or len(invalid_date):
        print("\nProblemas de revisor o fecha:")
        print(template.loc[
            template.index.isin(blank_reviewer.index)
            | template.index.isin(blank_date.index)
            | template.index.isin(invalid_date.index),
            ["review_id", "revisor", "fecha"],
        ].to_string(index=False))

    if len(incomplete) or len(invalid):
        print("\nCompleta las categorías antes de generar el resumen definitivo.")
        return

    if len(blank_justification):
        print("\nAdvertencia: las categorías están completas, pero faltan justificaciones.")
        print("El resumen se genera igualmente; completa las justificaciones para el acta de revisión.")

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
    print(f"Justificaciones vacías: {len(blank_justification)}")
    print("\nMatriz de confusión:")
    print(confusion.to_string())
    print("\nDiscrepancias:", len(discrepancies))
    print("Resumen:", SALIDAS / "revision_manual_resumen.csv")
    print("Discrepancias:", SALIDAS / "revision_manual_discrepancias.csv")


if __name__ == "__main__":
    main()
