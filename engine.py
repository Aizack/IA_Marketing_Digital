"""
Marketing AI Studio - Core Engine & Multi-Agent Orchestrator
Nivel 1: Manifiestos de Agentes (.antigravity/agentes/*.md)
Nivel 2: Subagentes Autónomos en Paralelo (Background Workers)
Motor: Google Cloud / Gemini AI Companion con Sesión OAuth Pro (PKCE + Client Secret)
"""

import os
import re
import json
import time
import glob
import base64
import hashlib
import secrets
import urllib.parse
import urllib.request
import asyncio
from pathlib import Path
from typing import Dict, List, Any, Optional

BASE_DIR = Path(__file__).resolve().parent
AGENTS_DIR = BASE_DIR / ".antigravity" / "agentes"
CREDS_FILE = BASE_DIR / "oauth_creds_marketing.json"
PKCE_STATE_FILE = BASE_DIR / ".pkce_state.json"
PORTABLE_AGY_BIN = Path("D:/Antigravity_Marketing/bin/agy.exe")
PORTABLE_DATA_DIR = Path("D:/Antigravity_Marketing/data")
CAMPAIGNS_DIR.mkdir(parents=True, exist_ok=True)

def _load_oauth_config() -> tuple:
    oauth_file = BASE_DIR / "oauth_config.json"
    if oauth_file.exists():
        try:
            with open(oauth_file, "r", encoding="utf-8") as f:
                d = json.load(f)
                return d.get("client_id", ""), d.get("client_secret", "")
        except Exception:
            pass
    return os.environ.get("GOOGLE_CLIENT_ID", ""), os.environ.get("GOOGLE_CLIENT_SECRET", "")

GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET = _load_oauth_config()
GOOGLE_SCOPES = "openid https://www.googleapis.com/auth/cloud-platform https://www.googleapis.com/auth/userinfo.profile https://www.googleapis.com/auth/userinfo.email"

class AgentManifest:
    def __init__(self, filename: str, content: str):
        self.filename = filename
        self.agent_id = filename.replace(".md", "")
        self.content = content
        self.name = self._extract_title()
        self.role = self._extract_role()

    def _extract_title(self) -> str:
        match = re.search(r"^#\s+(.+)$", self.content, re.MULTILINE)
        return match.group(1).strip() if match else self.agent_id

    def _extract_role(self) -> str:
        match = re.search(r"\*\*Rol Principal:\*\*\s+(.+)$", self.content, re.MULTILINE)
        return match.group(1).strip() if match else "Agente Especialista"

    def get_system_prompt(self) -> str:
        return self.content


