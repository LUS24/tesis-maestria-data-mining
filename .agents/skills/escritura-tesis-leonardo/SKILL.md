---
name: escritura-tesis-leonardo
title: Pipeline para la escritura de la tesis de Leonardo
description: "Instrucciones para la escritura de la tesis de Leonardo"
version: 1.0.0
author: Leonardo Spairani
disclaimer: Adaptado del SKILL original `research-paper-writing` de Orchestra Research.
license: MIT
dependencies: [semanticscholar, arxiv, habanero, requests, scipy, numpy, matplotlib, SciencePlots]
platforms: [linux]
metadata:
  hermes:
    tags: [Research, Thesis Writing, Experiments, ML, AI, Typst, Citations, Statistical Analysis]
    category: research
    related_skills: [arxiv, plan]
    requires_toolsets: [terminal, files]

---

# Pipeline de escritura de tesis de leonardo

Este **no es un pipeline lineal** — es un bucle iterativo. Los cambios disparan nuevas revisiones y las revisiones pueden disparar nuevos cambios. El agente debe manejar estos bucles de retroalimentación.

---

## Cuándo usar esta skill

Usa esta skill cuando:

- **Escribas o revises** cualquier sección de la tesis de Leonardo
- **Te prepares para la entrega** a la Universidad Austral o a los directores de tesis
- **Respondas a revisiones** con revisiones adicionales

## Filosofía central

1. **Sé proactivo.** Entrega borradores completos, no preguntas. Los científicos están ocupados — produce algo concreto sobre lo que puedan reaccionar, luego itera.
2. **Nunca alucines citas.** Las citas generadas por IA tienen ~40% de tasa de error. Siempre obténlas programáticamente. Marca las citas no verificables como `[CITA NECESARIA]`.
3. **La tesis es una historia, no una colección de experimentos.** La tesis necesita contribuciones claras expresadas en oraciones individuales. Si no puedes hacer eso, la tesis no está lista.

### Colaboración

**Por defecto: Sé proactivo. Busca tareas pendientes (`TODOs`) y resuélvelas**

| Nivel de confianza                        | Acción                                                     |
| ----------------------------------------- | ---------------------------------------------------------- |
| **Alto** (repo claro, contribución obvia) | Escribe borrador completo, entrega, itera según feedback   |
| **Medio** (cierta ambigüedad)             | Escribe borrador con incertidumbres señaladas, continúa    |
| **Bajo** (grandes incógnitas)             | Haz 1-2 preguntas específicas vía `clarify`, luego redacta |

**Pide input solo cuando**: el destino de publicación no está claro, hay múltiples enfoques contradictorios, los resultados parecen incompletos, hay solicitud explícita de revisión previa.

---

## Revisión bibliográfica

**Objetivo**: Encontrar trabajos relacionados, identificar líneas de base, recopilar citas.

### Identificar artículos semilla

Comienza desde los artículos ya referenciados en el código:

```bash
# Vía terminal:
grep -r "arxiv\|doi\|cite" --include="*.md" --include="*.bib" --include="*.py"
find . -name "*.bib"
```

### Buscar trabajos relacionados

**Carga la skill `arxiv`** para descubrimiento estructurado de artículos: `skill_view("arxiv")`. Proporciona búsqueda en API REST de arXiv, grafos de citas de Semantic Scholar, perfiles de autores y generación de BibTeX.

Usa `web_search` para descubrimiento amplio, `web_extract` para obtener artículos específicos:

```
# Vía web_search:
web_search("[técnica principal] + [dominio de aplicación] site:arxiv.org")
web_search("[método de referencia] comparación ICML NeurIPS 2024")

# Vía web_extract (para artículos específicos):
web_extract("https://arxiv.org/abs/2303.17651")
```

Consultas de búsqueda adicionales para probar:

```
Consultas de búsqueda:
- "[técnica principal] + [dominio de aplicación]"
- "[método de referencia] comparación"
- "[nombre del problema] estado-del-arte"
- Nombres de autores de citas existentes
```

### Profundizar la búsqueda (amplitud primero, luego profundidad)

Una búsqueda plana (una ronda de consultas) típicamente omite trabajos relacionados importantes. Usa un patrón iterativo de **amplitud luego profundidad** inspirado en pipelines de investigación profunda:

