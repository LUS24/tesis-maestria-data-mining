#!/usr/bin/env python3
"""Genera manifiesto SHA-256 de fuentes y artefactos.

No modifica las fuentes. El manifiesto excluye su propio archivo y __pycache__.
"""

from __future__ import annotations

import csv
import hashlib
from pathlib import Path

BASE = Path(__file__).resolve().parent
REPO = BASE.parents[1]
OUT = BASE / "manifiesto_sha256.csv"
EXCLUDE_PARTS = {"__pycache__", ".ipynb_checkpoints"}


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def add(path: Path, kind: str) -> dict[str, str] | None:
    if not path.exists():
        return None
    if path.resolve() == OUT.resolve():
        return None
    if any(part in EXCLUDE_PARTS for part in path.parts):
        return None
    return {
        "ruta": str(path.relative_to(REPO)),
        "tipo": kind,
        "bytes": str(path.stat().st_size),
        "sha256": digest(path),
    }


def main() -> None:
    sources = [
        REPO / "manuscrito" / "referencias.bib",
        REPO / "manuscrito" / "main.typ",
        REPO / "codigo_experimentos" / "pyproject.toml",
    ]
    sources.extend(sorted((REPO / "manuscrito" / "capitulos").glob("*.typ")))

    artifacts = sorted(
        p for p in BASE.rglob("*")
        if p.is_file()
        and p.resolve() != OUT.resolve()
        and not any(part in EXCLUDE_PARTS for part in p.parts)
    )

    rows = []
    for path in sources:
        row = add(path, "fuente")
        if row:
            rows.append(row)
    for path in artifacts:
        row = add(path, "artefacto")
        if row:
            rows.append(row)

    with OUT.open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["ruta", "tipo", "bytes", "sha256"])
        w.writeheader()
        w.writerows(rows)
    print(f"{len(rows)} archivos en {OUT}")


if __name__ == "__main__":
    main()
