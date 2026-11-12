# Resolución de contradicciones de IX.1.4

Este documento mapea cada acción de IX.1.4 con la evidencia y el artefacto listo para revisar. No afirma que el manuscrito ya esté corregido.

| Punto de IX.1.4 | Estado | Evidencia | Artefacto / acción propuesta |
| --- | --- | --- | --- |
| 1. Declarar factores confundidos | Resuelto como análisis; pendiente de inserción | 237 sesiones y 27 reportes auditados | `propuestas/tabla_factores_confundidos.typ` y sección 8 de `propuestas/cambios_manuscrito.md` |
| 2. Reproducir prompts literalmente y verificar variantes | Resuelto | Prompts del especialista: 1 variante; recuperador: 2 variantes; calidad: 0 ejecuciones; jueces: 27 reportes | `propuestas/anexo_02_prompts_y_parametros.typ`, `salidas/prompts_canonicos.json`, `salidas/sesiones_agentic.csv` |
| 3. Crear un anexo de prompts | Resuelto, compila | PDF de validación de 5 páginas | `propuestas/anexo_02_prompts_y_parametros.typ`; instrucción de inclusión en `main.typ` en `cambios_manuscrito.md` |
| 4. Excluir la afirmación de mejoras y conservar costo/complejidad | Resuelto con confirmación del autor | 0 logs y 0 llamadas al agente de calidad | Sección 4 de `cambios_manuscrito.md` |
| 5. Sustituir “búsquedas adicionales” por la configuración real | Resuelto, con excepción documentada | 236/237 sesiones con una llamada del especialista; `16_01` con tres | Secciones 2, 5 y 6 de `cambios_manuscrito.md` |
| 6. Corregir few-shot y Chain-of-Thought | Resuelto | Los prompts no contienen ejemplos ni instrucción de CoT | Sección 9 de `cambios_manuscrito.md` |
| 7. Definir operativamente Agentic-RAG | Resuelto | Dos agentes activos; una delegación; calidad inactiva | Sección 1 y sección 8 de `cambios_manuscrito.md` |
| 8. Objetivo 2 como cumplimiento parcial | Resuelto | Calidad no ejecutada y sin iteración del especialista | Sección 10 de `cambios_manuscrito.md` |

## Hallazgo adicional que debe decidirse antes de redactar

La corrida de gpt-5 usó el prompt `recuperador_system_7_gpt5` (límite 7, 79 sesiones, 12 de noviembre). Las corridas de gpt-5-mini y gpt-5-nano usaron `recuperador_system_6` (límite 6, 158 sesiones, 13 de noviembre). En gpt-5, 33/79 sesiones agotaron las siete búsquedas.

Esto agrega una amenaza específica al contraste por modelo. El texto propuesto la declara, pero el autor debe elegir una de estas dos líneas:

1. **Sin nueva corrida:** declarar la asimetría 7/6 y moderar la interpretación del efecto de modelo en Agentic-RAG.
2. **Con nueva corrida:** repetir únicamente la configuración Agentic-RAG + gpt-5 con el prompt de seis búsquedas, en un directorio nuevo, y actualizar los resultados y el anexo. Nunca sobrescribir `part_g/chat_data` ni los JSON históricos.

No se debe escribir “seis búsquedas” como propiedad uniforme sin elegir una de esas dos opciones.

## Segunda decisión: sesión 16_01

La sesión `16_01` de gpt-5 registra tres llamadas del especialista a `retrieve_relevant_documents`; las otras 236 registran una. El texto propuesto dice “límite nominal de una invocación; 236/237 sesiones lo respetan, con una excepción documentada”. Es preferible declararlo a omitirlo, porque el log está publicado y un lector puede reproducir el conteo.

## Tercera decisión: notebook de agentes

`part_g/01_generate_responses_using_agents.ipynb` no coincide con el script final: conserva un prompt con formato APA, un recuperador sin límite explícito y `evaluate_retrieval` activo. El script `.py` coincide con los logs. Para que la afirmación de reproducibilidad sea cierta, el notebook debe actualizarse o marcarse como exploratorio.

## Lo que no se puede afirmar

- No se puede afirmar que el Agente de Calidad mejoraba o empeoraba el sistema: nunca se ejecutó.
- No se puede afirmar que todas las configuraciones usaron seis búsquedas.
- No se puede afirmar que el especialista siempre hizo una única llamada.
- No se puede afirmar que el sistema implementa few-shot o Chain-of-Thought.
- No se puede atribuir el efecto de Agentic-RAG a la descomposición, a la selección o al prompt sin ablaciones.
- No se puede atribuir el efecto de modelo a la capacidad del modelo sin reconocer que gpt-5 tuvo un presupuesto de recuperación distinto.
