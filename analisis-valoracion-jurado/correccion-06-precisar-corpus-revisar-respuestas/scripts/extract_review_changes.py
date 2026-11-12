#!/usr/bin/env python3
"""Extract tracked changes from the reviewed ODT and compare with the unreviewed DOCX.

Inputs are read-only. Outputs are written next to this script under ../salidas/.
Uses only the Python standard library.
"""
from __future__ import annotations

import csv
import difflib
import hashlib
import json
import re
import unicodedata
import zipfile
import xml.etree.ElementTree as ET
from collections import Counter, defaultdict
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
REPO = BASE.parents[1]
DATA = REPO / "data"
ODT = DATA / "20250804_101435_generated_questions - 130825-REVISADO.odt"
DOCX = DATA / "20250804_101435_generated_questions-SIN_REVISION.docx"
OUT = BASE / "salidas"
OUT.mkdir(parents=True, exist_ok=True)

NS = {
    "office": "urn:oasis:names:tc:opendocument:xmlns:office:1.0",
    "text": "urn:oasis:names:tc:opendocument:xmlns:text:1.0",
    "dc": "http://purl.org/dc/elements/1.1/",
    "w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main",
}
O = "{" + NS["office"] + "}"
T = "{" + NS["text"] + "}"
W = "{" + NS["w"] + "}"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def norm(s: str) -> str:
    s = s.replace("\xa0", " ")
    s = unicodedata.normalize("NFC", s)
    return re.sub(r"\s+", " ", s).strip()


def region_content(node: ET.Element) -> str:
    """Text of a deletion region, excluding change-info metadata."""
    out: list[str] = []

    def walk(e: ET.Element) -> None:
        tag = e.tag.split("}")[-1]
        if tag == "change-info":
            return
        if tag in ("p", "h"):
            out.append("".join(e.itertext()))
            return
        if tag == "s":
            out.append(" ")
        elif tag == "tab":
            out.append("\t")
        elif tag == "line-break":
            out.append("\n")
        else:
            if e.text:
                out.append(e.text)
            for c in e:
                walk(c)
            if e.tail:
                out.append(e.tail)

    walk(node)
    return "".join(out)


def read_regions(root: ET.Element) -> dict[str, dict]:
    regions: dict[str, dict] = {}
    tc = root.find(".//text:tracked-changes", NS)
    if tc is None:
        return regions
    for r in tc.findall("text:changed-region", NS):
        rid = r.get(T + "id")
        info: dict = {}
        for typ in ("insertion", "deletion", "format-change"):
            e = r.find("text:" + typ, NS)
            if e is not None:
                ci = e.find("office:change-info", NS)
                info = {
                    "type": typ,
                    "creator": ci.findtext("dc:creator", default="", namespaces=NS) if ci is not None else "",
                    "date": ci.findtext("dc:date", default="", namespaces=NS) if ci is not None else "",
                    "content": region_content(e).strip("\n") if typ == "deletion" else "",
                }
                break
        regions[rid] = info
    return regions


def inline(el: ET.Element, mode: str, regs: dict[str, dict], state: list[tuple[str, str]],
           captured: dict[str, list[str]]) -> str:
    """Return visible text for mode final/original; capture inserted text by change id."""
    active = [rid for kind, rid in state if kind == "insert"]
    if mode == "original" and active:
        return ""
    out: list[str] = []

    def add(s: str | None) -> None:
        if not s:
            return
        out.append(s)
        if mode == "final" and active:
            for rid in active:
                captured[rid].append(s)

    add(el.text)
    for c in el:
        tag = c.tag.split("}")[-1]
        if tag == "s":
            add(" ")
        elif tag == "tab":
            add("\t")
        elif tag == "line-break":
            add("\n")
        elif tag == "change-start":
            state.append(("insert", c.get(T + "change-id")))
            add(c.text)
        elif tag == "change-end":
            rid = c.get(T + "change-id")
            for i in range(len(state) - 1, -1, -1):
                if state[i] == ("insert", rid):
                    del state[i:]
                    break
            add(c.text)
        elif tag == "change":
            rid = c.get(T + "change-id")
            info = regs.get(rid, {})
            if mode == "original" and info.get("type") == "deletion":
                add(info.get("content", ""))
            add(c.tail)
            continue
        elif tag in ("tracked-changes", "sequence-decls", "annotation"):
            pass
        else:
            add(inline(c, mode, regs, state, captured))
        if tag not in ("change", "change-start", "change-end"):
            add(c.tail)
    return "".join(out)