```
Búsqueda bibliográfica iterativa:

Ronda 1 (Amplitud): 4-6 consultas paralelas cubriendo diferentes ángulos
  - "[método] + [dominio]"
  - "[nombre del problema] estado-del-arte 2024 2025"
  - "[método de referencia] comparación"
  - "[enfoque alternativo] vs [tu enfoque]"
  → Recopila artículos, extrae conceptos clave y terminología

Ronda 2 (Profundidad): Genera consultas de seguimiento desde aprendizajes de Ronda 1
  - Nueva terminología descubierta en artículos de Ronda 1
  - Artículos citados por los resultados más relevantes de Ronda 1
  - Hallazgos contradictorios que necesitan investigación
  → Recopila artículos, identifica brechas restantes

Ronda 3 (Dirigida): Llena brechas específicas
  - Líneas de base faltantes identificadas en Rondas 1-2
  - Trabajo concurrente (últimos 6 meses, mismo problema)
  - Resultados negativos clave o enfoques fallidos
  → Detente cuando nuevas consultas devuelvan mayormente artículos ya vistos
```

**Cuándo detenerse**: Si una ronda devuelve >80% de artículos ya en tu colección, la búsqueda está saturada. Típicamente 2-3 rondas son suficientes. Para artículos de revisión, espera 4-5 rondas.

**Para flujos de trabajo basados en agentes**: Delega las consultas de cada ronda en paralelo vía `delegate_task`. Recopila resultados, deduplica, luego genera las consultas de la siguiente ronda a partir de los aprendizajes combinados.

### Verificar cada cita

**NUNCA generes BibTeX de memoria. SIEMPRE obténlo programáticamente.**

Para cada cita, sigue el proceso obligatorio de 5 pasos:

```
Verificación de citas (OBLIGATORIO por cada cita):
1. BUSCAR → Consultar Semantic Scholar o Exa MCP con palabras clave específicas
2. VERIFICAR → Confirmar que el artículo existe en 2+ fuentes (Semantic Scholar + arXiv/CrossRef)
3. RECUPERAR → Obtener BibTeX mediante negociación de contenido con DOI (programáticamente, no de memoria)
4. VALIDAR → Confirmar que la afirmación que citas realmente aparece en el artículo
5. AGREGAR → Añadir BibTeX verificado a la bibliografía
Si ALGÚN paso falla → marcar como [CITA NECESARIA], informar al científico
```

```python
# Obtener BibTeX vía DOI
import requests

def doi_to_bibtex(doi: str) -> str:
    response = requests.get(
        f"https://doi.org/{doi}",
        headers={"Accept": "application/x-bibtex"}
    )
    response.raise_for_status()
    return response.text
```

Si no puedes verificar una cita:

```typst
@placeholder_author2024_verify_this  // TODO: Verificar que esta cita existe
```

**Siempre dile al científico**: "He marcado [X] citas como marcadores de posición que necesitan verificación."

Consulta [flujo-de-trabajo-para-citas.md](./references/flujo-de-trabajo-para-citas.md) para la documentación completa de la API y la clase `CitationManager`.

### Organizar trabajos relacionados

Agrupa los artículos por metodología, no artículo por artículo:

**Bien**: "Una línea de trabajo usa el supuesto X [refs] mientras que nosotros usamos el supuesto Y porque..."
**Mal**: "Smith et al. introdujeron X. Jones et al. introdujeron Y. Nosotros combinamos ambos."

---

## Crear figuras y tablas

**Figuras**:
- Usa gráficos vectoriales (PDF) para todos los plots: `plt.savefig('fig.pdf')`
- Paletas aptas para daltonismo (Okabe-Ito o Paul Tol)
- Leyendas autocontenidas — el lector debe entender sin el texto principal
- Sin título dentro de la figura — la leyenda cumple esa función

**Imágenes externas**: cualquier imagen (diagramas, capturas, gráficos descargados) debe descargarse primero en la carpeta `media/` y referenciarse desde allí. No uses URLs externas directamente en `image()`.

Las figuras deben centrarse con `#align(center, ...)` y usar un tamaño razonable para hoja A4 (ancho máximo ~80% del área de texto). Ejemplo completo:

```typst
#figure(
  align(center, image("media/diagrama_flujo.pdf", width: 80%)),
  caption: [Descripción de la figura.],
) <fig-etiqueta>
```

