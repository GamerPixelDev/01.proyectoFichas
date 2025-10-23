from gestion_fichas.fichas import cargar_fichas, guardar_fichas, crear_ficha, mostrar_datos, buscar_ficha, modificar_ficha, eliminar_ficha
from gestion_fichas.usuarios import registrar_usuario, autenticar_usuario
from gestion_fichas.logger_config import app_logger, user_logger
from datetime import datetime

def pantalla_autenticacion():
    while True:
        print("\n1) Iniciar sesión\n2) Registrarse\n3) Salir")
        opt = input("Elige: ").strip()
        if opt == "1":
            username = input("Usuario: ").strip()
            password = input("Contraseña: ").strip()
            res = autenticar_usuario(username, password)
            if res:
                token, user_public = res
                print(f"Bienvenido {user_public['username']} (role = {user_public['role']}).")
                return token, user_public
            else:
                #app_logger.error(f"Usuario {username} ha fallado al intentar entrar (pass usado: {password}).")
                print("Credenciales incorrectas.")
        elif opt == "2":
            username = input("Usuario nuevo: ").strip()
            password = input("Contraseña: ").strip()
            try:
                registrar_usuario(username, password, role="user")
                #app_logger.info(f"Nuevo usuario creado: {username}/{password}")
                print("Usuario creado. Inicie seción.")
            except ValueError as e:
                print(e)
        else:
            return None, None

def menu_principal(current_user, token):
    fichas = cargar_fichas()
    cambios = False #Flag para controlar su hubo cambios
    while True:
        print("""
        ===== MENÚ PRINCIPAL =====
        1. Introducir nueva ficha
        2. Ver todas las fichas
        3. Buscar ficha por nombre
        4. Modificar ficha existente
        5. Eliminar ficha
        6. Salir
        ==========================      
        """)
        opcion = input("Elige una opción (1-6): ").strip()
        if opcion == "1":
            crear_ficha(fichas)
        elif opcion == "2":
            mostrar_datos(fichas)
        elif opcion == "3":
            buscar_ficha(fichas)
        elif opcion == "4":
            modificar_ficha(fichas)
        elif opcion == "5":
            eliminar_ficha(fichas)
        elif opcion == "6":
            if cambios:
                respuesta = input("Se han realizado cambios. ¿Desea guardarlos antes de salir? (s/n): ").strip().lower()
                if respuesta == "s":
                    guardar_fichas(fichas)
                    print("Cambios guardados correctamente.")
                else:
                    print("Cambios descartados.")
            print("Venga, hasta luego loco.")
            break
        else:
            print("Opción NO válida. Intentalo de nuevo.")

def main():
    menu_principal()

if __name__ == "__main__":
    token, current_user = pantalla_autenticacion()
    if not current_user:
        app_logger.info(f"Usuario a salido.")
        print("Saliendo.")
        exit(0)
    menu_principal(current_user, token) #Inicia menu principal pasando current_user y token