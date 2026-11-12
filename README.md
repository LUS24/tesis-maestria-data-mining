# Agentic-RAG para consulta del Código de Minería argentino 🇦🇷

[![Typst](https://img.shields.io/badge/Typst-0.14+-239DAD?logo=typst)](https://typst.app)
[![Python](https://img.shields.io/badge/Python-3.13+-3776AB?logo=python)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![uv](https://img.shields.io/badge/uv-package%20manager-DE5FE9?logo=uv)](https://docs.astral.sh/uv/)

**Sistema de Generación Aumentada por Recuperación Agéntica (Agentic-RAG) de código abierto para la consulta de normativa legal argentina.**

Tesis de Maestría en Ciencia de Datos — Universidad Austral  
Autor: **Leonardo Ulises Spairani**  
Tutores: Dra. Laura Lucía Bélfer y Dr. Rafael Crescenzi

---

## 📖 Sobre el proyecto

Este repositorio contiene el código, los datos y el manuscrito de la tesis de maestría que desarrolla y evalúa un **prototipo Agentic-RAG para consulta del Código de Minería argentino**.

### 🎯 ¿Qué hace el sistema?

El sistema permite realizar consultas en lenguaje natural sobre el Código de Minería Argentino y obtener respuestas fundamentadas en los artículos reales de la normativa, en lugar de depender únicamente del conocimiento interno de un modelo de lenguaje. Para lograrlo, combina tres componentes:

1. **Base de datos vectorial** (Milvus) con embeddings semánticos de cada artículo del Código de Minería, que permite búsquedas por similitud semántica.
2. **Sistema de dos agentes activos** (Pydantic AI): el Agente Especialista Legal, que interpreta la consulta y redacta la respuesta, y el Agente de Recuperación, que descompone la consulta y busca artículos. El Agente de Calidad fue diseñado pero no se ejecutó; el especialista no itera sobre los resultados ni verifica la respuesta con un agente adicional.
3. **Pipeline de evaluación** con un benchmark de 25 casos y 79 unidades, revisado por una profesional del derecho argentino, y evaluación mediante métricas textuales, semánticas y LLM-as-a-Judge.

### 🔬 Hallazgos principales

| Hallazgo | Descripción |
| --- | --- |
| **Interacción estrategia × modelo** | El efecto de la estrategia depende del modelo del Agente Especialista Legal (LR = 293,28; gl = 4; p = 3,05 × 10⁻⁶²). La interacción es robusta a los escenarios de fallo y a los tres jueces, pero no identifica un componente causal único. |
| **Efecto condicionado al modelo** | En el escenario principal (fallo = 0), Agentic-RAG es inferior a RAG básico en gpt-5-nano (−0,270; IC 95% −0,330 a −0,202), superior en gpt-5-mini (+0,150; IC 95% 0,096 a 0,203) y superior en gpt-5 (+0,106; IC 95% 0,054 a 0,155). |
| **Modo de fallo en Agentic-RAG + gpt-5-nano** | 41/79 salidas no sustantivas (27 vacías, 1 solo espacios, 2 abstenciones, 1 truncada y 10 indeterminadas). Cuando responde, la calidad es alta (38/79; media 0,820; mediana 0,958). No se atribuye a la “complejidad agéntica” sin réplicas ni ablaciones. |
| **RAG básico no iguala a los modelos** | Las diferencias observadas son menores, pero no desaparecen: mini−nano +0,063 (IC 95% 0,005–0,120), gpt-5−nano +0,128 (IC 95% 0,071–0,186), gpt-5−mini +0,065 (IC 95% 0,011–0,124). No se demostró equivalencia. |
| **Jueces: acuerdo, no validación** | α ordinal global de 0,807842 con valores originales (0,799542 tras transformar valores fuera de rúbrica), verificado de forma independiente. Mide confiabilidad entre jueces, no validez frente a criterio humano. No hay calificaciones humanas de las respuestas; se identificaron 23 discrepancias y 17 evaluaciones positivas sobre salidas no sustantivas. |
| **Costos: no hay ganador único** | “Respuesta correcta” se define como puntaje promedio ≥ 0,75 (D-02). RAG básico + gpt-5-nano presenta el menor costo puntual por respuesta correcta (USD 0,0061; IC bootstrap 0,0043–0,0091; 33/79), con IC solapado con Sin RAG + nano. Agentic-RAG + gpt-5 maximiza la media (0,812; USD 0,0792). Agentic-RAG + gpt-5-mini (0,788; USD 0,0564) es una alternativa no dominada, no la más barata. |
| **Alcance** | Un corpus (Código de Minería), 25 casos, 79 unidades, una ejecución por celda y un recuperador fijo en gpt-5. Los resultados son evidencia de viabilidad, no una validación externa ni una recomendación universal. |

### 🌍 ¿Por qué es relevante?

- **Acceso a la justicia**: explora una alternativa abierta para consultar normativa; no se evaluó su impacto ni su uso por ciudadanos o profesionales.
- **Código abierto**: el repositorio es público y accesible sin login; el código, el benchmark y los logs permiten auditar y adaptar el prototipo a otras normativas, sujeto a validación externa.
- **Metodología auditable**: el diseño apareado, el análisis de fallos y el costo por respuesta correcta (≥ 0,75) pueden reutilizarse en otras evaluaciones; no se demostró transferencia a otros dominios.
- **Antecedentes**: no se identificaron sistemas públicos comparables para normativa argentina en la búsqueda realizada; no se afirma una primacía absoluta.

---

## 📁 Estructura del repositorio

```
.
├── manuscrito/                     # Manuscrito de la tesis (Typst)
│   ├── main.typ                    # Documento raíz
│   ├── referencias.bib             # Bibliografía (BibTeX)
│   ├── capitulos/                  # Capítulos y anexos
│   ├── media/                      # Imágenes, diagramas y figuras
│   ├── codigo-helpers/             # Scripts Python auxiliares
│   └── salidas/                    # Salidas históricas de compilación
│
├── codigo_experimentos/            # Código de experimentos (Python)
│   ├── part_0/                     # Pruebas iniciales de extracción y pydantic-ai
│   ├── part_a/                     # Generación del benchmark de preguntas
│   ├── part_b/                     # Estructuración de datos normativos
│   ├── part_c/                     # Creación de la base de datos vectorial (Milvus)
│   ├── part_d/                     # Evaluación de recuperación sin LLM
│   ├── part_e/                     # Baseline sin RAG
│   ├── part_f/                     # RAG básico
│   ├── part_g/                     # Agentic-RAG (dos agentes activos)
│   ├── part_h/                     # Integración de datos
│   ├── part_h_1/                   # Evaluación LLM-as-a-Judge
│   ├── part_i/                     # Comparación de métricas
│   ├── part_j/                     # Análisis estadístico y costos
│   └── data/                       # Datos del Código de Minería (JSON, Python)
│
├── analisis-valoracion-jurado/     # Correcciones del jurado y verificaciones reproducibles
│   ├── correccion-01...07/         # Paquetes de corrección por observación
│   └── verificacion-analisis-estadistico/  # Alpha, reconciliación V.1/V.6, recuperación y umbrales
├── data/                           # Datos compartidos (benchmark, preguntas)
├── manuscrito_latest.pdf           # PDF generado por `make pdf`
├── Makefile                        # Compilación del manuscrito
└── AGENTS.md                       # Instrucciones para agentes de IA
```

---

## 🚀 Primeros pasos

### Requisitos

- [Typst CLI](https://typst.app) ≥ 0.14 — para compilar el manuscrito
- [uv](https://docs.astral.sh/uv/) — gestor de paquetes Python
- [direnv](https://direnv.net/) — carga automática de variables de entorno
- Python ≥ 3.13 para los experimentos y ≥ 3.14 para el entorno del manuscrito
- [Milvus](https://milvus.io/) — base de datos vectorial (solo para reproducir la recuperación desde cero)
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
# Compilar una vez → genera manuscrito_latest.pdf
make pdf
```

### Ejecutar experimentos

```bash
cd codigo_experimentos
direnv allow          # Solo la primera vez
uv sync               # Instalar dependencias

# Los notebooks se organizan por etapa: part_0, part_a … part_j.
# Cada directorio contiene notebooks de Jupyter documentados; consultar
# codigo_experimentos/performed_tasks_summary.md para el orden exacto.
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
- **Textuales y léxicas**: Token F1, Jaccard, Levenshtein, BLEU, ROUGE-1/2/L, CER, ratios de longitud y `exact_match` auxiliar
- **Semánticas**: SBERT Similarity (español y multilingüe) y BERTScore
- **LLM-as-a-Judge**: "respuesta correcta" y precisión legal (3 jueces: DeepSeek, Grok, Kimi K2)

**Análisis estadístico**: modelo ordinal mixto con interceptos por caso y unidad, Friedman/Wilcoxon como sensibilidad, bootstrap por casos, corrección de Holm dentro de familias y Krippendorff's alpha (acuerdo inter-juez).

---

## 📝 Citar este trabajo

Si utilizas este código, datos o metodología en tu investigación, por favor cita:

```bibtex
@mastersthesis{spairani2026agenticrag,
  author  = {Spairani, Leonardo Ulises},
  title   = {Desarrollo y evaluación de un prototipo Agentic-RAG
             para consulta del Código de Minería argentino},
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

A la Dra. Laura Lucía Bélfer y al Dr. Rafael Crescenzi por su dirección y apoyo durante el desarrollo de este trabajo. A la profesional del derecho argentino que revisó el benchmark y registró sus observaciones. A la Universidad Austral por proporcionar el marco académico para esta investigación.
