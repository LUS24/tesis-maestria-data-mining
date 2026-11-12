#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT"

uv run --project codigo_experimentos --no-sync --frozen \
  python analisis-valoracion-jurado/correccion-02-diagnostico-gpt-5-nano/src/diagnostico.py
