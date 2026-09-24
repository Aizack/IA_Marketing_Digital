# 📌 Memoria Persistente Sincronizada: Marketing AI Studio V3
**Marco de Trabajo:** Antigravity Agentic Framework v2.0 (`MANUAL_UNIVERSAL_DESARROLLO_IA.md`)  
**Proyecto:** Marketing AI Studio (Agency OS)  
**Ubicación Única:** `D:\Archivos\proyectos\IA_Marketing_Digital\`  
**Cuenta de Ejecución:** `diazbisac@gmail.com` (Suscripción Google AI Pro NATIVA - CERO API KEYS)  
**Modelo Configurado:** `gemini-3.7-flash` (Effort: `medium`)

---

## 🎯 Estado Actual del Proyecto
1. **Limpieza Completa Realizada**: Eliminadas todas las carpetas secundarias y scripts viejos. La única carpeta existente es `D:\Archivos\proyectos\IA_Marketing_Digital\`.
2. **Marco `.antigravity` fully injected**:
   - `context.md` (Memoria Persistente Sincronizada).
   - `.antigravity/contexto/01_negocio_y_objetivos.md`.
   - `.antigravity/orquestacion/01_orquestador_principal.md`.
   - `.antigravity/agentes/` (Los 5 agentes configurados y verificados).
3. **Fase 1 Completada & Verificada**:
   - `engine.py` (Motor conversacional multi-turno con Gemini 3.7 Flash Medium). Corrección aplicada: Orden de argumentos en CLI `agy.exe` (`--model`, `--effort`, `--dangerously-skip-permissions` antes de `--print`) y timeout de 120s.
   - `server.py` (FastAPI Server verificado en `/health` con `diazbisac@gmail.com`).
   - `app_desktop.py` (Launcher nativo Chromium App Mode sin pestañas ni caché, encoding UTF-8 forzado).
   - `iniciar_app.bat` (Lanzador en 1 clic).
   - **Prueba de Pipeline Exitosa**: Verificado flujo completo 00 (Diagnosticador) -> 01 (Director Estratega) -> 02 (Guionista UGC) generando entregables de alta calidad.

---

## 🛠️ Directivas Técnicas Obligatorias (Manual Universal v2.0)
* **CERO API Keys**: Se utiliza exclusivamente el inicio de sesión nativo de la máquina (`diazbisac@gmail.com`).
* **Modelo Fijo**: `gemini-3.7-flash` con razonamiento `--effort medium`.
* **Protocolo de 7 Pasos**: Toda modificación sincroniza `context.md`, ejecuta código modular y verifica la salud de la aplicación.
* **Interfaz UX/UI**: Web App Conversacional de 3 Columnas (Sidebar + Chat Vivo con Stepper y Tarjetas de Relevo + Live Canvas).
