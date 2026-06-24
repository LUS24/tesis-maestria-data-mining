---
name: revision-tesis-leonardo
title: Pipeline de revisión de la tesis de Leonardo
description: "Revisión del trabajo de tesis de Leonardo Spairani"
version: 1.0.0
author: Leonardo Spairani
disclaimer: Adaptado del SKILL original `research-paper-writing` de Orchestra Research.
license: MIT
dependencies: []
platforms: [linux]
metadata:
  hermes:
    tags: [Revisión de Tesis]
    category: research
    related_skills: [arxiv, plan]
    requires_toolsets: [terminal, files]

---

Este documento provee lineamientos de cómo revisar el trabajo de tesis de Leonardo Spairani.

---

## Contenido

- [Dimensiones Universales de Evaluación](#dimensiones-universales-de-evaluación)
- [Qué Hace que una Revisión sea Sólida](#qué-hace-que-una-revisión-sea-sólida)
- [Inquietudes Comunes de los Revisores](#inquietudes-comunes-de-los-revisores)
- [Cómo Abordar la Retroalimentación de los Revisores](#cómo-abordar-la-retroalimentación-de-los-revisores)

---

## Dimensiones Universales de Evaluación

Todas las conferencias importantes de ML evalúan artículos en cuatro dimensiones principales:

### 1. Calidad (Solidez Técnica)

**Lo que preguntan los revisores:**
- ¿Las afirmaciones están bien respaldadas por análisis teóricos o resultados experimentales?
- ¿Las demostraciones son correctas? ¿Los experimentos están adecuadamente controlados?
- ¿Las líneas de base son apropiadas y se comparan de manera justa?
- ¿La metodología es sólida?

**Cómo asegurar alta calidad:**
- Incluir demostraciones completas (en el artículo principal o en el apéndice con esquemas)
- Usar líneas de base apropiadas (no "strawmen")
- Reportar varianza/barras de error con la metodología
- Documentar el proceso de selección de hiperparámetros

### 2. Claridad (Redacción y Organización)

**Lo que preguntan los revisores:**
- ¿El artículo está escrito con claridad y bien organizado?
- ¿Un experto en el área podría reproducir los resultados?
- ¿La notación es consistente? ¿Los términos están definidos?
- ¿El artículo es autocontenido?

**Cómo asegurar claridad:**
- Usar terminología consistente en todo el documento
- Definir toda la notación en su primer uso
- Incluir detalles de reproducibilidad (el apéndice es aceptable)
- Hacer que personas no-autoras lo lean antes de la presentación

### 3. Relevancia (Impacto e Importancia)

**Lo que preguntan los revisores:**
- ¿Los resultados tienen impacto para la comunidad?
- ¿Otros investigadores construirán sobre este trabajo?
- ¿Aborda un problema importante?
- ¿Cuál es el potencial de impacto en el mundo real?

**Cómo demostrar relevancia:**
- Articular claramente la importancia del problema
- Conectar con temas de investigación más amplios
- Discutir aplicaciones potenciales
- Comparar con enfoques existentes de manera significativa

### 4. Originalidad (Novedad y Contribución)

**Lo que preguntan los revisores:**
- ¿Esto aporta nuevas perspectivas?
- ¿En qué se diferencia del trabajo previo?
- ¿La contribución es no trivial?

**Perspectiva clave de las guías de NeurIPS:**
> "La originalidad no necesariamente requiere introducir un método completamente nuevo. Los artículos que brindan nuevas perspectivas a partir de la evaluación de enfoques existentes o que esclarecen por qué ciertos métodos tienen éxito también pueden ser altamente originales."

---

## Guías para Revisores adaptadas de NeurIPS y ACL

### Sistema de Puntuación (Escala 1-6)

| Puntaje | Etiqueta               | Descripción                                                      |
| ------- | ---------------------- | ---------------------------------------------------------------- |
| **6**   | Aceptación Fuerte      | Trabajo innovador e impecable; top 2-3% de las presentaciones    |
| **5**   | Aceptación             | Técnicamente sólido, alto impacto; beneficiaría a la comunidad   |
| **4**   | Aceptación Limítrofe   | Trabajo sólido con evaluación limitada; inclina a aceptar        |
| **3**   | Rechazo Limítrofe      | Sólido pero las debilidades superan a las fortalezas; inclina a rechazar |
| **2**   | Rechazo                | Fallas técnicas o evaluación débil                               |
| **1**   | Rechazo Fuerte         | Resultados ya conocidos o preocupaciones éticas no abordadas     |

### Instrucciones para Revisores

Se instruye explícitamente a los revisores a:

1. **Evaluar el artículo tal como está escrito** — no lo que podría ser con revisiones
2. **Proporcionar retroalimentación constructiva** — 3 a 5 puntos accionables
3. **No penalizar limitaciones honestas** — reconocer debilidades es alentado
4. **Evaluar la reproducibilidad** — ¿se puede verificar el trabajo?
5. **Considerar implicaciones éticas** — posible uso indebido o daño

### Lo que los Revisores Deben Evitar

- Revisiones superficiales y desinformadas
- Exigir experimentos adicionales no razonables
- Penalizar a los autores por reconocer honestamente limitaciones
- Rechazar por falta de citas al trabajo propio del revisor

### Criterios Específicos de ACL

ACL añade evaluación específica de PLN:

1. **Solidez lingüística** — ¿Las afirmaciones lingüísticas son precisas?
2. **Documentación de recursos** — ¿Los conjuntos de datos/modelos están documentados adecuadamente?
3. **Consideración multilingüe** — Si aplica, ¿se aborda la diversidad lingüística?

### Sección de Limitaciones

ACL requiere específicamente una sección de Limitaciones. Los revisores verifican:
- ¿Las limitaciones son honestas y exhaustivas?
- ¿Las limitaciones socavan las afirmaciones principales?
- ¿Se abordan los posibles impactos negativos?


## Qué Hace que una Revisión sea Sólida

### Siguiendo las Reglas de Daniel Dennett

Los buenos revisores siguen estos principios:

1. **Re-expresar la postura de manera justa** — Demostrar que se entiende el artículo
2. **Enumerar acuerdos** — Reconocer lo que funciona bien
3. **Enumerar lo aprendido** — Reconocer la contribución
4. **Solo entonces criticar** — Después de haber establecido comprensión

### Mejores Prácticas de Estructura de Revisión

**Estructura de Revisión Sólida:**
```
Resumen (1 párrafo):
- Qué hace el artículo
- Contribución principal que se afirma

Fortalezas (3-5 viñetas):
- Aspectos positivos específicos
- Por qué son importantes

Debilidades (3-5 viñetas):
- Inquietudes específicas
- Por qué son importantes
- Sugerencias para abordarlas

Preguntas (2-4 ítems):
- Aclaraciones necesarias
- Aspectos que cambiarían la evaluación

Problemas Menores (opcional):
- Erratas, oraciones poco claras
- Problemas de formato

Evaluación General:
- Recomendación clara con fundamentos
```

---

## Inquietudes Comunes de los Revisores

### Inquietudes Técnicas

| Inquietud                          | Cómo Prevenirlo                                               |
| ---------------------------------- | ------------------------------------------------------------- |
| "Líneas de base demasiado débiles" | Usar líneas de base del estado del arte, citar trabajos recientes |
| "Faltan ablaciones"                | Incluir un estudio de ablación sistemático                    |
| "Sin barras de error"              | Reportar desviación estándar/error, múltiples ejecuciones     |
| "Hiperparámetros no ajustados"     | Documentar el proceso de ajuste y los rangos de búsqueda      |
| "Afirmaciones no respaldadas"      | Asegurar que cada afirmación tenga evidencia                  |

### Inquietudes de Novedad

| Inquietud                         | Cómo Prevenirlo                                            |
| --------------------------------- | ---------------------------------------------------------- |
| "Contribución incremental"        | Articular claramente qué es nuevo vs. el trabajo previo    |
| "Similar a [artículo X]"          | Comparar explícitamente con X en la sección de Trabajo Relacionado |
| "Extensión directa"               | Destacar los aspectos no obvios                            |

### Inquietudes de Claridad

| Inquietud                    | Cómo Prevenirlo                                       |
| ---------------------------- | ----------------------------------------------------- |
| "Difícil de seguir"          | Usar estructura clara y señalamiento                 |
| "Notación inconsistente"     | Revisar toda la notación, crear una tabla de notación |
| "Faltan detalles"            | Incluir un apéndice de reproducibilidad               |
| "Figuras poco claras"        | Leyendas autocontenidas, tamaño adecuado              |

### Inquietudes de Relevancia

| Inquietud                                    | Cómo Prevenirlo                                              |
| -------------------------------------------- | ------------------------------------------------------------ |
| "Impacto limitado"                           | Discutir implicaciones más amplias                           |
| "Evaluación limitada"                        | Evaluar en múltiples puntos de referencia                    |
| "Solo funciona en un entorno restringido"    | Reconocer el alcance, explicar por qué sigue siendo valioso  |

---

## Cómo Abordar la Retroalimentación de los Revisores

### Mejores Prácticas para la Réplica

**Sí:**
- Agradecer a los revisores por su tiempo
- Abordar cada inquietud de manera específica
- Proporcionar evidencia (nuevos experimentos si es posible)
- Ser conciso — los revisores están ocupados
- Reconocer las críticas válidas

**No:**
- Ponerse a la defensiva o ser despectivo
- Hacer promesas que no se puedan cumplir
- Ignorar críticas difíciles
- Escribir réplicas excesivamente largas
- Discutir sobre evaluaciones subjetivas

### Plantilla de Réplica

```markdown
Agradecemos a los revisores por sus comentarios reflexivos.

## Revisor 1

**R1-P1: [Inquietud citada]**
[Respuesta directa con evidencia]

**R1-P2: [Inquietud citada]**
[Respuesta directa con evidencia]

## Revisor 2

...

## Resumen de Cambios
Si es aceptado, realizaremos:
1. [Cambio específico]
2. [Cambio específico]
3. [Cambio específico]
```

### Cuándo Aceptar las Críticas

Algunos comentarios de los revisores simplemente deben aceptarse:
- Errores técnicos válidos
- Omisión de trabajos relacionados importantes
- Explicaciones poco claras
- Detalles experimentales faltantes

Reconócelos con elegancia: "El revisor tiene razón en que... Revisaremos para..."

### Cuándo Responder con Respeto

Se puede discrepar respetuosamente cuando:
- El revisor malinterpretó el artículo
- Los experimentos solicitados están fuera del alcance
- La crítica es factualmente incorrecta

Enmarca los desacuerdos de manera constructiva: "Apreciamos esta perspectiva. Sin embargo, [explicación]..."

---

## Simulación Pre-Presentación como Revisor

Antes de presentar, pregúntate:

**Calidad:**
- [ ] ¿Confiaría en estos resultados si los viera?
- [ ] ¿Todas las afirmaciones están respaldadas por evidencia?
- [ ] ¿Las líneas de base son justas y recientes?

**Claridad:**
- [ ] ¿Alguien podría reproducir esto a partir del artículo?
- [ ] ¿La redacción es clara para no expertos en este subcampo?
- [ ] ¿Todos los términos y la notación están definidos?

**Relevancia:**
- [ ] ¿Por qué debería importarle esto a la comunidad?
- [ ] ¿Qué puede hacer la gente con este trabajo?
- [ ] ¿El problema es importante?

**Originalidad:**
- [ ] ¿Qué es específicamente nuevo aquí?
- [ ] ¿En qué se diferencia del trabajo relacionado más cercano?
- [ ] ¿La contribución es no trivial?
