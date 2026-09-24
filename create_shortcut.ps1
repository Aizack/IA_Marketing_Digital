$wsh = New-Object -ComObject WScript.Shell
$shortcutPath = Join-Path ([Environment]::GetFolderPath("Desktop")) "Marketing AI Studio.lnk"
$shortcut = $wsh.CreateShortcut($shortcutPath)
$shortcut.TargetPath = "D:\Archivos\proyectos\IA_Marketing_Digital\run_desktop.bat"
$shortcut.WorkingDirectory = "D:\Archivos\proyectos\IA_Marketing_Digital"
$shortcut.IconLocation = "C:\Windows\System32\shell32.dll,14"
$shortcut.Save()
Write-Host "Acceso directo creado en: $shortcutPath"
