# DocSense PDF

A retrieval-augmented generation (RAG) API built with FastAPI, LangChain, Qdrant, FastEmbed, and Ollama.

The application lets you:

- Upload PDF documents.
- Split PDF text into searchable chunks.
- Generate local embeddings with `BAAI/bge-small-en-v1.5`.
- Store and search document vectors in Qdrant.
- Ask questions and receive answers based on the most relevant document content.

## Architecture

```text
PDF upload
    |
    v
PyPDFLoader -> Text splitter -> FastEmbed embeddings -> Qdrant
                                                        |
Question -> FastEmbed embedding -> Similarity search ----+
                                                        |
                                                        v
                                             Ollama LLM -> Answer
```

## Technologies

- **FastAPI** - API framework
- **LangChain** - document processing and LLM integration
- **FastEmbed** - local text embeddings
- **Qdrant** - vector database
- **Ollama** - local language model runtime
- **PyPDF** - PDF loading

## Prerequisites

Install the following software:

1. Python 3.10 or newer
2. Docker Desktop
3. Ollama

Verify the installations:

```powershell
python --version
docker --version
ollama --version
```

## Installation

Clone the repository and enter the project directory:

```powershell
git clone https://github.com/<your-username>/docsense-pdf.git
cd docsense-pdf
```

Create and activate a virtual environment:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

Install the Python dependencies:

```powershell
pip install -r requirements.txt
```

Create your local environment file:

```powershell
Copy-Item .env.example .env
```

Update `.env` if you want to use a different Qdrant collection or Ollama model.

## Start the services

Start Qdrant with Docker Compose:

```powershell
docker compose up -d
```

Download the Ollama model configured in `.env`. For the default configuration:

```powershell
ollama pull llama3.2:3b
```

If you configure a different model, pull that model instead:

```powershell
ollama pull <your-model-name>
```

Start the FastAPI application:

```powershell
uvicorn app.main:app --reload
```

The API is available at:

```text
http://127.0.0.1:8000
```

Interactive API documentation:

- Swagger UI: <http://127.0.0.1:8000/docs>
- ReDoc: <http://127.0.0.1:8000/redoc>

## Environment variables

Copy `.env.example` to `.env` and configure these values:

| Variable | Description | Default |
|---|---|---|
| `QDRANT_URL` | Qdrant server URL | `http://localhost:6333` |
| `COLLECTION_NAME` | Qdrant collection for document vectors | `documents` |
| `OLLAMA_MODEL` | Ollama model used to generate answers | `llama3.2:3b` |
| `TEMPERATURE` | LLM response randomness | `0` |

Never commit `.env`. It is excluded by `.gitignore`.

## API usage

### Health check

```http
GET /
```

Response:

```json
{
  "message": "Welcome to the RAG FastAPI application!"
}
```

### Upload a PDF

```http
POST /upload/
Content-Type: multipart/form-data
```

Example with PowerShell:

```powershell
curl.exe -X POST "http://127.0.0.1:8000/upload/" `
  -F "file=@.\path\to\document.pdf"
```

Example response:

```json
{
  "message": "PDF uploaded successfully",
  "file_name": "document.pdf",
  "pages": 5,
  "chunks": 12
}
```

Only PDF files are accepted. Uploaded files are processed and then removed from the local `uploads` directory.

### Ask a question

```http
POST /query/
Content-Type: application/json
```

Request:

```json
{
  "question": "What is this document about?"
}
```

Example with PowerShell:

```powershell
curl.exe -X POST "http://127.0.0.1:8000/query/" `
  -H "Content-Type: application/json" `
  -d '{"question":"What is this document about?"}'
```

Example response:

```json
{
  "question": "What is this document about?",
  "answer": "The document is about ...",
  "page_numbers": [0, 2, 3]
}
```

Upload at least one PDF before querying. The query endpoint retrieves the three most relevant chunks from Qdrant and sends them to the configured Ollama model.

## Project structure

```text
RAG/
├── app/
│   ├── core/
│   │   └── config.py              # Environment configuration
│   ├── prompts/
│   │   └── rag_prompt.py          # RAG prompt template
│   ├── routes/
│   │   ├── query.py               # Question answering endpoint
│   │   └── upload.py              # PDF upload endpoint
│   ├── schemas/
│   │   ├── query.py               # Query request and response models
│   │   └── upload.py              # Upload response model
│   ├── services/
│   │   ├── document_processor.py  # PDF loading, splitting, and indexing
│   │   ├── embeddings.py          # Cached embedding factory
│   │   ├── llm.py                 # Ollama model configuration
│   │   ├── rag.py                 # Retrieval and answer generation
│   │   └── vector_store.py        # Qdrant vector store access
│   └── main.py                    # FastAPI application
├── .env.example                   # Safe environment template
├── docker-compose.yml             # Qdrant service
├── requirements.txt               # Python dependencies
└── README.md
```

## Stopping services

Stop the Qdrant container:

```powershell
docker compose down
```

The Ollama service runs separately and can be stopped through the Ollama application or system service.

## Important notes

- The first embedding request may download the FastEmbed model.
- The Qdrant collection must use the same embedding model dimensions as the application.
- If you change the embedding model, recreate the Qdrant collection before indexing documents again.
- Keep secrets and local configuration in `.env`, not in source code.
