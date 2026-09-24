@echo off
title Marketing AI Studio - Docker Engine
echo ===================================================
echo   Iniciando Marketing AI Studio Engine (Docker)
echo ===================================================
cd /d "%~dp0"
docker-compose up -d --build
echo.
echo Microservicio iniciado en http://localhost:8090
echo Abriendo interfaz en el navegador...
start http://localhost:8090
pause
