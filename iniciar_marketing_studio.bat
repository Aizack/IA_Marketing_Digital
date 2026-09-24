@echo off
title Marketing AI Studio V3 - (diazbisac@gmail.com)
echo ======================================================================
echo   INICIANDO MARKETING AI STUDIO V3 - CONVENTIONAL CHAT ENGINE
echo   Cuenta: diazbisac@gmail.com | Modelo: Gemini 3.7 Flash (Medium)
echo ======================================================================
echo.

echo Abriendo la aplicacion conversacional en tu navegador...
start http://localhost:8090

echo.
echo Servidor activo en http://localhost:8090
cd /d D:\Archivos\proyectos\IA_Marketing_Digital
python server.py

pause
