# Agentic-RAG para Consulta de Normativa Argentina 🇦🇷

[![Typst](https://img.shields.io/badge/Typst-0.11+-239DAD?logo=typst)](https://typst.app)
[![Python](https://img.shields.io/badge/Python-3.12+-3776AB?logo=python)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![uv](https://img.shields.io/badge/uv-package%20manager-DE5FE9?logo=uv)](https://docs.astral.sh/uv/)

**Sistema de Generación Aumentada por Recuperación Agéntica (Agentic-RAG) de código abierto para la consulta de normativa legal argentina.**

Tesis de Maestría en Ciencia de Datos — Universidad Austral  
Autor: **Leonardo Ulises Spairani**  
Tutores: Dra. Laura Lucía Bélfer y Dr. Rafael Crescenzi

---

## 📖 Sobre el proyecto

Este repositorio contiene el código, los datos y el manuscrito de la tesis de maestría que desarrolla y evalúa un **prototipo de sistema inteligente para consulta de normativa nacional argentina mediante Agentic-RAG**, utilizando el **Código de Minería Argentino** como prueba de concepto.

### 🎯 ¿Qué hace el sistema?

El sistema permite realizar consultas en lenguaje natural sobre el Código de Minería Argentino y obtener respuestas fundamentadas en los artículos reales de la normativa, en lugar de depender únicamente del conocimiento interno de un modelo de lenguaje. Para lograrlo, combina tres componentes:

1. **Base de datos vectorial** (Milvus) con embeddings semánticos de cada artículo del Código de Minería, que permite búsquedas por similitud semántica.
2. **Sistema multi-agente** (Pydantic AI) con agentes especializados en interpretación de consultas, recuperación de artículos y generación de respuestas.
3. **Pipeline de evaluación** con un benchmark de 25 preguntas legales validadas por profesionales del derecho argentino, y evaluación mediante métricas textuales, semánticas y LLM-as-a-Judge.

### 🔬 Hallazgos principales

| Hallazgo                                     | Descripción                                                                             |
| -------------------------------------------- | --------------------------------------------------------------------------------------- |
| **RAG mejora significativamente la calidad** | Tanto RAG básico como Agentic-RAG superan al baseline sin recuperación (p < 0.001)      |
| **Efecto igualador del RAG**                 | Con RAG básico, modelos pequeños alcanzan desempeño comparable al de modelos superiores |
| **Interacción estrategia × modelo**          | La efectividad de cada estrategia depende del modelo con el que se combine (p < 10⁻¹¹)  |
| **Sobrecarga agéntica en modelos pequeños**  | Agentic-RAG puede degradar el desempeño de modelos de capacidad reducida                |
| **LLM-as-a-Judge validado**                  | Acuerdo inter-juez bueno (α = 0.81) para evaluación de correctitud en dominio legal     |

### 🌍 ¿Por qué es relevante?

- **Acceso a la justicia**: Facilita la consulta de normativa para ciudadanos y profesionales no especializados.
- **Código abierto**: Cualquier organización, institución pública o desarrollador puede replicar y adaptar el sistema a otras normativas o jurisdicciones.
- **Metodología replicable**: La documentación detallada permite extender el sistema a otros dominios (medicina, ingeniería, finanzas).
- **Primer sistema de este tipo**: Hasta donde se tiene conocimiento, es el primer sistema Agentic-RAG de código abierto aplicado a normativa argentina.

---

## 📁 Estructura del repositorio

```
.
├── manuscrito/                     # Manuscrito de la tesis (Typst)
│   ├── main.typ                    # Documento raíz
│   ├── referencias.bib             # Bibliografía (BibTeX)
│   ├── capitulos/                  # Capítulos (Introducción, Marco Teórico, Metodología, etc.)
│   ├── media/                      # Imágenes, diagramas y figuras
│   ├── codigo-helpers/             # Scripts Python auxiliares (generación de figuras)
│   └── salidas/                    # PDFs compilados
│
├── codigo_experimentos/            # Código de experimentos (Python)
│   ├── part_a/                     # Generación del benchmark de preguntas
│   ├── part_b/                     # Estructuración de datos normativos
│   ├── part_c/                     # Creación de la base de datos vectorial (Milvus)
│   ├── part_d/                     # Evaluación de recuperación sin LLM
│   ├── part_e/                     # Baseline sin RAG
│   ├── part_f/                     # RAG básico
│   ├── part_g/                     # Agentic-RAG (sistema multi-agente)
│   ├── part_h/                     # Integración de datos
│   ├── part_h1/                    # Evaluación LLM-as-a-Judge
│   ├── part_i/                     # Comparación de métricas
│   ├── part_j/                     # Análisis estadístico
│   ├── part_k/                     # Análisis de costos y tokens
│   └── data/                       # Datos del Código de Minería (JSON, Python)
│
├── data/                           # Datos compartidos (benchmark, preguntas)
├── Makefile                        # Compilación del manuscrito
└── AGENTS.md                       # Instrucciones para agentes de IA
```

---

## 🚀 Primeros pasos

### Requisitos

- [Typst CLI](https://typst.app) ≥ 0.11 — para compilar el manuscrito
- [uv](https://docs.astral.sh/uv/) — gestor de paquetes Python
- [direnv](https://direnv.net/) — carga automática de variables de entorno
- [Milvus](https://milvus.io/) — base de datos vectorial (para experimentos)
- Acceso a APIs de LLM (OpenAI, etc.) — para ejecutar los experimentos

### Instalación de Typst

```bash
# macOS
brew install typst

# Linux
cargo install typst-cli

# Windows
winget install typst
```

### Compilar el manuscrito

```bash
# Compilar una vez → genera manuscrito/salidas/<timestamp>_main.pdf
make pdf
```

### Ejecutar experimentos

```bash
cd codigo_experimentos
direnv allow          # Solo la primera vez
uv sync               # Instalar dependencias

# Ejecutar notebooks en orden: part_a → part_b → part_c → ... → part_k
# Cada directorio contiene notebooks de Jupyter documentados
```

> **Nota**: Los experimentos requieren credenciales para APIs de LLM, gestionadas mediante Bitwarden (ver `codigo_experimentos/.envrc`).

---

## 📊 Diseño experimental

El sistema fue evaluado mediante un **diseño factorial 3 × 3**:

| Factor                         | Niveles                            |
| ------------------------------ | ---------------------------------- |
| **Estrategia de recuperación** | Sin RAG · RAG básico · Agentic-RAG |
| **Modelo de lenguaje**         | gpt-5-nano · gpt-5-mini · gpt-5    |

**Métricas de evaluación**:
- **Textuales**: BLEU, ROUGE-1, ROUGE-L, METEOR, exactitud de tokens
- **Semánticas**: BERTScore (precisión, recall, F1)
- **LLM-as-a-Judge**: Correctitud de respuesta y precisión legal (3 jueces: DeepSeek, Grok, Kimi K2)

**Análisis estadístico**: Kruskal-Wallis, Dunn con corrección Bonferroni, Scheirer-Ray-Hare (interacción), Krippendorff's alpha (acuerdo inter-juez).

---

## 📝 Citar este trabajo

Si utilizas este código, datos o metodología en tu investigación, por favor cita:

```bibtex
@mastersthesis{spairani2025agenticrag,
  author  = {Spairani, Leonardo Ulises},
  title   = {Desarrollo y evaluación de un prototipo de sistema inteligente
             para consulta de normativa nacional argentina mediante
             recuperación agéntica},
  school  = {Universidad Austral},
  year    = {2026},
  type    = {Tesis de Maestría en Ciencia de Datos}
}
```

---

## 📄 Licencia

Este proyecto se distribuye bajo la licencia MIT. Consulta el archivo [LICENSE](LICENSE) para más detalles.

---

## 🙏 Agradecimientos

A la Dra. Laura Lucía Bélfer y al Dr. Rafael Crescenzi por su dirección y apoyo durante el desarrollo de este trabajo. A los profesionales del derecho argentino que colaboraron en la validación del benchmark. A la Universidad Austral por proporcionar el marco académico para esta investigación.
