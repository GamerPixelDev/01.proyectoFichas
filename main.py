from gestion_fichas.fichas import cargar_fichas, guardar_fichas, crear_ficha, mostrar_datos, buscar_ficha, modificar_ficha, eliminar_ficha
from gestion_fichas.usuarios import registrar_usuario, autenticar_usuario
from gestion_fichas.session_manager import iniciar_sesion, cerrar_sesion, obtener_sesion_actual
from gestion_fichas.logger_config import app_logger


def menu_autenticacion():
    while True:
        print(
            "=== MENÚ DE AUTENTICACIÓN ==="
            "\n1) Iniciar sesión."
            "\n2) Registrarse."
            "\n3) Salir."
        )
        opcion = input("Elige una opción: ").strip()
        if opcion == "1":
            username = input("Usuario: ").strip()
            password = input("Contraseña: ").strip()
            resultado = autenticar_usuario(username, password)
            if resultado:
                user, token = resultado
                print(f"Bienvenido {user['username']} (rol = {user.get('role', 'user')}).")
                iniciar_sesion(user, token)
                return user, token
            else:
                print("Credenciales incorrectas.")
                app_logger.info(f"Intento de login fallido para el usuario: {username}.")
        elif opcion == "2":
            username = input("Elige un nombre de usuario: ").strip()
            password = input("Elige una contraseña: ").strip()
            try:
                registrar_usuario(username, password) #espera username, password
                app_logger.info(f"Usuario registrado: {username}.")
            except ValueError as v:
                print(f"No se pudo crear el usuario: {v}")
                app_logger.warning(f"Intento de crear usuario inválido: {username} ({v})")
        elif opcion == "3":
            print("Hasta pronto.")
            app_logger.info("Usuario salió desde el menú de autenticación.")
            exit(0)
        else:
            print("Opción no válida.")

def menu_principal(current_user, token):
    fichas = cargar_fichas()
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
            cerrar_sesion()
            print("Venga, hasta luego loco. Volviendo al menu de autenticación...")
            return
        else:
            print("Opción NO válida. Intentalo de nuevo.")

def main():
    #Comprobamos si hy una sesión activa
    sesion = obtener_sesion_actual()
    if sesion:
        print(f"Sesión activa detectada: {sesion['usuario']}")
        continuar = input("¿Desea continuar con esa sesión? (s/n)").strip().lower()
        if continuar == "s":
            current_user = {"username": sesion["usuario"], "role": sesion["rol"]}
            token = sesion["token"]
        else:
            cerrar_sesion()
            current_user, token = menu_autenticacion()
    else:
        current_user, token = menu_autenticacion()
    #Inicia el menu principal (psa usuario y token)
    menu_principal(current_user, token)
    #Cuando se salga del menu principal -> cerrar sesión
    cerrar_sesion()
    print("Sesión cerrada correctamente.")
    app_logger.info(f"Sesión finalizada para el usuario: {current_user.get('username')}.")

if __name__ == "__main__":
    main()