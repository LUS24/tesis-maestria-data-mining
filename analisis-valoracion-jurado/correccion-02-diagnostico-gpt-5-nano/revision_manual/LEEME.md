# Revisión manual ciega — IX.1.2

Este paquete contiene 87 respuestas para revisar:

- las 57 salidas no sustantivas detectadas automáticamente;
- 30 respuestas sustantivas de control, estratificadas por celda.

El orden es aleatorio y **no** se indican estrategia, modelo ni categoría automática. No abras `../salidas/mapa_revision_ciega.csv` hasta terminar: ese archivo contiene la respuesta correcta del clasificador y arruinaría el cegamiento.

## Qué se evalúa

**Solo la forma de la respuesta**, no su corrección jurídica. La pregunta es: ¿la respuesta contiene una respuesta sustantiva al caso, o es un fallo de respuesta?

No evalúes si la conclusión jurídica es correcta, si cita el artículo adecuado o si sería útil para un abogado. Eso corresponde a la validación con profesionales (IX.2.3).

## Categorías

Usa exactamente una de estas categorías en `categoria_revisada`:

| Categoría | Definición |
|---|---|
| `sustantiva` | Contiene una respuesta al caso, aunque sea jurídicamente incorrecta, incompleta o con errores. Puede incluir una advertencia o una limitación, pero debe haber una respuesta reconocible. |
| `vacia` | Cadena vacía. |
| `solo_espacios` | Solo espacios, tabulaciones o saltos de línea. |
| `abstencion_explicita` | El modelo declara que no puede responder o que no tiene información suficiente, y no ofrece una respuesta sustantiva. |
| `error_explicito` | Error técnico, excepción, timeout, rate limit, error de API o HTTP. |
| `truncada` | Salida incompleta: JSON que empieza y no termina, frase cortada, marcador de truncamiento. |
| `indeterminada` | Marcador de prueba (`TEST`, `placeholder`, `PENDING`), mensaje de proceso (“espera”, “voy a consultar”, “se procede”), mensaje interno (“preliminar”) o texto que no se puede clasificar. |

### Casos dudosos

- Una respuesta que empieza con “No dispongo del texto…” pero después desarrolla un análisis jurídico: `sustantiva` si hay una respuesta reconocible; `abstencion_explicita` si solo se limita a decir que no puede.
- Una respuesta que empieza con “A continuación se resumen…” y luego responde: `sustantiva`.
- Una respuesta que solo dice “A continuación se resumen…” y no sigue: `truncada` o `indeterminada` según la evidencia.
- Un mensaje que solo anuncia una acción (“Voy a consultar…”): `indeterminada`.
- Una respuesta con una respuesta correcta pero sin citas: `sustantiva`; la falta de citas no la convierte en no sustantiva.

Si dudas entre dos categorías, elige la que mejor describa la **forma** y explica la duda en `justificacion`.

## Cómo completar

1. Abre `paquete_revision_ciega.csv` en una planilla.
2. Abre `plantilla_resultados.csv`.
3. Para cada `review_id`, completa:
   - `categoria_revisada`: una de las siete categorías;
   - `justificacion`: una frase breve con la evidencia (por ejemplo, “cadena vacía”, “solo anuncia que consultará”, “respuesta completa con conclusión y citas”);
   - `revisor`: nombre o iniciales;
   - `fecha`: `AAAA-MM-DD`.
4. No cambies el orden ni los `review_id`.
5. Guarda la plantilla como CSV UTF-8.

## Validación

Desde la raíz del repositorio:

```bash
uv run --project codigo_experimentos --no-sync --frozen \
  python analisis-valoracion-jurado/correccion-02-diagnostico-gpt-5-nano/src/validar_revision_manual.py
```

El script:

- comprueba que estén todas las filas y que las categorías sean válidas;
- compara tu clasificación con la automática;
- genera `salidas/revision_manual_resumen.csv` y `salidas/revision_manual_discrepancias.csv`;
- no modifica la plantilla ni el paquete ciego.

Si hay discrepancias, revísalas antes de incorporar la conclusión al manuscrito. Las 27 cadenas vacías y la salida de solo espacios no deberían generar duda; los mensajes de proceso y las respuestas con limitaciones son los casos que más importan.
