#!/usr/bin/env python3
"""Write a SHA-256 manifest for inputs and generated artifacts."""
from __future__ import annotations
import csv, hashlib
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
REPO = BASE.parents[1]
FILES = [
    REPO / "data/20250804_101435_generated_questions-SIN_REVISION.docx",
    REPO / "data/20250804_101435_generated_questions - 130825-REVISADO.odt",
    REPO / "data/20250804_101435_generated_questions - 130825.json",
    REPO / "data/evaluation_questions_v20250804_101435.json",
    REPO / "data/codigo_de_mineria_actualizado_2025_08_02.json",
    REPO / "data/codigo_de_mineria_actualizado_2025_08_02.py",
    REPO / "codigo_experimentos/data/inputs/html/codigo_minero_43797.html",
    REPO / "codigo_experimentos/data/inputs/pdf/seccion_primera_19970530.pdf",
    REPO / "codigo_experimentos/data/outputs/llm_img_to_md/texto_original_codigo_mineria.md",
    REPO / "codigo_experimentos/data/outputs/llm_img_to_md/output_codigo_mineria.md",
    REPO / "manuscrito/capitulos/06_capitulo_05_metodologia.typ",
    REPO / "manuscrito/capitulos/anexo_01.typ",
]
for p in sorted((BASE / "salidas").glob("*")):
    if p.is_file():
        FILES.append(p)
for p in sorted(BASE.glob("*.md")):
    if p.is_file():
        FILES.append(p)

def sha(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

with (BASE / "manifiesto_sha256.csv").open("w", encoding="utf-8", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["ruta", "bytes", "sha256"])
    for p in FILES:
        w.writerow([str(p.relative_to(REPO)), p.stat().st_size, sha(p)])
print("manifest", len(FILES), "files")
