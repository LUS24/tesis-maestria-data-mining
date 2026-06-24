from pymilvus import MilvusClient
from sentence_transformers import SentenceTransformer
import json
from pathlib import Path
import datetime
from dotenv import load_dotenv
from pydantic_ai import Agent, UsageLimits
from pydantic_ai.settings import ModelSettings
from pydantic_ai.run import AgentRunResult
from pydantic_ai.exceptions import UsageLimitExceeded
# import nest_asyncio
from uuid import uuid4
from dataclasses import dataclass
from pydantic_ai import (
    Agent, ModelRetry, UnexpectedModelBehavior, capture_run_messages, RunContext, ToolDefinition, ToolCallPart
)

#########################
# Initial configuration
#########################

# nest_asyncio.apply()  # To be able to run pydantic in jupyter notebooks preventing event loop issues


DATABASE_NAME = "tesis_MCD_v1"
COLLECTION_NAME = "codigo_de_mineria_v1"
EMBEDDING_MODEL_NAME = "hiiamsid/sentence_similarity_spanish_es"  # https://huggingface.co/hiiamsid/sentence_similarity_spanish_es/tree/main
ANSWER_VECTOR_FIELD_NAME = "vector_contenido_texto" # database field that contains the embedding vector to perform the search.
OUTPUT_FIELDS = [
    "codigo_norma",
    "id_parte",
    "id_padre",
    "tipo_parte",
    "numero_parte",
    "titulo_parte",
    "ultimo_estado",
    "contenido_texto",
]

embedding_model = SentenceTransformer(EMBEDDING_MODEL_NAME)

MODELS=[
    "openai:gpt-5-nano",
    "openai:gpt-5-mini",
    "openai:gpt-5",
]


#########################
# Helper functions
#########################

def get_db_client():
    print("get_db_client")
    client = MilvusClient(uri="http://localhost:19530", token="root:Milvus")
    client.use_database(DATABASE_NAME)
    return client

def save_retrieval_metadata(query, retrieved_documents):
    timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
    data = {
        "timestamp": timestamp,
        "query": query,
        "retrieved_documents": retrieved_documents
    }

    with open(RETRIEVAL_HISTORY_DIR_PATH.joinpath(f"{timestamp}_retrieval_log.json"), encoding="utf-8", mode="w") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def get_previous_search_results():
    results = []
    for document in RETRIEVAL_HISTORY_DIR_PATH.glob("*.json"):
        with open(document, mode="r", encoding="utf-8") as f:
            results.append(json.load(f))
    return results

def get_document_matches(client:MilvusClient, text: str, max_documents: int = 10) -> list[dict]:

    question_vector = embedding_model.encode(text)

    results = client.search(
        collection_name=COLLECTION_NAME,
        anns_field=ANSWER_VECTOR_FIELD_NAME,
        data=[question_vector],
        limit=5000,
        search_params={"metric_type": "COSINE"},
        output_fields=OUTPUT_FIELDS,
    )

    return [
        {"index": i, "distance": result["distance"], **result["entity"]}
        for i, result in enumerate(results[0], start=1)
    ][:max_documents]


def save_conversation_metadata(agent:Agent, model_name:str, result: AgentRunResult):
    conversation_data = {
        "messages": json.loads(result.all_messages_json()),
        "metadata": {
            "model_settings": agent.model_settings,
            "model_version": result.response.model_name,
            "provider_name": result.response.provider_name,
            "timestamp": result.timestamp().isoformat(),
            "usage": {
                "tokens": {
                    "input_tokens": result.usage().input_tokens,
                    "output_tokens": result.usage().output_tokens,
                    "tokens_details": result.usage().details,
                },
                "cost": {
                    "input_price": float(result.response.cost().input_price),
                    "output_price": float(result.response.cost().output_price),
                    "total_price": float(result.response.cost().total_price),
                    "model_input_price_mtok": float(result.response.cost().model_price.input_mtok),
                    "model_output_price_mtok": float(result.response.cost().model_price.output_mtok),
                    "model_id": result.response.cost().model.id,
                    "model_name": result.response.cost().model.name,
                },
            },
        }
    }

    with open(CHAT_DIR_PATH.joinpath(f"{model_name}.json"), encoding="utf-8", mode="w") as f:
        json.dump(conversation_data, f, ensure_ascii=False, indent=4)

#########################
# Limits
#########################

TOTAL_TOOL_CALL_LIMIT = 6
DOCUMENT_RETRIEVAL_LIMIT = 1
# DOCUMENT_RETRIEVAL_LIMIT = UsageLimits(tool_calls_limit=1)
VECTOR_SEARCH_LIMIT = UsageLimits(tool_calls_limit=6)

#########################
# Instructions
# The `instructions` parameter. Check the docs for more details: https://ai.pydantic.dev/agents/#instructions
#########################

