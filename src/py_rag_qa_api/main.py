from fastapi import FastAPI, Request
from pydantic import BaseModel
from contextlib import asynccontextmanager
from sentence_transformers import SentenceTransformer
from py_rag_qa_api.vectordb.store import connect
from py_rag_qa_api.config.settings import create_config, Config
from py_rag_qa_api.api.routes import router
import psycopg2
from openai import OpenAI

class QA(BaseModel):
    question: str

@asynccontextmanager
async def lifespan(app: FastAPI):
    #load embedding model
    app.state.embed_model = SentenceTransformer("all-MiniLM-l6-v2")
    print("embedding model loaded")

    #connect to vector database
    cfg = create_config()
    app.state.cfg = cfg
    app.state.db_conn = connect(cfg=cfg)
    print("database connected")

    yield
    #shutdown
    print("shutting down server...")
    
app = FastAPI(lifespan=lifespan)


@app.post("/answer")
async def answer(qa:QA, req: Request):
    cfg: Config = req.app.state.cfg

    llm = OpenAI(
        api_key=cfg.openaiApiKey,
        base_url=cfg.openaiApiBase
    )
    llmID = llm.models.list().data[0].id

    embed_model: SentenceTransformer = req.app.state.embed_model
    db_conn: psycopg2.extensions.connection = req.app.state.db_conn

    cur = db_conn.cursor()

    queryEmbedding = embed_model.encode(qa.question)

    cur.execute("SELECT content FROM cat_facts ORDER BY embedding <=> %s::vector LIMIT 3;", (queryEmbedding.tolist(), )) #biar jadi tuple (queryEmbedding.tolist(), ), kalau queryembedding.tolist() doang bukan. ::vector maksa jadi vector
    result = cur.fetchmany()
    cur.close()
    
    context = "\n\n".join(
    f"{row[0]}"
    for row in result
    )


    instruction = f""""
    You are a helpful chatbor to answer question about cat facts.
    Answer the question using ONLY relevant information from the context.
    Ignore any information that is not related to the question.

    If the answer is not found in the context, say you dont know.

    Context:
    {context}

    Question:
    {qa.question}

    Answer:
    """

    response = llm.responses.create(
        model=llmID,
        instructions=instruction,
        input=qa.question,
    )
    return {
        "answer":response.output_text
    }