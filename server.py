"""
Marketing AI Studio - FastAPI Backend Server
Microservicio REST y SSE Streaming para la Agencia de Marketing IA.
"""

import os
import json
import time
from pathlib import Path
from fastapi import FastAPI, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from pydantic import BaseModel
from typing import Optional, Dict, Any, List

from engine import engine, CAMPAIGNS_DIR

app = FastAPI(title="Marketing AI Studio Engine", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = Path(__file__).resolve().parent
GUI_DIR = BASE_DIR / "gui"

class GenerateRequest(BaseModel):
    agent_id: str
    prompt: str
    context_extra: Optional[str] = ""

class FullCampaignRequest(BaseModel):
    client_name: str
    niche: str
    product_desc: str
    target_audience: str

class SettingsRequest(BaseModel):
    api_key: str
    model: Optional[str] = "gemini-2.5-flash"

@app.get("/health")
def health_check():
    settings = engine.get_settings()
    return {
        "status": "healthy",
        "service": "marketing-ai-studio-engine",
        "timestamp": time.time(),
        "agents_loaded": len(engine.agents),
        "knowledge_base_ready": bool(engine.kb_summary),
        "has_api_key": settings["has_key"],
        "key_preview": settings["key_preview"]
    }

@app.get("/api/settings")
def get_settings():
    return engine.get_settings()

@app.post("/api/settings")
def update_settings(req: SettingsRequest):
    engine.save_settings(req.api_key, req.model or "gemini-2.5-flash")
    return {"status": "success", "message": "Configuración guardada correctamente", "settings": engine.get_settings()}

@app.get("/api/agents")
def get_agents():
    return {"agents": engine.get_available_agents()}

@app.post("/api/generate")
async def generate_content(req: GenerateRequest):
    if not req.prompt:
        raise HTTPException(status_code=400, detail="El prompt no puede estar vacío")
    
    result = await engine.execute_agent(
        agent_id=req.agent_id,
        prompt=req.prompt,
        context_extra=req.context_extra or ""
    )
    return {
        "status": "success",
        "agent_id": req.agent_id,
        "result": result
    }

@app.post("/api/campaign/parallel")
async def generate_parallel_campaign(req: FullCampaignRequest):
    if not req.client_name or not req.product_desc:
        raise HTTPException(status_code=400, detail="Faltan datos obligatorios para la campaña")

    result = await engine.run_parallel_campaign(
        client_name=req.client_name,
        niche=req.niche,
        product_desc=req.product_desc,
        target_audience=req.target_audience
    )
    return result

@app.get("/api/campaigns")
def list_campaigns():
    return {"campaigns": engine.list_saved_campaigns()}

@app.get("/api/campaigns/{campaign_id}/{filename}")
def get_campaign_file(campaign_id: str, filename: str):
    file_path = CAMPAIGNS_DIR / campaign_id / filename
    if not file_path.exists() or not file_path.is_file():
        raise HTTPException(status_code=404, detail="Archivo no encontrado")
    
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    return {"filename": filename, "content": content}

# Montar interfaz gráfica estática si existe
if GUI_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(GUI_DIR)), name="static")

@app.get("/")
def serve_index():
    index_file = GUI_DIR / "index.html"
    if index_file.exists():
        return FileResponse(str(index_file))
    return HTMLResponse("<h2>Marketing AI Studio Backend Running. GUI not found in /gui.</h2>")

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8090))
    print(f"🚀 Iniciando Marketing AI Studio Engine en http://127.0.0.1:{port}")
    uvicorn.run("server:app", host="0.0.0.0", port=port, reload=False)
