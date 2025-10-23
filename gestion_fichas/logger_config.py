import logging
import os
from datetime import datetime

#=== Configuración de carpetas ===
LOG_DIR = os.path.join(os.path.dirname(__file__), "..", "logs")
os.makedirs(LOG_DIR, exist_ok = True)

#=== Rutas de los archivos de log ===
APP_LOG_FILE = os.path.join(LOG_DIR, "app.log")
ERROR_LOG_FILE = os.path.join(LOG_DIR, "errors.log")
USER_LOG_FILE = os.path.join(LOG_DIR, "user_actions.log")

#=== Configuración general del logger ===
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

#--- Handler principal (mensajes generales) ---
app_handler = logging.FileHandler(APP_LOG_FILE, encoding="utf-8")
app_handler.setLevel(logging.INFO)
app_handler.setFormatter(formatter)

#--- Handler para errores ---
error_handler = logging.FileHandler(ERROR_LOG_FILE, encoding="utf-8")
error_handler.setLevel(logging.ERROR)
error_handler.setFormatter(formatter)

#--- Handler para acciones del usuario ---
user_handler = logging.FileHandler(USER_LOG_FILE, encoding="utf-8")
user_handler.setLevel(logging.INFO)
user_handler.setFormatter(formatter)

#=== Logger principal ===
logger = logging.getLogger("gestion_fichas")
logger.setLevel(logging.INFO)

#Para evitare duplicidades de handlers
if not logger.handlers:
    logger.addHandler(app_handler)
    logger.addHandler(error_handler)
    logger.addHandler(user_handler)

#Carpeta donde se guardam los logs
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_DIR = os.path.join(BASE_DIR, "logs")
os.makedirs(LOG_DIR, exist_ok=True)

#Nombre del archivo de log por fecha
log_filename = os.path.join(LOG_DIR, f"log_{datetime.now().strftime('%Y-%m-%d')}.log")
#Configuración básica del loggin
logging.basicConfig(
    level = logging.INFO, #Nivel mínimo que se registra (INFO, DEBUG, WARNING, ERROR, CRITICAL)
    format = "%(asctime)s - %(levelname)s - %(message)s",
    handlers = [
        logging.FileHandler(log_filename, encoding = 'utf-8'),
        logging.StreamHandler() #Esto también muestra los logs en la consola
    ]
)
#Crear un logger que podremos importar desde otros archivos
logger = logging.getLogger(__name__)