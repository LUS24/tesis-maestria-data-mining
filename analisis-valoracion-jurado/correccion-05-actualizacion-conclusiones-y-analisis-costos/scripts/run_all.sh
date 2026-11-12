#!/usr/bin/env bash
set -euo pipefail

# Corrección IX.1.5 — reproduce todos los artefactos sin modificar fuentes.
# Uso: bash scripts/run_all.sh

PACKAGE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
REPO_ROOT="$(cd "$PACKAGE_DIR/../.." && pwd)"
EXPERIMENT_PROJECT="$REPO_ROOT/codigo_experimentos"

cd "$PACKAGE_DIR"

echo "[1/4] Análisis de costos y figuras"
uv run --project "$EXPERIMENT_PROJECT" --frozen python scripts/build_cost_analysis.py

echo "[2/4] Tablas de conclusiones y trazabilidad"
python3 scripts/build_conclusion_tables.py

echo "[3/4] Controles de consistencia"
python3 scripts/verify_artifacts.py

echo "[4/4] Vista previa Typst"
if command -v typst >/dev/null 2>&1; then
  typst compile propuestas/vista_previa_tabla4_y_costos.typ propuestas/vista_previa_tabla4_y_costos.pdf
  if command -v pdftoppm >/dev/null 2>&1; then
    pdftoppm -png -r 110 -f 1 -singlefile propuestas/vista_previa_tabla4_y_costos.pdf propuestas/vista_previa
  fi
else
  echo "Aviso: typst no está instalado; se omite la vista previa." >&2
fi

echo
echo "Listo. Revisar:"
echo "  $PACKAGE_DIR/DECISIONES.md"
echo "  $PACKAGE_DIR/TABLA_4_REFORMULADA.md"
echo "  $PACKAGE_DIR/PROPUESTA_TEXTO_MANUSCRITO.md"
echo "  $PACKAGE_DIR/ANALISIS_COSTOS.md"
echo "  $PACKAGE_DIR/salidas/verificacion_artefactos.json"
