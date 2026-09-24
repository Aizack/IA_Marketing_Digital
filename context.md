# Contexto de Desarrollo - Marketing AI Studio (Agency OS)
## *Memoria Persistente Sincronizada · Antigravity Framework v2.0*

---

## 🛠️ 1. Identidad y Arquitectura General del Proyecto
*   **Nombre del Proyecto:** Marketing AI Studio (Agency OS)
*   **Ruta Base:** `D:\Archivos\proyectos\IA_Marketing_Digital\`
*   **Propósito:** Suite privada e independiente de Inteligencia Artificial para la Agencia de Marketing y Ventas. Automatiza el diagnóstico de avatares, diseño de ofertas, arquitectura de embudos, redacción de guiones UGC clip-a-clip, generación de prompts visuales fotorrealistas (Método 6C) y planificación de contenido persuasivo.
*   **Arquitectura de Ejecución:**
    *   **Nivel 1:** Manifiestos de Agentes Especialistas en `.antigravity/agentes/*.md`.
    *   **Nivel 2:** Subagentes Autónomos en Paralelo (`asyncio.gather` / workers en segundo plano).
    *   **Nivel 3 (Opcional):** Microservicio Docker con volúmenes en vivo (`docker-compose up -d`).
    *   **Frontend UI:** Desktop Nativo (PyWebView / Chromium WebView2 / Tailwind CSS Glassmorphism).
    *   **Persistencia de Campañas:** `campaigns/<timestamp>_<client_slug>/`.

---

## 🧠 2. Base de Conocimiento Centralizada (`knowledge_base/`)
El sistema está alimentado por 4 pilares de conocimiento estructurado:
1.  **Psicología y Creatividad:**
    *   `Made to Stick` (Chip & Dan Heath - Framework SUCCESs: Simple, Unexpected, Concrete, Credible, Emotional, Stories).
    *   `Steal Like an Artist` (Austin Kleon - Remix creativo, voz y diferenciación).
2.  **Respuesta Directa & Estrategia:**
    *   *El Estratega Master* (12 Ángulos de Venta, 5 Niveles de Consciencia de Eugene Schwartz, Sofisticación de Mercado, Mecanismo Único, Cialdini).
    *   *Oferta Irresistible* (Google Flow Paso a Paso).
3.  **Formatos de Vídeo & UGC:**
    *   *Avatar Hype Academy* (14 Módulos, 17 vídeos transcritos, formatos: Voz en Off, Podcast, Dualcast, Trends Virales, UGC con/sin producto, Ads Animados).
    *   *FCC (Formato de Contenido Creativo)* (Transcripciones parte 1 y 2).
4.  **Generación de Prompts Visuales:**
    *   *Método 6C* (Sujeto, Composición, Cámara, Color/Luz, Contexto, Calidad/Estilo para Midjourney/Flux/GPT Image).

---

## 🤖 3. Catálogo de Agentes Especialistas (`.antigravity/agentes/`)
*   `01_director_estratega_marketing.md` ➔ Diagnóstico de mercado, niveles de consciencia, mecanismo único y arquitectura de funnel.
*   `02_guionista_ugc_clip_a_clip.md` ➔ Redacción de guiones direct response con estructura Hook visual + Diálogo + B-Roll + CTA.
*   `03_ingeniero_prompts_visuales_6c.md` ➔ Creación de prompts precisos en inglés con el Método 6C para herramientas de imagen y avatares.
*   `04_creador_contenido_pegajoso.md` ➔ Parrillas de contenido orgánico y posts de autoridad basados en *Made to Stick*.

---

## 🚀 4. Archivos Clave del Sistema
*   `engine.py`: Motor orquestador multi-agente con soporte de Nivel 1 (manifiestos) y Nivel 2 (campañas paralelas).
*   `server.py`: Microservicio FastAPI con endpoints `/api/generate`, `/api/campaign/parallel`, `/api/campaigns`.
*   `gui/index.html`: Interfaz moderna Dark Glassmorphism con Markdown live rendering, selector de formatos y gestor de campañas.
*   `app_desktop.py`: Lanzador nativo de escritorio con PyWebView.
*   `Dockerfile` y `docker-compose.yml`: Microservicio contenerizado con volúmenes en vivo.
*   `run_desktop.bat` y `run_docker.bat`: Lanzadores de 1 solo clic.
*   Acceso directo en el Escritorio: `Marketing AI Studio.lnk`.