def walk_blocks(container: ET.Element, mode: str, regs: dict[str, dict], state: list[tuple[str, str]],
                captured: dict[str, list[str]], out: list[dict]) -> None:
    for c in container:
        tag = c.tag.split("}")[-1]
        if tag in ("p", "h"):
            out.append({
                "tag": tag,
                "style": c.get(T + "style-name", ""),
                "text": inline(c, mode, regs, state, captured),
            })
        elif tag == "list":
            for item in c:
                if item.tag.split("}")[-1] in ("list-item", "list-header"):
                    walk_blocks(item, mode, regs, state, captured, out)
        elif tag in ("tracked-changes", "sequence-decls"):
            continue
        elif tag == "section":
            walk_blocks(c, mode, regs, state, captured, out)
        elif tag == "table":
            for row in c.iter(T + "table-row"):
                for cell in row.findall(T + "table-cell", NS):
                    walk_blocks(cell, mode, regs, state, captured, out)
        elif tag in ("list-item", "list-header"):
            walk_blocks(c, mode, regs, state, captured, out)


def odt_blocks(mode: str) -> tuple[dict[str, dict], list[dict], dict[str, list[str]]]:
    with zipfile.ZipFile(ODT) as z:
        root = ET.fromstring(z.read("content.xml"))
    regs = read_regions(root)
    body = root.find(".//office:text", NS)
    out: list[dict] = []
    captured: dict[str, list[str]] = defaultdict(list)
    walk_blocks(body, mode, regs, [], captured, out)
    return regs, out, captured


def docx_blocks() -> list[dict]:
    with zipfile.ZipFile(DOCX) as z:
        root = ET.fromstring(z.read("word/document.xml"))
    body = root.find("w:body", NS)
    out: list[dict] = []
    for p in body.iter(W + "p"):
        style = ""
        ppr = p.find("w:pPr", NS)
        if ppr is not None:
            ps = ppr.find("w:pStyle", NS)
            if ps is not None:
                style = ps.get(W + "val", "")
        parts: list[str] = []
        for e in p.iter():
            if e.tag == W + "t":
                parts.append(e.text or "")
            elif e.tag == W + "tab":
                parts.append("\t")
            elif e.tag in (W + "br", W + "cr"):
                parts.append("\n")
        out.append({"tag": "p", "style": style, "text": "".join(parts)})
    return out


def align_sequences(a: list[dict], b: list[dict]) -> list[tuple[str, int | None, int | None]]:
    """Align normalized paragraph sequences; returns (opcode, i, j)."""
    an = [norm(x["text"]) for x in a]
    bn = [norm(x["text"]) for x in b]
    sm = difflib.SequenceMatcher(None, an, bn, autojunk=False)
    ops: list[tuple[str, int | None, int | None]] = []
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            for k in range(i2 - i1):
                ops.append(("equal", i1 + k, j1 + k))
        elif tag == "replace":
            # pair as many as possible, then mark additions/deletions
            n = min(i2 - i1, j2 - j1)
            for k in range(n):
                ops.append(("replace", i1 + k, j1 + k))
            for k in range(i1 + n, i2):
                ops.append(("delete", k, None))
            for k in range(j1 + n, j2):
                ops.append(("insert", None, k))
        elif tag == "delete":
            for k in range(i1, i2):
                ops.append(("delete", k, None))
        elif tag == "insert":
            for k in range(j1, j2):
                ops.append(("insert", None, k))
    return ops


def case_label(text: str) -> str:
    m = re.search(r"t[ií]tulo_([ivxlcdm]+)\.md", text)
    return f"Título {m.group(1)}" if m else ""


def annotate_context(blocks: list[dict]) -> None:
    """Assign the current case file and document section to every block."""
    case = ""
    section = "instruccion_generadora"
    for b in blocks:
        t = b["text"].strip()
        low = t.lower()
        if re.search(r"t[ií]tulo_[ivxlcdm]+\.md|t[ií]tulo_final\.md", t):
            case = t
            section = "caso"
        elif low.startswith(("caso ", "caso:", "pregunta basada", "caso práctico", "caso prã¡ctico")):
            section = "caso"
        elif low.startswith("respuesta"):
            section = "respuesta"
        elif low.startswith(("preguntas", "pregunta:", "responda", "en este contexto", "en ese contexto", "en función", "explique,")):
            section = "preguntas"
        b["case"] = case
        b["section"] = section


