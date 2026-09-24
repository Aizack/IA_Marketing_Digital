"""
Marketing AI Studio - FastAPI Backend Server
Microservicio REST y OAuth Bridge para vincular la 2da cuenta de Google Pro.
"""

import os
import json
import time
from pathlib import Path
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse, RedirectResponse
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

@app.get("/health")
def health_check():
    email = engine.get_active_user_email()
    return {
        "status": "healthy",
        "service": "marketing-ai-studio-engine",
        "timestamp": time.time(),
        "agents_loaded": len(engine.agents),
        "knowledge_base_ready": bool(engine.kb_summary),
        "authenticated_account": email or None,
        "is_authenticated": bool(email)
    }

# =========================================================================
# RUTAS DE AUTENTICACIÓN OAUTH CON GOOGLE (2DA CUENTA)
# =========================================================================
@app.get("/auth/login")
def auth_login():
    """Redirige al flujo oficial de OAuth de Google para elegir isacdiazb@gmail.com"""
    auth_url = engine.get_auth_url(redirect_uri="http://localhost:8090/auth/callback")
    return RedirectResponse(url=auth_url)

@app.get("/auth/callback")
def auth_callback(code: Optional[str] = None, error: Optional[str] = None):
    if error:
        return HTMLResponse(f"""
        <body style="background:#0b0f19;color:#fff;font-family:sans-serif;display:flex;align-items:center;justify-content:center;height:100vh;">
            <div style="background:#1e293b;padding:2rem;border-radius:1rem;max-width:500px;text-align:center;">
                <h2 style="color:#f87171;">⚠️ Error de Autorización</h2>
                <p style="color:#94a3b8;">{error}</p>
                <a href="/" style="color:#818cf8;">Volver al Studio</a>
            </div>
        </body>
        """)

    if not code:
        raise HTTPException(status_code=400, detail="Código de autorización no recibido")

    try:
        engine.exchange_code_for_tokens(code, redirect_uri="http://localhost:8090/auth/callback")
        email = engine.get_active_user_email()
        return HTMLResponse(f"""
        <body style="background:#080c15;color:#fff;font-family:'Segoe UI',sans-serif;display:flex;align-items:center;justify-content:center;height:100vh;">
            <div style="background:#131b2e;padding:2.5rem;border-radius:1.25rem;max-width:550px;text-align:center;border:1px solid #334155;box-shadow:0 20px 25px -5px rgba(0,0,0,0.5);">
                <div style="font-size:3rem;margin-bottom:1rem;">🎉</div>
                <h2 style="color:#34d399;margin-bottom:0.5rem;font-size:1.5rem;">¡Segunda Cuenta Vinculada con Éxito!</h2>
                <p style="color:#cbd5e1;font-size:1rem;margin-bottom:1.5rem;">
                    La sesión ha quedado configurada de forma 100% aislada para:<br>
                    <strong style="color:#818cf8;font-size:1.1rem;">{email or 'isacdiazb@gmail.com'}</strong>
                </p>
                <div style="margin-top:2rem;">
                    <a href="/" style="background:#6366f1;color:#fff;padding:0.75rem 1.75rem;border-radius:0.75rem;text-decoration:none;font-weight:600;display:inline-block;">Ir al Marketing AI Studio</a>
                </div>
            </div>
        </body>
        """)
    except Exception as e:
        return HTMLResponse(f"""
        <body style="background:#0b0f19;color:#fff;font-family:sans-serif;display:flex;align-items:center;justify-content:center;height:100vh;">
            <div style="background:#1e293b;padding:2rem;border-radius:1rem;max-width:500px;text-align:center;">
                <h2 style="color:#f87171;">Error vinculando cuenta</h2>
                <p style="color:#94a3b8;">{e}</p>
                <a href="/auth/login" style="color:#818cf8;">Reintentar</a>
            </div>
        </body>
        """)

@app.get("/auth/status")
def auth_status():
    email = engine.get_active_user_email()
    return {
        "authenticated": bool(email),
        "email": email
    }

# =========================================================================
# RUTAS DE AGENTES Y GENERACIÓN
# =========================================================================
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
