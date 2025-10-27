import os

#Ruta base del proyecto
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
#Carpeta de datos
DATA_DIR = os.path.join(BASE_DIR, "data")
#Archivos JSON principales
USUARIOS_FILE = os.path.join(DATA_DIR, "usuarios.json")
FICHAS_FILE = os.path.join(DATA_DIR, "fichas.json")
#Asegurarse que la carpeta de datos existe
os.makedirs(DATA_DIR, exist_ok=True)