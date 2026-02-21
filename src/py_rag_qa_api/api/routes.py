from fastapi import APIRouter, Depends
from pydantic import BaseModel
from py_rag_qa_api.dependencies.db_conn import get_db_conn
from py_rag_qa_api.dependencies.rag_service import get_rag_service


class QA(BaseModel):
    question: str    

router = APIRouter()

@router.post("/answer")
async def answer(
    qa:QA,
    dbConn = Depends(get_db_conn),
    ragService = Depends(get_rag_service)
    ):

    answer = ragService.answer(
        dbConn=dbConn,
        question=qa.question
    )
    
    return {
        "answer":answer
    }