"""
Marketing AI Studio - Core Engine & Multi-Agent Orchestrator
Nivel 1: Manifiestos de Agentes (.antigravity/agentes/*.md)
Nivel 2: Subagentes Autónomos en Paralelo (Background Workers)
Motor LLM: Google GenAI SDK (Gemini 2.5/2.0 Flash / Pro) + Antigravity CLI
"""

import os
import re
import json
import time
import glob
import asyncio
from pathlib import Path
from typing import Dict, List, Any, Optional

BASE_DIR = Path(__file__).resolve().parent
AGENTS_DIR = BASE_DIR / ".antigravity" / "agentes"
KB_DIR = BASE_DIR / "knowledge_base"
CAMPAIGNS_DIR = BASE_DIR / "campaigns"
CONFIG_FILE = BASE_DIR / "config.json"
CAMPAIGNS_DIR.mkdir(parents=True, exist_ok=True)

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
        self.api_key: str = self._load_api_key()
        self.model_name: str = "gemini-2.5-flash"
        self.reload_agents()
        self.load_knowledge_base()

    def _load_api_key(self) -> str:
        # 1. Desde variable de entorno
        key = os.environ.get("GEMINI_API_KEY", "")
        if key:
            return key
        # 2. Desde config.json
        if CONFIG_FILE.exists():
            try:
                with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    return data.get("api_key", "")
            except Exception:
                pass
        return ""

    def save_settings(self, api_key: str, model_name: str = "gemini-2.5-flash"):
        self.api_key = api_key.strip()
        self.model_name = model_name
        os.environ["GEMINI_API_KEY"] = self.api_key
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump({"api_key": self.api_key, "model": self.model_name}, f, indent=2)

    def get_settings(self) -> Dict[str, Any]:
        return {
            "has_key": bool(self.api_key),
            "key_preview": f"{self.api_key[:6]}...{self.api_key[-4:]}" if len(self.api_key) > 10 else "",
            "model": self.model_name
        }

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
        Ejecuta el agente con su manifiesto, la base de conocimiento y el modelo de IA.
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

        # 1. Ejecutar con Google GenAI SDK si hay API Key configurada
        if self.api_key:
            try:
                from google import genai
                client = genai.Client(api_key=self.api_key)
                
                # Intentar modelos en orden de preferencia
                models_to_try = [self.model_name, "gemini-2.5-flash", "gemini-2.0-flash", "gemini-1.5-flash"]
                last_error = None
                
                for m in models_to_try:
                    try:
                        response = client.models.generate_content(
                            model=m,
                            contents=f"Contexto adicional: {context_extra}\n\nBrief del usuario:\n{prompt}",
                            config={"system_instruction": full_system}
                        )
                        if response and response.text:
                            return response.text
                    except Exception as err:
                        last_error = err
                        continue

                if last_error:
                    return f"⚠️ Error llamando a Gemini ({last_error}). Verifica tu API Key en Configuración."
            except Exception as e:
                print(f"[Engine] Error en Google GenAI: {e}")

        # 2. Si no hay API Key configurada, mostrar guía amigable en el resultado
        return f"""# ⚠️ API Key Requerida para Generación en Vivo

Para activar las respuestas de IA en vivo sin límites:

1. Ve a **⚙️ Configuración** (en la esquina superior derecha o en la barra lateral).
2. Pega la **API Key** de tu 2da cuenta de Google (de [Google AI Studio](https://aistudio.google.com/app/apikey)).
3. Haz clic en **Guardar**.

Una vez guardada, todos los agentes procesarán tus briefs en tiempo real con la potencia de Gemini.

---
### 📋 Vista Previa del Brief Recibido:
* **Agente Solicitado:** `{agent_id}`
* **Requerimiento:** {prompt}
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