class MarketingEngine:
    def __init__(self):
        self.agents: Dict[str, AgentManifest] = {}
        self.kb_summary: str = ""
        self.creds: Dict[str, Any] = self._load_creds()
        self.reload_agents()
        self.load_knowledge_base()

    def _load_creds(self) -> Dict[str, Any]:
        """Carga las credenciales de la 2da cuenta aislada de Google"""
        # 1. Portable D: drive
        portable_file = PORTABLE_DATA_DIR / ".gemini" / "oauth_creds.json"
        if portable_file.exists():
            try:
                with open(portable_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass

        # 2. Archivo local del proyecto
        if CREDS_FILE.exists():
            try:
                with open(CREDS_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        
        # 3. Perfil en .gemini_marketing
        mkt_file = Path("C:/Users/PC/.gemini_marketing/.gemini/oauth_creds.json")
        if mkt_file.exists():
            try:
                with open(mkt_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass

        # 4. /root/.gemini en Docker
        docker_file = Path("/root/.gemini/oauth_creds.json")
        if docker_file.exists():
            try:
                with open(docker_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass

        return {}

    def get_active_user_email(self) -> str:
        if not self.creds:
            return ""
        id_token = self.creds.get("id_token", "")
        if id_token and "." in id_token:
            try:
                payload = id_token.split(".")[1]
                payload += "=" * ((4 - len(payload) % 4) % 4)
                data = json.loads(base64.urlsafe_b64decode(payload).decode("utf-8"))
                return data.get("email", "")
            except Exception:
                pass
        return self.creds.get("email", "")

    def get_auth_url(self, redirect_uri: str = "http://localhost:8090/auth/callback") -> str:
        """Genera el enlace de login con PKCE para conectar isacdiazb@gmail.com"""
        verifier = secrets.token_urlsafe(64)
        challenge = base64.urlsafe_b64encode(hashlib.sha256(verifier.encode("ascii")).digest()).decode("ascii").rstrip("=")
        
        # Guardar verifier temporal para el intercambio
        with open(PKCE_STATE_FILE, "w", encoding="utf-8") as f:
            json.dump({"verifier": verifier, "redirect_uri": redirect_uri}, f)

        params = {
            "client_id": GOOGLE_CLIENT_ID,
            "redirect_uri": redirect_uri,
            "response_type": "code",
            "scope": GOOGLE_SCOPES,
            "code_challenge": challenge,
            "code_challenge_method": "S256",
            "access_type": "offline",
            "prompt": "consent select_account"
        }
        return f"https://accounts.google.com/o/oauth2/v2/auth?{urllib.parse.urlencode(params)}"

    def exchange_code_for_tokens(self, code: str, redirect_uri: str = "http://localhost:8090/auth/callback") -> Dict[str, Any]:
        """Intercambia el código de autorización por los tokens OAuth de Google usando PKCE y Client Secret"""
        verifier = ""
        if PKCE_STATE_FILE.exists():
            try:
                with open(PKCE_STATE_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    verifier = data.get("verifier", "")
                    redirect_uri = data.get("redirect_uri", redirect_uri)
            except Exception:
                pass

        token_url = "https://oauth2.googleapis.com/token"
        params = {
            "code": code,
            "client_id": GOOGLE_CLIENT_ID,
            "client_secret": GOOGLE_CLIENT_SECRET,
            "redirect_uri": redirect_uri,
            "grant_type": "authorization_code"
        }
        if verifier:
            params["code_verifier"] = verifier

        data = urllib.parse.urlencode(params).encode("utf-8")

        req = urllib.request.Request(token_url, data=data, headers={"Content-Type": "application/x-www-form-urlencoded"})
        with urllib.request.urlopen(req) as resp:
            token_data = json.loads(resp.read().decode("utf-8"))

        self.creds = token_data
        email = self.get_active_user_email()
        if email:
            self.creds["email"] = email

        with open(CREDS_FILE, "w", encoding="utf-8") as f:
            json.dump(self.creds, f, indent=2)

        if PKCE_STATE_FILE.exists():
            try:
                PKCE_STATE_FILE.unlink()
            except Exception:
                pass

        return self.creds

    def get_valid_access_token(self) -> Optional[str]:
        """Obtiene o refresca el token de acceso OAuth"""
        if not self.creds:
            self.creds = self._load_creds()
        if not self.creds:
            return None

        refresh_token = self.creds.get("refresh_token")
        if refresh_token:
            try:
                token_url = "https://oauth2.googleapis.com/token"
                data = urllib.parse.urlencode({
                    "client_id": GOOGLE_CLIENT_ID,
                    "client_secret": GOOGLE_CLIENT_SECRET,
                    "refresh_token": refresh_token,
                    "grant_type": "refresh_token"
                }).encode("utf-8")
                req = urllib.request.Request(token_url, data=data, headers={"Content-Type": "application/x-www-form-urlencoded"})
                with urllib.request.urlopen(req) as resp:
                    refreshed = json.loads(resp.read().decode("utf-8"))
                    self.creds["access_token"] = refreshed["access_token"]
                    with open(CREDS_FILE, "w", encoding="utf-8") as f:
                        json.dump(self.creds, f, indent=2)
                    return refreshed["access_token"]
            except Exception as e:
                print(f"[Engine] Error refrescando token: {e}")

        return self.creds.get("access_token")

    def reload_agents(self):
        """Carga en vivo los manifiestos de agentes desde .antigravity/agentes/"""
        self.agents.clear()
        if not AGENTS_DIR.exists():
            return
        
        for file in sorted(AGENTS_DIR.glob("*.md")):
            with open(file, "r", encoding="utf-8") as f:
                content = f.read()
                manifest = AgentManifest(file.name, content)
                self.agents[manifest.agent_id] = manifest

    def load_knowledge_base(self):
        """Indexa los archivos clave de la base de conocimiento"""
        summaries = []
        if KB_DIR.exists():
            for file in KB_DIR.rglob("*.md"):
                summaries.append(f"- {file.relative_to(KB_DIR)}")
            for file in KB_DIR.rglob("*.txt"):
                summaries.append(f"- {file.relative_to(KB_DIR)}")
        self.kb_summary = "\n".join(summaries[:50])

    def get_available_agents(self) -> List[Dict[str, Any]]:
        self.reload_agents()
        return [
            {
                "id": a.agent_id,
                "name": a.name,
                "role": a.role,
                "file": a.filename
            }
            for a in self.agents.values()
        ]

    async def execute_agent(self, agent_id: str, prompt: str, context_extra: str = "") -> str:
        """
        Ejecuta el agente utilizando el token OAuth de tu 2da cuenta de Google Pro.
        """
        manifest = self.agents.get(agent_id)
        if not manifest:
            self.reload_agents()
            manifest = self.agents.get(agent_id)

        system_rules = manifest.get_system_prompt() if manifest else ""
        
        full_system = f"""{system_rules}

---
BASE DE CONOCIMIENTO DISPONIBLE EN EL SISTEMA:
{self.kb_summary}

INSTRUCCIONES CLAVE:
1. Aplica estrictamente las metodologías del manifiesto (Eugene Schwartz, 12 Ángulos, Método 6C, Made to Stick SUCCESs o formatos UGC).
2. Desarrolla respuestas detalladas, completas y accionables. No resumas ni recortes la entrega.
3. Formatea todo con Markdown profesional, tablas estructuradas, negritas y llamadas a la acción claras.
"""
        # 1. Intentar ejecución vía Antigravity Portable en Disco D:
        if PORTABLE_AGY_BIN.exists():
            try:
                env = os.environ.copy()
                env["USERPROFILE"] = str(PORTABLE_DATA_DIR)
                env["HOME"] = str(PORTABLE_DATA_DIR)
                env["HOMEDRIVE"] = "D:"
                env["HOMEPATH"] = "\\Antigravity_Marketing\\data"
                env["PYTHONIOENCODING"] = "utf-8"

                full_prompt = f"""{system_rules}

---
BASE DE CONOCIMIENTO LOCAL:
{self.kb_summary}

---
CONTEXTO ADICIONAL:
{context_extra}

---
BRIEF DE AGENCIA:
{prompt}
"""
                proc = await asyncio.create_subprocess_exec(
                    str(PORTABLE_AGY_BIN),
                    "--print",
                    full_prompt,
                    "--dangerously-skip-permissions",
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE,
                    env=env,
                    cwd=str(BASE_DIR)
                )
                stdout, stderr = await proc.communicate()
                output_text = stdout.decode("utf-8", errors="replace").strip()
                if output_text and len(output_text) > 50:
                    return output_text
            except Exception as e:
                print(f"[Engine] Error ejecutando Antigravity Portable D:: {e}")

        # 2. Intentar llamada con token OAuth
        token = self.get_valid_access_token()
        if token:
            try:
                url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"
                payload = {
                    "contents": [{
                        "parts": [{"text": f"Contexto adicional: {context_extra}\n\nBrief del usuario:\n{prompt}"}]
                    }],
                    "systemInstruction": {
                        "parts": [{"text": full_system}]
                    }
                }
                req = urllib.request.Request(
                    url,
                    data=json.dumps(payload).encode("utf-8"),
                    headers={
                        "Authorization": f"Bearer {token}",
                        "Content-Type": "application/json"
                    }
                )
                with urllib.request.urlopen(req, timeout=90) as resp:
                    res_json = json.loads(resp.read().decode("utf-8"))
                    text = res_json["candidates"][0]["content"]["parts"][0]["text"]
                    return text
            except Exception as e:
                print(f"[Engine] Error en llamada con OAuth: {e}")

        return f"""# 🔑 Vinculación Requerida para Antigravity Pro en Disco D:

Para procesar tus solicitudes usando tu suscripción Pro de Google en la carpeta aislada de `D:\\Antigravity_Marketing`:

1. Haz doble clic en el acceso directo de tu Escritorio **`Antigravity Pro (Disco D)`**.
2. En la consola negra que se abre, escribe: `hola` (y presiona Enter).
3. Se abrirá el navegador para seleccionar tu segunda cuenta **`isacdiazb@gmail.com`**.
4. ¡Listo! La sesión se guardará 100% aislada en Disco D: sin tocar tu cuenta del ERP.

---
### 📋 Solicitud en Espera:
* **Agente:** `{agent_id}`
* **Brief:** {prompt}
"""

    async def run_parallel_campaign(self, client_name: str, niche: str, product_desc: str, target_audience: str) -> Dict[str, Any]:
        """
        NIVEL 2: Lanza 4 subagentes autónomos en paralelo para crear una campaña 360° completa.
        """
        slug = re.sub(r'[^a-zA-Z0-9_-]', '_', client_name.lower())
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        campaign_folder = CAMPAIGNS_DIR / f"{timestamp}_{slug}"
        campaign_folder.mkdir(parents=True, exist_ok=True)

        brief_text = f"""
CLIENTE / MARCA: {client_name}
NICHO: {niche}
DESCRIPCIÓN DE LA OFERTA: {product_desc}
AUDIENCIA OBJETIVO: {target_audience}
"""

        async def task_estratega():
            prompt = f"Desarrolla el diagnóstico completo del Avatar, Nivel de Sofisticación, 3 Ángulos de Venta ganadores, el Mecanismo Único y la Oferta Irresistible para:\n{brief_text}"
            res = await self.execute_agent("01_director_estratega_marketing", prompt)
            with open(campaign_folder / "01_Estrategia_y_Avatar.md", "w", encoding="utf-8") as f:
                f.write(res)
            return {"module": "estratega", "title": "🎯 Estrategia & Avatar", "result": res}

        async def task_ugc():
            prompt = f"Escribe 2 Guiones UGC audiovisuales completos clip a clip (uno formato 'Voz en off con B-roll' y otro formato 'Hablando a cámara') para:\n{brief_text}"
            res = await self.execute_agent("02_guionista_ugc_clip_a_clip", prompt)
            with open(campaign_folder / "02_Guiones_UGC_Clip_a_Clip.md", "w", encoding="utf-8") as f:
                f.write(res)
            return {"module": "ugc", "title": "🎬 Guiones UGC Clip a Clip", "result": res}

        async def task_prompts_6c():
            prompt = f"Genera 5 Prompts hiperrealistas en inglés bajo la fórmula 6C (Context, Character, Camera, Composition, Color/Lighting, Consistency) para los anuncios de:\n{brief_text}"
            res = await self.execute_agent("03_ingeniero_prompts_visuales_6c", prompt)
            with open(campaign_folder / "03_Prompts_Visuales_6C.md", "w", encoding="utf-8") as f:
                f.write(res)
            return {"module": "prompts_6c", "title": "🎨 Prompts Visuales 6C", "result": res}

        async def task_organico():
            prompt = f"Diseña una parrilla de contenido orgánico de 7 días y 2 posts de autoridad aplicando el modelo Made to Stick (SUCCESs) para:\n{brief_text}"
            res = await self.execute_agent("04_creador_contenido_pegajoso", prompt)
            with open(campaign_folder / "04_Contenido_Organico_SUCCESs.md", "w", encoding="utf-8") as f:
                f.write(res)
            return {"module": "organico", "title": "🧲 Contenido Orgánico Made to Stick", "result": res}

        results = await asyncio.gather(
            task_estratega(),
            task_ugc(),
            task_prompts_6c(),
            task_organico(),
            return_exceptions=True
        )

        master_report = f"""# 🚀 Campaña 360°: {client_name}
**Nicho:** {niche}
**Fecha:** {time.strftime('%Y-%m-%d %H:%M:%S')}
**Carpeta:** `{campaign_folder.name}`

---
## 📁 Entregables Generados:
1. `01_Estrategia_y_Avatar.md`
2. `02_Guiones_UGC_Clip_a_Clip.md`
3. `03_Prompts_Visuales_6C.md`
4. `04_Contenido_Organico_SUCCESs.md`
"""
        with open(campaign_folder / "README_Campana.md", "w", encoding="utf-8") as f:
            f.write(master_report)

        return {
            "status": "success",
            "campaign_id": campaign_folder.name,
            "path": str(campaign_folder),
            "modules": [r for r in results if not isinstance(r, Exception)]
        }

    def list_saved_campaigns(self) -> List[Dict[str, Any]]:
        campaigns = []
        if not CAMPAIGNS_DIR.exists():
            return campaigns

        for folder in sorted(CAMPAIGNS_DIR.iterdir(), reverse=True):
            if folder.is_dir():
                files = [f.name for f in folder.glob("*.md")]
                campaigns.append({
                    "id": folder.name,
                    "path": str(folder),
                    "created_at": folder.stat().st_ctime,
                    "files": files
                })
        return campaigns

engine = MarketingEngine()
