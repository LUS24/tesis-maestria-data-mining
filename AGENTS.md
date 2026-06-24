# AGENTS.md - Tesis Leonardo

Para saber de que trata el proyecto consulta el archivo con la [Introducción](manuscrito/capitulos/02_capitulo_01_introduccion.typ).

Este proyecto usa [Typst](https://typst.app/docs/) para la generación del manuscrito y [uv](https://docs.astral.sh/uv/) + [direnv](https://direnv.net/) para la gestión del entorno Python.

## 1. Organización del proyecto

```
.
├── manuscrito/                  # Generación del manuscrito (Typst)
│   ├── main.typ                 # Archivo principal de la tesis
│   ├── referencias.bib          # Base de datos bibliográfica
│   ├── capitulos/               # Capítulos y secciones en archivos separados
│   ├── codigo-helpers/          # Scripts Python de apoyo (diagramas, figuras)
│   ├── media/                   # Imágenes, gráficos y otros elementos
│   ├── salidas/                 # PDFs generados (patrón <timestamp>_main.pdf)
│   ├── temp/                    # Archivos temporales (ignorado por git)
│   ├── bibliography/           # PDFs de referencia (ignorado por git)
│   ├── .envrc                   # Configuración direnv (MEDIA_DIR, CODE_DIR, OUTPUTS_DIR)
│   ├── .gitignore
│   ├── pyproject.toml           # Definición del proyecto Python (uv)
│   └── uv.lock
├── codigo_experimentos/         # Código de experimentos (partes A-J)
│   ├── main.py                  # Punto de entrada de experimentos
│   ├── part_a/ ... part_j/      # Experimentos organizados por partes
│   ├── data/                    # Datos de leyes y normativas
│   ├── .envrc                   # Configuración direnv (usa Bitwarden para secrets)
│   ├── .gitignore
│   ├── pyproject.toml
│   └── README.md
├── data/                        # Datos compartidos (preguntas benchmark, etc.)
├── Makefile                     # Tareas de compilación (make pdf, watch, clean)
├── .envrc                       # Configuración direnv raíz (obsoleto, ver manuscrito/.envrc)
├── .gitignore
├── AGENTS.md                    # Este archivo
├── README.md                    # Documentación del proyecto
└── archivo/                     # Cosas no "core" de la tesis (excluido de git)
```

## 2. Entorno y ejecución

### Manuscrito (Typst)

- El proyecto utiliza [direnv](https://direnv.net/) para cargar automáticamente las variables definidas en [manuscrito/.envrc](manuscrito/.envrc). Ejecuta `direnv allow` dentro de `manuscrito/` la primera vez.
- Las carpetas referenciadas en las variables de direnv (`MEDIA_DIR=./media`, `CODE_DIR=./codigo-helpers`, `OUTPUTS_DIR=./salidas`) **deben existir** dentro de `manuscrito/`. Si no están presentes, créalas antes de ejecutar cualquier comando.
- El entorno Python se gestiona con [uv](https://docs.astral.sh/uv/) y se ubica en `$UV_PROJECT_ENVIRONMENT` (definido en `manuscrito/.envrc`). Sincroniza las dependencias con `uv sync` dentro de `manuscrito/`.
- **Todo comando Python debe ejecutarse con `uv run`** (con direnv previamente activado). Por ejemplo: `uv run python codigo-helpers/generacion_diagramas_y_figs/main.py`.

### Experimentos (Python)

- El código de experimentos está en [codigo_experimentos/](codigo_experimentos/). Consulta su [README](codigo_experimentos/README.md) para más detalles.
- Usa su propio entorno Python gestionado con uv. Activa direnv en `codigo_experimentos/` y ejecuta `uv sync`.
- Las credenciales se gestionan mediante Bitwarden (ver `codigo_experimentos/.envrc`).

## 3. Compilación del manuscrito

```bash
# Desde la raíz del repositorio
make pdf          # Compilar una vez
make save         # Hace commit a todos los cambios a modo de "checkpoint"
```

## 4. Flujo de trabajo

1. REVISAR `TODOs`: En los distintos archivos voy a ir dejando `TODOs` en forma de comentarios, por favor revísalos e intenta completarlos. Ejemplos de `TODOs`:

```typ
/**
TODO: Mejorar diagrama, intentar emplear el paquete [zeitline](https://typst.app/universe/package/zeitline) ya que es específico para líneas de tiempo.
**/
```

```typ
// TODO: Agregar algo de información sobre las limitaciones de los n-gramas
```

- IMPORTANTE:
  - Utiliza la SKILL [escritura-tesis-leonardo](.agents/skills/escritura-tesis-leonardo) para completar los `TODOs`.
  - Para buscar imágenes prioriza la utilización de imágenes de wikipedia con la cita correspondiente.
