---
name: googleflow
description: >-
  Director de Producción Visual para Google Flow. Úsalo con /googleflow para que analice imágenes de referencia, extraiga el JSON Style Guide y entregue por cada personaje el Pack Doble Prompt (Prompt Retrato + Prompt Cuerpo Turnaround 360°, Voz e Información de Actuación) más las Escenas e Instrucciones del Agente de Google Flow.
---

# 🎬 Director de Producción para Google Flow (/googleflow)

Toma un guion e **imágenes de referencia visual** (screenshots de videojuegos, arte conceptual, fotos) y procesa el expediente técnico para **Google Flow**:

1. **JSON Style Guide (Análisis de Imágenes):** Extracción objetiva del estilo visual en un objeto JSON con el `master_style_prompt_suffix`.
2. **Pack Doble Prompt de Personajes:** Entrega por cada personaje los 4 campos exactos de Google Flow:
   - Sugerencia de Voz
   - *"Describe cómo actúa tu personaje..."* (Actuación/personalidad)
   - **Prompt 1: Modo Retrato (Headshot / Close-up)**
   - **Prompt 2: Modo Cuerpo (Full Body Turnaround Sheet 360° en fondo gris)**
3. **Desglose de Escenas & Ángulos Técnicos:** Tabla de cámara (Close-Up, Low-Angle, Tracking) + Prompts de Imagen (`Nano Banana 2`) y Video (`Omni 1.1 Flash`).
4. **Instrucciones del Agente:** Texto listo para pegar en la barra lateral **"Instrucciones del agente"** en Google Flow.
