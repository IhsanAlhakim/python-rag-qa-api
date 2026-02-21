from dataclasses import dataclass
import psycopg2.pool
from py_rag_qa_api.service.rag_service import RAGService

@dataclass
class AppState:
    dbConnPool: psycopg2.pool.ThreadedConnectionPool
    ragService: RAGService 
