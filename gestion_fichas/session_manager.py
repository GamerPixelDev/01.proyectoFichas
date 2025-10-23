import json
import os
from datetime import datetime
from gestion_fichas.logger_config import app_logger

SESSION_FILE = os.path.join(os.path.dirname(__file__), "data", "session.json")

def iniciar_sesion(usuario, token):
    #Guarda la sesión actual en un archivo JSON
    session_data = {
        "usuario": usuario["username"],
        "rol": usuario["role"],
        "token": token,
        "inicio": datetime.now().isoformat()
    }
    with open(SESSION_FILE, "w", encoding="utf-8") as f:
        json.dump(session_data, f, indent=4)
    app_logger.info(f"Sesión iniciada para el usuario: {usuario['username']}.")
    return session_data

def obtener_sesion_actual():
    #Devuelve los datos de la sesión actual (si existe)
    if not os.path.exists(SESSION_FILE):
        return None
    with open(SESSION_FILE, "r", encoding="utf-8") as f:
        return json.load(f)
    
def cerrar_sesion():
    #Elimina la sesión actual
    if os.path.exists(SESSION_FILE):
        with open(SESSION_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            usuario = data.get("usuario")
        os.remove(SESSION_FILE)
        app_logger.info(f"Sesión cerrada para el usuario: {usuario}")
    else:
        app_logger.warning("Intento de cierre de sesión sin sesión activa.")