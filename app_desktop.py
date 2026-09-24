"""
Marketing AI Studio - Desktop Launcher (PyWebView)
Ejecuta la interfaz de escritorio de la Agencia con los 4 Agentes y Subagentes Nivel 2.
"""

import sys
import time
import socket
import threading
import uvicorn
import webview

def is_port_in_use(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('127.0.0.1', port)) == 0

def start_backend(port: int):
    uvicorn.run("server:app", host="127.0.0.1", port=port, log_level="warning")

def main():
    port = 8090
    if not is_port_in_use(port):
        server_thread = threading.Thread(target=start_backend, args=(port,), daemon=True)
        server_thread.start()
        time.sleep(1.2)

    url = f"http://127.0.0.1:{port}"
    print(f"🚀 Iniciando Marketing AI Studio Desktop en {url}")

    window = webview.create_window(
        title="Marketing AI Studio · Agency OS v2.0",
        url=url,
        width=1280,
        height=860,
        min_size=(980, 650),
        background_color="#080c15"
    )

    webview.start(debug=False)

if __name__ == "__main__":
    main()
