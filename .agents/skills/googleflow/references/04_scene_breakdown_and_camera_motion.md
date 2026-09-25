# 04 - Google Flow: Desglose de Escenas y Movimientos de Cámara (Omni 1.1 Flash)

En Google Flow, cada escena del guion se traduce en un **Keyframe Fijo** (generado con `Nano Banana 2`) y una **Instrucción de Movimiento de Video** (procesada por `Gemini Omni 1.1 Flash`).

---

## 1. Estructura de Desglose Escena por Escena

Para cada toma del guion, el agente debe proporcionar una tabla técnica que divida exactamente la generación de imagen fija y el movimiento de cámara:

| Toma | Tipo de Plano | Ángulo de Cámara | Keyframe Prompt (`Nano Banana 2`) | Video Motion & Camera Prompt (`Omni 1.1 Flash`) | Duración |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **01** | Plano General (Wide Shot) | Contrapicado (Low Angle) | *Descripción completa de la composición visual fija, personajes presentes, ambiente e iluminación.* | *Movimiento preciso de cámara: Slow tracking shot, slow pan right, dramatic zoom in, orbit around subject.* | 4s |
| **02** | Primer Plano (Close-up) | Ángulo Frontal a la altura de los ojos | *Detalle del rostro del personaje, expresión, iluminación lateral chiaroscuro.* | *Slow push-in zoom into eyes, subtle wind motion in hair.* | 3s |

---

## 2. Movimientos Técnicos de Cámara Recomendados en `Omni 1.1 Flash`

- **Slow Push-In / Zoom In**: Avance lento de cámara hacia el sujeto para aumentar la tensión dramática.
- **Slow Tracking Shot**: Seguimiento lateral o frontal del personaje mientras camina.
- **Pan Left / Pan Right**: Barrido horizontal de la cámara para revelar el entorno.
- **Low Angle Crane Up**: Ascenso en contrapicado para otorgar poder y autoridad al sujeto.
- **Orbit 360 / Arc Shot**: Giro circular de la cámara alrededor del personaje durante una escena de combate o revelación.
- **Dutch Angle Tilt**: Inclinación de la cámara para generar desconcierto o peligro.