Parámetros clave de `#figure()`:
- `caption`: texto descriptivo que aparece como título de la figura.
- `placement: auto` para que flote al tope/fondo de página automáticamente.
- `kind`: se detecta automáticamente (imagen, tabla, código).
- Se puede referenciar con `@fig-etiqueta` en el texto.

**Tablas**:
- Usa sintaxis de tabla de Typst con reglas horizontales
- Negrita para el mejor valor por métrica
- Incluye símbolos de dirección (mayor/menor es mejor)
- Precisión decimal consistente

```typst
#table(
  columns: 3,
  stroke: none,
  [*Método*], [*Precisión* $uarr$], [*Latencia* $darr$],
  [],
  [Línea base], [85.2], [45ms],
  [*Nuestro*], [*92.1*], [38ms],
)
```

## Escritura

Consulta el archivo [guia-de-escritura.md](references/guia-de-escritura.md) para las pautas de escritura.

### Título

El título es el elemento más leído. Determina si alguien hace clic para leer el resumen.

**Buenos títulos**:
- Expresan la contribución o hallazgo: "Autoreason: When Iterative LLM Refinement Works and Why It Fails"
- Destacan un resultado sorprendente: "Scaling Data-Constrained Language Models" (implica que se puede)
- Nombran el método + lo que hace: "DPO: Direct Preference Optimization of Language Models"

**Malos títulos**:
- Demasiado genéricos: "An Approach to Improving Language Model Outputs"
- Demasiado largos: más de ~15 palabras
- Solo jerga: "Asymptotic Convergence of Iterative Stochastic Policy Refinement" (¿para quién es?)

**Reglas**:
- Incluye el nombre de tu método si tienes uno (para citabilidad)
- Incluye 1-2 palabras clave que los revisores buscarán
- Evita los dos puntos a menos que ambas mitades tengan significado
- Prueba: ¿sabría un revisor el dominio y la contribución solo con el título?

### Resumen (Fórmula de 5 oraciones)

De Sebastian Farquhar (DeepMind):

```
1. Lo que lograste: "Presentamos...", "Demostramos...", "Probamos..."
2. Por qué esto es difícil e importante
3. Cómo lo haces (con palabras clave especializadas para descubribilidad)
4. Qué evidencia tienes
5. Tu número/resultado más notable
```

**Elimina** aperturas genéricas como "Los modelos de lenguaje grandes han logrado un éxito notable..."

### Figura 1

La Figura 1 es lo segundo que la mayoría de los lectores mira (después del resumen). Redáctala antes de escribir la introducción — te obliga a clarificar la idea central.

| Tipo de Figura 1             | Cuándo usarla                                     | Ejemplo                                                      |
| ---------------------------- | ------------------------------------------------- | ------------------------------------------------------------ |
| **Diagrama del método**      | Nueva arquitectura o pipeline                     | Diagrama de flujo mostrando tu sistema                       |
| **Avance de resultados**     | Un resultado convincente cuenta toda la historia  | Gráfico de barras: "Nuestro vs líneas base" con brecha clara |
| **Ilustración del problema** | El problema no es intuitivo                       | Antes/después mostrando el modo de falla que corriges        |
| **Diagrama conceptual**      | La contribución abstracta necesita anclaje visual | Matriz 2x2 de propiedades del método                         |

**Reglas**: La Figura 1 debe ser comprensible sin leer ningún texto. Solo la leyenda debe comunicar la idea central. Usa el color con propósito — no solo decores.

### Métodos

Habilita la reimplementación:
- Esquema conceptual o pseudocódigo
- Todos los hiperparámetros listados
- Detalles arquitectónicos suficientes para la reproducción
- Presenta las decisiones de diseño finales; los ablations van en experimentos

### Experimentos y resultados

Para cada experimento, indica explícitamente:
- **Qué afirmación respalda**
- Cómo se conecta con la contribución principal
- Qué observar: "la línea azul muestra X, lo que demuestra Y"

Requisitos:
- Barras de error con metodología (desviación estándar vs error estándar)
- Rangos de búsqueda de hiperparámetros
- Infraestructura de cómputo (tipo de GPU, horas totales)
- Métodos de fijación de semillas

### Trabajos relacionados

Organiza metodológicamente, no artículo por artículo. Cita generosamente — los revisores probablemente son autores de artículos relevantes.

### Limitaciones (OBLIGATORIO)

Todas las conferencias importantes lo requieren. La honestidad ayuda:
- Se instruye a los revisores a no penalizar el reconocimiento honesto de limitaciones
- Anticípate a las críticas identificando debilidades primero
- Explica por qué las limitaciones no socavan las afirmaciones centrales

