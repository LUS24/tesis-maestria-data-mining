# Conteo de preguntas revisadas por la profesional

**Fuente:** `salidas/cambios_rastreados.csv` (cambios con texto del ODT).
**Método:** los 21 archivos de título anteriores a `título_final.md` se asignan en orden a Q1-Q21; el bloque final se asigna a Q22-Q25 por párrafo y contenido.

| Indicador | Valor |
| --- | ---: |
| Preguntas del benchmark | 25 |
| Preguntas con alguna intervención | 18 |
| Preguntas con cambio de contenido | 17 |
| Preguntas solo con comentario no aplicado | 1 |
| Preguntas sin intervención | 7 |
| Cambios con texto (fragmentos) | 130 |
| Comentarios generales del bloque final | 3 |
| Cambios del caso de hidrocarburos excluido | 4 |
| Cambios de instrucción/prompt general | 24 |
| Cambios no asignados | 0 |

## Detalle

| Q | Descripción | Intervenciones | Contenido | Comentarios | Estado |
| ---: | --- | ---: | ---: | ---: | --- |
| 1 | Q1.1-Q1.3 (litio) | 16 | 16 | 0 | corregida |
| 2 | Q2 (conflicto de interés) | 18 | 16 | 2 | corregida |
| 3 | Q3 (permiso de exploración) | 2 | 2 | 0 | corregida |
| 4 | Q4 (descubrimiento) | 10 | 5 | 5 | corregida |
| 5 | Q5 (pertenencias) | 5 | 3 | 2 | corregida |
| 6 | Q6 (servidumbres) | 6 | 4 | 2 | corregida |
| 7 | Q7 (grupo minero) | 0 | 0 | 0 | sin intervención |
| 8 | Q8 (servidumbres) | 0 | 0 | 0 | sin intervención |
| 9 | Q9 (turba) | 0 | 0 | 0 | sin intervención |
| 10 | Q10 (canteras) | 8 | 6 | 2 | corregida |
| 11 | Q11 (sociedades) | 5 | 1 | 4 | corregida |
| 12 | Q12 (caducidad) | 0 | 0 | 0 | sin intervención |
| 13 | Q13 (infracciones) | 0 | 0 | 0 | sin intervención |
| 14 | Q14 (avío) | 1 | 1 | 0 | corregida |
| 15 | Q15 (sociedad minera) | 0 | 0 | 0 | sin intervención |
| 16 | Q16 (matrimonio) | 6 | 6 | 0 | corregida |
| 17 | Q17 (litio Catamarca) | 2 | 2 | 0 | corregida |
| 18 | Q18 (Título XVIII) | 10 | 10 | 0 | corregida |
| 19 | Q19 (Santa Cruz) | 3 | 2 | 1 | corregida |
| 20 | Q20 (usufructo) | 0 | 0 | 0 | sin intervención |
| 21 | Q21 (zona de interés especial) | 1 | 1 | 0 | corregida |
| 22 | Q22 (manifestación de descubrimiento) | 1 | 0 | 1 | corregida (comentario aplicado) |
| 23 | Q23 (Río Turbio) | 3 | 2 | 1 | corregida |
| 24 | Q24 (Ley 24.585) | 1 | 0 | 1 | solo comentario / no aplicada |
| 25 | Q25 (litio 2025) | 1 | 1 | 0 | corregida |

## Lectura

- 18 de 25 preguntas fueron objeto de alguna intervención.
- 17 tienen un cambio de contenido identificable.
- 1 quedó solo con un comentario no aplicado (Q24).
- 7 no fueron intervenidas: Q7, Q8, Q9, Q12, Q13, Q15, Q20.

El conteo es una cota inferior: el ODT registra comentarios y cambios, pero no un campo de “aceptado/rechazado” por pregunta. Las decisiones del autor se verifican contra el JSON final en `decisiones_revision.csv`.
