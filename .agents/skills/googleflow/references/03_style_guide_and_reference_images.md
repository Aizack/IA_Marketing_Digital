# 03 - Google Flow: Guía de Estilo Visual y Extracción JSON desde Imágenes

Para garantizar que Google Flow mantenga una estética idéntica y objetiva a lo largo de todo el proyecto, el agente debe analizar las imágenes de referencia enviadas por el usuario y extraer un **JSON de Guía de Estilo**.

---

## 1. Extracción de Estilo desde Imágenes de Referencia

Cuando el usuario adjunta capturas o imágenes conceptuales (ej. Arte 3D del videojuego SIFU, estilo Arcane, anime 2D, realismo cinematográfico), el agente ejecuta el análisis visual objetivo:

### Componentes del Análisis Visual:
1. **Medio Técnico y Renderizado**: 3D Stylized vs 2D Illustration vs Realismo Fotográfico.
2. **Geometría y Modelado**: Facetas angulares, planos definidos, polígonos estilizados vs formas orgánicas suaves.
3. **Pintura y Texturas**: Pinceladas visibles estilo óleo/guache, textura física vs shaders limpios sin ruido.
4. **Delineado (Outlines)**: Sin líneas de tinta negra 2D (No toon-shading) vs contornos marcados.
5. **Paleta de Color y Rango Dinámico**: Colores desaturados, tonos tierra, acentos dramáticos (ej. rojo sangre, dorado, azul medianoche).
6. **Iluminación y Claroscuro**: Luz de recorte (Rim lighting), sombras duras con alto contraste, ambiente claroscuro.

---

## 2. Esquema JSON de Guía de Estilo (Style Lock)

```json
{
  "style_name": "SIFU Stylized 3D Martial Arts Realism",
  "engine_target": "Nano Banana 2 / Google Flow",
  "art_medium": "3D stylized character model render (Unreal Engine 5 style)",
  "geometry": "Sharply chiseled angular facial planes, polygonal anatomical structure, low-poly stylized mesh look",
  "textures": "Hand-painted oil and gouache brushstrokes on 3D surfaces, subtle canvas noise, strictly no photorealistic skin pores",
  "outlines": "Clean rendering with NO 2D ink outlines, NO comic book hatching, NO toon lines",
  "lighting": "Cinematic chiaroscuro, harsh rim lighting, deep ambient shadows, strong directional key lights",
  "color_palette": "Muted historical tones (charcoal gray, deep crimson, tarnished bronze, gold trim, warm parchment)",
  "prompt_style_suffix": "3D stylized character render, Unreal Engine 5 render, Slocap SIFU art style, chiseled angular planes, painted gouache textures, chiaroscuro rim lighting, neutral background --ar 16:9"
}
```