### Conclusión y discusión

**Conclusión** (obligatoria):
- Reexpresa la contribución en una oración (redacción diferente al resumen)
- Resume los hallazgos clave (2-3 oraciones, no una lista)
- Implicaciones: ¿qué significa esto para el campo?
- Trabajo futuro: 2-3 pasos concretos (no vagos "dejamos X para trabajo futuro")

**Discusión** (opcional, a veces combinada con la conclusión):
- Implicaciones más amplias más allá de los resultados inmediatos
- Conexiones con otros subcampos
- Evaluación honesta de cuándo el método funciona y cuándo no
- Consideraciones prácticas de implementación

**NO** introduzcas nuevos resultados o afirmaciones en la conclusión.

### Estrategia de apéndices

Los apéndices son ilimitados en todas las conferencias importantes y son esenciales para la reproducibilidad. Estructura:

| Sección del apéndice                    | Qué va aquí                                                                                                                                        |
| --------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Demostraciones y derivaciones**       | Demostraciones completas demasiado largas para el texto principal. El texto principal puede enunciar teoremas con "demostración en el Apéndice A". |
| **Experimentos adicionales**            | Ablations, curvas de escalado, desgloses por conjunto de datos, sensibilidad de hiperparámetros                                                    |
| **Detalles de implementación**          | Tablas completas de hiperparámetros, detalles de entrenamiento, especificaciones de hardware, semillas aleatorias                                  |
| **Documentación del conjunto de datos** | Proceso de recolección de datos, pautas de anotación, licencias, preprocesamiento                                                                  |
| **Prompts y plantillas**                | Prompts exactos usados (para métodos basados en LLM), plantillas de evaluación                                                                     |
| **Evaluación humana**                   | Capturas de pantalla de la interfaz de anotación, instrucciones dadas a los anotadores, detalles de IRB                                            |
| **Figuras adicionales**                 | Desgloses por tarea, visualizaciones de trayectorias, ejemplos de casos de falla                                                                   |

**Reglas**:
- Nunca pongas evidencia crítica solo en el apéndice
- Referencia cruzada: "Resultados completos en la Tabla 5 (Apéndice B)" no solo "ver apéndice"
- Usa `#heading(level: 1, numbering: "A.1")` para secciones de apéndice, etc.

### Declaración de ética e impacto más amplio

La mayoría de las conferencias ahora requieren o recomiendan firmemente una declaración de ética/impacto más amplio. Esto no es un texto de relleno — los revisores lo leen y pueden señalar preocupaciones éticas que desencadenan el rechazo directo.

**Qué incluir:**

| Componente                     | Contenido                                                       | Requerido por              |
| ------------------------------ | --------------------------------------------------------------- | -------------------------- |
| **Impacto social positivo**    | Cómo beneficia tu trabajo a la sociedad                         | NeurIPS, ICML              |
| **Impacto negativo potencial** | Riesgos de mal uso, preocupaciones de doble uso, modos de falla | NeurIPS, ICML              |
| **Equidad y sesgo**            | ¿Tu método/datos tienen sesgos conocidos?                       | Todas (implícitamente)     |
| **Impacto ambiental**          | Huella de carbono de cómputo para entrenamiento a gran escala   | ICML, cada vez más NeurIPS |
| **Privacidad**                 | ¿Tu trabajo usa o permite procesar datos personales?            | ACL, NeurIPS               |
| **Divulgación de LLM**         | ¿Se usó IA en la escritura o experimentos?                      | ICLR (obligatorio), ACL    |

**Redacción de la declaración:**

```typst
= Declaración de Impacto Más Amplio
// Después de la conclusión, no cuenta para el límite de páginas

// 1. Aplicaciones positivas (1-2 oraciones)
Este trabajo permite [#aplicación específica] que puede beneficiar a [#grupo específico].

// 2. Riesgos y mitigaciones (1-3 oraciones, sé específico)
[#Método/modelo] podría ser mal utilizado para [#riesgo específico]. Mitigamos
esto mediante [#mitigación específica, ej., liberar solo pesos de modelo por encima del tamaño X,
incluir filtros de seguridad, documentar modos de falla].

// 3. Limitaciones de las afirmaciones de impacto (1 oración)
Nuestra evaluación se limita a [#dominio específico]; una implementación más amplia requeriría
[#trabajo adicional específico].
```

