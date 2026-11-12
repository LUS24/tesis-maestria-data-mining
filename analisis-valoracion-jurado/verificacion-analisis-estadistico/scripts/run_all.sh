#!/usr/bin/env bash
set -euo pipefail

PACKAGE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
REPO_ROOT="$(cd "$PACKAGE_DIR/../.." && pwd)"
cd "$PACKAGE_DIR"

uv run --project "$REPO_ROOT/codigo_experimentos" --frozen python scripts/recalcular_acuerdo.py
echo
echo "Verificación generada en $PACKAGE_DIR"
echo "Revisar: salidas/resumen_verificacion.json"
