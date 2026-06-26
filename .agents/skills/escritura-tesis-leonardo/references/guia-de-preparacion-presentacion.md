# Guía de Preparación de la Presentación (Diatypst)

Esta guía documenta cómo crear y mantener la presentación de la tesis de Leonardo usando el paquete [Diatypst](https://typst.app/universe/package/diatypst/) para Typst.

---

## Contenido

- [Guía de Preparación de la Presentación (Diatypst)](#guía-de-preparación-de-la-presentación-diatypst)
  - [Contenido](#contenido)
  - [Estructura del Proyecto](#estructura-del-proyecto)
  - [Configuración Inicial](#configuración-inicial)
    - [Importación y configuración básica](#importación-y-configuración-básica)
    - [Portada personalizada](#portada-personalizada)
  - [Opciones de Diatypst](#opciones-de-diatypst)
  - [Estructura de Diapositivas](#estructura-de-diapositivas)
    - [Secciones y diapositivas](#secciones-y-diapositivas)
    - [Navegación entre diapositivas](#navegación-entre-diapositivas)
  - [Elementos de Contenido](#elementos-de-contenido)
    - [Términos y definiciones](#términos-y-definiciones)
    - [Código](#código)
    - [Tablas](#tablas)
    - [Listas](#listas)
    - [Imágenes](#imágenes)
  - [Tema y Estilo](#tema-y-estilo)
    - [Tema "normal" (por defecto)](#tema-normal-por-defecto)
    - [Tema "full"](#tema-full)
    - [Personalización de color](#personalización-de-color)
  - [Compilación](#compilación)
    - [Desde la raíz del repositorio](#desde-la-raíz-del-repositorio)
  - [Flujo de Trabajo: Sincronización con el Manuscrito](#flujo-de-trabajo-sincronización-con-el-manuscrito)
    - [1. Extraer la narrativa central](#1-extraer-la-narrativa-central)
    - [2. Mapear capítulos a secciones de la presentación](#2-mapear-capítulos-a-secciones-de-la-presentación)
    - [3. Reglas de extracción](#3-reglas-de-extracción)
    - [4. Actualización tras cambios en el manuscrito](#4-actualización-tras-cambios-en-el-manuscrito)
  - [Estructura Recomendada de la Presentación](#estructura-recomendada-de-la-presentación)
  - [Buenas Prácticas](#buenas-prácticas)
    - [Para presentaciones académicas](#para-presentaciones-académicas)
    - [Errores comunes](#errores-comunes)
  - [Referencias](#referencias)

---

## Estructura del Proyecto

La presentación se encuentra en:

```
presentacion/
└── diatypst/
    └── main.typ          # Archivo principal de la presentación
```

El PDF generado se guarda en la raíz del repositorio como `presentacion_latest.pdf`.

---

## Configuración Inicial

### Importación y configuración básica

```typst
#import "@preview/diatypst:0.9.3": *

#show: slides.with(
  title: "Desarrollo y evaluación de un prototipo de sistema inteligente para consulta de normativa nacional argentina mediante recuperación agéntica",
  subtitle: "Tesis de Maestría — Universidad Austral",
  date: "2026",
  authors: ("Leonardo Ulises Spairani"),

  // Opciones visuales
  ratio: 16/9,
  layout: "medium",
  title-color: blue.darken(60%),
  toc: true,
)
```

### Portada personalizada

Para incluir el logo de la universidad, deshabilita la portada por defecto y crea una personalizada:

```typst
#import "@preview/diatypst:0.9.3": *

#set page(
  footer: none, header: none, margin: 0cm,
  height: 10.5cm,   // small=9cm, medium=10.5cm, large=12cm
  width: 16/9*10.5cm, // ratio * height
)

// Portada personalizada
#align(center + horizon)[
  #image("../../manuscrito/media/logo_universidad_austral_ingenieria.png", height: 40%)
  #v(2cm)
  #text(size: 24pt, weight: "bold")[Título de la Tesis]
  #v(1cm)
  #text(size: 18pt)[Leonardo Ulises Spairani]
]

#show: slides.with(
  ...,
  first-slide: false,
)
```

---

## Opciones de Diatypst

| Parámetro         | Descripción                                            | Default              |
| ----------------- | ------------------------------------------------------ | -------------------- |
| `title`           | Título de la presentación (obligatorio)                | `none`               |
| `subtitle`        | Subtítulo visible en el footer                         | `none`               |
| `date`            | Fecha de la presentación                               | `none`               |
| `authors`         | Autor(es) — string o array de strings                  | `none`               |
| `layout`          | Tamaño: `"small"`, `"medium"`, `"large"`               | `"medium"`           |
| `ratio`           | Relación de aspecto (ej. `16/9`, `4/3`)                | `4/3`                |
| `title-color`     | Color base de la presentación                          | `blue.darken(50%)`   |
| `bg-color`        | Color de fondo                                         | `white`              |
| `count`           | Contador: `"dot"`, `"number"`, `"dot-section"`, `none` | `"dot"`              |
| `footer`          | Mostrar footer                                         | `true`               |
| `toc`             | Mostrar tabla de contenidos                            | `true`               |
| `footer-title`    | Texto personalizado en footer (izquierda)              | igual que `title`    |
| `footer-subtitle` | Texto personalizado en footer (derecha)                | igual que `subtitle` |
| `theme`           | Tema: `"normal"` o `"full"`                            | `"normal"`           |
| `first-slide`     | Incluir portada por defecto                            | `true`               |

**Notas importantes:**
- `title-color`: usa colores oscuros para buen contraste. Ej: `rgb("#ff851b").darken(50%)` o `blue.darken(60%)`.
- `count`: los dots son cliqueables para navegar entre diapositivas. `"dot-section"` es mejor para presentaciones largas.
- `layout`: `"small"` para más contenido por slide, `"large"` para menos pero más legible.

---

## Estructura de Diapositivas

### Secciones y diapositivas

```typst
// = (level-1 heading) = Nueva sección (diapositiva de separación)
= Introducción

// == (level-2 heading) = Nueva diapositiva de contenido
== Motivación

#lorem(20)

// También se puede usar #pagebreak() para forzar una nueva diapositiva
```

### Navegación entre diapositivas

```typst
// Enlace a una diapositiva específica por etiqueta
#ref(<etiqueta>, supplement: "ir a")

// O usando etiquetas de heading
@etiqueta
```

---

## Elementos de Contenido

### Términos y definiciones

```typst
/ *RAG*: Retrieval-Augmented Generation — técnica que combina recuperación de información con generación de texto.
/ *Agente*: Sistema autónomo que percibe su entorno y actúa para lograr objetivos.
```

### Código

```typst
```python
def retrieve(query: str, k: int = 5) -> list[Document]:
    return vector_store.similarity_search(query, k=k)
```
```

### Citas y referencias

```typst
#quote(attribution: [Lewis y col., 2020])[
  La recuperación aumentada permite a los modelos acceder a conocimiento externo actualizado.
]
```

### Tablas

```typst
#table(
  columns: 3,
  [*Modelo*], [*Precisión*], [*Recall*],
  [RAG básico], [85.2%], [82.1%],
  [*Agentic RAG*], [*92.1%*], [*90.5%*],
)
```

### Listas

```typst
// No numerada
- Punto uno
  - Subpunto
- Punto dos

// Numerada
1. Primer paso
2. Segundo paso
3. Tercer paso
```

### Imágenes

```typst
#figure(
  align(center, image("../../manuscrito/media/diagrama_arquitectura.pdf", width: 80%)),
  caption: [Arquitectura del sistema propuesto.],
)
```

**Importante**: Las imágenes deben residir en `manuscrito/media/` y referenciarse con ruta relativa desde `presentacion/diatypst/`.

---

## Tema y Estilo

### Tema "normal" (por defecto)

Tema limpio y minimalista. Ideal para presentaciones académicas donde el contenido es el protagonista.

### Tema "full"

Similar a Beamer de LaTeX. Más recargado visualmente. Útil cuando se busca un estilo más formal.

### Personalización de color

```typst
// Usar un color específico
title-color: rgb("#1a5276"),  // Azul oscuro institucional

// Oscurecer un color para mejor contraste
title-color: rgb("#ff851b").darken(50%),
```

---

## Compilación

### Desde la raíz del repositorio

```bash
make presentation
```

Esto ejecuta:

```bash
cd ./presentacion/diatypst && typst compile main.typ ../../presentacion_latest.pdf
```

---

## Flujo de Trabajo: Sincronización con el Manuscrito

La presentación debe derivarse del manuscrito, no ser independiente. Sigue este proceso:

### 1. Extraer la narrativa central

Antes de escribir diapositivas, identifica:

- **Problema**: ¿Qué problema resuelve la tesis? (1-2 diapositivas)
- **Contribución**: ¿Cuál es la contribución principal? (1 diapositiva)
- **Método**: ¿Cómo se aborda el problema? (2-4 diapositivas)
- **Resultados**: ¿Qué evidencia respalda la contribución? (2-3 diapositivas)
- **Conclusiones**: ¿Qué implicaciones tiene? (1-2 diapositivas)

### 2. Mapear capítulos a secciones de la presentación

| Capítulo del manuscrito                 | Sección en presentación       |
| --------------------------------------- | ----------------------------- |
| 01 — Introducción                       | Introducción (3-4 slides)     |
| 02 — Fundamentos e historia del PLN     | Contexto (1-2 slides)         |
| 03 — Aplicación de PLN al dominio legal | Contexto (1-2 slides)         |
| 04 — Marco teórico Agentic RAG          | Marco Teórico (2-3 slides)    |
| 05 — Metodología                        | Método (3-4 slides)           |
| 06 — Evaluación                         | Resultados (3-4 slides)       |
| 07 — Trabajos relacionados              | (Integrar en contexto/método) |
| 08 — Conclusiones y trabajos futuros    | Conclusiones (2-3 slides)     |

### 3. Reglas de extracción

- **No copies texto literalmente** del manuscrito. Reescribe para el formato oral.
- **Una idea por diapositiva**. Si una diapositiva tiene más de 3 viñetas, divídela.
- **Menos texto, más imágenes**. Prioriza diagramas, tablas y gráficos sobre párrafos.
- **Usa figuras del manuscrito** cuando sea posible (referencia a `../../manuscrito/media/...`).
- **Incluye el número de diapositiva** para referencia durante la defensa.

### 4. Actualización tras cambios en el manuscrito

Cuando el manuscrito cambie (nuevos resultados, figuras, secciones):

1. Identifica qué capítulos cambiaron.
2. Localiza las diapositivas correspondientes en la presentación.
3. Actualiza:
   - **Figuras**: si cambió el diagrama en `manuscrito/media/`, la presentación lo refleja automáticamente (misma ruta).
   - **Resultados**: actualiza tablas y métricas numéricas.
   - **Narrativa**: ajusta el texto de las diapositivas para reflejar cambios en la argumentación.
4. Recompila: `make presentation`.

---

## Estructura Recomendada de la Presentación

Para una defensa de tesis de maestría (~20-25 minutos, ~15-20 diapositivas):

```
1.  Portada (título, autor, tutores, universidad)
2.  Agenda / Índice
3.  Motivación (¿por qué este problema?)
4.  Pregunta de investigación
5.  Contexto: PLN + Dominio Legal
6.  Marco Teórico: Agentic RAG
7.  Método Propuesto (diagrama de arquitectura)
8.  Implementación (componentes clave)
9.  Diseño Experimental
10. Resultados (tabla comparativa)
11. Resultados (gráficos)
12. Discusión
13. Trabajos Relacionados (breve)
14. Contribuciones
15. Limitaciones
16. Conclusiones
17. Trabajo Futuro
18. Preguntas / Gracias
```

---

## Buenas Prácticas

### Para presentaciones académicas

1. **Regla 10-20-30** (Guy Kawasaki): 10 diapositivas, 20 minutos, tamaño de fuente mínimo 30pt.
2. **Una idea por diapositiva**: si necesitas explicar dos conceptos, usa dos diapositivas.
3. **La diapositiva debe entenderse en 3 segundos**: el público debe captar la idea principal sin leer.
4. **Jerarquía visual**: título → contenido → detalle. Usa tamaño, color y posición.
5. **Contraste**: texto oscuro sobre fondo claro o viceversa. Evita fondos con patrones.
6. **Fuentes**: usa la misma familia tipográfica del manuscrito (`New Computer Modern`).
7. **Imágenes de alta calidad**: prefiere PDF (vectorial) sobre PNG/JPG para diagramas.
8. **Consistencia**: mismo estilo de títulos, bullets, tablas en toda la presentación.

### Errores comunes

- ❌ Diapositivas con párrafos largos (el público lee en vez de escuchar).
- ❌ Tablas con demasiadas filas/columnas (ilegibles en pantalla).
- ❌ Colores sin contraste suficiente (título claro sobre fondo claro).
- ❌ Demasiadas transiciones/animaciones (distraen).
- ❌ Figuras del manuscrito sin adaptar (demasiado detalle para una diapositiva).

---

## Referencias

- [Diatypst en Typst Universe](https://typst.app/universe/package/diatypst/)
- [Repositorio GitHub de Diatypst](https://github.com/skriptum/Diatypst)
- [Documentación oficial de Diatypst](https://mdwm.org/diatypst/)
- [Guía de inicio rápido](https://mdwm.org/diatypst/quickstart.html)
- [Referencia de opciones](https://mdwm.org/diatypst/reference.html)
- [Estilos y elementos](https://mdwm.org/diatypst/styling.html)
