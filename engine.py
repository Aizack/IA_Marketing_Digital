"""
Marketing AI Studio - Core Engine & Multi-Agent Orchestrator
Nivel 1: Manifiestos de Agentes (.antigravity/agentes/*.md)
Nivel 2: Subagentes Autónomos en Paralelo (Background Workers)
Motor: Antigravity CLI Mirror (Sesión Pro de Google)
"""

import os
import re
import json
import time
import glob
import asyncio
import subprocess
from pathlib import Path
from typing import Dict, List, Any, Optional

BASE_DIR = Path(__file__).resolve().parent
AGENTS_DIR = BASE_DIR / ".antigravity" / "agentes"
KB_DIR = BASE_DIR / "knowledge_base"
CAMPAIGNS_DIR = BASE_DIR / "campaigns"
CONFIG_FILE = BASE_DIR / "config.json"
CAMPAIGNS_DIR.mkdir(parents=True, exist_ok=True)

# Perfil aislado de Antigravity para la 2da cuenta
MARKETING_PROFILE_DIR = Path("C:/Users/PC/.gemini_marketing")
DEFAULT_PROFILE_DIR = Path("C:/Users/PC/.gemini")

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
        self.reload_agents()
        self.load_knowledge_base()

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

    def _find_agy_binary(self) -> Optional[str]:
        possible_paths = [
            "C:\\Users\\PC\\.gemini\\bin\\agy.exe",
            os.path.expanduser("~/.gemini/bin/agy.exe"),
            os.environ.get("AGY_BIN_PATH"),
            "/root/.gemini/bin/agy"
        ]
        for p in possible_paths:
            if p and os.path.isfile(p):
                return p
        return None

    def _get_active_profile_dir(self) -> str:
        """Usa el perfil aislado de marketing si existe, o el perfil por defecto"""
        if (MARKETING_PROFILE_DIR / ".gemini" / "oauth_creds.json").exists() or MARKETING_PROFILE_DIR.exists():
            return str(MARKETING_PROFILE_DIR)
        return str(DEFAULT_PROFILE_DIR)

    async def execute_agent(self, agent_id: str, prompt: str, context_extra: str = "") -> str:
        """
        Ejecuta el agente a través del Mirror de Antigravity (agy.exe) con la sesión Pro de Google.
        """
        manifest = self.agents.get(agent_id)
        if not manifest:
            self.reload_agents()
            manifest = self.agents.get(agent_id)

        system_rules = manifest.get_system_prompt() if manifest else ""
        
        full_instructions = f"""{system_rules}

---
BASE DE CONOCIMIENTO LOCAL:
{self.kb_summary}

---
CONTEXTO ADICIONAL:
{context_extra}

---
TAREA / BRIEF DE AGENCIA:
{prompt}

REGLAS DE RESPUESTA:
- Responde directamente con el entregable profesional completo en Markdown.
- Incluye tablas, pasos, estructuras y redacción persuasiva detallada sin recortar información.
"""
        agy_bin = self._find_agy_binary()
        if agy_bin:
            try:
                profile_dir = self._get_active_profile_dir()
                env = os.environ.copy()
                env["USERPROFILE"] = profile_dir
                env["HOME"] = profile_dir
                env["PYTHONIOENCODING"] = "utf-8"

                proc = await asyncio.create_subprocess_exec(
                    agy_bin,
                    "--print",
                    full_instructions,
                    "--dangerously-skip-permissions",
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE,
                    env=env,
                    cwd=str(BASE_DIR)
                )
                stdout, stderr = await proc.communicate()
                output_text = stdout.decode("utf-8", errors="replace").strip()
                if output_text:
                    return output_text
            except Exception as e:
                print(f"[Engine] Error ejecutando Antigravity CLI: {e}")

        return f"""⚠️ No se pudo conectar con el binario de Antigravity.
Asegúrate de que `agy.exe` esté disponible y la sesión vinculada."""

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
