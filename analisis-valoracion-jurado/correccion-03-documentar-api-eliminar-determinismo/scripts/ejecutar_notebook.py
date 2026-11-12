# -*- coding: utf-8 -*-
"""Ejecuta el notebook de IX.1.3 con el kernel del entorno actual.

No requiere nbconvert/nbclient: usa jupyter_client, ya presente en el entorno
de experimentos. Guarda las salidas dentro del propio notebook.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

from jupyter_client import KernelManager


ARTIFACT_DIR = Path(__file__).resolve().parents[1]
NOTEBOOK_PATH = ARTIFACT_DIR / "02_parametros_prompts_y_configuracion.ipynb"


def _normalize_data(data: dict[str, Any]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for mime, value in data.items():
        if isinstance(value, list):
            result[mime] = value
        elif isinstance(value, str):
            result[mime] = value
        else:
            result[mime] = str(value)
    return result


def execute_notebook(path: Path) -> None:
    notebook = json.loads(path.read_text(encoding="utf-8"))
    km = KernelManager(kernel_name="python3")
    km.start_kernel(cwd=str(path.parent))
    kc = km.client()
    kc.start_channels()
    try:
        kc.wait_for_ready(timeout=60)
        for cell_index, cell in enumerate(notebook["cells"]):
            if cell["cell_type"] != "code":
                continue
            source = "".join(cell["source"])
            print(f"Ejecutando celda {cell_index + 1}/{len(notebook['cells'])}...")
            msg_id = kc.execute(source, store_history=True, allow_stdin=False)
            outputs: list[dict[str, Any]] = []
            execution_count = None
            while True:
                msg = kc.get_iopub_msg(timeout=600)
                if msg.get("parent_header", {}).get("msg_id") != msg_id:
                    continue
                msg_type = msg["msg_type"]
                content = msg["content"]
                if msg_type == "execute_input":
                    execution_count = content.get("execution_count")
                elif msg_type == "stream":
                    outputs.append(
                        {
                            "output_type": "stream",
                            "name": content.get("name", "stdout"),
                            "text": content.get("text", ""),
                        }
                    )
                elif msg_type in {"execute_result", "display_data"}:
                    outputs.append(
                        {
                            "output_type": msg_type,
                            "data": _normalize_data(content.get("data", {})),
                            "metadata": content.get("metadata", {}),
                            "execution_count": content.get("execution_count"),
                        }
                    )
                elif msg_type == "error":
                    outputs.append(
                        {
                            "output_type": "error",
                            "ename": content.get("ename"),
                            "evalue": content.get("evalue"),
                            "traceback": content.get("traceback", []),
                        }
                    )
                elif msg_type == "status" and content.get("execution_state") == "idle":
                    break
            cell["outputs"] = outputs
            cell["execution_count"] = execution_count
    finally:
        kc.stop_channels()
        km.shutdown_kernel(now=True)

    path.write_text(
        json.dumps(notebook, ensure_ascii=False, indent=1) + "\n", encoding="utf-8"
    )
    print("Notebook ejecutado y guardado:", path)


if __name__ == "__main__":
    if not NOTEBOOK_PATH.exists():
        raise SystemExit(f"No existe el notebook: {NOTEBOOK_PATH}")
    execute_notebook(NOTEBOOK_PATH)
