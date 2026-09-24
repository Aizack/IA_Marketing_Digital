$wsh = New-Object -ComObject WScript.Shell
$shortcutPath = Join-Path ([Environment]::GetFolderPath("Desktop")) "Vincular Segunda Cuenta.lnk"
$shortcut = $wsh.CreateShortcut($shortcutPath)
$shortcut.TargetPath = "D:\Archivos\proyectos\IA_Marketing_Digital\login_segunda_cuenta.bat"
$shortcut.WorkingDirectory = "D:\Archivos\proyectos\IA_Marketing_Digital"
$shortcut.IconLocation = "C:\Windows\System32\shell32.dll,44"
$shortcut.Save()
Write-Host "Acceso directo creado en: $shortcutPath"
