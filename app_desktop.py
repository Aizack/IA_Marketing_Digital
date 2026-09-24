"""
Marketing AI Studio V3 - Native Chromium Desktop Window Wrapper
Lanza la aplicación en una Ventana Nativa de Escritorio Independiente (Edge WebView2 / Chromium App).
"""

import os
import sys
import time
import subprocess
import threading
import uvicorn

from server import app

def start_backend():
    port = int(os.environ.get("PORT", 8090))
    print(f"🚀 Iniciando servidor FastAPI en 127.0.0.1:{port}...")
    uvicorn.run(app, host="127.0.0.1", port=port, log_level="warning")

def launch_chromium_window():
    url = "http://127.0.0.1:8090"
    profile_dir = os.path.join(os.path.dirname(__file__), ".app_profile")
    
    edge_exe = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
    edge_64 = r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"
    chrome_exe = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    
    exe_path = None
    for p in [edge_exe, edge_64, chrome_exe]:
        if os.path.exists(p):
            exe_path = p
            break

    if not exe_path:
        print("⚠️ No se encontró ejecutable de Chromium. Abriendo navegador predeterminado...")
        import webbrowser
        webbrowser.open(url)
        return

    cmd = [
        exe_path,
        f"--app={url}",
        f"--user-data-dir={profile_dir}",
        "--no-first-run",
        "--no-default-browser-check",
        "--window-size=1440,900"
    ]
    
    print(f"🖥️ Abriendo Ventana Nativa de Escritorio: {exe_path}")
    subprocess.run(cmd)

if __name__ == "__main__":
    t = threading.Thread(target=start_backend, daemon=True)
    t.start()
    time.sleep(1.5)
    launch_chromium_window()
