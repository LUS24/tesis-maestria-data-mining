# Evidencia de código

Fragmentos relevantes para revisar IX.1.4. No se modificó ninguno.

## 1. Prompts del script final

**Archivo:** `codigo_experimentos/part_g/01_generate_responses_using_agents.py`

```python
# líneas 140-169, resumidas
INSTRUCTIONS = {
    "law_specialist_agent": (
        "## Descripción:"
        "Eres un asistente legal experto en derecho Argentino. [...]"
        "## Requisitos"
        "* Analizas la pregunta del usuario [...] utilizas la herramienta "
        "`retrieve_relevant_documents` una vez [...]."
        "[...]"
    ),
    "retrieval_agent": (
        "Eres un especialista en búsqueda de información legislativa que:"
        "[...]"
        f"* Realizas una búsqueda por cada subconsulta [...] como máximo "
        f"{VECTOR_SEARCH_LIMIT} veces."
        "[...]"
        # "* Utilizas la herramienta `evaluate_retrieval` para evaluar la calidad de la recuperación."
        '[...]'
    ),
    "retrieval_quality_agent": (
        "## Descripción:"
        'Eres un especialista en "retrieval augmented generation" encargado de evaluar la calidad de la recuperación.'
        "[...]"
    ),
}
```

El prompt exacto, sin abreviaturas, está en `salidas/prompts_canonicos.json` y en el anexo.

## 2. Declaración de agentes y herramientas

**Archivo:** `codigo_experimentos/part_g/01_generate_responses_using_agents.py`, líneas 355–374.

```python
law_specialist_agent = Agent(
    model=law_specialist_agent_model,
    instructions=INSTRUCTIONS["law_specialist_agent"],
    prepare_tools=cap_document_retrieval_tool_calls,
    tools=[retrieve_relevant_documents],
    model_settings=model_settings,
)
retrieval_agent = Agent(
    model=retrieval_agent_model,
    instructions=INSTRUCTIONS["retrieval_agent"],
    prepare_tools=cap_total_tool_calls,
    # tools=[cosine_distance_vector_search, evaluate_retrieval],
    tools=[cosine_distance_vector_search],
    model_settings=model_settings,
    deps_type=RetrievalDependencies,
)
retrieval_quality_agent = Agent(
    model=MODELS[2],
    instructions=INSTRUCTIONS["retrieval_quality_agent"],
    model_settings=model_settings,
)
```

Hechos verificables:

- El recuperador **no** registra `evaluate_retrieval` como herramienta.
- El agente de calidad se instancia, pero **no tiene tools** ni se invoca desde el flujo.
- La función `evaluate_retrieval` existe en el archivo, pero es código inalcanzable en la configuración final.

## 3. Función de calidad no utilizada

**Archivo:** `codigo_experimentos/part_g/01_generate_responses_using_agents.py`, líneas 276–311.

```python
def evaluate_retrieval(original_query:str, search_query:str, retrieved_data:list[dict]):
    [...]
    result = retrieval_quality_agent.run_sync(
        f"""
        Please evaluate the quality for the following case:
        User query: {original_query}
        Search query: {search_query}
        Search result: {retrieved_data}

        Do the results answer the question or should I search again?
        """,
        usage_limits=DOCUMENT_RETRIEVAL_LIMIT,
        output_type=RetrievalEvaluation,
    )
    save_conversation_metadata(retrieval_quality_agent, "retrieval_quality_agent", result)
    return result.output
```

No se encontró ningún archivo `retrieval_quality_agent.json` en las 237 sesiones.

## 4. Límite nominal y variante histórica

**Script final, líneas 130–133:**

```python
TOTAL_TOOL_CALL_LIMIT = 6
DOCUMENT_RETRIEVAL_LIMIT = 1
VECTOR_SEARCH_LIMIT = UsageLimits(tool_calls_limit=6)
```

**Log de gpt-5:** el prompt registrado contiene `UsageLimits(tool_calls_limit=7)` y 33 sesiones realizaron 7 búsquedas.

**Log de mini/nano:** contiene `UsageLimits(tool_calls_limit=6)` y ninguna sesión superó 6.

## 5. Notebook antiguo

**Archivo:** `codigo_experimentos/part_g/01_generate_responses_using_agents.ipynb`

El notebook conserva:

```python
retrieval_agent = Agent(
    model=MODELS[2],
    instructions=INSTRUCTIONS["retrieval_agent"],
    tools=[cosine_distance_vector_search, evaluate_retrieval],
    model_settings=model_settings,
)
```

y prompts con formato APA y sin límite explícito. La comparación completa está en `salidas/diff_prompts_script_vs_notebook.diff`.

## 6. Ubicación de la evidencia completa

- `salidas/prompts_canonicos.json`
- `salidas/sesiones_agentic.csv`
- `salidas/variantes_prompts_agente.csv`
- `salidas/inventario_prompts.csv`
- `salidas/diff_prompts_script_vs_notebook.diff`
- `salidas/resumen_auditoria.json`
