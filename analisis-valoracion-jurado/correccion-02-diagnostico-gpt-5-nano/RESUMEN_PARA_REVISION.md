# Resumen para revisión rápida — IX.1.2

**Qué revisar primero:** `INFORME_DIAGNOSTICO.md` y `PROPUESTAS_MANUSCRITO.md`.  
**Evidencia principal:** `salidas/14_dataset_categoria_final.csv`, `salidas/11_celda_nano_agentic_79.csv`, `salidas/04_auditoria_faltantes_join.csv`, `salidas/17_auditoria_jueces_salidas_no_sustantivas_final.csv` y `diagnostico_gpt5_nano.ipynb`.

## Cinco hallazgos

1. **Las 27 medias ausentes son un join, no 27 fallos.** Son las unidades 23–25 × 9 configuraciones. En métricas la subpregunta está vacía; en jueces vale `0`. Se recuperan 711 observaciones y 2.133 evaluaciones.
2. **Agentic-RAG + gpt-5-nano tiene 41/79 salidas no sustantivas:** 27 vacías, 1 solo espacios, 2 abstenciones, 1 truncada y 10 indeterminadas. Tasa 51,9% (IC 95% 41,1–62,6%).
3. **No es falta de recuperación ni truncamiento.** Los 79 logs tienen `retrieve_relevant_documents` y al menos un `final_result`; el `finish_reason` es `tool_call` en los 79. Las salidas vacías tienen 1–12 documentos y 575–7.015 tokens de salida. El `response_text` del `final_result` es vacío o un marcador.
4. **Cuando responde, la calidad es alta.** 38 respuestas sustantivas: media 0,820 y mediana 0,958. Con fallo = 0 la celda completa tiene mediana 0,000; con exclusión, 0,958. La diferencia con RAG básico es −0,205 con fallo = 0 y +0,182 con exclusión (38 pares). La exclusión es una submuestra seleccionada.
5. **Los jueces no miden bien las salidas no sustantivas.** Hay 12 filas de corrección > 0 (10 combinaciones celda-unidad; 9 unidades distintas) y 5 filas de precisión legal > 0 en las 58 salidas no sustantivas finales. Algunas justificaciones citan artículos que no están en la respuesta. No deben promediarse como calidad.

## Qué cambia en el manuscrito

- Reemplazar “27 observaciones eliminadas por fallos de generación” por la explicación del join.
- Reemplazar “sobrecarga agéntica” por “modo de fallo de respuesta” y separar resultado a nivel sistema de calidad condicional a respuesta sustantiva.
- Actualizar las medianas: la tabla actual se calculó sobre 76 filas; cambian 5 de 9 celdas. Sin RAG + mini queda 64/15 y su mediana condicional es 0,375.
- Añadir la tabla de categorías final y la nota sobre jueces.
- Ajustar el ejemplo del anexo: es una de las 38 respuestas sustantivas, no representa las 41 no sustantivas.
- No afirmar causalidad por “complejidad agéntica” sin réplicas/ablación.

## Qué queda pendiente

- La revisión manual ya fue aceptada y consolidada en `salidas/14_dataset_categoria_final.csv`. No hace falta volver a revisar.
- Proceder con el reanálisis IX.1.1 usando esa base final.
- Confirmar las decisiones editoriales después de IX.1.1 antes de editar la tabla de medianas y las conclusiones.

## Cómo reproducir

```bash
bash analisis-valoracion-jurado/correccion-02-diagnostico-gpt-5-nano/reproducir.sh
```

El script no modifica los archivos fuente: regenera la base automática y luego consolida la revisión aceptada en `14_dataset_categoria_final.csv` y `figuras_final/`. El notebook ya está ejecutado sin errores.
