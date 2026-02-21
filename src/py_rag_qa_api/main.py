from fastapi import FastAPI
from contextlib import asynccontextmanager
from sentence_transformers import SentenceTransformer
from py_rag_qa_api.db.store import createDBConnPool
from py_rag_qa_api.core.config import create_config
from py_rag_qa_api.api.routes import router
from openai import OpenAI
from py_rag_qa_api.service.rag_service import RAGService    
from py_rag_qa_api.core.app_state import AppState

@asynccontextmanager
async def lifespan(app: FastAPI):
    config = create_config()

    #load embedding model
    embeddingModel = SentenceTransformer("all-MiniLM-L6-v2")
    print("embedding model ready...")

    # llm model
    llmModel = OpenAI(
        api_key=config.openaiApiKey,
        base_url=config.openaiApiBase
    )
    print("LLM model ready...")

    ragService = RAGService(embedModel=embeddingModel, llmModel=llmModel)
    
    #connect to vector database
    dbConnPool = createDBConnPool(cfg=config)

    app.state.appState = AppState(
        dbConnPool=dbConnPool,
        ragService=ragService
    )
    
    yield
    #shutdown
    dbConnPool.closeall()
    print("shutting down server...")
    
app = FastAPI(lifespan=lifespan)

app.include_router(router=router)