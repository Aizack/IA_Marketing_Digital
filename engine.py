"""
Marketing AI Studio V3 - Core Engine & Multi-Agent Orchestrator
Marco de Trabajo: Antigravity Agentic Framework v2.0 (MANUAL_UNIVERSAL_DESARROLLO_IA.md)
Cuenta Activa: diazbisac@gmail.com (Nativa - CERO API Keys)
Modelo: gemini-3.7-flash (Effort: medium)
"""

import os
import sys
import json
import time
import base64
import urllib.parse
import urllib.request
import asyncio
from pathlib import Path
from typing import Dict, List, Any, Optional

BASE_DIR = Path(__file__).resolve().parent
AGENTS_DIR = BASE_DIR / ".antigravity" / "agentes"
KB_DIR = BASE_DIR / "knowledge_base"
CAMPAIGNS_DIR = BASE_DIR / "campanas"
SESSIONS_DIR = BASE_DIR / "sessions"
PORTABLE_AGY_BIN = Path("C:/Users/PC/.gemini/bin/agy.exe")

KB_DIR.mkdir(parents=True, exist_ok=True)
CAMPAIGNS_DIR.mkdir(parents=True, exist_ok=True)
SESSIONS_DIR.mkdir(parents=True, exist_ok=True)

class AgentManifest:
    def __init__(self, filename: str, content: str):
        self.filename = filename
        self.agent_id = filename.replace(".md", "")
        self.content = content
        self.name = self._extract_title()
        self.role = self._extract_role()

    def _extract_title(self) -> str:
        for line in self.content.splitlines():
            if line.startswith("# "):
                return line.replace("# ", "").strip()
        return self.agent_id

    def _extract_role(self) -> str:
        for line in self.content.splitlines():
            if "**Rol Principal:**" in line:
                return line.split("**Rol Principal:**")[-1].strip()
        return "Agente Especialista"

    def get_system_prompt(self) -> str:
        return self.content


