# 📘 Documentación Técnica: Gestión Multicuenta en Antigravity CLI (Windows Vault)

## 📌 Contexto y Problema
En entornos Windows, cambiar entre múltiples cuentas de Google en **Antigravity CLI** presenta un desafío técnico:
1. **Persistencia en Win32 Vault**: Antigravity **no** almacena únicamente sus tokens OAuth en archivos del sistema de archivos (`.json` en `.gemini`). Guarda el token activo de sesión directamente en el **Administrador de Credenciales de Windows (Windows Vault)** bajo la clave `gemini:antigravity`.
2. **Bypass de Variables de Entorno**: Cambiar `%USERPROFILE%` o `%HOME%` mediante scripts `.bat` falla para el inicio de sesión porque la binaria compilada en Go (`agy.exe`) consulta las APIs nativas de Windows (`SHGetKnownFolderPath` y `advapi32.dll`), las cuales retornan las credenciales globales del usuario en la sesión de Windows.

---

## 🔬 Causa Raíz e Investigación

| Elemento | Ubicación Real | Comportamiento |
| :--- | :--- | :--- |
| **Tokens OAuth Activos** | Windows Credential Manager (`gemini:antigravity`) | `agy.exe` lee esta clave al iniciar. Si existe, omite el login y reutiliza los tokens. |
| **Archivos de Configuración** | `C:\Users\PC\.gemini\google_accounts.json` | Contiene metadatos estáticos del correo activo (`active: email`). |

Si intentas borrar solo los archivos `.json`, `agy.exe` continúa leyendo el token válido almacenado en el Administrador de Credenciales de Windows, reconectando la misma cuenta automáticamente.

---

## 🛠️ Solución Implementada: Conmutador de Vault mediante Python (`ctypes` & `advapi32.dll`)

Para lograr un aislamiento perfecto y cambio en **1 milisegundo** entre cuentas Pro (sin cerrar sesión manualmente en el navegador ni usar máquinas virtuales), creamos el script `manage_vault.py`.

---

## 📜 Código del Gestor (`C:\Users\PC\.gemini\manage_vault.py`)

El script utiliza `ctypes` para llamar a la librería nativa de Windows `advapi32.dll`:

```python
import ctypes
from ctypes import wintypes
import os, json, sys

GEMINI_DIR = r"C:\Users\PC\.gemini"
VAULT_MAIN = os.path.join(GEMINI_DIR, "vault_diazbisac.bin")
VAULT_MARKETING = os.path.join(GEMINI_DIR, "vault_isacdiazb.bin")

class CREDENTIAL(ctypes.Structure):
    _fields_ = [
        ('Flags', wintypes.DWORD),
        ('Type', wintypes.DWORD),
        ('TargetName', wintypes.LPWSTR),
        ('Comment', wintypes.LPWSTR),
        ('LastWritten', wintypes.FILETIME),
        ('CredentialBlobSize', wintypes.DWORD),
        ('CredentialBlob', ctypes.POINTER(ctypes.c_byte)),
        ('Persist', wintypes.DWORD),
        ('AttributeCount', wintypes.DWORD),
        ('Attributes', ctypes.c_void_p),
        ('TargetAlias', wintypes.LPWSTR),
        ('UserName', wintypes.LPWSTR),
    ]

def read_vault():
    pcred = ctypes.POINTER(CREDENTIAL)()
    res = ctypes.windll.advapi32.CredReadW('gemini:antigravity', 1, 0, ctypes.byref(pcred))
    if res:
        cred = pcred.contents
        blob = ctypes.string_at(cred.CredentialBlob, cred.CredentialBlobSize)
        ctypes.windll.advapi32.CredFree(pcred)
        return blob
    return None

def write_vault(blob_bytes):
    cred = CREDENTIAL()
    cred.Flags = 0
    cred.Type = 1 # CRED_TYPE_GENERIC
    cred.TargetName = 'gemini:antigravity'
    cred.Comment = 'Antigravity OAuth Token'
    cred.CredentialBlobSize = len(blob_bytes)
    cred.CredentialBlob = (ctypes.c_byte * len(blob_bytes))(*blob_bytes)
    cred.Persist = 2 # CRED_PERSIST_LOCAL_MACHINE
    cred.UserName = 'antigravity'
    return ctypes.windll.advapi32.CredWriteW(ctypes.byref(cred), 0) != 0

def delete_vault():
    return ctypes.windll.advapi32.CredDeleteW('gemini:antigravity', 1, 0) != 0
```

---

## 📂 Scripts Batch Disponibles

### 1. `vincular_cuenta_isacdiazb.bat` *(Solo primera vez)*
* Resguarda las credenciales de la cuenta principal (`diazbisac@gmail.com`).
* Elimina `gemini:antigravity` del Windows Vault.
* Ejecuta `agy.exe --new-project`, mostrando la pantalla de selección de OAuth.
* Una vez completada la sesión de `isacdiazb@gmail.com`, guarda el respaldo en `vault_isacdiazb.bin`.

### 2. `iniciar_marketing_studio.bat` *(Uso Diario Marketing)*
* Restaura `vault_isacdiazb.bin` en Windows Vault.
* Levanta el microservicio FastAPI (`server.py`) en `http://localhost:8090`.

### 3. `restaurar_cuenta_principal.bat` *(Retorno a ERP / Dev)*
* Restaura `vault_diazbisac.bin` en Windows Vault.
* Permite continuar el trabajo en el ERP con la cuenta principal.

---

## ⚡ Optimización de Modelo y Consumo de Tokens

En `engine.py`, las llamadas al CLI de Antigravity han sido configuradas con los siguientes parámetros para minimizar consumo de tokens y maximizar velocidad:

* **Modelo:** `gemini-2.5-flash`
* **Nivel de Razonamiento (Effort):** `medium`
* **Flags CLI:** `--model gemini-2.5-flash --effort medium --dangerously-skip-permissions`

---

## 📝 Resumen para Futuras Implementaciones
Si necesitas replicar este método en otra máquina o proyecto:
1. Copia `manage_vault.py` a `%USERPROFILE%\.gemini\`.
2. Para vincular una nueva cuenta, llama a `delete_vault()` y ejecuta `agy.exe`.
3. Para respaldar/conmutar tokens entre cuentas, lee y escribe los bytes del blob usando `CredReadW` y `CredWriteW`.
