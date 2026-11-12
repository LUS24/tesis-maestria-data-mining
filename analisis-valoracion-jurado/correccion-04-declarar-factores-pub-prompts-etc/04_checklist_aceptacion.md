# Checklist de aceptación de IX.1.4

## Auditoría y artefactos

- [x] Se identificaron 237 sesiones agénticas y 27 reportes de jueces.
- [x] Se extrajo una única variante del prompt del Agente Especialista Legal.
- [x] Se extrajeron las dos variantes del prompt del Agente de Recuperación.
- [x] Se verificó que el Agente de Calidad tiene cero logs y cero llamadas.
- [x] Se identificó la razón confirmada de exclusión: costo y complejidad.
- [x] Se identificó la diferencia histórica de límite 7 (gpt-5) frente a 6 (mini/nano).
- [x] Se identificó la sesión `16_01` con tres llamadas del especialista.
- [x] Se reconstruyeron los prompts de los jueces con `pydantic-evals` 1.1.0.
- [x] Se calcularon hashes SHA-256 de todos los prompts.
- [x] Se generó el anexo `anexo_02_prompts_y_parametros.typ`.
- [x] El anexo compila en `validacion/preview_anexo.pdf`.
- [x] La tabla de factores confundidos compila en `validacion/preview_tabla.pdf`.
- [x] Se generó y renderizó el diagrama operativo en SVG.
- [x] No se modificó ningún archivo fuente, log, JSON, CSV o notebook existente.

## Decisiones del autor antes de editar el manuscrito

- [ ] Aceptar que se declare la asimetría 7/6 entre gpt-5 y mini/nano.
- [ ] Decidir si se repite la corrida de gpt-5 con límite 6 o se mantiene la asimetría declarada.
- [ ] Aceptar que se documente la excepción `16_01`.
- [ ] Aceptar el texto propuesto para el Agente de Calidad (costo y complejidad; sin afirmación de mejoras).
- [ ] Decidir si se reemplaza el diagrama o solo su epígrafe.
- [ ] Decidir si se actualiza el notebook de agentes o se marca como exploratorio.
- [ ] Confirmar el título y el alcance reales; no forma parte de este paquete salvo la referencia del README.

## Edición del manuscrito

- [ ] Insertar el texto de arquitectura general.
- [ ] Reemplazar la sección del Agente Especialista Legal.
- [ ] Reemplazar la sección del Agente de Recuperación.
- [ ] Reemplazar la sección del Agente de Calidad.
- [ ] Reemplazar la sección de orquestación.
- [ ] Insertar la subsección de alcance y factores confundidos.
- [ ] Reemplazar la tabla de hiperparámetros y el párrafo del límite.
- [ ] Corregir el capítulo 3 (few-shot/CoT y cierre de síntesis).
- [ ] Corregir el objetivo 2 en conclusiones.
- [ ] Actualizar el epígrafe o la imagen del diagrama.
- [ ] Agregar `#include "capitulos/anexo_02_prompts_y_parametros.typ"` en `main.typ`.
- [ ] Actualizar `README.md` y `performed_tasks_summary.md`.
- [ ] Actualizar o marcar como exploratorio el notebook de `part_g`.

## Verificación final

- [ ] Compilar con `make pdf` sin errores.
- [ ] Verificar que `@anexo-prompts` resuelve y que la numeración de anexos es correcta.
- [ ] Buscar en el PDF: “no se tradujo en mejoras marginales significativas”.
- [ ] Buscar en el PDF: “puede solicitar búsquedas adicionales”.
- [ ] Buscar en el PDF: “few-shot prompting para fijar el formato”.
- [ ] Buscar en el PDF: “Chain-of-Thought para inducir razonamiento”.
- [ ] Buscar en el PDF: “seis búsquedas” sin la aclaración 7/6.
- [ ] Confirmar que la tabla de hiperparámetros no afirma determinismo por temperatura (IX.1.3).
- [ ] Confirmar que los prompts del anexo y el script final describen la misma configuración, salvo la variante histórica declarada.
- [ ] Confirmar que el repositorio público conserva los logs y el anexo final.

## Comando de reproducción

Desde `codigo_experimentos/`:

```bash
uv run --no-sync --frozen python \
  ../analisis-valoracion-jurado/correccion-04-declarar-factores-pub-prompts-etc/02_auditoria_prompts_y_configuracion.py
```

El script solo escribe dentro de esta carpeta de corrección. Comparar los hashes de `salidas/hashes_fuentes.json` antes y después de cualquier revisión.
