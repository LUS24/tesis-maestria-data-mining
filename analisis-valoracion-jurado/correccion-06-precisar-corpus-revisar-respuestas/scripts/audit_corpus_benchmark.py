#!/usr/bin/env python3
"""Audit corpus provenance and benchmark references/answers without modifying sources.

Outputs:
  salidas/corpus_nodos.csv
  salidas/corpus_articulos.csv
  salidas/corpus_metadatos.csv
  salidas/corpus_vs_fuentes.csv
  salidas/referencias_benchmark.csv
  salidas/unidades_benchmark.csv
  salidas/citas_respuestas.csv
  salidas/auditoria_corpus_benchmark.md
"""
from __future__ import annotations

import csv
import difflib
import hashlib
import html
import json
import re
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
REPO = BASE.parents[1]
CORPUS = REPO / "data" / "codigo_de_mineria_actualizado_2025_08_02.json"
BENCH = REPO / "data" / "evaluation_questions_v20250804_101435.json"
HTML = REPO / "codigo_experimentos" / "data" / "inputs" / "html" / "codigo_minero_43797.html"
OCR_SHORT = REPO / "codigo_experimentos" / "data" / "outputs" / "llm_img_to_md" / "texto_original_codigo_mineria.md"
OCR_LONG = REPO / "codigo_experimentos" / "data" / "outputs" / "llm_img_to_md" / "output_codigo_mineria.md"
OUT = BASE / "salidas"
OUT.mkdir(parents=True, exist_ok=True)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def norm(s: str) -> str:
    s = html.unescape(s or "").replace("\xa0", " ")
    s = unicodedata.normalize("NFC", s)
    return re.sub(r"\s+", " ", s).strip()


def tokens(s: str) -> set[str]:
    return set(re.findall(r"\w+", norm(s).lower(), re.UNICODE))


def jaccard(a: str, b: str) -> float:
    ta, tb = tokens(a), tokens(b)
    return len(ta & tb) / len(ta | tb) if ta | tb else 0.0


def ratio(a: str, b: str) -> float:
    return difflib.SequenceMatcher(None, norm(a), norm(b), autojunk=False).ratio()


def walk(parts, path=(), ancestors=()):
    for i, x in enumerate(parts):
        yield x, path, ancestors, i
        yield from walk(x.get("partes", []) or [], path + (x.get("numero_parte"),), ancestors + (x,))


def section_of(path) -> str:
    if path and path[0] is not None:
        return "cuerpo"
    if len(path) == 1:
        return "disposiciones"
    return "apendice"


def load_corpus():
    data = json.loads(CORPUS.read_text(encoding="utf-8"))
    nodes = []
    for x, path, ancestors, idx in walk(data.get("partes", [])):
        sec = section_of(path) if x.get("tipo_parte") == "artículo" else ""
        nodes.append({
            "tipo": x.get("tipo_parte", ""),
            "numero": x.get("numero_parte"),
            "titulo": x.get("titulo_parte", ""),
            "estado": x.get("ultimo_estado", ""),
            "texto": x.get("contenido_texto") or "",
            "path": " > ".join(str(p) for p in path if p is not None),
            "path_raw": path,
            "section": sec,
            "parent_title": ancestors[0].get("titulo_parte") if ancestors else "",
            "parent_type": ancestors[0].get("tipo_parte") if ancestors else "",
            "node_index": idx,
        })
    return data, nodes


def html_paragraphs() -> list[str]:
    s = HTML.read_text(encoding="cp1252", errors="replace")
    paras = []
    for m in re.finditer(r"<p[^>]*>(.*?)</p>", s, flags=re.I | re.S):
        t = re.sub(r"<[^>]+>", " ", m.group(1))
        t = html.unescape(t).replace("\xa0", " ")
        t = re.sub(r"\s+", " ", t).strip()
        if t:
            paras.append(t)
    return paras


