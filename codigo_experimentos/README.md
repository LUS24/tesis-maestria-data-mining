# Thesis Notebooks

Notebooks that contain tests and proof of concepts for the Masters in Data Science, Austral University.

## Tasks organization

### Part A - Base questions set

#### Objective

Generate example questions for each "Título"/ from the updated text of the "Código de minería"

#### Tasks

* [X] A.1. Get the text from the updated "Código de minería" in md: [see text in html](https://servicios.infoleg.gob.ar/infolegInternet/anexos/40000-44999/43797/texact.htm)
    - Notes: The text was extracted from the html file
* [X] A.2. Extract each "Título" from the text
* [X] A.3. Use the best OpenaAI model to generate 1 question per "Título".
* [X] A.4. Pass the questions set to a human evaluator for a first iteration
* ~~[ ] A.5. Continue to iterate to improve the benchmark.~~
* [X] A.6. Explore how benchmarks should be organized and add that information to the doc files.
    - The following schemas files were created to represent the norms and questions.
        - [schemas/norm.json](schemas/norm.json)
        - [schemas/benchmark_question.json](schemas/benchmark_question.json)
        - [schemas/benchmark_question_context.json](schemas/benchmark_question_context.json)
    - They serve as a basic example about how the norms can be organized.
    - In [Part B](#part-b---initial-relational-database) the schemas will be used to define the structure of the relational database.
    - The file [20250804_101435_generated_questions - 130825.md](<part_a/20250804_101435_generated_questions - 130825.md>) will be used for:
        - Create a relational database for the benchmark questions for easier access.

### Part B - Initial relational database

#### Objective

Organize the norms and benchmark questions into a relational database

#### Tasks 1 - Norms Database - updated text

* ~~[ ] B.1.1. Explore the structure of the files for the [`titulos_codigo_mineria` directory.](data/law_data/titulos_codigo_mineria)~~
* ~~[ ] B.1.2. Create a database using the library [SQLModel](https://sqlmodel.tiangolo.com/) that respects the hierarchy of the parts of the law. Use the [law_database.py](part_b/law_database.py) file.~~

Created a python script with the norm data represented in a python dictionary that can be exported to json.
A relational database is not used for this since the structure of the norms is variable, even within a single norm.

For this reason, an object storage like a JSON file is more convenient due to its flexibility.

See the files [codigo_de_mineria_actualizado_2025_08_02.py](data/law_data/codigo_de_mineria_actualizado_2025_08_02.py) and [codigo_de_mineria_actualizado_2025_08_02.json](data/law_data/codigo_de_mineria_actualizado_2025_08_02.json).

#### Tasks 2 - Benchmark questions Database

* ~~[ ] B.2.1. Create a relational database for the benchmark questions in the file [20250804_101435_generated_questions - 130825.md](<part_a/20250804_101435_generated_questions - 130825.md>). Use the library [SQLModel](https://sqlmodel.tiangolo.com/) and put the code in the [questions_database.py](part_b/questions_database.py).~~
    - ~~Check the following schemas for the database creation:~~
        - ~~part_a/schemas/benchmark_question_contex.json~~
        - ~~part_a/schemas/benchmark_question.json~~
        - ~~part_a/schemas/norm.json~~



### Part C - Initial Vector Database

* [X] Select vector DB --> Milvus
* Select embedding model: https://chat.mistral.ai/chat/dc8b2de7-d6f7-4f4c-958c-4985f0ef0144 --> 'hiiamsid/sentence_similarity_spanish_es'
* [X] Select base vector size --> Determined by embedding model: 768
* [X] Select embedding granularity (Título/Sección/Artículo) --> Artículo
* [X] Generate embeddings and populate DB

### Part D - Evaluate retrieval without LLM curated db query.

* [X] Create script to:
    - load the question data
    - Generate embeddings from the question
    - Retrieve data from the vector db
    - Get the index of the retrieved articles that are useful to answer the question based on the articles listed as "Context references" in the questions file.
* [X] Based on the result determine how many articles should be retrieved for the RAG system. (set the limit in the db search.): from the results there isn't a clear cutoff value, some are near the top other really far.


### Part E - No RAG metrics

* [X] Pass the questions to an LLM with no RAG and store the results
* [X] Compare the reviewed answers to the LLM answers and calculate some metric.

### Part F - RAG metrics

* [X] Use the base RAG system to retrieve relevant text.
* [X] Pass the questions along with the text to an LLM with and store the answers results.
* [X] Calculate the metrics.

### Part G - Agentic RAG metrics

* [X] Create an Agentic RAG system
    * User interaction agent
    * Data retriever agent
    * ~~Vector DB MCP~~
* [X] Use the Agentic RAG system to retrieve relevant text.
* [X] Pass the questions along with the text to an LLM with and store the answers results.
* [X] Calculate the metrics.

### Part H - Integrate all data

* [X] Put all the data into the same file

### Part H 1 - Use LLM as a Judge to compare answers.

* [X] Do some prompt test in OpenWebUI
* [X] Select models
* [X] Iterate over all records

### Part I - Compare metrics

* [X] Compare metrics for the final response. Which strategy generated the best answer?
    - No RAG
    - Basic RAG
    - Agentic RAG
* [X] Analyze retrieval of the correct articles. Did the agentic rag improve final article retrieval?: tested later on using LLM as a Judge

Classical metrics don't show a difference between Basic RAG and Agentic RAG. --> This is the reason LLM as a Judge was used due to the complexity of the Law language.


### ~~Part K - Analyze metadata~~ --> Done in part_j 05_analisis_costos.ipynb

* Compare the different systems: number of tokens and costs
    - No RAG
    - Basic RAG
    - Agentic RAG

### Experiment A - Initial RAG vs NO RAG

* Decide evaluation metric
* Design statistical hypothesis testing
* Create initial evaluation experiment
    - Compare basic RAG vs No RAG
        - Select a model
        - Part A
            - Use base benchmark questions with the model
            - Store answers
        - Part B
            - With the same model, update the system prompt to inform about the tool availability
            - Use base benchmark questions with the model
            - Store answers
        - Part C
            - Using the curated answers for the questions, calculate the metric for Part A answers and Part B answers.
            - Perform hypothesis testing
            - Present results.

## Cancelled

Cancelled due to time constraints.

### ~~Part L - MVP with Gradio (If there is time) or FastAPI?~~: Cancelled due to time constraints

* Use gradio
    - https://www.udemy.com/course/llm-engineering-master-ai-and-large-language-models/learn/lecture/52940555#overview
    - https://www.gradio.app/guides/deploying-gradio-with-docker

### Part ? - Graph RAG

* Design and create a graph database for the código de minería.
    - Define nodes
    - Define edges
    - How embeddings would be used?: https://chat.mistral.ai/chat/21600859-759c-4771-9fb5-7775e84c670c
* Create Agentic Graph RAG system

### Experiment ? - NO RAG vs Initial RAG vs Graph RAG

Cancelled

### Experiment ? - Effect of embedding design

See: https://chat.mistral.ai/chat/dc8b2de7-d6f7-4f4c-958c-4985f0ef0144

* Variables
    - Embedding model
    - Embedding size

## Tools to parse HTMLs

See [these](html_transform_packages.md) html transformation packages and [these](python_toolkits_crawling_linguistics.md) other toolkits.
