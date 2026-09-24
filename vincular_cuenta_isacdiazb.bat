@echo off
title Vincular Cuenta Marketing Pro (isacdiazb@gmail.com)
echo ======================================================================
echo   VINCULACION DE CUENTA PRO PARA MARKETING (isacdiazb@gmail.com)
echo ======================================================================
echo.
echo 1. Se resguardara tu cuenta principal (diazbisac@gmail.com) en Windows Vault.
echo 2. Se eliminara temporalmente la credencial activa para FORZAR a Antigravity
echo    a abrir el navegador de Google para autorizar tu 2da cuenta.
echo.
echo Presiona cualquier tecla para comenzar...
pause > nul

python C:\Users\PC\.gemini\manage_vault.py marketing

echo.
echo Abriendo inicio de sesion de Antigravity CLI...
echo INSTRUCCION: En el navegador que se abrira, selecciona: isacdiazb@gmail.com
echo.
"C:\Users\PC\.gemini\bin\agy.exe" --new-project

echo.
echo Guardando credenciales de isacdiazb@gmail.com en el Vault...
python C:\Users\PC\.gemini\manage_vault.py backup

echo.
echo ======================================================================
echo   ¡VINCULACION COMPLETADA EXITOSAMENTE!
echo   Las credenciales de isacdiazb@gmail.com han sido guardadas.
echo ======================================================================
pause
