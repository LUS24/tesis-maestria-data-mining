# Auditoría del corpus y del benchmark

## Inspección

- Corpus: `data/codigo_de_mineria_actualizado_2025_08_02.json` — SHA-256 `b27e08ab32ae3e04f3499500f3a53fe8253d86d73c29d6c3216e351106b1b9fb`
- Benchmark: `data/evaluation_questions_v20250804_101435.json` — SHA-256 `a2645343dc8e97195b9d1914fae96f1e9477fe6e25f56883e638155805f58bd2`
- HTML de contraste: `codigo_experimentos/data/inputs/html/codigo_minero_43797.html` — SHA-256 `5c4f65b2a3f430c7d6bd491162f64c35eed27bdbf1cf6be51861b24dd2808d54`
- OCR corto: `codigo_experimentos/data/outputs/llm_img_to_md/texto_original_codigo_mineria.md` — SHA-256 `2401cb94f601af4cfec69e91267351e5e544232ab3bda618af79e34415e043c0`
- OCR largo: `codigo_experimentos/data/outputs/llm_img_to_md/output_codigo_mineria.md` — SHA-256 `ca6fb3c0a62b7492f225b54193c7575623bb6e06c0cc283f00b28ce670c9fb09`

## Corpus

- Nodos totales: **482**.
- Nodos artículo: **398**.
- Cuerpo: **347** artículos (1–347).
- Disposiciones generales y transitorias: **15** (348–362).
- Apéndice: **36** (1–36).
- Números únicos: **362**; duplicados cuerpo/apéndice: **36**.
- Artículos vacíos: **1** (artículo 239, derogado).

### Metadatos

| Campo | Valor en JSON | Valor verificado | Estado |
| --- | --- | --- | --- |
| `fecha_sancion` | `1994-01-01` | 1886-11-25 | **incorrecto** |
| `fecha_promulgacion` | `1994-01-10` | no verificado / no usar sin fuente | **no sustentado** |
| `fecha_publicacion` | `1994-01-15` | Registro Nacional 1885/86, p. 578; texto ordenado: B.O. 1997-05-30 | **incorrecto** |
| `fecha_ultima_actualizacion` | `2024-12-09` | no verificada en las fuentes locales; el HTML contiene notas hasta 2023 | **no verificada** |
| `conteo_articulos` | `398 nodos tipo artículo` | 347 cuerpo + 15 disposiciones (348-362) + 36 apéndice = 398 | **aclarar: 398 nodos, 362 numeros únicos** |
| `articulo_239` | `texto vacío` | derogado por Ley 26.909 (B.O. 2013-12-05), según HTML | **consistente pero debe explicarse** |

**Conclusión de linaje:** el corpus no es una copia literal del PDF/OCR de 1997. Contiene texto posterior a 1997 y coincide con el HTML actualizado de Infoleg en los artículos verificados. El PDF y el OCR sirven como fuente histórica parcial, pero no explican por sí solos el texto indexado. La afirmación del manuscrito de que las estrategias basadas en Infoleg “se descartaron” no describe el artefacto final.

### Artículos clave: comparación de fuentes

| Art. | Corpus | HTML actual | OCR 1997 corto | OCR largo | Observación |
| ---: | ---: | ---: | ---: | ---: | --- |
| 3 | 508 car. | 571 car. | 476 car. | 480 car. | Corpus incluye 'wollastonita' y no incluye 'talio'; el OCR de 1997 no incluye 'wollastonita'. HTML contiene nota de sustitución por Ley 25.225/1999. |
| 8 | 156 car. | 156 car. | 156 car. | 160 car. |  |
| 11 | 194 car. | 194 car. | 194 car. | 194 car. |  |
| 17 | 193 car. | 193 car. | 193 car. | 293 car. |  |
| 31 | 2391 car. | 2857 car. | 0 car. | 163 car. | Corpus coincide con el artículo 31 actual del HTML (20.000/40.000 km2; 120 días); el OCR corto no llega al artículo 31 y el largo no contiene el artículo 31 del cuerpo. |
| 215 | 1367 car. | 2270 car. | 0 car. | 117 car. | Corpus contiene el texto actual con valores $1.900/$960; el OCR largo contiene una versión incompatible (porcentajes y remisiones distintas). |
| 221 | 691 car. | 1097 car. | 0 car. | 0 car. | Corpus contiene el texto actual con $960/$4.800 y nota de Ley 27.701/2022; el OCR largo no contiene el artículo 221. |
| 239 | 0 car. | 66 car. | 0 car. | 350 car. | Corpus lo marca derogado y deja texto vacío; HTML conserva la nota de derogación por Ley 26.909/2013. |
| 351 | 441 car. | 440 car. | 0 car. | 156 car. | Corpus contiene la redacción actual (multiplicador 10/5/2); el OCR largo contiene una redacción anterior ('duplicando... cánones suspendidos'). |
| 355 | 267 car. | 267 car. | 0 car. | 41 car. | Corpus contiene la redacción actual sobre informe de impacto ambiental; el OCR largo contiene una redacción anterior sobre cánones. |

