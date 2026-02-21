from fastapi import Request
from py_rag_qa_api.core.app_state import AppState

def get_rag_service(req: Request):
    appState: AppState = req.app.state.appState
    return appState.ragService