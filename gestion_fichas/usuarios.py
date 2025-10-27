import os
import json
import uuid
import secrets
import hashlib
import hmac
from datetime import datetime, timedelta
from gestion_fichas.logger_config import app_logger, error_logger, user_logger

#Rutas
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "..", "data")
os.makedirs(DATA_DIR, exist_ok=True)
USUARIOS_FILE = os.path.join(DATA_DIR, "usuarios.json")

#Configuración de hashing
HASH_NAME = "sha256"
ITERATIONS = 200_000
SALT_SIZE = 16 #bytes
TOKEN_EXPIRATION_HOURS = 12 #duración de la sesión (ajustable)

#=== Utilidades de hashing ===
def _generar_salt():
    return secrets.token_bytes(SALT_SIZE)

def _hash_password(password: str, salt:bytes) -> str:
    #Devuelve hex string del hash pbkdf2
    pw = password.encode("utf-8")
    dk = hashlib.pbkdf2_hmac(HASH_NAME, pw, salt, ITERATIONS)
    return dk.hex()

def _verificar_password(password: str, salt: bytes, stored_hash_hex: str) -> bool:
    candidate = _hash_password(password, salt)
    #compare_digest para evitar timing attacks
    return hmac.compare_digest(candidate, stored_hash_hex)

#=== IO usuarios ===
def cargar_usuarios():
    if not os.path.exists(USUARIOS_FILE):
        return []
    try:
        with open(USUARIOS_FILE, "r", encoding = "utf-8") as f:
            return json.load(f)
    except Exception as e:
        error_logger.exception(f"Error cargando usuarios: {e}")
        return []

def guardar_usuarios(usuarios):
    try:
        with open(USUARIOS_FILE, "w", encoding = "utf-8") as f:
            json.dump(usuarios, f, ensure_ascii=False, indent = 4)
        app_logger.info(f"Guardados {len(usuarios)} usuarios.")
    except Exception as e:
        error_logger.exception(f"Error guardando usuarios: {e}")

#=== Funciones Principales ===
def _buscar_por_username(usuarios, username:str):
    username = username.strip().lower()
    for u in usuarios:
        if u["username"].lower() == username:
            return u
    return None

def registrar_usuario(username: str, password: str, role: str = "editor") -> dict:
    #Crea un usuario nuevo. Devuelve el usuario creado (sin password claro) o lanza ValueError
    usuarios = cargar_usuarios()
    if _buscar_por_username(usuarios, username):
        raise ValueError("El nombre del usuario ya existe.")
    salt = _generar_salt()
    hash_hex = _hash_password(password, salt)
    user = {
        "id": str(uuid.uuid4()),
        "username": username,
        "salt": salt.hex(), #Almacenamos salt en hex para serializar
        "password_hash": hash_hex,
        "role": role,
        "created_at":datetime.now().isoformat()
    }
    usuarios.append(user)
    guardar_usuarios(usuarios)
    user_logger.info(f"Usuario registrado: {username} (role={role})")
    return {k: v for k, v in user.items() if k not in ("salt", "password_hash")}

_SESSIONS = {} #Sessions in memory: token -> {user_id, expires_at}

def autenticar_usuario(username: str, password: str):
    #Comprueba credenciales. Si OK devuelve session_token, user_without_secrets; si no None.
    usuarios = cargar_usuarios()
    user = _buscar_por_username(usuarios, username)
    if not user:
        return None
    salt = bytes.fromhex(user["salt"])
    if not _verificar_password(password, salt, user["password_hash"]):
        return None
    #Generar token y guardar sesion en memoria
    token = secrets.token_urlsafe(32)
    expires_at = datetime.now() + timedelta(hours = TOKEN_EXPIRATION_HOURS)
    _SESSIONS[token] = {"user_id": user["id"], "expires_at": expires_at}
    user_logger.info(f"Usuario autenticado: {username}")
    #Devolvemos token y datos públicos del usuario
    public = {k: v for k, v in user.items() if k not in ("salt", "password_hash")}
    return public, token

def verificar_token(token: str):
    #Devuelve user public si token válido, sino None
    ses = _SESSIONS.get(token)
    if not ses:
        return None
    if ses["expires_at"] < datetime.now():
        del _SESSIONS[token] #Borra la sesión expirada
        return None
    usuarios = cargar_usuarios() #Cargamos usuario
    for u in usuarios:
        if u["id"] == ses["user_id"]:
            return {k: v for k, v in u.items() if k not in ("salt", "password:hash")}
    return None

def logout(token: str):
    #Se elimina la sesión en memoria (logout)
    if token in _SESSIONS:
        del _SESSIONS[token]
        user_logger.info(f"Logout session token = {token}")
        return True
    return False

#=== Funciones administrativas ===
def listar_usuarios_publicos():
    usuarios = cargar_usuarios()
    return [{k: v for k, v in u.items() if k not in ("salt", "password_hash")} for u in usuarios]

def eliminar_usuario(username:str):
    usuarios = cargar_usuarios()
    u = _buscar_por_username(usuarios, username)
    if not u:
        raise ValueError("Usuario no existe.")
    usuarios = [x for x in usuarios if x["username"].lower() != username.lower()]
    guardar_usuarios(usuarios)
    user_logger.info(f"Usuario eliminado: {username}")

def cambiar_rol(username: str, new_role: str):
    usuarios = cargar_usuarios()
    u = _buscar_por_username(usuarios, username)
    if not u:
        raise ValueError("Usuario no existe.")
    u["role"] = new_role
    guardar_usuarios(usuarios)
    user_logger.info(f"Rol cambiado: {username} -> {new_role}")

def gestionar_roles(current_user):
    #Esta función permite al administrador ver y cambiar roles
    usuarios = cargar_usuarios()
    if current_user.get("role") != "admin":
        print("No tienes permisos para gestionar roles")
        return
    print("\=== GESTIÓN DE ROLES ===")
    for username, data in usuarios.items():
        print(f"- {username} (rol actual: {data.get('role', 'editor')})")
    usuario_objetivo = input("\nIntroduce el nombre del usuario al que quieres cambiar el rol: ").strip()
    if usuario_objetivo not in usuarios:
        print("Ese usuario no existe.")
        return
    nuevo_rol = input("Nuevo rol (aadmin o editor): ").strip().lower()
    if nuevo_rol not in ["admin", "editor"]:
        print("Rol no válido")
        return
    usuarios[usuario_objetivo]["role"] = nuevo_rol
    guardar_usuarios(usuarios)
    user_logger.info(f"El administrador {current_user['username']} cambió el rol de {usuario_objetivo} a {nuevo_rol}")
    print(f"Rol de {usuario_objetivo} actualizado a {nuevo_rol}.")