def locate_block(content: str, blocks: list[dict]) -> int | None:
    c = norm(content)
    if not c:
        return None
    exact = [i for i, b in enumerate(blocks) if c in norm(b["text"])]
    if exact:
        return exact[0]
    best = max(((difflib.SequenceMatcher(None, c, norm(b["text"]), autojunk=False).ratio(), i) for i, b in enumerate(blocks)), default=(0, None))
    return best[1] if best[0] >= 0.45 else None


def classify_change(content: str, section: str) -> tuple[str, str]:
    c = content.lower()
    if re.search(r"comentario|sugier|sugiero|fijate|fíjate|ojo|ver estilo|estilo|insisto|quiz|me parece|revis|aclar|localizar|eliminar|omitir|convenva|realidad", c):
        return "comentario_o_instruccion_editorial", "Revisar decisión; no incorporar como texto del benchmark sin resolverla."
    if re.search(r"código|normativa|disposiciones|artículo|art\.", c):
        return "precision_normativa", "Verificar referencia y redacción contra el corpus."
    if re.search(r"\b(?:[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+\s+){1,3}[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+\b", content) or re.search(r"San Juan|Chubut|Tierra del Fuego|Jujuy|Santa Cruz|Neuquén|Salta|Mendoza", content):
        return "precision_factica", "Verificar nombre/lugar y consistencia con el resto del caso."
    if section == "respuesta":
        return "posible_cambio_de_contenido", "Revisar si altera la respuesta de referencia."
    if section in ("caso", "preguntas"):
        return "cambio_de_enunciado", "Revisar si altera el alcance de la pregunta."
    return "cambio_de_redaccion", "Revisar redacción."


