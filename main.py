from gestion_fichas.fichas import cargar_fichas, guardar_fichas, crear_ficha, mostrar_datos, buscar_ficha, modificar_ficha, eliminar_ficha
from gestion_fichas.usuarios import (registrar_usuario, autenticar_usuario, cambiar_rol_admin, cambiar_pass_propio, cambiar_pass_usuario_admin, ver_usuarios_admin,
                                    crear_usuario_admin, eliminar_usuario_admin, verificar_o_crear_admin_inicial)
from gestion_fichas.session_manager import iniciar_sesion, cerrar_sesion, obtener_sesion_actual
from gestion_fichas.logger_config import app_logger
from config import DATA_DIR
from webapp import create_app

#app = create_app()

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
                print(f"Bienvenido {user['username']} (rol = {user.get('role', 'editor')}).")
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
        print(
            "===== MENÚ PRINCIPAL =====",
            "\n1. Introducir nueva ficha",
            "\n2. Ver todas las fichas",
            "\n3. Buscar ficha por nombre",
            "\n4. Modificar ficha existente",
            "\n5. Eliminar ficha",
            "\n6. Área personal de usuario",
            "\n7. Salir"
            )
        opcion = input("Elige una opción: ").strip()
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
            if current_user.get("role") == "admin":
                menu_admin(current_user)
            else:
                menu_editor(current_user)
        elif opcion == "7":
            cerrar_sesion()
            print("Venga, hasta luego loco. Volviendo al menu de autenticación...")
            app_logger.info(f"Usuario {current_user['username']} cerró sesión.")
            return
        else:
            print("Opción NO válida. Intentalo de nuevo.")

def menu_editor(current_user):
    while True:
        print(
            "===== MENÚ EDITOR =====",
            "\n1. Cambiar contraseña",
            "\n2. Salir"
            )
        opcion = input("Elige una opción: ").strip()
        if opcion == "1":
            cambiar_pass_propio(current_user)
            app_logger.info(f"El usuario {current_user['username']} cambió su contraseña.")
        elif opcion == "2":
            print("Volviendo al menu principal")
            return
        else:
            print("Opción NO válida. Intentalo de nuevo.")

def menu_admin(current_user):
    while True:
        print(
            "===== MENÚ ADMIN =====",
        "\n1. Ver usuarios",
        "\n2. Crear usuario",
        "\n3. Eliminar usuario",
        "\n4. Cambiar rol de usuario",
        "\n5. Cambiar contraseña de usuario",
        "\n6. Salir"
        )
        opcion = input("Elige una opción: ").strip()
        if opcion == "1":
            ver_usuarios_admin(current_user)
        elif opcion == "2":
            crear_usuario_admin(current_user)
        elif opcion == "3":
            eliminar_usuario_admin(current_user)
        elif opcion == "4":
            cambiar_rol_admin(current_user)
        elif opcion == "5":
            cambiar_pass_usuario_admin(current_user)
        elif opcion == "6":
            print("Volviendo al menu principal")
            return
        else:
            print("Opción NO válida. Intentalo de nuevo.")

def main():
    #Verificamos o creamos el admin inicial
    verificar_o_crear_admin_inicial()
    while True:
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
    #app.run(debug=True)
    main()  # Descomentar para ejecutar la versión consola