**Errores comunes:**
- Escribir "no prevemos impactos negativos" (casi nunca es cierto — los revisores desconfían de esto)
- Ser vago: "esto podría ser mal utilizado" sin especificar cómo
- Ignorar los costos de cómputo para trabajos a gran escala
- Olvidar divulgar el uso de LLM en conferencias que lo requieren

**Huella de carbono de cómputo** (para trabajos con entrenamiento intensivo):
```python
# Estimar usando la metodología de la herramienta ML CO2 Impact
gpu_hours = 1000  # horas totales de GPU
gpu_tdp_watts = 400  # ej., A100 = 400W
pue = 1.1  # Efectividad de uso de energía (gasto general del centro de datos)
carbon_intensity = 0.429  # kg CO2/kWh (promedio EE.UU.; varía por región)

energy_kwh = (gpu_hours * gpu_tdp_watts * pue) / 1000
carbon_kg = energy_kwh * carbon_intensity
print(f"Energía: {energy_kwh:.0f} kWh, Carbono: {carbon_kg:.0f} kg CO2eq")
```

### Hojas de datos y fichas de modelo (si aplica)

Si tu artículo introduce un **nuevo conjunto de datos** o **libera un modelo**, incluye documentación estructurada. Los revisores lo esperan cada vez más, y el track de Datasets & Benchmarks de NeurIPS lo requiere.

**Hojas de datos para conjuntos de datos** (Gebru et al., 2021) — incluir en el apéndice:

```
Documentación del conjunto de datos (Apéndice):
- Motivación: ¿Por qué se creó este conjunto de datos? ¿Qué tarea respalda?
- Composición: ¿Cuáles son las instancias? ¿Cuántas? ¿Qué tipos de datos?
- Recolección: ¿Cómo se recolectaron los datos? ¿Cuál fue la fuente?
- Preprocesamiento: ¿Qué limpieza/filtrado se aplicó?
- Distribución: ¿Cómo se distribuye el conjunto de datos? ¿Bajo qué licencia?
- Mantenimiento: ¿Quién lo mantiene? ¿Cómo reportar problemas?
- Consideraciones éticas: ¿Contiene datos personales? ¿Se obtuvo consentimiento?
  ¿Potencial de daño? ¿Sesgos conocidos?
```

**Fichas de modelo** (Mitchell et al., 2019) — incluir en el apéndice para liberaciones de modelos:

```
Ficha de modelo (Apéndice):
- Detalles del modelo: Arquitectura, datos de entrenamiento, procedimiento de entrenamiento
- Uso previsto: Casos de uso principales, usos fuera de alcance
- Métricas: Métricas de evaluación y resultados en benchmarks
- Consideraciones éticas: Sesgos conocidos, evaluaciones de equidad
- Limitaciones: Modos de falla conocidos, dominios donde el modelo rinde por debajo
```

### Estilo de escritura

**Claridad a nivel de oración (7 principios de Gopen & Swan):**

| Principio                  | Regla                                       |
| -------------------------- | ------------------------------------------- |
| Proximidad sujeto-verbo    | Mantén sujeto y verbo cerca                 |
| Posición de énfasis        | Coloca el énfasis al final de las oraciones |
| Posición del tema          | Pon el contexto primero, info nueva después |
| Viejo antes que nuevo      | Info familiar → info no familiar            |
| Una unidad, una función    | Cada párrafo hace un punto                  |
| Acción en el verbo         | Usa verbos, no nominalizaciones             |
| Contexto antes de lo nuevo | Establece el escenario antes de presentar   |

**Elección de palabras (Lipton, Steinhardt):**
- Sé específico: "precisión" no "rendimiento"
- Elimina las ambigüedades: omite "puede" a menos que sea genuinamente incierto
- Terminología consistente en todo el texto
- Evita vocabulario incremental: "desarrolla", no "combina"

**Guía de escritura completa con ejemplos**: Consulta [references/guia-de-escritura.md](references/guia-de-escritura.md)


## Autorevisión y revisión

**Objetivo**: Simular el proceso de revisión antes de la entrega. Detectar debilidades temprano.

Para lograrlo, lanza subagentes e indícales que sigan el archivo `./references/guia-de-revision.md`.

Indícales que pongan el informe de revisión en el directorio `temp`.