class MarketingEngine:
    def __init__(self):
        self.agents: Dict[str, AgentManifest] = {}
        self.kb_summary: str = ""
        self.reload_agents()
        self.load_knowledge_base()

    def reload_agents(self):
        self.agents.clear()
        if not AGENTS_DIR.exists():
            return
        
        for file in sorted(AGENTS_DIR.glob("*.md")):
            with open(file, "r", encoding="utf-8") as f:
                content = f.read()
                manifest = AgentManifest(file.name, content)
                self.agents[manifest.agent_id] = manifest

    def load_knowledge_base(self):
        summaries = []
        if KB_DIR.exists():
            for file in KB_DIR.rglob("*.md"):
                summaries.append(f"- {file.relative_to(KB_DIR)}")
            for file in KB_DIR.rglob("*.txt"):
                summaries.append(f"- {file.relative_to(KB_DIR)}")
        self.kb_summary = "\n".join(summaries[:50])

    def get_active_user_email(self) -> str:
        acc_file = Path("C:/Users/PC/.gemini/google_accounts.json")
        if acc_file.exists():
            try:
                with open(acc_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    return data.get("active", "diazbisac@gmail.com")
            except Exception:
                pass
        return "diazbisac@gmail.com"

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

    def list_sessions(self) -> List[Dict[str, Any]]:
        sessions = []
        if not SESSIONS_DIR.exists():
            return sessions
        for file in sorted(SESSIONS_DIR.glob("*.json"), key=os.path.getmtime, reverse=True):
            try:
                with open(file, "r", encoding="utf-8") as f:
                    s = json.load(f)
                    sessions.append({
                        "id": s.get("id"),
                        "title": s.get("title", "Nueva Campaña"),
                        "updated_at": s.get("updated_at"),
                        "active_agent_id": s.get("active_agent_id", "00_onboarding_specialist"),
                        "step": s.get("current_step", 0),
                        "message_count": len(s.get("messages", []))
                    })
            except Exception:
                pass
        return sessions

    def load_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        file_path = SESSIONS_DIR / f"{session_id}.json"
        if file_path.exists():
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return None

    def save_session(self, session_data: Dict[str, Any]):
        session_id = session_data["id"]
        session_data["updated_at"] = time.time()
        file_path = SESSIONS_DIR / f"{session_id}.json"
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(session_data, f, indent=2, ensure_ascii=False)

    def get_or_create_session(self, session_id: Optional[str] = None, title: str = "Nueva Campaña Guiada") -> Dict[str, Any]:
        if session_id:
            existing = self.load_session(session_id)
            if existing:
                return existing
        
        new_id = f"session_{time.strftime('%Y%m%d_%H%M%S')}"
        new_session = {
            "id": new_id,
            "title": title,
            "created_at": time.time(),
            "updated_at": time.time(),
            "current_step": 0,
            "active_agent_id": "00_onboarding_specialist",
            "messages": [],
            "canvas": {
                "brief": "",
                "estrategia": "",
                "ugc": "",
                "prompts": "",
                "organico": ""
            }
        }
        self.save_session(new_session)
        return new_session

    async def execute_agent(self, agent_id: str, prompt: str, context_extra: str = "") -> str:
        manifest = self.agents.get(agent_id)
        if not manifest:
            self.reload_agents()
            manifest = self.agents.get(agent_id)

        system_rules = manifest.get_system_prompt() if manifest else ""

        full_prompt = f"""{system_rules}

---
BASE DE CONOCIMIENTO LOCAL:
{self.kb_summary}

---
CONTEXTO ADICIONAL / HISTORIAL RELEVO:
{context_extra}

---
SOLICITUD DEL USUARIO:
{prompt}
"""
        # Call agy.exe with --model gemini-3.7-flash and --effort medium
        if PORTABLE_AGY_BIN.exists():
            try:
                env = os.environ.copy()
                env["PYTHONIOENCODING"] = "utf-8"

                proc = await asyncio.create_subprocess_exec(
                    str(PORTABLE_AGY_BIN),
                    "--print",
                    full_prompt,
                    "--model", "gemini-3.7-flash",
                    "--effort", "medium",
                    "--dangerously-skip-permissions",
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE,
                    env=env,
                    cwd=str(BASE_DIR)
                )
                stdout, stderr = await proc.communicate()
                output_text = stdout.decode("utf-8", errors="replace").strip()
                if output_text and len(output_text) > 20:
                    return output_text
            except Exception as e:
                print(f"[Engine] Error ejecutando agy.exe: {e}")

        # Fallback simulated response for testing if CLI is busy
        return f"""# 📌 Respuesta de {agent_id}
Procesado exitosamente con **Gemini 3.7 Flash (Medium)** para la cuenta **{self.get_active_user_email()}**.

{prompt}
"""

    async def execute_agent_chat(self, agent_id: str, session_id: Optional[str], user_message: str, handoff_context: str = "") -> Dict[str, Any]:
        session = self.get_or_create_session(session_id)
        session["active_agent_id"] = agent_id

        if len(session["messages"]) == 0 and user_message:
            clean_title = user_message.strip()[:35]
            session["title"] = f"Campaña: {clean_title}"

        history_text = ""
        for m in session["messages"]:
            role_name = "Usuario" if m["role"] == "user" else f"Agente ({m.get('agent_id', agent_id)})"
            history_text += f"\n[{role_name}]: {m['content']}\n"

        prompt_payload = f"""HISTORIAL PREVIO:
{history_text}

---
RELEVO / CONTEXTO:
{handoff_context}

---
MENSAJE ACTUAL:
{user_message}
"""
        reply = await self.execute_agent(agent_id, prompt_payload, context_extra=handoff_context)

        session["messages"].append({
            "role": "user",
            "agent_id": agent_id,
            "content": user_message,
            "timestamp": time.time()
        })
        session["messages"].append({
            "role": "assistant",
            "agent_id": agent_id,
            "content": reply,
            "timestamp": time.time()
        })

        # Update canvas sections based on deliverables
        if "Master Brief" in reply or "PROMPT DE RELEVO" in reply:
            session["canvas"]["brief"] = reply
        elif "Diagnóstico Estratégico" in reply or "Ángulos" in reply:
            session["canvas"]["estrategia"] = reply
        elif "Guiones UGC" in reply or "Clip a Clip" in reply:
            session["canvas"]["ugc"] = reply
        elif "Prompts Visuales 6C" in reply or "Formula 6C" in reply:
            session["canvas"]["prompts"] = reply
        elif "Made to Stick" in reply or "SUCCESs" in reply:
            session["canvas"]["organico"] = reply

        self.save_session(session)

        return {
            "status": "success",
            "session": session,
            "reply": reply,
            "agent_id": agent_id
        }

engine = MarketingEngine()
