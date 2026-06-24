# Performed Tasks Summary

This document summarizes the code and tasks performed in each directory of the project, which focuses on building and evaluating a RAG (Retrieval-Augmented Generation) system for Argentinian Mining Law (Código de Minería Argentino).

---

## 📁 `notebooks/`

Test and exploration notebooks for various technologies.

| File                                            | Description                                                                                                                                                                                                            |
| ----------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `01_docling_download_htmls_from_infoleg.ipynb`  | Downloads legal texts (Código de Minería, Código Penal) from Infoleg using the Docling library. Converts HTML to Markdown and saves locally. Also processes PDF documents from Boletín Oficial.                            |
| `01_openai_parse_pdf.ipynb`                     | Uses OpenAI's vision models (o4-mini) to extract structured legal text from scanned PDF images of the "Código de Minería". Includes SQLite storage for API responses and iterative processing of multi-page documents. |
| `01_requests_download_htmls_from_infoleg.ipynb` | Alternative approach using `requests` and `BeautifulSoup` to download and parse legal HTML from Infoleg. Extracts structured norm data including articles, sanction dates, and annexes.                                |
| `test_encoding.ipynb`                           | Tests Pydantic AI agent functionality with a simple translation example (English to Spanish).                                                                                                                          |
| `test_pydantic_ai.ipynb`                        | Explores Pydantic AI agent capabilities with tool calls, including a roulette game example demonstrating context dependencies.                                                                                         |

---

## 📁 `part_a/` - Question Generation

Generates evaluation questions from the Mining Code text.

| File                                          | Description                                                                                                                                                                                |
| --------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `part_A_2_split_codigo_mineria_titulos.ipynb` | Splits the consolidated Mining Code markdown file into individual title files (Título I, II, etc.) using regex pattern matching.                                                           |
| `part_A_3_generate_questions.ipynb`           | Uses OpenAI GPT-4.1 to generate comprehensive legal case-study questions with expected answers from each title of the Mining Code. Questions are designed for legal specialist evaluation. |
| `part_A_4_generate_word_file.ipynb`           | Concatenates generated questions and converts them to a Word document (.docx) using pypandoc. Orders files by Roman numeral titles.                                                        |

---

## 📁 `part_b/`

Empty directory (only contains README.md).

---

## 📁 `part_c/` - Vector Database Creation

Creates and populates the Milvus vector database for semantic search.

| File                                  | Description                                                                                                                                                                                                                                                                                   |
| ------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `01_initial_vector_db_creation.ipynb` | Sets up Milvus vector database with Docker. Creates schema for legal document parts (articles, titles, chapters). Generates embeddings using `hiiamsid/sentence_similarity_spanish_es` model (768 dimensions). Populates database with Mining Code content and tests vector search retrieval. |

---

## 📁 `part_d/` - Baseline Retrieval Testing

Tests vector database retrieval performance.

| File                                | Description                                                                                                                                                                          |
| ----------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `01_data_retrieval_base_test.ipynb` | Loads generated questions, performs vector similarity search for each question, and records the ranking/distance of correct source articles. Establishes baseline retrieval metrics. |

---

## 📁 `part_e/` - LLM Responses (No RAG)

Generates and evaluates LLM responses without retrieval augmentation.

| File                                | Description                                                                                                                                                                                                                                   |
| ----------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `01_organize_questions.ipynb`       | Normalizes question format: flattens multi-part questions into individual items with unified structure (question text, context, expected answer).                                                                                             |
| `02_query_llms_for_responses.ipynb` | Queries multiple OpenAI models (gpt-5-nano, gpt-5-mini, gpt-5) for legal answers without RAG context. Uses Pydantic AI agents with temperature=0 for deterministic responses. Stores responses with full metadata (tokens, cost, timestamps). |
| `03_compare_texts.ipynb`            | Calculates comprehensive text similarity metrics between ground truth and LLM responses.                                                                                                                                                      |
| `03_compare_texts.py`               | Reusable Python module implementing 11+ metrics: Exact Match, Token F1, Jaccard Similarity, Levenshtein Distance, CER, BLEU (1-4), ROUGE (1, 2, L), SBERT Similarity (multilingual + Spanish), BERTScore, Length/Word ratios.                 |

---

## 📁 `part_f/` - Basic RAG Responses

Implements traditional RAG pipeline.

| File                                 | Description                                                                                                                                                                 |
| ------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `01_rag_llm_responses.ipynb`         | Performs vector search to retrieve top-10 relevant documents, injects them into the system prompt, and generates LLM responses. Tests same three models as no-RAG baseline. |
| `02_rag_llm_calculate_metrics.ipynb` | Calculates all text comparison metrics for RAG responses against ground truth answers.                                                                                      |

---

## 📁 `part_g/` - Agentic RAG Responses

Implements multi-agent RAG architecture.

