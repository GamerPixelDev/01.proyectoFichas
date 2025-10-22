import logging
import os
from datetime import datetime

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