def html_sections() -> dict[tuple[str, int], str]:
    paras = html_paragraphs()
    start = next(i for i, t in enumerate(paras) if t.startswith("Dada en la Sala de Sesiones"))
    start = next(i for i in range(start, len(paras)) if paras[i] == "CODIGO DE MINERIA")
    app = next(i for i, t in enumerate(paras) if i > start and t == "APENDICE")

    def parse(a, b):
        out = {}
        cur = None
        for i in range(a, b):
            t = paras[i]
            m = re.match(r"^Art\.?\s*(\d+)\s*(?:°|º|\.)?\s*[-–—.]?\s*(.*)$", t, re.I)
            if m:
                n = int(m.group(1))
                cur = n
                out[cur] = [m.group(2).strip()]
            elif cur is not None:
                if re.match(r"^(TITULO|[IVX]+\s|APENDICE|Antecedentes)", t, re.I) and len(t) < 120:
                    cur = None
                else:
                    out[cur].append(t)
        return {k: " ".join(v) for k, v in out.items()}

    main = parse(start, app)
    ap = parse(app, len(paras))
    result = {}
    for n, t in main.items():
        result[("disposiciones" if 348 <= n <= 362 else "cuerpo", n)] = t
    for n, t in ap.items():
        result[("apendice", n)] = t
    return result


def ocr_articles(path: Path) -> dict[int, str]:
    s = path.read_text(encoding="utf-8")
    matches = list(re.finditer(r"ARTÍCULO\s+(\d+)\s*[°º.]?\s*[—–-]?\s*", s, re.I))
    out = {}
    for i, m in enumerate(matches):
        n = int(m.group(1))
        end = matches[i + 1].start() if i + 1 < len(matches) else len(s)
        if n not in out:
            out[n] = norm(s[m.end():end])
    return out


def parse_ref(ref: str):
    m = re.search(r"(\d+)", ref)
    n = int(m.group(1)) if m else None
    inciso = ""
    mi = re.search(r"inciso\s+([a-z0-9]+)", ref, re.I)
    if mi:
        inciso = mi.group(1).lower()
    return n, inciso


def extract_citations(text: str) -> list[dict]:
    """Extract article citations, including lists such as 'artículos 7°, 10° y 11°'.

    Only the citation list immediately after the keyword is parsed. This avoids
    treating quantities later in the sentence (for example "10 metros") as articles.
    """
    cites = []
    pat = re.compile(r"\b(?:artículos?|articulo?s?|arts?\.?)\s*(?:N[°º.]?|Nro\.?)?\s*", re.I)
    list_pat = re.compile(r"^\s*(\d+(?:\s*(?:°|º|\.)?\s*(?:,|y|e|/|-|–)\s*\d+)*)", re.I)
    for m in pat.finditer(text):
        tail = text[m.end():m.end() + 80]
        lm = list_pat.match(tail)
        if not lm:
            continue
        nums = [int(x) for x in re.findall(r"\d+", lm.group(1))]
        for a, b in re.findall(r"(\d+)\s*[-–]\s*(\d+)", lm.group(1)):
            a, b = int(a), int(b)
            if 0 < a <= b <= 400 and b - a <= 20:
                nums.extend(range(a, b + 1))
        for n in sorted(set(nums)):
            if 1 <= n <= 400:
                cites.append({"numero": n, "snippet": norm(text[m.start():m.end() + 90])})
    seen = set()
    result = []
    for c in cites:
        if c["numero"] not in seen:
            seen.add(c["numero"])
            result.append(c)
    return result