| File                                              | Description                                                                                                                                                                                                                                                           |
| ------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `01_generate_responses_using_agents.ipynb`        | Defines three-agent architecture: **Law Specialist Agent** (answers questions), **Retrieval Agent** (performs vector searches with sub-queries), **Retrieval Quality Agent** (evaluates retrieval quality). Uses Pydantic AI with tool limits and structured outputs. |
| `01_generate_responses_using_agents.py`           | Standalone Python script for running agentic RAG pipeline on all questions. Includes conversation logging and retrieval history storage.                                                                                                                              |
| `02_0_integrate_agentic_rag_results.ipynb`        | Merges results from different model runs (GPT-5 and GPT-5-mini) into a unified result file.                                                                                                                                                                           |
| `02_1_handle_missing_responses.ipynb`             | Identifies and documents missing/failed responses in the agentic RAG results.                                                                                                                                                                                         |
| `03_calculate_agentic_rag_response_metrics.ipynb` | Calculates all text comparison metrics for agentic RAG responses.                                                                                                                                                                                                     |
| `04_integrate_metadata.ipynb`                     | Integrates detailed metadata (agent logs, retrieval history, cost/token usage) into the final results file.                                                                                                                                                           |

---

## 📁 `part_h/` - Data Integration

Consolidates all results into a unified file.

| File                                | Description                                                                                                                                   |
| ----------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------- |
| `01_integrate_responses_data.ipynb` | Merges results from `part_f` (basic RAG) and `part_g` (agentic RAG) into a single comprehensive JSON file containing all response strategies. |

---

## 📁 `part_h_1/` - LLM-as-a-Judge Evaluation

Uses LLM judges to evaluate response quality.

| File                                                   | Description                                                                                                                                                                                                                                                                                                             |
| ------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `01_llm_as_a_judge.ipynb`                              | Implements LLM-as-a-Judge evaluation using `pydantic_evals` . Defines two evaluation rubrics: **respuesta_correcta** (answer correctness 0-1) and **precision_legal** (legal citation accuracy 0-1). Tests multiple judge models (DeepSeek, Grok, etc.). Evaluates all 9 system combinations (3 strategies × 3 models). |
| `01_llm_as_a_judge_batch_2.ipynb`                      | Additional batch of LLM judge evaluations using Kimi K2 model.                                                                                                                                                                                                                                                          |
| `02_integrate_llm_judge_results_into_final_file.ipynb` | Parses all judge report JSON files and consolidates scores into a final CSV file with columns: question ID, judge model, strategy, response model, correctness score/reason, legal precision score/reason.                                                                                                              |

---

## 📁 `part_i/` - Analysis and Visualization

Prepares data for statistical analysis and visualization.

| File                                 | Description                                                                                                                                                                                                                            |
| ------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `01_prepare_data.ipynb`              | Transforms nested JSON results into flat CSV files using Polars: `responses_text_cleaned.csv` (raw text outputs), `metric_comparison_source_data_cleaned.csv` (all metrics), `metadata_tokens_cost_cleaned.csv` (token/cost metadata). |
| `02_analyze_metric_comparison.ipynb` | Performs statistical analysis of metrics across strategies and models. Generates boxplot visualizations for each metric using plotnine (ggplot2-style).                                                                                |

---

## 📁 `part_j/` - Statistical analysis


Performs statistical analysis


---

## 📁 Root Directory

| File      | Description             |
| --------- | ----------------------- |
| `main.py` | Empty placeholder file. |

---

## 🔄 Overall Workflow

```
01. Data Collection (notebooks/)
   └── Download legal texts from Infoleg → Parse HTML/PDF → Extract structured content

02. Question Generation (part_a/)
   └── Split code into sections → Generate Q&A pairs with GPT-4.1

03. Vector Database (part_c/)
   └── Create Milvus schema → Generate embeddings → Populate database

04. Baseline Retrieval (part_d/)
   └── Test vector search accuracy on generated questions

05. No-RAG Responses (part_e/)
   └── Query LLMs directly → Calculate comparison metrics

06. Basic RAG Responses (part_f/)
   └── Vector search → Inject context → Generate responses → Calculate metrics

07. Agentic RAG Responses (part_g/)
   └── Multi-agent architecture → Iterative retrieval → Generate responses → Calculate metrics

08. Data Integration (part_h/)
   └── Merge all results into unified format

09. LLM Judge Evaluation (part_h_1/)
   └── Evaluate with multiple LLM judges → Score correctness and legal precision

10. Analysis (part_i/)
    └── Prepare flat CSVs → Statistical analysis → Visualization
    
11. Analysis (part_j/)
    └── Statistical analysis.
```

---

## 📊 Key Technologies Used

* **LLM Providers**: OpenAI (GPT-5 family), DeepSeek, Grok, Kimi
* **Frameworks**: Pydantic AI, pydantic_evals
* **Vector Database**: Milvus
* **Embedding Model**: `hiiamsid/sentence_similarity_spanish_es`
* **Metrics**: BLEU, ROUGE, BERTScore, SBERT Similarity, Jaccard, Levenshtein
* **Data Processing**: Polars, JSON

