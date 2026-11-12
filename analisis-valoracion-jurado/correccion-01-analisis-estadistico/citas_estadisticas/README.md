# Citas estadísticas validadas — IX.1.1

Este directorio contiene las referencias propuestas para la guía de pruebas estadísticas y su validación.

## Archivos

| Archivo | Contenido |
|---|---|
| `inventario_citas_estadisticas.csv` | 19 entradas con clave, tipo, autores, año, título, venue, DOI/URL y uso |
| `citas_estadisticas.bib` | Entradas BibTeX propuestas para el manuscrito |
| `verificacion_citas_estadisticas.csv` | Metadatos devueltos por Crossref/URL y comparación con el inventario |
| `resumen_validacion_citas.json` | Conteo de estados y entradas no verificadas |
| `validar_citas.py` | Script reproducible de validación |
| `prueba_citas.typ` | Documento Typst que cita y compila las 19 entradas |
| `prueba_citas.pdf` | Resultado de la compilación de prueba |
| `cache/` | Respuestas crudas de Crossref/URL; no contiene credenciales |

## Método

Se reutiliza la lógica de `correccion-07-forma-y-bibliografia/verificar_fuentes.py`:

1. Para cada DOI, se consulta Crossref.
2. Se compara el título normalizado con similitud de secuencia.
3. Se compara el año y el primer autor.
4. Para las entradas sin DOI, se consulta la URL y se registra el estado HTTP.
5. Se guarda la respuesta original en `cache/` para reproducibilidad.

Resultado: **15 DOI verificados** y **4 URL que responden**. No hay entradas sin identificador. JSTOR devuelve `Client Challenge` para Holm; la URL responde y se conserva la observación.

## Reproducir

Desde la raíz del repositorio:

```bash
python3 analisis-valoracion-jurado/correccion-01-analisis-estadistico/citas_estadisticas/validar_citas.py
```

Para compilar la prueba de citas:

```bash
typst compile --root . \
  analisis-valoracion-jurado/correccion-01-analisis-estadistico/citas_estadisticas/prueba_citas.typ \
  analisis-valoracion-jurado/correccion-01-analisis-estadistico/citas_estadisticas/prueba_citas.pdf
```

## Cómo incorporarlas

Copiar solo las entradas aprobadas a `manuscrito/referencias.bib`. La clave `holm1979` ya existe en el manuscrito: no duplicarla. Las entradas de software (`@manual`) pueden ir en una nota de implementación o en el anexo de reproducibilidad.

La guía de uso y las citas en contexto están en `../GUIA_PRUEBAS_ESTADISTICAS.md`.
