from fastapi import Request
from py_rag_qa_api.core.app_state import AppState
import psycopg2

def get_db_conn(req: Request):
    appState: AppState = req.app.state.appState
    pool = appState.dbConnPool

    dbConn: psycopg2.extensions.connection = pool.getconn()

    try:
        yield dbConn
    finally:
        pool.putconn(dbConn)