#!/usr/bin/env bash
# Ejecuta de extremo a extremo la corrección IX.1.1.
# No modifica archivos fuente ni registros históricos.

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
CORR="analisis-valoracion-jurado/correccion-01-analisis-estadistico"
R_LIBS_C01="${R_LIBS_C01:-/tmp/pi-rlib-c01}"

if ! command -v uv >/dev/null 2>&1; then
  echo "Falta uv. Instalarlo desde https://docs.astral.sh/uv/" >&2
  exit 1
fi
if ! command -v Rscript >/dev/null 2>&1; then
  echo "Falta Rscript. Instalar R antes de ejecutar el modelo ordinal." >&2
  exit 1
fi

echo "== 1. Base analítica =="
cd "$ROOT/codigo_experimentos"
uv run --no-sync --frozen python "../$CORR/src/build_dataset.py"

echo "== 2. Pruebas pareadas y bootstrap =="
uv run --no-sync --frozen python "../$CORR/src/run_nonparametric.py"

echo "== 3. Modelo ordinal mixto =="
R_LIBS_C01="$R_LIBS_C01" Rscript "../$CORR/src/run_ordinal_model.R"

echo "== 4. Figuras =="
uv run --no-sync --frozen python "../$CORR/src/make_figures.py"

echo "== 5. Resumen =="
uv run --no-sync --frozen python "../$CORR/src/summarize_results.py"

echo "== 6. Tablas Typst de borrador =="
uv run --no-sync --frozen python "../$CORR/src/make_typst_tables.py"
if command -v typst >/dev/null 2>&1; then
  typst compile --root "$ROOT" "$ROOT/$CORR/propuestas/preview_tablas.typ" "$ROOT/$CORR/propuestas/preview_tablas.pdf"
fi

echo "== 7. Validación =="
uv run --no-sync --frozen python "../$CORR/src/validate_artifacts.py"

echo
echo "Listo. Revisar:"
echo "  $ROOT/$CORR/INFORME_ANALISIS_ESTADISTICO.md"
echo "  $ROOT/$CORR/PROPUESTA_TEXTO_MANUSCRITO.md"
