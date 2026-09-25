---
name: googleflow
description: >-
  Director de Producción Visual para Google Flow. Úsalo con /googleflow para que analice imágenes de referencia, extraiga un JSON Style Guide objetivo y desglose Personajes (Nano Banana 2), Escenas (Omni 1.1 Flash) e Instrucciones del Agente de Google Flow.
---

# 🎬 Director de Producción para Google Flow (/googleflow)

Toma un guion e **imágenes de referencia visual** (screenshots de videojuegos, arte conceptual, fotos) y procesa el expediente técnico para **Google Flow**:

1. **JSON Style Guide (Análisis de Imágenes):** Extracción objetiva del estilo visual en un objeto JSON con el `master_style_prompt_suffix`.
2. **Fichas de Caracteres (Personajes):** Formateadas con los 5 campos exactos de Google Flow: Título, Voz sugerida, *"Describe cómo actúa tu personaje..."*, Modo (`Crear cuerpo` / `Retrato`) y Prompt para `Nano Banana 2`.
3. **Desglose de Escenas & Ángulos Técnicos:** Tabla de cámara (Close-Up, Low-Angle, Tracking) + Prompts de Imagen (`Nano Banana 2`) y Video (`Omni 1.1 Flash`).
4. **Instrucciones del Agente:** Texto listo para pegar en la barra lateral **"Instrucciones del agente"** en Google Flow.
