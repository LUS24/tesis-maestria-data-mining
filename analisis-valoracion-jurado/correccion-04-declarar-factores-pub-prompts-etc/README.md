# Corrección IX.1.4 — Factores confundidos, prompts y contradicciones

Carpeta de revisión para resolver el punto **IX.1.4** del plan de correcciones. Todo el material es nuevo; no se editó ningún archivo existente del manuscrito, del repositorio de experimentos ni de los logs.

## Qué revisar primero

1. **`01_informe_auditoria.md`**: hallazgos verificados y evidencia.
2. **`propuestas/cambios_manuscrito.md`**: texto anterior y reemplazo propuesto para cada sección.
3. **`propuestas/anexo_02_prompts_y_parametros.typ`**: anexo con prompts literales, hashes y configuración observada.
4. **`propuestas/diagrama_agentic_rag_operativo.svg`**: diagrama coherente con los dos agentes activos y los límites 6/7.
5. **`04_checklist_aceptacion.md`**: criterios que deben cumplirse antes de cerrar el punto.

## Hallazgos que cambian la redacción

- El **Agente de Calidad** se excluyó por **costo y complejidad**, como confirmó el autor. No existe una comparación empírica que permita decir que “no produjo mejoras”.
- El **Agente de Calidad** tiene **0 logs y 0 llamadas**. Su prompt se incluye en el anexo, pero nunca se envió a un modelo.
- El **Agente Especialista Legal** tiene una única variante de prompt en 237 sesiones. El texto del manuscrito es una paráfrasis; el anexo reproduce el texto canónico.
- El **Agente de Recuperación** tuvo dos variantes:
  - gpt-5: límite **7**, 79 sesiones, 12 de noviembre de 2025;
  - gpt-5-mini y gpt-5-nano: límite **6**, 158 sesiones, 13 de noviembre de 2025.
- En gpt-5, **33/79 sesiones** usaron las siete búsquedas. En mini y nano, ninguna superó seis.
- El especialista registró una llamada en **236/237** sesiones. La sesión `16_01` de gpt-5 registró **tres**.
- El notebook de `part_g` conserva una versión anterior con `evaluate_retrieval` activo y prompts distintos. El script `.py` y los logs son la fuente canónica de la corrida final.
- El capítulo 3 atribuye al sistema few-shot y Chain-of-Thought; los prompts no contienen ni ejemplos ni una instrucción explícita de razonamiento paso a paso.

## Contenido

```
.
├── 01_informe_auditoria.md
├── 02_auditoria_prompts_y_configuracion.py
├── 03_resolucion_contradicciones.md
├── 04_checklist_aceptacion.md
├── README.md
├── propuestas/
│   ├── anexo_02_prompts_y_parametros.typ
│   ├── cambios_manuscrito.md
│   ├── diagrama_agentic_rag_operativo.mmd
│   ├── diagrama_agentic_rag_operativo.svg
│   └── tabla_factores_confundidos.typ
├── salidas/
│   ├── configuracion_observada.csv
│   ├── diff_prompts_script_vs_notebook.diff
│   ├── evidencia_codigo.md
│   ├── hashes_fuentes.json
│   ├── inventario_prompts.csv
│   ├── prompts_canonicos.json
│   ├── resumen_auditoria.json
│   ├── sesiones_agentic.csv
│   └── variantes_prompts_agente.csv
└── validacion/
    ├── preview_anexo.pdf
    ├── preview_anexo.typ
    ├── preview_tabla.pdf
    └── preview_tabla.typ
```

## Reproducción

Desde `codigo_experimentos/`:

```bash
uv run --no-sync --frozen python \
  ../analisis-valoracion-jurado/correccion-04-declarar-factores-pub-prompts-etc/02_auditoria_prompts_y_configuracion.py
```

El script:

- lee el script final, los notebooks y los 237 logs;
- reconstruye los prompts y sus hashes;
- verifica los 27 reportes de jueces;
- escribe solo en `salidas/` y regenera `propuestas/anexo_02_prompts_y_parametros.typ`;
- no modifica fuentes ni logs.

## Validación

Los PDF de `validacion/` se generaron con:

```bash
typst compile --root . validacion/preview_anexo.typ validacion/preview_anexo.pdf
typst compile --root . validacion/preview_tabla.typ validacion/preview_tabla.pdf
```

Ambos compilan. El anexo ocupa cinco páginas en la previsualización.

## Decisiones pendientes antes de editar el manuscrito

1. Declarar la asimetría 7/6 o repetir la corrida de gpt-5 con límite 6.
2. Aceptar la mención de la excepción `16_01`.
3. Aceptar el reemplazo de la explicación del Agente de Calidad por costo y complejidad.
4. Decidir si se usa el SVG nuevo o solo se corrige el epígrafe del existente.
5. Actualizar el notebook de `part_g` o marcarlo como exploratorio.

Ninguna de estas decisiones se tomó por el autor en este paquete; quedan explícitas en `04_checklist_aceptacion.md`.