Pregunta al usuario qué sección del directorio `capitulos` desea revisar.

El usuario tiene una suscripción a Ollama, usa tres revisores, las respuestas de los revisores deben integrarse en el mismo informe de revisión como se menciona en el archivo `./references/guia-de-revision.md`.

Las mejores opciones para el proceso de revisión son:

- glm-5.2:cloud
- minimax-m3:cloud (Vision)
- deepseek-v4-flash:cloud
- kimi-k2.6:cloud (Vision)


## Presentación (Diatypst)

**Objetivo**: Crear y mantener la presentación de la tesis usando [Diatypst](https://typst.app/universe/package/diatypst/), un paquete Typst para diapositivas.

La presentación se encuentra en `presentacion/diatypst/main.typ` y se compila con `make presentation`.

### Cuándo usar esta sección

- Cuando necesites **crear la presentación desde cero** para la defensa de tesis.
- Cuando el manuscrito haya cambiado y necesites **sincronizar la presentación**.
- Cuando necesites **agregar, modificar o eliminar diapositivas**.
- Cuando necesites **actualizar figuras, tablas o resultados** en la presentación.

### Filosofía

1. **La presentación deriva del manuscrito, no es independiente.** Cada diapositiva debe tener una correspondencia clara con una sección del manuscrito.
2. **Una idea por diapositiva.** Si una diapositiva tiene más de 3 viñetas o cubre múltiples conceptos, divídela.
3. **Prioriza lo visual sobre el texto.** Usa diagramas, tablas y gráficos del manuscrito. El público debe entender la diapositiva en 3 segundos.
4. **Reescribe, no copies.** El texto de las diapositivas debe estar adaptado para formato oral, no pegado literalmente del manuscrito.

### Flujo de trabajo

#### 1. Extraer la narrativa central del manuscrito

Antes de escribir diapositivas, identifica desde el manuscrito:

- **Problema**: ¿Qué problema resuelve la tesis? (1-2 diapositivas)
- **Contribución**: ¿Cuál es la contribución principal? (1 diapositiva)
- **Método**: ¿Cómo se aborda el problema? (2-4 diapositivas)
- **Resultados**: ¿Qué evidencia respalda la contribución? (2-3 diapositivas)
- **Conclusiones**: ¿Qué implicaciones tiene? (1-2 diapositivas)

#### 2. Mapear capítulos a secciones de la presentación

| Capítulo del manuscrito | Sección en presentación |
| --- | --- |
| 01 — Introducción | Introducción (3-4 slides) |
| 02 — Fundamentos e historia del PLN | Contexto (1-2 slides) |
| 03 — Aplicación de PLN al dominio legal | Contexto (1-2 slides) |
| 04 — Marco teórico Agentic RAG | Marco Teórico (2-3 slides) |
| 05 — Metodología | Método (3-4 slides) |
| 06 — Evaluación | Resultados (3-4 slides) |
| 07 — Trabajos relacionados | (Integrar en contexto/método) |
| 08 — Conclusiones y trabajos futuros | Conclusiones (2-3 slides) |

#### 3. Sincronizar tras cambios en el manuscrito

Cuando el manuscrito cambie:

1. Identifica qué capítulos cambiaron.
2. Localiza las diapositivas correspondientes en `presentacion/diatypst/main.typ`.
3. Actualiza:
   - **Figuras**: si cambió el diagrama en `manuscrito/media/`, la presentación lo refleja automáticamente (misma ruta relativa).
   - **Resultados**: actualiza tablas y métricas numéricas.
   - **Narrativa**: ajusta el texto para reflejar cambios en la argumentación.
4. Recompila: `make presentation`.

### Compilación

```bash
# Desde la raíz del repositorio
make presentation

# O manualmente
cd presentacion/diatypst
typst compile main.typ ../../presentacion_latest.pdf

# Vista previa en vivo
cd presentacion/diatypst
typst watch main.typ ../../presentacion_latest.pdf
```

### Guía detallada

Consulta [references/guia-de-preparacion-presentacion.md](references/guia-de-preparacion-presentacion.md) para la documentación completa incluyendo:

- Configuración inicial y opciones de Diatypst
- Estructura de diapositivas (secciones, contenido)
- Elementos de contenido (términos, código, tablas, imágenes, citas)
- Tema y personalización de estilo
- Estructura recomendada para defensa de tesis (~15-20 diapositivas)
- Buenas prácticas y errores comunes