INSTRUCTIONS = {
    "law_specialist_agent": (
        "## Descripción:"
        "Eres un asistente legal experto en derecho Argentino. Respondes preguntas legales basadas en la Constitución Nacional Argentina, Códigos, Leyes y jurisprudencia."
        "## Requisitos"
        "* Analizas la pregunta del usuario, extraes los puntos importantes y utilizas la herramienta `retrieve_relevant_documents` una vez para obtener información de la base de datos legislativa."
        "* Analizas los documentos para generar la respuesta final."
        "* Siempre citas las fuentes legales consultadas para la elaboración de tu respuesta. Por ejemplo: Código de Minería. Ley 1919 y sus modificatorias. Artículos 2, 3 inc. a, 5, 7, 8, 10 y 44. 25 de noviembre 1886 (Argentina)"
        "* Si no sabes la respuesta y los documentos legales no son suficientes para crear una respuesta, di que no cuentas con información para responderla."
        "* Las respuestas deben ser claras, concisas y directas al punto."
        "* Solo retorna la respuesta. No agregues texto irrelevante."
        "* Respondes en español al menos que el usuario solicite otro idioma."
    ),
    "retrieval_agent": (
        "Eres un especialista en búsqueda de información legislativa que:"
        "* Recibes una consulta relacionada con cuestiones legales de derecho Argentino."
        "* La consulta puede dividirse en máximo 3 subconsultas para mejorar la recuperación."
        f"* Realizas una búsqueda por cada subconsulta en una base de datos de vectores empleando la herramienta `cosine_distance_vector_search` como máximo {VECTOR_SEARCH_LIMIT} veces."
        "Usa el valor para la clave 'usage_counts' del resultado para monitorear cuantas consultas has hecho"
        # "* Utilizas la herramienta `evaluate_retrieval` para evaluar la calidad de la recuperación."
        '* Seleccionas los documentos que mejor se ajustan a la consulta inicial y respondes con los resultados de la búsqueda. por ejemplo: {"selected_documents": [<document_1>, <document_2>, ...]}'
    ),
    "retrieval_quality_agent": (
        "## Descripción:"
        'Eres un especialista en "retrieval augmented generation" encargado de evaluar la calidad de la recuperación.'
        "* Comparas la consulta original con la información recuperada y decides si la información es suficiente para responder la consulta."
        "* Provees feedback para mejorar la consulta."
        "* El feedback debe ser conciso."
    ),
}

#########################
# Dependencies
#########################

@dataclass
class RetrievalDependencies:
    vector_db_client: MilvusClient

#########################
# Outputs
#########################
@dataclass
class RetrievalFinalOutput:
    retrieved_documents: list[dict]

@dataclass
class RetrievalEvaluation:
    feedback_text: str
    repeat_search: bool

@dataclass
class ExpertResponse:
    response_text: str

#########################
# Tools
#########################


async def cap_total_tool_calls(
    ctx: RunContext[None], tool_defs: list[ToolDefinition]
) -> list[ToolDefinition] | None:
    """Disable all tools after TOTAL_TOOL_CALL_LIMIT total tool calls in this run.

    Counts prior ToolCallPart occurrences in ctx.messages and returns an empty
    list once the cap is reached, preventing further tool usage.
    """
    print("cap_total_tool_calls")
    total_calls = 0
    for message in ctx.messages or []:
        parts = getattr(message, "parts", None)
        if not parts:
            continue
        for part in parts:
            if isinstance(part, ToolCallPart):
                total_calls += 1

    if (
        TOTAL_TOOL_CALL_LIMIT is not None
        and total_calls >= TOTAL_TOOL_CALL_LIMIT
    ):
        return []

    return tool_defs



async def cap_document_retrieval_tool_calls(
    ctx: RunContext[None], tool_defs: list[ToolDefinition]
) -> list[ToolDefinition] | None:
    """Disable all tools after DOCUMENT_RETRIEVAL_LIMIT total tool calls in this run.

    Counts prior ToolCallPart occurrences in ctx.messages and returns an empty
    list once the cap is reached, preventing further tool usage.
    """
    print("cap_document_retrieval_tool_calls")
    total_calls = 0
    for message in ctx.messages or []:
        parts = getattr(message, "parts", None)
        if not parts:
            continue
        for part in parts:
            if isinstance(part, ToolCallPart):
                total_calls += 1

    if (
        DOCUMENT_RETRIEVAL_LIMIT is not None
        and total_calls >= DOCUMENT_RETRIEVAL_LIMIT
    ):
        return []

    return tool_defs

# Agent tools
def retrieve_relevant_documents(question: str) -> dict[str,]:
    """
    Retrieves documents to answer the user's questions.
    """
    print("Tool used: retrieve_relevant_documents")

    retrieval_deps = RetrievalDependencies(
        vector_db_client=get_db_client(),
    )
    result = retrieval_agent.run_sync(
        f"""
        Please retrieve documents for this user query:
        > {question}
        """,
        usage_limits=VECTOR_SEARCH_LIMIT,
        # output_type=RetrievalFinalOutput
        deps=retrieval_deps,
    )
    save_conversation_metadata(retrieval_agent, "retrieval_agent", result)
    return result.output

