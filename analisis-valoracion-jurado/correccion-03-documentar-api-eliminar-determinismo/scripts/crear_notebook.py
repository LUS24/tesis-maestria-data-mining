# -*- coding: utf-8 -*-
"""Crea el notebook de revisión de IX.1.3 con nbformat mínimo.

Se usa JSON estándar para no depender de nbformat/nbclient en el entorno de
experimentos. El notebook se ejecuta después con ``ejecutar_notebook.py``.
"""

from __future__ import annotations

import json
from pathlib import Path

ARTIFACT_DIR = Path(__file__).resolve().parents[1]
NOTEBOOK_PATH = ARTIFACT_DIR / "02_parametros_prompts_y_configuracion.ipynb"


def markdown(source: str) -> dict:
    return {
        "cell_type": "markdown",
        "metadata": {},
        "source": source.splitlines(keepends=True),
    }


def code(source: str) -> dict:
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": source.splitlines(keepends=True),
    }


cells = [
    markdown(
        """# IX.1.3 — Parámetros de API y eliminación del determinismo

Este notebook reproduce la evidencia del punto **IX.1.3** sin llamar a APIs externas y sin modificar fuentes.

Objetivo:

1. separar lo solicitado por el código, lo registrado en los artefactos y lo enviado por la biblioteca;
2. documentar la ausencia de `reasoning_effort` y el valor desconocido del esfuerzo histórico;
3. dejar constancia de la ejecución única;
4. señalar las ubicaciones del manuscrito que deben revisarse.

> **Advertencia:** los logs de agentes no son volcados HTTP. No deben usarse como prueba de la temperatura aplicada.
"""
    ),
    code(
        """from pathlib import Path
import sys

import pandas as pd
from IPython.display import Image, display

ART = Path.cwd()
if not (ART / "scripts" / "generar_evidencia.py").exists():
    candidates = [
        Path.cwd().parent / "analisis-valoracion-jurado" / "correccion-03-documentar-api-eliminar-determinismo",
        Path.cwd() / "analisis-valoracion-jurado" / "correccion-03-documentar-api-eliminar-determinismo",
    ]
    ART = next(path for path in candidates if (path / "scripts" / "generar_evidencia.py").exists())

sys.path.insert(0, str(ART))
from scripts.generar_evidencia import main

print("Carpeta de artefactos:", ART)
"""
    ),
    markdown(
        """## 1. Generar la evidencia

La siguiente celda ejecuta el mismo script que produce `salidas/`. No usa red: la captura del payload se hace con `httpx.MockTransport`.
"""
    ),
    code(
        """summary = main()
summary
"""
    ),
    markdown(
        """## 2. Configuración solicitada, registrada y perfil de la biblioteca

`temperatura_en_payload=False` significa que el cuerpo construido por Pydantic AI no contiene `temperature`. `settings_registrados_log` muestra lo que quedó en el metadata de la aplicación, que no es el cuerpo HTTP.
"""
    ),
    code(
        """config = pd.read_csv(ART / "salidas" / "tabla_configuracion_solicitado_registrado_efectivo.csv")
display(
    config[
        [
            "estrategia",
            "componente",
            "modelo_rol",
            "modelo_especialista",
            "settings_solicitados_codigo",
            "settings_registrados_log",
            "temperatura_en_payload",
            "reasoning_effort_solicitado",
            "reasoning_effort_registrado",
            "respuestas_blancas",
        ]
    ]
)
"""
    ),
    markdown(
        """## 3. Tokens de razonamiento y ejecución única

Los tokens de razonamiento están presentes, pero no identifican el esfuerzo solicitado ni el aplicado. La tabla de ejecuciones muestra 79 registros para 79 unidades en cada celda y ningún campo de réplica.
"""
    ),
    code(
        """reasoning = pd.read_csv(ART / "salidas" / "tabla_reasoning_tokens_por_celda.csv")
display(reasoning)
execution = pd.read_csv(ART / "salidas" / "tabla_ejecuciones_unicas.csv")
display(
    execution[
        [
            "estrategia",
            "modelo",
            "registros",
            "unidades_unicas",
            "duplicados_unidad",
            "replicas_identificadas",
            "campo_run_id_replica",
            "respuestas_blancas",
        ]
    ]
)
"""
    ),
    markdown(
        """## 4. Captura local del payload

Se capturaron 12 cuerpos de petición: sin RAG, RAG básico, especialista agéntico y recuperador agéntico para los tres modelos. Ninguno contiene `temperature` ni `reasoning_effort`.
"""
    ),
    code(
        """import json

payloads = json.loads((ART / "salidas" / "evidencia_payloads_locales.json").read_text(encoding="utf-8"))
payload_rows = []
for call in payloads["calls"]:
    payload_rows.append(
        {
            "clave": call["clave"],
            "claves_del_cuerpo": ", ".join(call["request_body_keys"]),
            "temperature_presente": call["temperature_presente"],
            "reasoning_effort_presente": call["reasoning_effort_presente"],
            "max_completion_tokens_presente": call["max_completion_tokens_presente"],
            "settings_solicitados": call["model_settings_solicitados"],
        }
    )
display(pd.DataFrame(payload_rows))
"""
    ),
    markdown(
        """## 5. Perfil de Pydantic AI

Los tres perfiles declaran `temperature` entre los parámetros no admitidos. El extracto fuente muestra el `pop` que elimina esos settings antes de construir la solicitud.
"""
    ),
    code(
        """pydantic_evidence = json.loads(
    (ART / "salidas" / "evidencia_perfil_pydantic.json").read_text(encoding="utf-8")
)
profile_rows = []
for model, profile in pydantic_evidence["perfiles"].items():
    profile_rows.append(
        {
            "modelo": model,
            "temperatura_no_admitida": profile["temperatura_entre_no_admitidos"],
            "settings_no_admitidos": ", ".join(profile["openai_unsupported_model_settings"]),
        }
    )
display(pd.DataFrame(profile_rows))
print((ART / "salidas" / "evidencia_pydantic_ai_excerpt.txt").read_text(encoding="utf-8"))
"""
    ),
    markdown(
        """## 6. Ubicaciones del texto que deben revisarse

Esta tabla es la entrada para la edición posterior. No se modifica ningún `.typ` desde este notebook.
"""
    ),
    code(
        """claims = pd.read_csv(ART / "salidas" / "tabla_ubicaciones_texto_a_modificar.csv")
display(
    claims[
        [
            "archivo",
            "linea",
            "alcance",
            "prioridad",
            "texto_actual_coincidente",
            "texto_propuesto",
        ]
    ]
)
"""
    ),
    markdown(
        """## 7. Figura de apoyo

La figura muestra la mediana de tokens de razonamiento por celda. Es una descripción del consumo, no una medida del esfuerzo.
"""
    ),
    code(
        """display(Image(filename=str(ART / "salidas" / "fig_tokens_razonamiento_por_celda.png")))
"""
    ),
    markdown(
        """## 8. Lectura de resultados

- La temperatura fue solicitada en el código, pero no está en el payload de los modelos GPT-5.
- Los logs de sin RAG/RAG básico conservan `temperature=0.0`; los de Agentic-RAG guardan `{}`. El log no es el payload.
- No hay `reasoning_effort` en el código de generación ni en los logs revisados; el esfuerzo histórico es desconocido.
- Las 711 respuestas tienen `reasoning_tokens`, pero esos tokens no permiten reconstruir el esfuerzo.
- Hay 79 registros por celda para 79 unidades y ningún campo de réplica: la ejecución única debe declararse como limitación.
- Los jueces tienen su propia configuración en OpenRouter y no se usan para afirmar determinismo de los generadores.

Las propuestas concretas de redacción están en `propuestas_edicion.md` y en `salidas/tabla_ubicaciones_texto_a_modificar.csv`.
"""
    ),
]

notebook = {
    "cells": cells,
    "metadata": {
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3",
        },
        "language_info": {
            "name": "python",
            "version": "3.13",
        },
    },
    "nbformat": 4,
    "nbformat_minor": 5,
}

NOTEBOOK_PATH.write_text(
    json.dumps(notebook, ensure_ascii=False, indent=1) + "\n", encoding="utf-8"
)
print("Notebook creado:", NOTEBOOK_PATH)
