#!/usr/bin/env bash
set -euo pipefail

PACKAGE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
REPO_ROOT="$(cd "$PACKAGE_DIR/../.." && pwd)"
cd "$PACKAGE_DIR"

uv run --project "$REPO_ROOT/codigo_experimentos" --frozen python scripts/recalcular_acuerdo.py
uv run --project "$REPO_ROOT/codigo_experimentos" --frozen python reconciliacion_v1/scripts/reconciliar_v1.py
uv run --project "$REPO_ROOT/codigo_experimentos" --frozen python metricas_recuperacion/scripts/calcular_metricas.py
uv run --project "$REPO_ROOT/codigo_experimentos" --frozen python sensibilidad_umbral/scripts/verificar_umbrales.py
echo
echo "Verificación generada en $PACKAGE_DIR"
echo "Revisar: salidas/resumen_verificacion.json, reconciliacion_v1/, metricas_recuperacion/ y sensibilidad_umbral/"
