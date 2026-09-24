@echo off
title Marketing AI Studio - Servidor Pro (isacdiazb@gmail.com)
echo ======================================================================
echo   INICIANDO MARKETING AI STUDIO CON ISACDIAZB@GMAIL.COM
echo ======================================================================
echo.

python C:\Users\PC\.gemini\manage_vault.py marketing

echo.
echo Iniciando microservicio FastAPI en http://localhost:8090...
cd /d D:\Archivos\proyectos\IA_Marketing_Digital
python server.py

pause
