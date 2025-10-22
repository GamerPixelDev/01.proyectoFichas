from gestion_fichas.fichas import (
    cargar_fichas, guardar_fichas, crear_ficha, mostrar_datos, buscar_ficha, modificar_ficha, eliminar_ficha
)

def menu_principal():
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
        opcion = input("Elige una opción (1-5): ").strip()
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
    main()