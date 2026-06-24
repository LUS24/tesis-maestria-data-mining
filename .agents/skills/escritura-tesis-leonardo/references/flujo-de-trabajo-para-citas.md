# Gestión de Citas y Prevención de Alucinaciones

Esta referencia proporciona un flujo de trabajo completo para gestionar citas de forma programática, prevenir alucinaciones de citas generadas por IA y mantener bibliografías limpias.

---

## Contenido

- [Por qué es importante la verificación de citas](#por-qu%C3%A9-es-importante-la-verificaci%C3%B3n-de-citas)
- [Resumen de APIs de citas](#resumen-de-apis-de-citas)
- [Flujo de trabajo de citas verificadas](#flujo-de-trabajo-de-citas-verificadas)
- [Implementación en Python](#implementaci%C3%B3n-en-python)
- [Formatos de cita comunes](#formatos-de-cita-comunes)
- [Solución de problemas](#soluci%C3%B3n-de-problemas)

---

## Por qué es importante la verificación de citas

### El problema de las alucinaciones

La investigación ha documentado problemas significativos con las citas generadas por IA:
- **~40% de tasa de error** en citas generadas por IA (investigación de Enago Academy)
- NeurIPS 2025 encontró **más de 100 citas alucinadas** que pasaron la revisión
- Los errores comunes incluyen:
  - Títulos de artículos inventados con nombres reales de autores
  - Eventos o años de publicación incorrectos
  - Artículos inexistentes con metadatos plausibles
  - DOIs o arXiv IDs incorrectos

### Consecuencias

- Rechazo directo en algunas conferencias
- Pérdida de credibilidad con los revisores
- Posible retractación si se publica
- Pérdida de tiempo buscando fuentes inexistentes

### Solución

**Nunca generes citas de memoria—verifica siempre programáticamente.**

---

## Resumen de APIs de citas

### APIs principales

| API                  | Cobertura   | Límites de tasa          | Mejor para                       |
| -------------------- | ----------- | ------------------------ | -------------------------------- |
| **Semantic Scholar** | 214M art.  | 1 RPS (clave gratuita)   | Artículos ML/IA, grafos de citas |
| **CrossRef**         | 140M+ DOIs  | Grupo cortés con mailto  | Búsqueda DOIs, recuperar BibTeX  |
| **arXiv**            | Preprints   | 3 segundos de espera     | Preprints ML, acceso a PDF       |

### Guía de selección de API

```
¿Necesitas buscar artículos de ML? → Semantic Scholar
¿Tienes DOI, necesitas BibTeX? → Negociación de contenido de CrossRef
¿Buscas un preprint? → arXiv API
```
---

## Flujo de trabajo de citas verificadas

### Proceso de 6 pasos

```
1. BUSCAR → Consultar Semantic Scholar con palabras clave específicas
       ↓
2. VERIFICAR → Confirmar que el artículo existe en 2+ fuentes
       ↓
3. RECUPERAR → Obtener BibTeX mediante negociación de contenido con DOI
       ↓
4. VALIDAR → Confirmar que la afirmación aparece en la fuente
       ↓
5. AGREGAR → Añadir entrada verificada al archivo .bib
       ↓
6. DESCARGAR (OPCIONAL) → Si está disponible, descargar el archivo pdf y colocarlo en el directorio `bibliography` en el subdirectorio correspondiente al capítulo donde se referencia.
```

### Paso 1: Buscar

Antes de buscar, verifica que el artículo no esté ya en la bibliografía ni su PDF descargado, para evitar duplicados.

> **⚠️ Límite de tasa**: Todas las llamadas a APIs externas deben limitarse a **≥1.05 segundos** entre solicitudes. Inserta `time.sleep(1.05)` antes de cada llamada al hacer lotes.

```python
import os
import re

def paper_ya_en_bibliografia(titulo: str, año: int, autores: list,
                              bib_path: str) -> bool:
    """Verificar si el artículo ya existe en el archivo .bib por título o DOI."""
    if not os.path.exists(bib_path):
        return False

    with open(bib_path, 'r', encoding='utf-8') as f:
        contenido = f.read()

    # Buscar título en el contenido (case-insensitive, fragmento)
    if titulo:
        # Tomar los primeros 40 caracteres del título para la comparación
        fragmento = re.escape(titulo[:40].strip())
        if re.search(fragmento, contenido, re.IGNORECASE):
            return True

    return False


def pdf_ya_descargado(titulo: str, año: int, autores: list,
                      download_dir: str) -> bool:
    """Verificar si el PDF ya fue descargado en el directorio."""
    if not os.path.exists(download_dir):
        return False

    # Generar el nombre de archivo esperado
    first_author = autores[0].split()[-1] if autores else "unknown"
    first_word = titulo.split()[0].lower().replace(',', '').replace(':', '')
    filename = f"{first_author.lower()}_{año}_{first_word}.pdf"
    filepath = os.path.join(download_dir, filename)

    return os.path.exists(filepath)


# --- Ejemplo de uso integrado con la búsqueda ---
from semanticscholar import SemanticScholar

BIB_PATH = "referencias.bib"
DOWNLOAD_DIR = "bibliography/05_capitulo_04_marco_teorico_agentic_rag"

sch = SemanticScholar()
results = sch.search_paper("transformer attention mechanism", limit=10)

for paper in results:
    titulo = paper.title
    año = paper.year or 0
    autores = [a.name for a in (paper.authors or [])]

    # Saltar si ya está en la bibliografía
    if paper_ya_en_bibliografia(titulo, año, autores, BIB_PATH):
        print(f"  [SKIP] Ya en bibliografía: {titulo}")
        continue

    # Saltar si el PDF ya fue descargado
    if pdf_ya_descargado(titulo, año, autores, DOWNLOAD_DIR):
        print(f"  [SKIP] PDF ya descargado: {titulo}")
        continue

    print(f"Title: {titulo}")
    print(f"Year: {año}")
    print(f"DOI: {paper.externalIds.get('DOI', 'N/A')}")
    print(f"arXiv: {paper.externalIds.get('ArXiv', 'N/A')}")
    print(f"Citation count: {paper.citationCount}")
    print("---")
```

### Paso 2: Verificar existencia

Confirma que el artículo existe en al menos dos fuentes:

> **⚠️ Límite de tasa**: Cada `requests.get()` y `sch.get_paper()` es una llamada a API externa. Inserta `time.sleep(1.05)` entre llamadas consecutivas para respetar los límites de tasa.

```python
import requests

def verify_paper(doi=None, arxiv_id=None, title=None):
    """Verificar que el artículo existe en múltiples fuentes."""
    sources_found = []

    # Verificar Semantic Scholar
    sch = SemanticScholar()
    if doi:
        paper = sch.get_paper(f"DOI:{doi}")
        if paper:
            sources_found.append("Semantic Scholar")

    # Verificar CrossRef (vía DOI)
    if doi:
        resp = requests.get(f"https://api.crossref.org/works/{doi}")
        if resp.status_code == 200:
            sources_found.append("CrossRef")

    # Verificar arXiv
    if arxiv_id:
        resp = requests.get(
            f"http://export.arxiv.org/api/query?id_list={arxiv_id}"
        )
        if "<entry>" in resp.text:
            sources_found.append("arXiv")

    return len(sources_found) >= 2, sources_found
```

### Paso 3: Recuperar BibTeX

Usa la negociación de contenido con DOI para precisión garantizada:

> **⚠️ Límite de tasa**: `requests.get()` a `doi.org` cuenta como una llamada a API externa. Asegura un intervalo ≥1.05s desde la última solicitud.

```python
import requests

def doi_to_bibtex(doi: str) -> str:
    """Obtener BibTeX verificado desde DOI mediante negociación de contenido de CrossRef."""
    response = requests.get(
        f"https://doi.org/{doi}",
        headers={"Accept": "application/x-bibtex"},
        allow_redirects=True
    )
    response.raise_for_status()
    return response.text

# Ejemplo: "Attention Is All You Need"
bibtex = doi_to_bibtex("10.48550/arXiv.1706.03762")
print(bibtex)
```

### Paso 4: Validar afirmaciones

Antes de citar un artículo para una afirmación específica, verifica que la afirmación exista:

> **⚠️ Límite de tasa**: `sch.get_paper()` consulta la API de Semantic Scholar. Mantén ≥1.05s entre llamadas consecutivas a la API.

```python
def get_paper_abstract(doi):
    """Obtener resumen para verificar afirmaciones."""
    sch = SemanticScholar()
    paper = sch.get_paper(f"DOI:{doi}")
    return paper.abstract if paper else None

# Verificar que la afirmación aparece en el resumen
abstract = get_paper_abstract("10.48550/arXiv.1706.03762")
claim = "attention mechanism"
if claim.lower() in abstract.lower():
    print("La afirmación aparece en el artículo")
```

### Paso 5: Agregar a la bibliografía

Añade la entrada verificada a tu archivo .bib con un formato de clave consistente:

```python
def generate_citation_key(bibtex: str) -> str:
    """Generar clave de cita consistente: autor_año_primerapalabra."""
    import re

    # Extraer autor
    author_match = re.search(r'author\s*=\s*\{([^}]+)\}', bibtex, re.I)
    if author_match:
        first_author = author_match.group(1).split(',')[0].split()[-1]
    else:
        first_author = "unknown"

    # Extraer año
    year_match = re.search(r'year\s*=\s*\{?(\d{4})\}?', bibtex, re.I)
    year = year_match.group(1) if year_match else "0000"

    # Extraer primera palabra del título
    title_match = re.search(r'title\s*=\s*\{([^}]+)\}', bibtex, re.I)
    if title_match:
        first_word = title_match.group(1).split()[0].lower()
        first_word = re.sub(r'[^a-z]', '', first_word)
    else:
        first_word = "paper"

    return f"{first_author.lower()}_{year}_{first_word}"
```

### Paso 6: Descargar PDF (opcional)

Si el artículo tiene acceso abierto, Semantic Scholar proporciona una URL de descarga del PDF en el campo `openAccessPdf`. Verifica este campo después de buscar y descarga el PDF en el subdirectorio correspondiente dentro de `bibliography/`.

> **⚠️ Límite de tasa**: `requests.get()` para descargar el PDF cuenta como una llamada a API externa. Mantén ≥1.05s entre solicitudes.

```python
import requests
import os

def download_pdf(paper, download_dir: str) -> Optional[str]:
    """Descargar PDF si está disponible en openAccessPdf."""
    if not paper.download_url:
        print(f"No hay PDF disponible para: {paper.title}")
        return None

    # Crear directorio si no existe
    os.makedirs(download_dir, exist_ok=True)

    # Generar nombre de archivo: autor_año_primerapalabra.pdf
    first_author = paper.authors[0].split()[-1] if paper.authors else "unknown"
    first_word = paper.title.split()[0].lower().replace(',', '').replace(':', '')
    filename = f"{first_author.lower()}_{paper.year}_{first_word}.pdf"
    filepath = os.path.join(download_dir, filename)

    # Descargar
    print(f"Descargando PDF: {paper.title}")
    resp = requests.get(paper.download_url, timeout=30)
    resp.raise_for_status()

    with open(filepath, 'wb') as f:
        f.write(resp.content)

    print(f"PDF guardado en: {filepath}")
    return filepath

# Ejemplo de uso
chapter_dir = "bibliography/05_capitulo_04_marco_teorico_agentic_rag"
# paper.download_url se obtiene del campo openAccessPdf.url de Semantic Scholar
download_pdf(paper, chapter_dir)
```

La estructura de directorios esperada es:

```
bibliography/
├── 01_texto_preliminar/
├── 02_capitulo_01_introduccion/
├── 03_capitulo_02_fundamentos_e_historia_pln/
├── 04_capitulo_03_aplicacion_de_pln_a_dominio_legal/
├── 05_capitulo_04_marco_teorico_agentic_rag/
├── 06_capitulo_05_metodologia/
├── 07_capitulo_06_implementacion/
├── 08_capitulo_07_evaluacion/
├── trabajos_relacionados/
└── conclusion_y_trabajos_futuros/
```

---

## Implementación en Python

### Clase completa CitationManager

> **⚠️ Límite de tasa**: Todos los métodos de esta clase que hacen solicitudes HTTP o consultan APIs externas deben respetar un intervalo mínimo de **1.05 segundos** entre llamadas consecutivas. Al llamar a `cite()` en un bucle (ej. en `batch_cite`), inserta `time.sleep(1.05)` entre iteraciones.

{% raw %}
```python
"""
Gestor de Citas - Flujo de trabajo de citas verificadas para artículos ML.
"""

import requests
import time
from typing import Optional, List, Dict, Tuple
from dataclasses import dataclass

try:
    from semanticscholar import SemanticScholar
except ImportError:
    print("Instalar: pip install semanticscholar")
    SemanticScholar = None

@dataclass
class Paper:
    title: str
    authors: List[str]
    year: int
    doi: Optional[str]
    arxiv_id: Optional[str]
    venue: Optional[str]
    citation_count: int
    abstract: Optional[str]
    download_url: Optional[str] = None

class CitationManager:
    """Gestionar citas con verificación."""

    def __init__(self, api_key: Optional[str] = None):
        self.sch = SemanticScholar(api_key=api_key) if SemanticScholar else None
        self.verified_papers: Dict[str, Paper] = {}

    def search(self, query: str, limit: int = 10) -> List[Paper]:
        """Buscar artículos usando Semantic Scholar."""
        if not self.sch:
            raise RuntimeError("Semantic Scholar no disponible")

        results = self.sch.search_paper(query, limit=limit)
        papers = []

        for r in results:
            # Extraer URL de openAccessPdf si está disponible
            download_url = None
            if hasattr(r, 'open_access_pdf') and r.open_access_pdf:
                download_url = r.open_access_pdf.get('url')

            paper = Paper(
                title=r.title,
                authors=[a.name for a in (r.authors or [])],
                year=r.year or 0,
                doi=r.externalIds.get('DOI') if r.externalIds else None,
                arxiv_id=r.externalIds.get('ArXiv') if r.externalIds else None,
                venue=r.venue,
                citation_count=r.citationCount or 0,
                abstract=r.abstract,
                download_url=download_url
            )
            papers.append(paper)

        return papers

    def verify(self, paper: Paper) -> Tuple[bool, List[str]]:
        """Verificar que el artículo existe en múltiples fuentes."""
        sources = []

        # Ya encontrado en Semantic Scholar mediante búsqueda
        sources.append("Semantic Scholar")

        # Verificar CrossRef si el DOI está disponible
        if paper.doi:
            try:
                resp = requests.get(
                    f"https://api.crossref.org/works/{paper.doi}",
                    timeout=10
                )
                if resp.status_code == 200:
                    sources.append("CrossRef")
            except Exception:
                pass

        # Verificar arXiv si el ID está disponible
        if paper.arxiv_id:
            try:
                resp = requests.get(
                    f"http://export.arxiv.org/api/query?id_list={paper.arxiv_id}",
                    timeout=10
                )
                if "<entry>" in resp.text and "<title>" in resp.text:
                    sources.append("arXiv")
            except Exception:
                pass

        return len(sources) >= 2, sources

    def get_bibtex(self, paper: Paper) -> Optional[str]:
        """Obtener BibTeX para un artículo verificado."""
        if paper.doi:
            try:
                resp = requests.get(
                    f"https://doi.org/{paper.doi}",
                    headers={"Accept": "application/x-bibtex"},
                    timeout=10,
                    allow_redirects=True
                )
                if resp.status_code == 200:
                    return resp.text
            except Exception:
                pass

        # Alternativa: generar a partir de los datos del artículo
        return self._generate_bibtex(paper)

    def _generate_bibtex(self, paper: Paper) -> str:
        """Generar BibTeX a partir de metadatos del artículo."""
        # Generar clave de cita
        first_author = paper.authors[0].split()[-1] if paper.authors else "unknown"
        first_word = paper.title.split()[0].lower().replace(',', '').replace(':', '')
        key = f"{first_author.lower()}_{paper.year}_{first_word}"

        # Formatear autores
        authors = " and ".join(paper.authors) if paper.authors else "Unknown"

        bibtex = f"""@article{{{key},
  title = {{{paper.title}}},
  author = {{{authors}}},
  year = {{{paper.year}}},
  {'doi = {' + paper.doi + '},' if paper.doi else ''}
  {'eprint = {' + paper.arxiv_id + '},' if paper.arxiv_id else ''}
  {'journal = {' + paper.venue + '},' if paper.venue else ''}
}}"""
        return bibtex

    def download_pdf(self, paper: Paper, download_dir: str) -> Optional[str]:
        """Descargar PDF del artículo si está disponible."""
        if not paper.download_url:
            print(f"No hay PDF disponible para: {paper.title}")
            return None

        os.makedirs(download_dir, exist_ok=True)

        # Generar nombre de archivo: autor_año_primerapalabra.pdf
        first_author = paper.authors[0].split()[-1] if paper.authors else "unknown"
        first_word = paper.title.split()[0].lower().replace(',', '').replace(':', '')
        filename = f"{first_author.lower()}_{paper.year}_{first_word}.pdf"
        filepath = os.path.join(download_dir, filename)

        print(f"Descargando PDF: {paper.title}")
        resp = requests.get(paper.download_url, timeout=30)
        resp.raise_for_status()

        with open(filepath, 'wb') as f:
            f.write(resp.content)

        print(f"PDF guardado en: {filepath}")
        return filepath

    def cite(self, query: str, download_dir: Optional[str] = None) -> Optional[str]:
        """Flujo de trabajo completo: buscar, verificar, devolver BibTeX.

        Args:
            query: Términos de búsqueda.
            download_dir: Si se proporciona, descarga el PDF en este directorio.
        """
        # Buscar
        papers = self.search(query, limit=5)
        if not papers:
            return None

        # Tomar el mejor resultado
        paper = papers[0]

        # Verificar
        verified, sources = self.verify(paper)
        if not verified:
            print(f"Advertencia: Solo se pudo verificar en {sources}")

        # Obtener BibTeX
        bibtex = self.get_bibtex(paper)

        # Descargar PDF si se especificó directorio
        if download_dir and paper.download_url:
            time.sleep(1.05)  # Límite de tasa
            self.download_pdf(paper, download_dir)

        # Almacenar en caché
        if bibtex:
            self.verified_papers[paper.title] = paper

        return bibtex


# Ejemplo de uso
if __name__ == "__main__":
    cm = CitationManager()

    # Buscar y citar
    bibtex = cm.cite("attention is all you need transformer")
    if bibtex:
        print(bibtex)
```
{% endraw %}

### Funciones rápidas

```python
def quick_cite(query: str) -> str:
    """Cita en una línea."""
    cm = CitationManager()
    return cm.cite(query)

def batch_cite(queries: List[str], output_file: str = "references.bib",
               download_dir: Optional[str] = None):
    """Citar múltiples artículos y guardar en archivo."""
    cm = CitationManager()
    bibtex_entries = []

    for query in queries:
        print(f"Procesando: {query}")
        bibtex = cm.cite(query, download_dir=download_dir)
        if bibtex:
            bibtex_entries.append(bibtex)
        time.sleep(1.05)  # Límite de tasa: ≥1.05s entre llamadas API

    with open(output_file, 'w') as f:
        f.write("\n\n".join(bibtex_entries))

    print(f"Guardadas {len(bibtex_entries)} citas en {output_file}")
```

---

## Sintaxis de citas en Typst

Typst usa un sistema de citas simple y elegante. Puedes citar trabajos usando la sintaxis de referencia (`@clave`) o llamadas a funciones explícitas (`#cite`).

### Citas básicas

```typst
// Sintaxis de referencia (en línea) — la más común
Esto ya fue notado por piratas hace mucho tiempo. @arrgh

// Citas múltiples
Múltiples fuentes dicen ... @arrgh @netwok.

// Función de cita explícita
#cite(<vaswani_2017_attention>)
```

### Formas de cita

Typst soporta diferentes formas de cita mediante el parámetro `form`:

```typst
// Normal (predeterminada) — cita estándar para el estilo activo
#cite(<vaswani_2017_attention>, form: "normal")

// Prosa — adecuada para inclusión en una oración
#cite(<vaswani_2017_attention>, form: "prose")

// Completa — imita una entrada bibliográfica con información completa
#cite(<vaswani_2017_attention>, form: "full")

// Solo autor
#cite(<vaswani_2017_attention>, form: "author")

// Solo año
#cite(<vaswani_2017_attention>, form: "year")

// Oculta — incluye en la bibliografía pero no muestra nada
#cite(<vaswani_2017_attention>, form: none)
```

### Suplementos (números de página, etc.)

Agrega suplementos como números de página o capítulo entre corchetes:

```typst
// Con sintaxis de referencia
@vaswani_2017_attention[p. 12]

// Con función de cita explícita
#cite(<vaswani_2017_attention>, supplement: [p. 12])
```

### Agregar la bibliografía

Coloca la bibliografía al final de tu documento:

```typst
// Básico — usa el estilo predeterminado (IEEE)
#bibliography("referencias.bib")

// Con estilo personalizado
#bibliography("referencias.bib", style: "apa")

// Con título personalizado
#bibliography("referencias.bib", title: [Referencias])

// Múltiples archivos de bibliografía
#bibliography(("refs.bib", "additional.bib"))

// Formato Hayagriva YAML (nativo de Typst)
#bibliography("references.yaml")
```

### Estilos bibliográficos

Typst ofrece muchos estilos integrados basados en CSL:

| Disciplina                | Estilo recomendado           |
| ------------------------- | ---------------------------- |
| Ingeniería, TI            | `"ieee"`                     |
| Psicología, Ciencias naturales | `"apa"`                 |
| Ciencias sociales         | `"chicago-author-date"`      |
| Humanidades               | `"mla"`, `"chicago-notes"`   |
| Economía                  | `"harvard-cite-them-right"`  |
| Física                    | `"american-physics-society"` |

También puedes usar archivos CSL (Citation Style Language) personalizados:

```typst
#bibliography("refs.bib", style: "mi-estilo.csl")
```

### Sobrescritura de estilo por cita

Sobrescribe el estilo de la bibliografía para citas individuales:

```typst
#cite(<vaswani_2017_attention>, style: "apa")
```

### Bibliografías múltiples

Typst soporta múltiples bibliografías en un solo documento, útil para listas de referencias por capítulo o temáticas:

```typst
// Primera bibliografía (capítulo 1)
#bibliography("capitulo1.bib")

// Segunda bibliografía (capítulo 2)
#bibliography("capitulo2.bib")
```

Las citas se asignan automáticamente a la bibliografía siguiente más cercana que contenga su clave.

### Ejemplo completo

```typst
= Introducción

La arquitectura transformer @vaswani_2017_attention
revolucionó el PLN. Como mostraron @devlin_2019_bert[p. 3],
el preentrenamiento mejora el rendimiento downstream.

Más recientemente, los modelos de lenguaje grandes han demostrado
notables capacidades de few-shot @brown_2020_language.

#bibliography("referencias.bib", style: "ieee")
```

### Claves de cita consistentes

Usa el formato: `autor_año_primerapalabra`

```
vaswani_2017_attention
devlin_2019_bert
brown_2020_language
```

---

## Formatos de cita comunes

### Artículo de conferencia

```bibtex
@inproceedings{vaswani_2017_attention,
  title = {Attention Is All You Need},
  author = {Vaswani, Ashish and Shazeer, Noam and Parmar, Niki and
            Uszkoreit, Jakob and Jones, Llion and Gomez, Aidan N and
            Kaiser, Lukasz and Polosukhin, Illia},
  booktitle = {Advances in Neural Information Processing Systems},
  volume = {30},
  year = {2017},
  publisher = {Curran Associates, Inc.}
}
```

### Artículo de revista

```bibtex
@article{hochreiter_1997_long,
  title = {Long Short-Term Memory},
  author = {Hochreiter, Sepp and Schmidhuber, J{\"u}rgen},
  journal = {Neural Computation},
  volume = {9},
  number = {8},
  pages = {1735--1780},
  year = {1997},
  publisher = {MIT Press}
}
```

### Preprint de arXiv

```bibtex
@misc{brown_2020_language,
  title = {Language Models are Few-Shot Learners},
  author = {Brown, Tom and Mann, Benjamin and Ryder, Nick and others},
  year = {2020},
  eprint = {2005.14165},
  archiveprefix = {arXiv},
  primaryclass = {cs.CL}
}
```

---

## Solución de problemas

### Problemas comunes

**Problema: Semantic Scholar no devuelve resultados**
- Prueba con palabras clave más específicas
- Verifica la ortografía de los nombres de autores
- Usa comillas para frases exactas

**Problema: El DOI no se resuelve a BibTeX**
- El DOI puede estar registrado pero no enlazado a CrossRef
- Prueba con el arXiv ID si está disponible
- Genera BibTeX manualmente a partir de metadatos

**Problema: Errores de límite de tasa**
- Agrega demoras entre solicitudes (≥1.05 segundos como mínimo)
- Usa una clave API si está disponible para aumentar los límites de tasa
- Almacena resultados en caché para evitar consultas repetidas

**Problema: Problemas de codificación en BibTeX**
- Asegúrate de que el archivo esté codificado en UTF-8

### Lista de verificación

Antes de agregar una cita:

- [ ] Artículo encontrado en al menos 2 fuentes
- [ ] DOI o arXiv ID verificado (excepto en citas a blogs)
- [ ] BibTeX recuperado (no generado de memoria)
- [ ] Tipo de entrada correcto (@inproceedings vs @article)
- [ ] Nombres de autores completos y formateados correctamente
- [ ] Año y evento/revista verificados
- [ ] Clave de cita sigue el formato consistente

---

## Recursos adicionales

**APIs:**
- Semantic Scholar: https://api.semanticscholar.org/api-docs/
- CrossRef: https://www.crossref.org/documentation/retrieve-metadata/rest-api/
- arXiv: https://info.arxiv.org/help/api/basics.html
- OpenAlex: https://docs.openalex.org/ (requiere clave API)

**Librerías de Python:**
- `semanticscholar`: https://pypi.org/project/semanticscholar/
- `arxiv`: https://pypi.org/project/arxiv/
- `habanero` (CrossRef): https://github.com/sckott/habanero

**Herramientas de verificación:**
- Citely: https://citely.ai/citation-checker (requiere clave API)
- ReciteWorks: https://reciteworks.com/ (requiere clave API)
