# Resumen ejecutivo — IX.1.6

## Qué se pidió

Precisar la versión del corpus, resolver las contradicciones sobre su origen y revisar las respuestas de referencia, usando como evidencia el DOCX sin revisión, el ODT revisado por la abogada y el JSON generado por el autor.

## Qué se encontró

### 1. El corpus contiene texto posterior a 1997

El corpus indexado **no puede describirse como una copia del PDF de 1997**. Contiene, entre otras, las siguientes modificaciones:

- artículo 3: “wollastonita” (Ley 25.225/1999);
- artículo 31: redacción de la Ley 27.111/2015;
- artículos 215 y 221: actualizaciones de la Resolución 90/2023 y la Ley 27.701/2022;
- artículos 351 y 355: redacciones distintas de las que aparecen en el OCR largo.

El HTML de Infoleg conserva las notas de esas modificaciones y coincide con el corpus en los artículos verificados. La conclusión defendible es:

> **PDF de 1997 como texto base + HTML actualizado de Infoleg para las modificaciones + OCR parcial como insumo histórico.**

La afirmación de que “las estrategias basadas en Infoleg se descartaron” es incompleta: se descartaron como pipeline automático, pero el texto actualizado quedó incorporado. El autor debe confirmar si fue manual o mediante un parser.

### 2. Los conteos deben corregirse

| Dato | Valor verificado |
| --- | ---: |
| Nodos estructurales | 482 |
| Nodos artículo | 398 |
| Cuerpo principal | 347 (1–347) |
| Disposiciones generales y transitorias | 15 (348–362) |
| Apéndice | 36 (1–36) |
| Números únicos | 362 |
| Nodos artículo con texto | 397 |
| Artículo vacío | 239 (derogado) |

El manuscrito dice “399 artículos” en metodología y “245 artículos” en el capítulo 3. La tabla de 398 es correcta como nodos, pero debe explicar la duplicación del apéndice y el artículo 239.

### 3. Las fechas del benchmark son incorrectas o no están sustentadas

- Sanción: **1886-11-25**, no 1994-01-01.
- Publicación original: Registro Nacional 1885/86, p. 578; texto ordenado: **B.O. 1997-05-30**.
- `1994-01-10` no está verificado.
- `2024-12-09` no está verificado; el HTML local contiene notas hasta 2023.

### 4. La revisión de la abogada está registrada, pero no es una validación cerrada

El ODT contiene **166 regiones de cambio**, **130 con texto** y **80 párrafos con diferencias**. Incluye comentarios, nombres, lugares, cambios de terminología, correcciones de redacción y decisiones de alcance. No todos los comentarios fueron incorporados al JSON.

El autor aplicó algunas decisiones que no están registradas como cambios rastreados (San Juan, Chubut, Tierra del Fuego, Jujuy). No hay evidencia de una segunda revisión independiente. Por tanto, el manuscrito debe decir **“revisión por una profesional”**, no “validación final” ni “revisión por segunda vez”, salvo que se documente.

### 5. Respuestas de referencia que requieren corrección

| Unidad | Hallazgo | Acción |
| --- | --- | --- |
| Q1.1 | “Artículo 2, inciso 1”: el artículo 2 usa categorías, no incisos. | “Artículo 2, categoría 1ª (numeral 1°)” |
| Q1.2 | El anexo Typst atribuye al artículo 8 la separación de la propiedad; el artículo 8 se refiere a la facultad de buscar minas. | Usar art. 11 para propiedad distinta; 7 y 10 para dominio/concesión; 18 para “tiempo ilimitado”. |
| Q1.3 | La respuesta dice “seguridad pública, salud o conservación ambiental”; el art. 17 dice “seguridad pública, conservación de las pertenencias y salud o existencia de los trabajadores”. | Reproducir el art. 17 o reformular la pregunta; revisión jurídica. |
| Q13.2 | La respuesta cita 235, 236, 237, 240, 241 y 243; las referencias solo incluyen 243. | Agregar las referencias usadas. |
| Q13.3 | La respuesta cita 264 y 265 además de 245; las referencias solo incluyen 245. | Agregar 264/265 o justificar. |
| Q22.1 | Declara el artículo 353, pero la respuesta solo cita el 45. | Verificar Q22.2 o ampliar la respuesta. |
| Q23 | Río Turbio involucra un régimen especial no explicitado. La revisora pidió separar el caso combinado, no eliminar Q23; el caso que propuso eliminar es el de hidrocarburos. | Revisar alcance de Q23 (mantener, rotular o mover a anexo). |
| Q24 | La Ley 24.585 se menciona sin explicar su tema. | Aclarar que es la ley de protección ambiental minera o mover a anexo. |
| Q25 | La respuesta cita el art. 76, pero las referencias solo incluyen el 351. | Agregar el 76 y verificar la versión vigente en 2025. |

## Qué se entrega

- **`propuesta_edicion_manuscrito.md`**: texto actual y propuesto para los `.typ` y README.
- **`hallazgos_respuestas_referencia.md`**: auditoría detallada con textos del corpus.
- **`salidas/decisiones_revision.md`**: 30 decisiones de la revisión, con estado en el JSON.
- **`salidas/parrafos_revisados.md`**: los 80 párrafos antes/después.
- **`salidas/corpus_vs_fuentes.csv`**: comparación con HTML y OCR.
- **`salidas/propuestas_benchmark.csv`**: 12 cambios para una versión v2 del benchmark.
- **`salidas/referencias_benchmark.csv`** y **`unidades_benchmark.csv`**: auditoría de las 166 referencias y 79 unidades.

## Qué necesito de ti

1. Confirmar si el texto actualizado de Infoleg se incorporó manualmente o con un parser.
2. Decidir Q23 (Río Turbio): mantener, rotular como régimen especial o mover a anexo. La revisora no pidió eliminarlo.
3. Decidir Q24 (Ley 24.585): aclarar o mover a anexo.
4. Confirmar con la abogada la paráfrasis del artículo 17 (Q1.3).
5. Decidir si Q1.2 se corrige solo en el anexo o también en una versión v2 del benchmark con el artículo 18.
6. Confirmar si hubo una segunda revisión independiente; si no, ajustar el lenguaje del manuscrito.