def main():
    data, nodes = load_corpus()
    articles = [n for n in nodes if n["tipo"] == "artículo"]
    by_key = {(n["section"], n["numero"]): n for n in articles if n["numero"] is not None}
    by_num = defaultdict(list)
    for n in articles:
        by_num[n["numero"]].append(n)
    html_art = html_sections()
    ocr_short = ocr_articles(OCR_SHORT)
    ocr_long = ocr_articles(OCR_LONG)

    # corpus_nodos.csv
    with (OUT / "corpus_nodos.csv").open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["tipo", "numero", "titulo", "estado", "section", "path", "parent_title", "texto_len", "texto_sha256"])
        w.writeheader()
        for n in nodes:
            w.writerow({
                "tipo": n["tipo"], "numero": n["numero"], "titulo": n["titulo"], "estado": n["estado"],
                "section": n["section"], "path": n["path"], "parent_title": n["parent_title"],
                "texto_len": len(n["texto"]), "texto_sha256": hashlib.sha256(n["texto"].encode()).hexdigest(),
            })

    # corpus_articulos.csv
    with (OUT / "corpus_articulos.csv").open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["section", "numero", "estado", "parent_title", "path", "texto_len", "duplicado_en_otra_seccion", "texto"])
        w.writeheader()
        for n in articles:
            w.writerow({
                "section": n["section"], "numero": n["numero"], "estado": n["estado"],
                "parent_title": n["parent_title"], "path": n["path"], "texto_len": len(n["texto"]),
                "duplicado_en_otra_seccion": "sí" if len(by_num[n["numero"]]) > 1 else "no",
                "texto": n["texto"],
            })

    # metadata audit
    meta = data
    metadata_rows = [
        {"campo": "fecha_sancion", "valor_json": meta.get("fecha_sancion"), "valor_verificado": "1886-11-25", "fuente": "Argentina.gob.ar/InfoLeg, Ley 1919/1886: https://www.argentina.gob.ar/normativa/nacional/ley-1919-43797", "estado": "incorrecto"},
        {"campo": "fecha_promulgacion", "valor_json": meta.get("fecha_promulgacion"), "valor_verificado": "no verificado / no usar sin fuente", "fuente": "No surge de la ficha oficial consultada", "estado": "no sustentado"},
        {"campo": "fecha_publicacion", "valor_json": meta.get("fecha_publicacion"), "valor_verificado": "Registro Nacional 1885/86, p. 578; texto ordenado: B.O. 1997-05-30", "fuente": "Ficha oficial Ley 1919/1886 y Decreto 456/1997: https://www.argentina.gob.ar/normativa/nacional/decreto-456-1997-43581", "estado": "incorrecto"},
        {"campo": "fecha_ultima_actualizacion", "valor_json": meta.get("fecha_ultima_actualizacion"), "valor_verificado": "no verificada en las fuentes locales; el HTML contiene notas hasta 2023", "fuente": "HTML local codigo_minero_43797.html", "estado": "no verificada"},
        {"campo": "conteo_articulos", "valor_json": "398 nodos tipo artículo", "valor_verificado": "347 cuerpo + 15 disposiciones (348-362) + 36 apéndice = 398", "fuente": "data/codigo_de_mineria_actualizado_2025_08_02.json", "estado": "aclarar: 398 nodos, 362 numeros únicos"},
        {"campo": "articulo_239", "valor_json": "texto vacío", "valor_verificado": "derogado por Ley 26.909 (B.O. 2013-12-05), según HTML", "fuente": "HTML local; corpus JSON", "estado": "consistente pero debe explicarse"},
    ]
    with (OUT / "corpus_metadatos.csv").open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["campo", "valor_json", "valor_verificado", "fuente", "estado"])
        w.writeheader()
        w.writerows(metadata_rows)

    # source comparisons for key articles
    compare_rows = []
    for n in [3, 8, 11, 17, 31, 215, 221, 239, 351, 355]:
        c = by_key.get(("cuerpo", n)) or by_key.get(("disposiciones", n)) or by_key.get(("apendice", n))
        if not c:
            continue
        h = html_art.get((c["section"], n), "")
        oc = ocr_short.get(n, "")
        ol = ocr_long.get(n, "")
        compare_rows.append({
            "articulo": n, "seccion_corpus": c["section"], "estado_corpus": c["estado"],
            "corpus_len": len(c["texto"]), "html_len": len(h), "ocr_corto_len": len(oc), "ocr_largo_len": len(ol),
            "corpus_vs_html_jaccard": round(jaccard(c["texto"], h), 4) if h else "",
            "corpus_vs_ocr_corto_jaccard": round(jaccard(c["texto"], oc), 4) if oc else "",
            "corpus_vs_ocr_largo_jaccard": round(jaccard(c["texto"], ol), 4) if ol else "",
            "corpus_excerpt": norm(c["texto"])[:500],
            "html_excerpt": norm(h)[:500],
            "ocr_corto_excerpt": norm(oc)[:500],
            "ocr_largo_excerpt": norm(ol)[:500],
            "corpus_marcadores": "", "html_marcadores": "", "ocr_marcadores": "",
            "observacion": "",
        })
    obs = {
        3: "Corpus incluye 'wollastonita' y no incluye 'talio'; el OCR de 1997 no incluye 'wollastonita'. HTML contiene nota de sustitución por Ley 25.225/1999.",
        31: "Corpus coincide con el artículo 31 actual del HTML (20.000/40.000 km2; 120 días); el OCR corto no llega al artículo 31 y el largo no contiene el artículo 31 del cuerpo.",
        215: "Corpus contiene el texto actual con valores $1.900/$960; el OCR largo contiene una versión incompatible (porcentajes y remisiones distintas).",
        221: "Corpus contiene el texto actual con $960/$4.800 y nota de Ley 27.701/2022; el OCR largo no contiene el artículo 221.",
        239: "Corpus lo marca derogado y deja texto vacío; HTML conserva la nota de derogación por Ley 26.909/2013.",
        351: "Corpus contiene la redacción actual (multiplicador 10/5/2); el OCR largo contiene una redacción anterior ('duplicando... cánones suspendidos').",
        355: "Corpus contiene la redacción actual sobre informe de impacto ambiental; el OCR largo contiene una redacción anterior sobre cánones.",
    }
    markers = {3: ["wollastonita", "talio"], 31: ["20.000", "40.000", "ciento veinte (120)"], 215: ["1.900", "960"], 221: ["960", "4.800"], 351: ["multiplicado por DIEZ (10)", "CINCO (5)", "DUPLICANDO", "cánones suspendidos"], 355: ["informe de impacto ambiental", "no regirán cánones"]}
    for r in compare_rows:
        r["observacion"] = obs.get(r["articulo"], "")
        for key, col in [("corpus_excerpt", "corpus_marcadores"), ("html_excerpt", "html_marcadores"), ("ocr_corto_excerpt", "ocr_corto_marcadores"), ("ocr_largo_excerpt", "ocr_largo_marcadores")]:
            r[col] = "; ".join(f"{m}: {'sí' if m.lower() in r[key].lower() else 'no'}" for m in markers.get(r["articulo"], []))
    with (OUT / "corpus_vs_fuentes.csv").open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(compare_rows[0].keys()))
        w.writeheader()
        w.writerows(compare_rows)

    # benchmark units and references
    bench = json.loads(BENCH.read_text(encoding="utf-8"))
    units = []
    ref_rows = []
    for q in bench["preguntas"]:
        qn = q["numero_pregunta"]
        subs = q.get("sub_preguntas", []) or []
        if subs:
            for s in subs:
                units.append({
                    "caso": qn, "sub": s.get("numero_subpregunta"), "tipo": q.get("tipo_pregunta", ""),
                    "enunciado": q.get("texto_enunciado", ""), "pregunta": s.get("texto_subpregunta", ""),
                    "respuesta": s.get("respuesta", ""), "refs": s.get("contexto_para_respuesta", []) or [],
                })
        else:
            units.append({
                "caso": qn, "sub": "", "tipo": q.get("tipo_pregunta", ""),
                "enunciado": q.get("texto_enunciado", ""), "pregunta": q.get("texto_pregunta", ""),
                "respuesta": q.get("respuesta", ""), "refs": q.get("contexto_para_respuesta", []) or [],
            })

    for u in units:
        u["unidad_id"] = f"Q{u['caso']}.{u['sub'] or '0'}"
        u["refs_nums"] = []
        u["refs_detail"] = []
        for ref in u["refs"]:
            n, inciso = parse_ref(ref)
            if n is None:
                continue
            u["refs_nums"].append(n)
            candidates = by_num.get(n, [])
            primary = by_key.get(("cuerpo", n)) or by_key.get(("disposiciones", n)) or by_key.get(("apendice", n))
            if primary is None:
                status = "no_encontrado"
            elif not primary["texto"].strip():
                status = "nodo_vacio"
            else:
                status = "ok"
            ambiguo = len(candidates) > 1
            u["refs_detail"].append({"ref": ref, "numero": n, "inciso": inciso, "status": status, "primary": primary, "candidates": candidates})
            ref_rows.append({
                "unidad_id": u["unidad_id"], "caso": u["caso"], "sub": u["sub"], "referencia": ref,
                "numero": n, "inciso": inciso, "estado": status,
                "ambiguedad_numeracion": "sí" if ambiguo else "no",
                "seccion_principal": primary["section"] if primary else "",
                "texto_len": len(primary["texto"]) if primary else 0,
                "candidatos": " | ".join(f"{x['section']}:{x['numero']} ({x['estado']})" for x in candidates),
                "alerta": "artículo 2 usa categorías/numerales, no incisos" if n == 2 and inciso else "",
            })

    # citation audit
    cite_rows = []
    with (OUT / "unidades_benchmark.csv").open("w", encoding="utf-8", newline="") as fh:
        fields = ["unidad_id", "caso", "sub", "tipo", "pregunta", "respuesta", "refs", "refs_nums", "citas", "citas_fuera_ref", "refs_no_citadas", "citas_inexistentes", "citas_ambiguas", "alertas"]
        w = csv.DictWriter(fh, fieldnames=fields)
        w.writeheader()
        for u in units:
            cites = extract_citations(u["respuesta"])
            cited_nums = sorted({c["numero"] for c in cites})
            refs_nums = sorted(set(u["refs_nums"]))
            fuera = sorted(set(cited_nums) - set(refs_nums))
            no_citadas = sorted(set(refs_nums) - set(cited_nums))
            inexistentes = sorted(n for n in cited_nums if n not in by_num)
            ambiguas = sorted(n for n in cited_nums if n in by_num and len(by_num[n]) > 1)
            alerts = []
            if inexistentes:
                alerts.append("cita_inexistente")
            if fuera:
                alerts.append("cita_fuera_de_referencia")
            if no_citadas:
                alerts.append("referencia_no_citada")
            if ambiguas:
                alerts.append("numero_ambiguo_cuerpo/apendice")
            if any(r["numero"] == 2 and r["inciso"] for r in u["refs_detail"]):
                alerts.append("referencia_2_como_inciso")
            if u["unidad_id"] == "Q23.0":
                alerts.append("ley_especial_17.319_fuera_del_codigo")
            if u["unidad_id"] == "Q24.0":
                alerts.append("ley_24.585_sin_contexto")
            if u["unidad_id"] in {"Q1.2", "Q1.3"}:
                alerts.append("revisar_texto_referencia")
            w.writerow({
                "unidad_id": u["unidad_id"], "caso": u["caso"], "sub": u["sub"], "tipo": u["tipo"],
                "pregunta": u["pregunta"], "respuesta": u["respuesta"], "refs": " | ".join(u["refs"]),
                "refs_nums": ",".join(map(str, refs_nums)), "citas": ",".join(map(str, cited_nums)),
                "citas_fuera_ref": ",".join(map(str, fuera)), "refs_no_citadas": ",".join(map(str, no_citadas)),
                "citas_inexistentes": ",".join(map(str, inexistentes)), "citas_ambiguas": ",".join(map(str, ambiguas)),
                "alertas": " | ".join(alerts),
            })
            for c in cites:
                primary = by_key.get(("cuerpo", c["numero"])) or by_key.get(("disposiciones", c["numero"])) or by_key.get(("apendice", c["numero"]))
                cite_rows.append({
                    "unidad_id": u["unidad_id"], "numero": c["numero"], "snippet": c["snippet"],
                    "existe": "sí" if c["numero"] in by_num else "no",
                    "seccion_principal": primary["section"] if primary else "",
                    "estado_principal": primary["estado"] if primary else "",
                    "ambiguedad": "sí" if len(by_num.get(c["numero"], [])) > 1 else "no",
                })

    with (OUT / "referencias_benchmark.csv").open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(ref_rows[0].keys()))
        w.writeheader()
        w.writerows(ref_rows)
    with (OUT / "citas_respuestas.csv").open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(cite_rows[0].keys()))
        w.writeheader()
        w.writerows(cite_rows)

    # Report
    n_refs = len(ref_rows)
    n_units = len(units)
    bad_refs = [r for r in ref_rows if r["estado"] != "ok" or r["alerta"]]
    missing_units = [u for u in units if u["unidad_id"] in {"Q1.2", "Q1.3"}]
    lines = [
        "# Auditoría del corpus y del benchmark",
        "",
        "## Inspección",
        "",
        f"- Corpus: `{CORPUS.relative_to(REPO)}` — SHA-256 `{sha256(CORPUS)}`",
        f"- Benchmark: `{BENCH.relative_to(REPO)}` — SHA-256 `{sha256(BENCH)}`",
        f"- HTML de contraste: `{HTML.relative_to(REPO)}` — SHA-256 `{sha256(HTML)}`",
        f"- OCR corto: `{OCR_SHORT.relative_to(REPO)}` — SHA-256 `{sha256(OCR_SHORT)}`",
        f"- OCR largo: `{OCR_LONG.relative_to(REPO)}` — SHA-256 `{sha256(OCR_LONG)}`",
        "",
        "## Corpus",
        "",
        f"- Nodos totales: **{len(nodes)}**.",
        f"- Nodos artículo: **{len(articles)}**.",
        f"- Cuerpo: **{sum(1 for n in articles if n['section'] == 'cuerpo')}** artículos (1–347).",
        f"- Disposiciones generales y transitorias: **{sum(1 for n in articles if n['section'] == 'disposiciones')}** (348–362).",
        f"- Apéndice: **{sum(1 for n in articles if n['section'] == 'apendice')}** (1–36).",
        f"- Números únicos: **{len(by_num)}**; duplicados cuerpo/apéndice: **{sum(1 for n, v in by_num.items() if len(v) > 1)}**.",
        f"- Artículos vacíos: **{sum(1 for n in articles if not n['texto'].strip())}** (artículo 239, derogado).",
        "",
        "### Metadatos",
        "",
        "| Campo | Valor en JSON | Valor verificado | Estado |",
        "| --- | --- | --- | --- |",
    ]
    for r in metadata_rows:
        lines.append(f"| `{r['campo']}` | `{r['valor_json']}` | {r['valor_verificado']} | **{r['estado']}** |")
    lines += [
        "",
        "**Conclusión de linaje:** el corpus no es una copia literal del PDF/OCR de 1997. Contiene texto posterior a 1997 y coincide con el HTML actualizado de Infoleg en los artículos verificados. El PDF y el OCR sirven como fuente histórica parcial, pero no explican por sí solos el texto indexado. La afirmación del manuscrito de que las estrategias basadas en Infoleg “se descartaron” no describe el artefacto final.",
        "",
        "### Artículos clave: comparación de fuentes",
        "",
        "| Art. | Corpus | HTML actual | OCR 1997 corto | OCR largo | Observación |",
        "| ---: | ---: | ---: | ---: | ---: | --- |",
    ]
    for r in compare_rows:
        lines.append(f"| {r['articulo']} | {r['corpus_len']} car. | {r['html_len']} car. | {r['ocr_corto_len']} car. | {r['ocr_largo_len']} car. | {r['observacion']} |")
    lines += [
        "",
        "## Benchmark",
        "",
        f"- Casos: **{len(bench['preguntas'])}** (22 con subpreguntas y 3 de unidad única).",
        f"- Unidades: **{n_units}**.",
        f"- Referencias: **{n_refs}**; únicas por número: **{len({r['numero'] for r in ref_rows})}**.",
        f"- Referencias con alerta sustantiva: **{len(bad_refs)}**. Las referencias a números 1–36 se marcan como ambiguas por la duplicación cuerpo/apéndice, pero se resuelven al cuerpo como fuente principal.",
        "",
        "### Referencias con alerta",
        "",
        "| Unidad | Referencia | Estado | Ambigüedad | Detalle |",
        "| --- | --- | --- | --- | --- |",
    ]
    for r in bad_refs:
        lines.append(f"| {r['unidad_id']} | {r['referencia']} | {r['estado']} | {r['ambiguedad_numeracion']} | {r['alerta'] or r['candidatos']} |")
    lines += [
        "",
        "### Unidades que requieren revisión jurídica inmediata",
        "",
        "| Unidad | Referencias | Citas en la respuesta | Alertas |",
        "| --- | --- | --- | --- |",
    ]
    for u in units:
        cites = extract_citations(u["respuesta"])
        if u["unidad_id"] in {"Q1.1", "Q1.2", "Q1.3", "Q13.2", "Q13.3", "Q22.1", "Q23.0", "Q24.0", "Q25.0"}:
            refs = ", ".join(u["refs"])
            cs = ", ".join(str(c["numero"]) for c in cites)
            alerts = []
            if u["unidad_id"] == "Q1.2":
                alerts.append("El anexo Typst cita art. 8 para la separación de propiedad; la respuesta JSON y el corpus sostienen arts. 7, 10 y 11. Corregir el anexo, no la respuesta.")
            if u["unidad_id"] == "Q1.3":
                alerts.append("La respuesta parafrasea el art. 17 como 'seguridad pública, salud o conservación ambiental'; el texto dice 'seguridad pública, conservación de las pertenencias y salud o existencia de los trabajadores'. Revisar la paráfrasis y el alcance de 'solamente'.")
            if u["unidad_id"] == "Q13.2":
                alerts.append("La respuesta cita 235, 236, 237, 240, 241 y 243; la lista de referencias solo incluye 243.")
            if u["unidad_id"] == "Q13.3":
                alerts.append("La respuesta cita 264 y 265 además de 245; la lista de referencias solo incluye 245.")
            if u["unidad_id"] == "Q22.1":
                alerts.append("La unidad declara el artículo 353, pero la respuesta solo cita el 45; verificar si 353 corresponde a Q22.2.")
            if u["unidad_id"] == "Q23.0":
                alerts.append("Caso de Río Turbio con régimen especial no explicitado. La revisora no pidió eliminar Q23; el caso que propuso eliminar es el de hidrocarburos (Ley 17.319).")
            if u["unidad_id"] == "Q24.0":
                alerts.append("La pregunta usa la Ley 24.585 sin explicar su tema; la abogada sugirió aclararlo.")
            if u["unidad_id"] == "Q25.0":
                alerts.append("La respuesta cita el artículo 76, pero la lista de referencias solo incluye el 351.")
            if u["unidad_id"] == "Q1.1":
                alerts.append("La referencia 'Artículo 2, inciso 1' debe expresarse como categoría/numeral 1°: el artículo 2 divide en categorías, no en incisos.")
            lines.append(f"| {u['unidad_id']} | {refs} | {cs} | {' '.join(alerts)} |")
    lines += [
        "",
        "### Cobertura de citas",
        "",
        "Los detalles por unidad están en `unidades_benchmark.csv`; cada cita extraída está en `citas_respuestas.csv`. Las alertas automáticas son un punto de partida: no sustituyen la lectura jurídica de la respuesta.",
        "",
        "## Lectura para la corrección del manuscrito",
        "",
        "1. Corregir la fecha de sanción y la fecha de publicación en el anexo y en el JSON de metadatos usado para generar tablas; no afirmar 1994.",
        "2. Describir el corpus como **texto actualizado a partir del HTML de Infoleg**, con el PDF de 1997 como fuente histórica y el OCR como insumo parcial. No afirmar que Infoleg fue descartado sin explicar que su texto quedó incorporado.",
        "3. Unificar el conteo: 398 nodos artículo = 347 cuerpo + 15 disposiciones + 36 apéndice; 362 números únicos; 239 derogado/vacío.",
        "4. Corregir el anexo Typst de la subpregunta 1.2 (art. 8 → arts. 7, 10 y 11) y revisar la paráfrasis de 1.3.",
        "5. Llevar a revisión de la abogada los casos Q23–Q25 y las respuestas que dependen de leyes especiales; no presentarlos como evaluación pura del Código.",
        "6. Resolver las referencias 'Artículo 2, inciso 1' y otras etiquetas de inciso antes de volver a calcular métricas de citación.",
        "",
    ]
    (OUT / "auditoria_corpus_benchmark.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps({"nodes": len(nodes), "articles": len(articles), "unique_numbers": len(by_num), "units": n_units, "refs": n_refs, "bad_refs": len(bad_refs)}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
