#!/usr/bin/env python3
"""Comprueba que los archivos listados en manifiesto_sha256.csv no cambiaron."""

from __future__ import annotations

import csv
import hashlib
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent
REPO = BASE.parents[1]
MANIFEST = BASE / "manifiesto_sha256.csv"


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    if not MANIFEST.exists():
        print("Falta manifiesto_sha256.csv. Ejecutar generar_manifiesto.py primero.")
        return 2
    with MANIFEST.open(encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    errors = []
    for row in rows:
        path = REPO / row["ruta"]
        if not path.exists():
            errors.append(f"FALTA {row['ruta']}")
            continue
        current = digest(path)
        if current != row["sha256"]:
            errors.append(f"CAMBIÓ {row['ruta']}: {row['sha256'][:12]} -> {current[:12]}")
    if errors:
        print("\n".join(errors))
        return 1
    print(f"OK: {len(rows)} archivos coinciden con el manifiesto.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