def main() -> None:
    regs_o, orig, _ = odt_blocks("original")
    regs_f, fin, captured = odt_blocks("final")
    doc = docx_blocks()
    annotate_context(orig)
    annotate_context(fin)

    # Build changes from tracked regions.
    changes: list[dict] = []
    for rid, info in regs_f.items():
        content = "".join(captured.get(rid, [])) if info["type"] == "insertion" else info.get("content", "")
        content = norm(content)
        if not content:
            continue
        target = locate_block(content, fin if info["type"] == "insertion" else orig)
        tb = (fin if info["type"] == "insertion" else orig)[target] if target is not None else {"case": "", "section": "", "text": ""}
        categoria, impacto = classify_change(content, tb["section"])
        changes.append({
            "change_id": rid,
            "tipo": info["type"],
            "fecha": info["date"],
            "autor": info["creator"],
            "texto": content,
            "caso": tb["case"],
            "seccion": tb["section"],
            "block_index": target,
            "parrafo": tb["text"],
            "categoria": categoria,
            "impacto": impacto,
        })
    changes.sort(key=lambda x: (x["fecha"], x["change_id"]))

    # Align unrevised DOCX against reconstructed original ODT.
    ops = align_sequences(doc, orig)
    alignment: list[dict] = []
    for op, i, j in ops:
        d = doc[i]["text"] if i is not None else ""
        o = orig[j]["text"] if j is not None else ""
        alignment.append({
            "op": op,
            "docx_index": i,
            "odt_original_index": j,
            "docx_text": d,
            "odt_original_text": o,
            "docx_norm": norm(d),
            "odt_original_norm": norm(o),
            "same": norm(d) == norm(o),
        })

    # Align original and final ODT blocks.
    ops2 = align_sequences(orig, fin)
    para_changes: list[dict] = []
    for op, i, j in ops2:
        o = orig[i]["text"] if i is not None else ""
        f = fin[j]["text"] if j is not None else ""
        if norm(o) == norm(f):
            continue
        para_changes.append({
            "op": op,
            "original_index": i,
            "final_index": j,
            "original_text": o,
            "final_text": f,
            "original_norm": norm(o),
            "final_norm": norm(f),
            "case": (fin[j]["case"] if j is not None else "") or (orig[i]["case"] if i is not None else ""),
            "section": (fin[j]["section"] if j is not None else "") or (orig[i]["section"] if i is not None else ""),
        })

    # Write CSVs.
    with (OUT / "cambios_rastreados.csv").open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["change_id", "tipo", "fecha", "autor", "texto", "caso", "seccion", "block_index", "categoria", "impacto", "parrafo"])
        w.writeheader()
        w.writerows(changes)

    with (OUT / "parrafos_antes_despues.csv").open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["op", "original_index", "final_index", "case", "section", "original_text", "final_text", "original_norm", "final_norm"])
        w.writeheader()
        w.writerows(para_changes)

    with (OUT / "alineacion_docx_odt.csv").open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["op", "docx_index", "odt_original_index", "docx_text", "odt_original_text", "docx_norm", "odt_original_norm", "same"])
        w.writeheader()
        w.writerows(alignment)

    # Human-readable review report.
    lines = [
        "# Comparación del benchmark sin revisión y revisado por la abogada",
        "",
        "## Archivos de entrada",
        "",
        f"- Sin revisión: `{DOCX.relative_to(REPO)}` — SHA-256 `{sha256(DOCX)}`",
        f"- Revisado con cambios registrados: `{ODT.relative_to(REPO)}` — SHA-256 `{sha256(ODT)}`",
        "",
        "## Resumen estructural",
        "",
        f"- Párrafos/bloques en DOCX: **{len(doc)}**",
        f"- Bloques reconstruidos del ODT original: **{len(orig)}**",
        f"- Bloques reconstruidos del ODT final: **{len(fin)}**",
        f"- Regiones de cambio registradas: **{len(regs_f)}**",
        f"- Inserciones con texto: **{sum(1 for c in changes if c['tipo'] == 'insertion')}**",
        f"- Eliminaciones con texto: **{sum(1 for c in changes if c['tipo'] == 'deletion')}**",
        f"- Párrafos con texto distinto entre original y final: **{len(para_changes)}**",
        "",
        "## Cambios registrados",
        "",
    ]
    for c in changes:
        lines.append(f"### {c['tipo']} — {c['fecha']} — `{c['change_id']}`")
        lines.append("")
        lines.append(f"- Caso: `{c['caso'] or 'instrucción general'}`")
        lines.append(f"- Sección: `{c['seccion']}`")
        lines.append(f"- Clasificación: `{c['categoria']}` — {c['impacto']}")
        if c["parrafo"]:
            lines.append(f"- Párrafo: {c['parrafo'][:500]}")
        lines.append("")
        lines.append(f"> {c['texto']}")
        lines.append("")
    (OUT / "comparacion_docx_odt.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    # Grouped by case: a compact review table.
    grouped = defaultdict(list)
    for c in changes:
        grouped[c["caso"] or "instrucción general"].append(c)
    glines = ["# Cambios por caso", "", "Cada fila es una inserción o eliminación registrada en el ODT. Los comentarios y decisiones editoriales no son texto del benchmark hasta que se resuelvan.", ""]
    for case in sorted(grouped, key=lambda x: (x == "instrucción general", x)):
        glines.append(f"## {case}")
        glines.append("")
        glines.append("| Fecha | Tipo | Sección | Clasificación | Texto |")
        glines.append("| --- | --- | --- | --- | --- |")
        for c in grouped[case]:
            txt = c["texto"].replace("|", "\\|").replace("\n", " ")[:350]
            glines.append(f"| {c['fecha']} | {c['tipo']} | {c['seccion']} | {c['categoria']} | {txt} |")
        glines.append("")
    (OUT / "cambios_por_caso.md").write_text("\n".join(glines) + "\n", encoding="utf-8")

    # JSON index.
    meta = {
        "docx": {"path": str(DOCX.relative_to(REPO)), "sha256": sha256(DOCX), "blocks": len(doc)},
        "odt": {"path": str(ODT.relative_to(REPO)), "sha256": sha256(ODT), "regions": len(regs_f), "blocks_original": len(orig), "blocks_final": len(fin)},
        "changes": changes,
        "paragraph_changes": para_changes,
    }
    (OUT / "comparacion_docx_odt.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")

    print(json.dumps({k: meta[k] for k in ("docx", "odt")}, ensure_ascii=False, indent=2))
    print("changes with text", len(changes), "paragraph changes", len(para_changes))
    print("same DOCX/ODT original", sum(1 for x in alignment if x["same"]), "of", len(alignment))


if __name__ == "__main__":
    main()
