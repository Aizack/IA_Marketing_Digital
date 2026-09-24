@echo off
title Marketing AI Studio V3 - Aplicacion de Escritorio
echo ======================================================================
echo   INICIANDO MARKETING AI STUDIO V3 (VENTANA DE ESCRITORIO NATIVA)
echo   Cuenta: diazbisac@gmail.com | Modelo: Gemini 3.7 Flash (Medium)
echo   Marco: Antigravity Framework v2.0 (MANUAL_UNIVERSAL_DESARROLLO_IA)
echo ======================================================================
echo.

cd /d D:\Archivos\proyectos\IA_Marketing_Digital
python app_desktop.py

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ⚠️ Ocurrio un problema iniciando la aplicacion.
    pause
)
