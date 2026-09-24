"""
Marketing AI Studio V3 - FastAPI Server
Server API con cabeceras strict Anti-Caché para la Web App Conversacional.
"""

import os
import json
import time
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from pydantic import BaseModel
from typing import Optional, Dict, Any, List

from engine import engine, CAMPAIGNS_DIR, SESSIONS_DIR

app = FastAPI(title="Marketing AI Studio Engine V3", version="3.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = Path(__file__).resolve().parent
GUI_DIR = BASE_DIR / "gui"

class ChatMessageRequest(BaseModel):
    agent_id: str
    session_id: Optional[str] = None
    message: str
    handoff_context: Optional[str] = ""

class NewSessionRequest(BaseModel):
    title: Optional[str] = "Nueva Campaña Guiada"

class HandoffRequest(BaseModel):
    target_agent_id: str
    step: Optional[int] = 0
    handoff_context: Optional[str] = ""

@app.get("/health")
def health_check():
    email = engine.get_active_user_email()
    return {
        "status": "healthy",
        "service": "marketing-ai-studio-engine-v3",
        "timestamp": time.time(),
        "agents_loaded": len(engine.agents),
        "knowledge_base_ready": bool(engine.kb_summary),
        "authenticated_account": email,
        "model": "gemini-3.7-flash (Medium)"
    }

@app.get("/api/agents")
def get_agents():
    return {"agents": engine.get_available_agents()}

@app.get("/api/sessions")
def list_sessions():
    return {"sessions": engine.list_sessions()}

@app.post("/api/sessions/new")
def create_session(req: NewSessionRequest):
    session = engine.get_or_create_session(title=req.title)
    return {"status": "success", "session": session}

@app.get("/api/sessions/{session_id}")
def get_session(session_id: str):
    session = engine.load_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Sesión no encontrada")
    return {"session": session}

@app.post("/api/chat/send")
async def chat_send(req: ChatMessageRequest):
    if not req.message:
        raise HTTPException(status_code=400, detail="El mensaje no puede estar vacío")
    
    res = await engine.execute_agent_chat(
        agent_id=req.agent_id,
        session_id=req.session_id,
        user_message=req.message,
        handoff_context=req.handoff_context or ""
    )
    return res

@app.post("/api/sessions/{session_id}/handoff")
def session_handoff(session_id: str, req: HandoffRequest):
    session = engine.load_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Sesión no encontrada")
    
    session["active_agent_id"] = req.target_agent_id
    session["current_step"] = req.step if req.step is not None else session.get("current_step", 0) + 1
    engine.save_session(session)
    return {"status": "success", "session": session}

if GUI_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(GUI_DIR)), name="static")

@app.get("/")
def serve_index():
    index_file = GUI_DIR / "index.html"
    if index_file.exists():
        response = FileResponse(str(index_file))
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
        return response
    return HTMLResponse("<h2>Marketing AI Studio V3 Backend Running.</h2>")

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8090))
    print(f"🚀 Iniciando Marketing AI Studio V3 en http://127.0.0.1:{port}")
    uvicorn.run("server:app", host="0.0.0.0", port=port, reload=False)
