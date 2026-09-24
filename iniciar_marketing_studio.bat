@echo off
title Marketing AI Studio - (isacdiazb@gmail.com)
echo ======================================================================
echo   INICIANDO MARKETING AI STUDIO
echo ======================================================================
echo.

python C:\Users\PC\.gemini\manage_vault.py marketing

echo Abriendo la aplicacion en tu navegador...
start http://localhost:8090

echo.
echo Servidor activo en http://localhost:8090
cd /d D:\Archivos\proyectos\IA_Marketing_Digital
python server.py

pause
