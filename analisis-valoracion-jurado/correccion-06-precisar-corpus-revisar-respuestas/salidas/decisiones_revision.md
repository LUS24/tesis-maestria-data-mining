# Intervenciones de la revisión y estado en el JSON

Esta tabla separa lo que la profesional propuso, lo que el autor incorporó al JSON y lo que quedó sin aplicar. **No son decisiones de la tesis**: las decisiones locales están en `resumen_ejecutivo.md` y el registro global en `../DECISIONES_integradas.md`, Bloque D. No se modificó ningún archivo fuente.

| ID | Caso | Propuesta / cambio | Estado en el JSON |
| --- | --- | --- | --- |
| R01 | Instrucción general | Reemplazar 'abogado experto en código minero' por 'experto/a en Derecho Minero', con mirada de género y especialización focalizada en el Código de Minería. | no evaluable en benchmark; afecta el prompt de generación |
| R02 | Instrucción general | Unificar 'Código de Minería' y 'Código Minero'. | aplicado en el JSON |
| R03 | Instrucción general | Añadir 'ante situaciones concretas' para precisar el alcance de las preguntas. | no verificable en el benchmark |
| R04 | Q1 | Corregir '1&' a '1' en la cita del art. 2. | aplicado (el JSON no contiene '1&') |
| R05 | Q1 | Añadir 'Ing.' al nombre de Juan Pérez en la respuesta 1.2. | aplicado |
| R06 | Q2 | Nombrar a Laura Álvarez, Raúl Juárez y Oscar Castro. | aplicado con variantes de acentuación |
| R07 | Q2 | Aclarar que la normativa aplicable es el Código de Minería Argentino. | aplicado en la introducción del caso |
| R08 | Q2 | Reemplazar 'ningún derecho' por 'derecho alguno'. | aplicado |
| R09 | Q3 | Reemplazar 'provincia X' por una provincia concreta (el autor usa San Juan). | aplicado por el autor fuera del control de cambios |
| R10 | Q4 | Nombrar al abogado Jorge Ramírez y corregir 'criaderode'. | aplicado |
| R11 | Q5 | Sustituir 'normas' por 'disposiciones del Código Minero' y pedir fundamento normativo. | aplicado solo parcialmente; la pregunta del JSON quedó reducida a la extensión |
| R12 | Q6 | Localizar la provincia (el autor usa Chubut) y aceptar 'obligación/obligaciones'. | aplicado por el autor; Chubut no está en el ODT final |
| R13 | Q9 | Localizar la provincia (el autor usa Tierra del Fuego). | aplicado por el autor; el ODT final deja '…...' |
| R14 | Q10 | Nombrar a Don Ricardo Ojeda. | aplicado |
| R15 | Q14 | Localizar la provincia (el autor usa Jujuy). | aplicado por el autor; el ODT final deja '…..' |
| R16 | Q16 | Nombrar a Martina Truman y Jorge Speed. | aplicado |
| R17 | Q17 | Nombrar a Adrián López. | aplicado |
| R18 | Q18 | Nombrar a Joaquín Gómez y Ofelia Maldonado; aclarar el articulado del Título XVIII. | aplicado |
| R19 | Q19 | Localizar la provincia de Santa Cruz. | aplicado |
| R20 | Q20 | Nombrar a Ana López. | aplicado |
| R21 | Q21 | Aclarar 'empresa estatal provincial'. | aplicado |
| R22 | Q22–Q25 | El caso final combinaba varios clientes; la profesional sugirió abrirlo en tres casos individuales. El autor generó cuatro unidades (Q22–Q25), no tres. | aplicado con una diferencia: 4 unidades en lugar de 3 |
| R23 | Q22 | Nombrar a Rodrigo Asís. | aplicado |
| R24 | Q23 | La profesional no recomendó eliminar Q23: pidió separar el caso final combinado. Q23 (Río Turbio) no explicita si el régimen aplicable se agota en el Código o requiere legislación especial. | Q23 se mantiene en el JSON; su alcance no se reabre en esta tesis |
| R25 | Q24 | Aclarar genéricamente el tema de la Ley 24.585. | no aplicado; la pregunta se mantiene como fue revisada |
| R26 | Q25 | Añadir temporalidad al régimen de litio. | parcial; la pregunta se mantiene como fue revisada |
| R27 | Caso adicional | Omitir el caso de hidrocarburos añadido al final del ODT; la profesional lo consideró fuera del alcance. | aparente omisión; no se reabre en esta tesis |
| R28 | Q1.2 (anexo) | El anexo Typst atribuye a 'art. 8' la separación de la propiedad minera; la respuesta JSON y el corpus usan arts. 7, 10 y 11. | error solo en el anexo; la respuesta JSON es correcta |
| R29 | Q1.3 | La respuesta parafrasea el art. 17 como 'seguridad pública, salud o conservación ambiental'. | error en JSON y anexo; el corpus es correcto |
| R30 | Q1.1 | La referencia 'Artículo 2, inciso 1' no es técnicamente correcta: el artículo 2 divide en categorías, no en incisos. | etiqueta 'inciso' en el benchmark; fuera de alcance |

## Observaciones

- Los cambios rastreados del ODT incluyen comentarios editoriales y fragmentos de edición; no todos son texto aprobado del benchmark. La tabla anterior es la lectura curada.
- El autor aplicó varias elecciones que no quedaron registradas como cambios rastreados (por ejemplo, provincia de San Juan, Chubut, Tierra del Fuego y Jujuy). Esas elecciones deben confirmarse antes de tomarlas como parte de la revisión de la profesional.
- La profesional pidió separar el caso final combinado y omitió el caso de hidrocarburos por la Ley 17.319. No recomendó eliminar Q23 (Río Turbio). El JSON conserva Q23 y Q24 y omite el caso de hidrocarburos; esta tabla no reabre esas preguntas (ver `resumen_ejecutivo.md` §5).
