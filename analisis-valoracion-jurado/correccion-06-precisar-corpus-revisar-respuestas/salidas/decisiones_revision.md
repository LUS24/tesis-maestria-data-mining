# Decisiones de la revisión de la abogada

Esta tabla separa lo que la abogada propuso, lo que el autor incorporó al JSON y lo que sigue pendiente. No se modificó ningún archivo fuente.

| ID | Caso | Propuesta / cambio | Estado en el JSON | Acción propuesta |
| --- | --- | --- | --- | --- |
| R01 | Instrucción general | Reemplazar 'abogado experto en código minero' por 'experto/a en Derecho Minero', con mirada de género y especialización focalizada en el Código de Minería. | no evaluable en benchmark; afecta el prompt de generación | Si se regenera el benchmark, actualizar el prompt; no cambiar el texto del benchmark actual. |
| R02 | Instrucción general | Unificar 'Código de Minería' y 'Código Minero'. | aplicado en el JSON | Mantener 'Código de Minería' en manuscrito, anexo y futuras regeneraciones. |
| R03 | Instrucción general | Añadir 'ante situaciones concretas' para precisar el alcance de las preguntas. | no verificable en el benchmark | Documentar la decisión si se publica el prompt; no afecta la redacción del benchmark actual. |
| R04 | Q1 | Corregir '1&' a '1' en la cita del art. 2. | aplicado (el JSON no contiene '1&') | Corregir además la etiqueta 'inciso' por 'categoría/numeral 1°'. |
| R05 | Q1 | Añadir 'Ing.' al nombre de Juan Pérez en la respuesta 1.2. | aplicado | Mantener. |
| R06 | Q2 | Nombrar a Laura Álvarez, Raúl Juárez y Oscar Castro. | aplicado con variantes de acentuación | Mantener; unificar la tilde de Álvarez. |
| R07 | Q2 | Aclarar que la normativa aplicable es el Código de Minería Argentino. | aplicado en la introducción del caso | Mantener; revisar que la subpregunta 2.3 no deje 'normativa mencionada' como referencia vaga. |
| R08 | Q2 | Reemplazar 'ningún derecho' por 'derecho alguno'. | aplicado | Mantener. |
| R09 | Q3 | Reemplazar 'provincia X' por una provincia concreta (el autor usa San Juan). | aplicado por el autor fuera del control de cambios | Confirmar que San Juan es la jurisdicción elegida y que no altera el caso. |
| R10 | Q4 | Nombrar al abogado Jorge Ramírez y corregir 'criaderode'. | aplicado | Mantener; el comentario 'OJO cambiaste el estilo' es editorial. |
| R11 | Q5 | Sustituir 'normas' por 'disposiciones del Código Minero' y pedir fundamento normativo. | aplicado solo parcialmente; la pregunta del JSON quedó reducida a la extensión | Restaurar una fórmula como '¿Cuál es la extensión... y en base a qué disposiciones del Código de Minería?'. |
| R12 | Q6 | Localizar la provincia (el autor usa Chubut) y aceptar 'obligación/obligaciones'. | aplicado por el autor; Chubut no está en el ODT final | Confirmar Chubut; mantener la alternativa gramatical. |
| R13 | Q9 | Localizar la provincia (el autor usa Tierra del Fuego). | aplicado por el autor; el ODT final deja '…...' | Confirmar la jurisdicción. |
| R14 | Q10 | Nombrar a Don Ricardo Ojeda. | aplicado | Mantener. |
| R15 | Q14 | Localizar la provincia (el autor usa Jujuy). | aplicado por el autor; el ODT final deja '…..' | Confirmar la jurisdicción. |
| R16 | Q16 | Nombrar a Martina Truman y Jorge Speed. | aplicado | Mantener. |
| R17 | Q17 | Nombrar a Adrián López. | aplicado | Mantener; corregir el espacio doble en la respuesta 17.2 si se edita el benchmark. |
| R18 | Q18 | Nombrar a Joaquín Gómez y Ofelia Maldonado; aclarar el articulado del Título XVIII. | aplicado | Mantener; unificar 'Joaquín' y 'Joaquin'. |
| R19 | Q19 | Localizar la provincia de Santa Cruz. | aplicado | Mantener. |
| R20 | Q20 | Nombrar a Ana López. | aplicado | Mantener. |
| R21 | Q21 | Aclarar 'empresa estatal provincial'. | aplicado | Mantener. |
| R22 | Q22–Q25 | El caso final combinaba varios clientes; la abogada sugirió abrirlo en tres casos individuales. El autor generó cuatro unidades (Q22–Q25), no tres. | aplicado con una diferencia: 4 unidades en lugar de 3 | Mantener y documentar la separación; explicar por qué se generaron cuatro y no tres. |
| R23 | Q22 | Nombrar a Rodrigo Asís. | aplicado | Mantener. |
| R24 | Q23 | La abogada no recomendó eliminar Q23: pidió separar el caso final combinado. Q23 (Río Turbio) no explicita si el régimen aplicable se agota en el Código o requiere legislación especial. | Q23 fue separado del caso combinado; su alcance sigue pendiente | No atribuir la eliminación a la revisora; decidir si Q23 se mantiene, se rotula como régimen especial o se mueve a anexo. |
| R25 | Q24 | Aclarar genéricamente el tema de la Ley 24.585. | no aplicado: la pregunta sigue mencionando la ley sin explicar su materia | Añadir 'ley de protección ambiental' o trasladar el caso a un anexo de legislación especial. |
| R26 | Q25 | Añadir temporalidad al régimen de litio. | parcial: el JSON pregunta 'al año 2025', pero no aclara la versión normativa | Verificar que el artículo 351 citado sea el vigente en 2025 y documentar la fecha de consulta. |
| R27 | Caso adicional | Omitir el caso de hidrocarburos añadido al final del ODT; la abogada lo consideró fuera del alcance. | aparente omisión: el JSON no contiene el caso de hidrocarburos, pero no puede probarse que la decisión se tomara después de la revisión | Confirmar que la omisión es deliberada y documentarla; el ODT conserva el borrador y no debe tomarse como benchmark final. |
| R28 | Q1.2 (anexo) | El anexo Typst atribuye a 'art. 8' la separación de la propiedad minera; la respuesta JSON y el corpus usan arts. 7, 10 y 11. | corregir el anexo, no la respuesta | Reemplazar la referencia del anexo por art. 11 (y, si se explican dominio y concesión, arts. 7 y 10). |
| R29 | Q1.3 | La respuesta parafrasea el art. 17 como 'seguridad pública, salud o conservación ambiental'. | revisar | Corregir la paráfrasis y revisar el alcance de 'solamente'. |
| R30 | Q1.1 | La referencia 'Artículo 2, inciso 1' no es técnicamente correcta: el artículo 2 divide en categorías, no en incisos. | corregir etiqueta | Usar 'Artículo 2, categoría 1°' o 'numeral 1°' en el benchmark y en el anexo. |

## Observaciones

- Los cambios rastreados del ODT incluyen comentarios editoriales y fragmentos de edición; no todos son texto aprobado del benchmark. La tabla anterior es la lectura curada.
- El autor aplicó varias decisiones que no quedaron registradas como cambios rastreados (por ejemplo, provincia de San Juan, Chubut, Tierra del Fuego y Jujuy). Esas elecciones deben confirmarse antes de tomarlas como parte de la revisión de la abogada.
- La abogada pidió separar el caso final combinado y eliminó/omitió el caso de hidrocarburos por la Ley 17.319. No recomendó eliminar Q23 (Río Turbio). El JSON conserva Q23 y Q24 y omite el caso de hidrocarburos; las decisiones de alcance deben ser explícitas.
