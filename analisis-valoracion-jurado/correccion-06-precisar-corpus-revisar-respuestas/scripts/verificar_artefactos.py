#!/usr/bin/env python3
"""Verify key invariants of the generated artifacts."""
from __future__ import annotations
import csv, hashlib, sys
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
REPO = BASE.parents[1]
checks = []

def rows(name):
    with (BASE / "salidas" / name).open(encoding="utf-8") as fh:
        return list(csv.DictReader(fh))

def check(label, cond, detail=""):
    checks.append((label, bool(cond), detail))

check("130 cambios con texto", len(rows("cambios_rastreados.csv")) == 130, str(len(rows("cambios_rastreados.csv"))))
check("80 párrafos modificados", len(rows("parrafos_antes_despues.csv")) == 80, str(len(rows("parrafos_antes_despues.csv"))))
check("482 nodos de corpus", len(rows("corpus_nodos.csv")) == 482, str(len(rows("corpus_nodos.csv"))))
check("398 nodos artículo", len(rows("corpus_articulos.csv")) == 398, str(len(rows("corpus_articulos.csv"))))
check("79 unidades benchmark", len(rows("unidades_benchmark.csv")) == 79, str(len(rows("unidades_benchmark.csv"))))
check("166 referencias benchmark", len(rows("referencias_benchmark.csv")) == 166, str(len(rows("referencias_benchmark.csv"))))
check("12 propuestas benchmark", len(rows("propuestas_benchmark.csv")) == 12, str(len(rows("propuestas_benchmark.csv"))))
# source hashes must match manifest
with (BASE / "manifiesto_sha256.csv").open(encoding="utf-8") as fh:
    manifest = list(csv.DictReader(fh))
source_prefixes = ("data/", "codigo_experimentos/data/", "manuscrito/capitulos/")
for r in manifest:
    if r["ruta"].startswith(source_prefixes) and not r["ruta"].startswith("analisis-"):
        p = REPO / r["ruta"]
        if p.exists():
            h = hashlib.sha256(p.read_bytes()).hexdigest()
            check(f"hash fuente {r['ruta']}", h == r["sha256"], "OK" if h == r["sha256"] else "CAMBIÓ")
for label, ok, detail in checks:
    print(("OK  " if ok else "FAIL"), label, detail)
sys.exit(0 if all(x[1] for x in checks) else 1)
