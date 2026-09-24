"""
Marketing AI Studio V3 - Standalone Chromium Desktop Application Wrapper
Lanza la aplicación como una ventana de escritorio nativa independiente (WebView2 / Chromium),
desvinculada completamente de los navegadores locales y de problemas de caché.
"""

import os
import sys
import time
import threading
import uvicorn
import webview

# Ensure C:\Users\PC\.gemini is in path for vault manager
sys.path.append(r"C:\Users\PC\.gemini")
try:
    import manage_vault
    manage_vault.switch_to_main()
except Exception as e:
    print(f"[DesktopApp] Note: Vault switch error: {e}")

from server import app

def start_backend():
    port = int(os.environ.get("PORT", 8090))
    print(f"🚀 Iniciando servidor FastAPI en 127.0.0.1:{port}...")
    uvicorn.run(app, host="127.0.0.1", port=port, log_level="warning")

if __name__ == "__main__":
    # 1. Start FastAPI server in background thread
    server_thread = threading.Thread(target=start_backend, daemon=True)
    server_thread.start()

    # 2. Wait 1 second for FastAPI initialization
    time.sleep(1)

    # 3. Create Desktop Chromium Window (Native Edge WebView2)
    print("🖥️ Abriendo ventana nativa de escritorio (Chromium App)...")
    window = webview.create_window(
        title="Marketing AI Studio V3 · Agency OS Conversacional",
        url="http://127.0.0.1:8090",
        width=1440,
        height=900,
        min_size=(1024, 720),
        resizable=True,
        background_color="#080c15"
    )

    # Launch with private mode to prevent any browser caching
    webview.start(private_mode=True)