## Benchmark

- Casos: **25** (22 con subpreguntas y 3 de unidad única).
- Unidades: **79**.
- Referencias: **166**; únicas por número: **143**.
- Referencias con alerta sustantiva: **1**. Las referencias a números 1–36 se marcan como ambiguas por la duplicación cuerpo/apéndice, pero se resuelven al cuerpo como fuente principal.

### Referencias con alerta

| Unidad | Referencia | Estado | Ambigüedad | Detalle |
| --- | --- | --- | --- | --- |
| Q1.1 | Artículo 2, inciso 1 | ok | sí | artículo 2 usa categorías/numerales, no incisos |

### Unidades con alertas de referencias o citas

| Unidad | Referencias | Citas en la respuesta | Alertas |
| --- | --- | --- | --- |
| Q1.1 | Artículo 2, inciso 1, Artículo 3, inciso a | 3, 2 | La referencia 'Artículo 2, inciso 1' usa 'inciso'; el artículo 2 divide en categorías, no en incisos. |
| Q1.2 | Artículo 7, Artículo 10, Artículo 11 | 7, 10, 11 | El anexo Typst cita art. 8 para la separación de propiedad; la respuesta JSON y el corpus sostienen arts. 7, 10 y 11. Ver propuesta §3.1. |
| Q1.3 | Artículo 8, Artículo 13, Artículo 17 | 8, 13, 17 | La respuesta parafrasea el art. 17 como 'seguridad pública, salud o conservación ambiental'; el texto dice 'seguridad pública, conservación de las pertenencias y salud o existencia de los trabajadores'. Ver propuesta §3.2. |
| Q13.2 | Artículo 243 | 243, 236, 237, 235, 241, 240 | La respuesta cita 235, 236, 237, 240, 241 y 243; la lista de referencias solo incluye 243. |
| Q13.3 | Artículo 245 | 245, 265, 264 | La respuesta cita 264 y 265 además de 245; la lista de referencias solo incluye 245. |
| Q22.1 | Artículo 45, Artículo 353 | 45 | La unidad declara el artículo 353, pero la respuesta solo cita el 45; verificar si 353 corresponde a Q22.2. |
| Q23.0 | Artículo 348, Artículo 349 | 348, 349 | Caso de Río Turbio con régimen especial no explicitado. La revisora no pidió eliminar Q23; el caso que propuso eliminar es el de hidrocarburos (Ley 17.319). |
| Q24.0 | Artículo 355 | 355 | La pregunta usa la Ley 24.585 sin explicar su tema; la profesional sugirió aclararlo. |
| Q25.0 | Artículo 351 | 76, 351 | La respuesta cita el artículo 76, pero la lista de referencias solo incluye el 351. |

### Cobertura de citas

Los detalles por unidad están en `unidades_benchmark.csv`; cada cita extraída está en `citas_respuestas.csv`. Las alertas automáticas son un punto de partida: no sustituyen la lectura jurídica de la respuesta.

## Trazabilidad

Las alertas de este informe son evidencia, no decisiones. Las decisiones locales están en `resumen_ejecutivo.md`; los textos propuestos, en `propuesta_edicion_manuscrito.md`.

- Q1.2 y Q1.3: ver `propuesta_edicion_manuscrito.md` §3.1 y §3.2.
- Fechas y conteos: ver `propuesta_edicion_manuscrito.md` §1.4 y §2.1.
- Q1.1, Q13, Q22 y Q23–Q25: fuera de alcance; ver `resumen_ejecutivo.md` §5.

