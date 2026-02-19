# Python RAG-Based QA API

## How to run

set PYTHONPATH

```bash
set PYTHONPATH=src
```

run ingest.py to add dataset to vector database

```bash
uv run -m py_rag_qa_api.ingestion.ingest
```

run main.py to run server

```bash
uv run uvicorn py_rag_qa_api.main:app --reload
```
