@echo off
title Vincular Segunda Cuenta Google (isacdiazb@gmail.com)
echo ======================================================================
echo   VINCULACION DE SEGUNDA CUENTA GOOGLE PRO: isacdiazb@gmail.com
echo ======================================================================
echo.
echo 1. Se abrira una nueva sesion de Antigravity 100%% aislada.
echo 2. En el navegador que se abrira a continuacion, selecciona:
echo    👉 isacdiazb@gmail.com
echo.
echo Presiona cualquier tecla para continuar...
pause > nul

set "USERPROFILE=C:\Users\PC\.gemini_marketing"
set "HOME=C:\Users\PC\.gemini_marketing"
set "HOMEDRIVE=C:"
set "HOMEPATH=\Users\PC\.gemini_marketing"
set "LOCALAPPDATA=C:\Users\PC\.gemini_marketing\AppData\Local"
set "APPDATA=C:\Users\PC\.gemini_marketing\AppData\Roaming"

"C:\Users\PC\.gemini\bin\agy.exe" --new-project

echo.
echo ======================================================================
echo   Sesion vinculada con exito en C:\Users\PC\.gemini_marketing
echo ======================================================================
pause