def evaluate_retrieval(original_query:str, search_query:str, retrieved_data:list[dict]):
    """
    original_query: the user's original query.
    search_query: the query used by the retrieval agent to get the retrieved data.
    retrieved_data: resulting data from the retrieval operation, for example:
    ```json
        {
        "index": 1,
        "distance": 0.6904841065406799,
        "tipo_parte": "artículo",
        "numero_parte": 25,
        "titulo_parte": null,
        "ultimo_estado": "en vigor",
        "contenido_texto": "Some text content",
        "codigo_norma": "Código de Minería Argentino",
        "id_padre": "7305f9fee43e3553ad5e856cdf3c99ff",
        "id_parte": "8d21b964b0fa52b6b673df7724c42c55"
    },
    ```
    """
    print("Tool used: evaluate_retrieval")
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

# Code tools
def cosine_distance_vector_search(ctx: RunContext[RetrievalDependencies], query:str) -> list[dict]:
    """
    Looks for documents in a vector database based on the Cosine Distance Metric.
    Counts the number of searches performed.
    If there were previous searches it returns the previous results. 
    """
    print("Tool used: cosine_distance_vector_search")
    print("Query:", query)
    print("Query:", query.encode('utf-8'))

    global vector_search_counter
    result = get_document_matches(ctx.deps.vector_db_client, query, max_documents=5)
    save_retrieval_metadata(query, result)
    vector_search_counter+=1
    print(vector_search_counter)
    return {"usage_counts": vector_search_counter, "search_result": result}

def get_documents_by_ids(id_list:list[str]) -> list[dict]:
    try:
        client = get_db_client()
        results = client.get(
            collection_name=COLLECTION_NAME, ids=id_list, output_fields=OUTPUT_FIELDS
        )
    except Exception as e:
        print(e)
    finally:
        client.close()

    return list(results)

#########################
# Agents
# Definition of agents to be used globally per chat session.
#########################
model_settings = ModelSettings(temperature=0.0)

law_specialist_agent_model = MODELS[1]
retrieval_agent_model = MODELS[2]

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

#########################
# Main functions
#########################

def answer_user(question:str) -> AgentRunResult:
    print("Generating answer")
    result = law_specialist_agent.run_sync(
        question,
        output_type=ExpertResponse,
    )
    print("Saving results")
    save_conversation_metadata(law_specialist_agent, "law_specialist_agent", result)
    return result.output

"""
# Workflow description

1. User submits a question to the `Law Specialist Agent`
2. The `Law Specialist Agent` processes the question structuring it for the `Retrieval Agent`
3. Based on an Agent's input, the `Retrieval Agent` prepares query for the vector database and uses a tool to perform the query.
4. A `Retrieval Quality Agent` evaluates the output and decides if the returned data is sufficient to answer the query
    4.1. If not, the model prepares a short helpful feedback and instructs the `Retrieval Agent` to generate new queries based on the feedback.
    4.2. If it is, the retrieved data is passed to the `Law Specialist Agent` to generate the final answer.
    - LIMIT Sequence to 3 times.
    - The retrieval quality agent needs to have a memory tool to interact with previous retrievals
        - Get best matches based on the metric distance
        - Store ids of the retrieved documents.
5. The `Law Specialist Agent` returns the final answer to the user.

Tools:
    - Milvus
        - Retrieve documents by semantic search
        - Retrieve document by id
```

"""

if __name__ == "__main__":
    load_dotenv()
    timestamp = datetime.datetime.now().strftime("%Y%m%d")

    BASE_PATH = Path().resolve()
    CHAT_DATA_PATH = BASE_PATH.joinpath("chat_data", law_specialist_agent_model.replace(":", "_"))
    CHAT_DATA_PATH.mkdir(parents=True, exist_ok=True)

    DATA_FILE_PATH = BASE_PATH.joinpath("20251112_llm_responses_agentic_rag_results.json")
    OUTPUT_FILE_PATH = BASE_PATH.joinpath(f"{timestamp}_llm_responses_agentic_rag_results.json")

    with open(DATA_FILE_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    for pregunta in data:
        vector_search_counter = 0
        chat_id = f"{pregunta['numero_pregunta']:02d}_{pregunta['numero_subpregunta'] if pregunta['numero_subpregunta'] else 0:02d}"
        print(f"--------------------Processing question {chat_id}--------------------")
        CHAT_DIR_PATH = CHAT_DATA_PATH.joinpath(chat_id)
        CHAT_DIR_PATH.mkdir(parents=True, exist_ok=True)
        RETRIEVAL_HISTORY_DIR_PATH = CHAT_DIR_PATH.joinpath("retrieval_history")
        RETRIEVAL_HISTORY_DIR_PATH.mkdir(parents=True, exist_ok=True)
        answer = answer_user(pregunta["texto"])

        if "llm_responses_agentic_rag" not in pregunta:
            pregunta["llm_responses_agentic_rag"] = []

        pregunta["llm_responses_agentic_rag"].append({"texto": answer.response_text, "law_specialist_model": law_specialist_agent_model, "retrieval_model": retrieval_agent_model})

        with open(OUTPUT_FILE_PATH, encoding="utf-8", mode="w") as f:
            f.write(json.dumps(data, ensure_ascii=False, indent=4))
