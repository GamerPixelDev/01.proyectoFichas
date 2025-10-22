import json
import os
from datetime import datetime
from gestion_fichas.utils import pedir_nombre, pedir_edad, pedir_ciudad, obtener_fecha

#=== Configuración de rutas ===
#Carpeta base --> donde está este archivo (gestion_fichas/)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
#Carpeta 'data' --> un nivel por encima
DATA_DIR = os.path.join(BASE_DIR, "..", "data")
#Crear la carpeta si no existe
os.makedirs(DATA_DIR, exist_ok=True)
#Ruta completa del archivo JSON
NOMBRE_ARCHIVO = os.path.join(DATA_DIR, "fichas.json")

#=== Funciones de carga y guardado ===
def cargar_fichas(nombre_archivo=NOMBRE_ARCHIVO):
    #Carga las fichas desde un archivo JSON si existe, o crea una lista vacia.
    if os.path.exists(nombre_archivo):
        try:
            with open(nombre_archivo, "r", encoding="utf-8") as f:
                fichas = json.load(f)
                #print(f"{len(fichas)} fichas cargadas desde {nombre_archivo}.")
                return fichas
        except json.JSONDecodeError:
            print(f"El archivo {nombre_archivo} está dañado o vacío. Se creará uno nuevo.")
            return []
        except Exception as e:
            print(f"Error leyendo {nombre_archivo}: {e}")
            return []
    else:
        print(f"No se encontró {nombre_archivo}. Se creará uno nuevo al cargar.")
        return []

def guardar_fichas(fichas, nombre_archivo=NOMBRE_ARCHIVO):
    #Guarda la lista completa en JSON (sobreescribe).
    try:
        with open(nombre_archivo, "w", encoding="utf-8") as f:
            json.dump(fichas, f, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"Error al guardar fichas: {e}")
    else:
        print(f"Fichas guardadas en {nombre_archivo} (total: {len(fichas)}).")

def crear_ficha(fichas, nombre_archivo=NOMBRE_ARCHIVO):
    #Crea una nueva ficha y la añade a la lista, guardando después.
    nombre = pedir_nombre()
    edad = pedir_edad() #Devuelve un int
    ciudad = pedir_ciudad()
    fecha_now = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    nueva_ficha={
        "nombre": nombre,
        "edad": edad,
        "ciudad": ciudad,
        "fecha_creacion":fecha_now,
        "fecha_modificacion":None
    }
    #Comprobamos duplicados por nombre exacto (insensible a mayúsculas)
    existentes = [f for f in fichas if f["nombre"].lower() == nombre.lower()]
    if existentes:
        print(f"Ya existe/n {len(existentes)} ficha/s con ese nombre.")
        if input("¿Crear otra igualmente? (s/n): ").strip().lower() != "s":
            print("Cancelado.")
            return
    fichas.append(nueva_ficha)
    guardar_fichas(fichas, nombre_archivo)

def mostrar_datos(fichas):
    if not fichas:
        print("No hay fichas registradas todavía.")
        return
    print("\n=== FICHAS REGISTRADAS ===")
    for i, ficha in enumerate(fichas, start=1):
        print(f"\nFicha {i}:")
        for clave, valor in ficha.items():
            print(f"{clave}: {valor}")
    print("==========================\n")

def buscar_fichas_por_nombre(fichas, termino):
    #Búsqueda (devuelve lista de tuplas(idx, ficha))
    termino = termino.strip().lower()
    resultados = []
    for idx, f in enumerate(fichas):
        if termino in f.get("nombre", "").lower():
            resultados.append((idx, f))
    return resultados

def buscar_ficha(fichas):
    termino = input("Introduce el nombre a buscar: ").strip()
    resultados = buscar_fichas_por_nombre(fichas, termino)
    if not resultados:
        print("No se encuetran coincidencias.")
        return
    print(f"\nSe encontraron {len(resultados)} que coindice/n:")
    for i, (idx, f) in enumerate(resultados, start=1):
        print(
            f"\nFicha: {i}"
            f"\nNombre: {f['nombre']}"
            f"\nEdad: {f['edad']}"
            f"\nCiudad: {f['ciudad']}"
            f"\nCreada: {f['fecha_creacion']}"
            f"\nModificada: {f['fecha_modificacion']}"
        )

def modificar_ficha(fichas, nombre_archivo=NOMBRE_ARCHIVO):
    nombre_buscado= input("Introduce el nombre de la ficha que quieras buscar/modificar: ").strip().lower()
    coincidencias = buscar_fichas_por_nombre(fichas, nombre_buscado)
    if not coincidencias:
        print("No se encontraron fichas con ese nombre.")
        return
    print(f"\nSe encontraron {len(coincidencias)} coincidencia/s:\n")
    for i, (idx, f) in enumerate(coincidencias, start=1):
        print(
            f"Ficha [{i}]"
            f"\nNombre: {f.get('nombre')}"
            f"\nEdad: {f.get('edad')}"
            f"\nCiudad: {f.get('ciudad')}"
        )
    if len(coincidencias) > 1:
        try:
            pos = int(input(f"Elige el número de la ficha a modificar: (1 - {len(coincidencias)}): ").strip())
            #ficha = coincidencias[pos]
        except ValueError:
            print("Entrada no válida.")
            return
        sel_index = pos - 1
    else:
        sel_index = 0
    idx_global, ficha = coincidencias[sel_index] #Índice real en la lista fichas
    while True:
        print("\nDatos actuales:")
        print(f"1. Nombre: {ficha['nombre']}")
        print(f"2. Edad: {ficha['edad']}")
        print(f"3. Ciudad: {ficha['ciudad']}")
        print(f"4. Guardar cambios y salir")
        print(f"5. Salir sin guardar.")
        eleccion = input("Elige que desea cambiar (1 - 5): ").strip()
        if eleccion == "1":
            ficha["nombre"] = pedir_nombre()
        elif eleccion == "2":
            ficha["edad"] = pedir_edad()
        elif eleccion == "3":
            ficha["ciudad"] = pedir_ciudad()
        elif eleccion == "4":
            ficha["fecha_modificacion"] = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
            fichas[idx_global] = ficha #Se actualiza la lista principal
            guardar_fichas(fichas, nombre_archivo)
            print("Ficha modificada y guardada.")
            return #Se puede cambiar por un return para volver al menu principal
        elif eleccion == "5":
            print("Modificación cancelada, no se ha guardado nada.")
            return
        else:
            print("Opción NO válida. Inténtelo de nuevo.")

def eliminar_ficha(fichas, nombre_archivo=NOMBRE_ARCHIVO):
    nombre_buscado= input("Introduce el nombre de la ficha que quieras eliminar: ").strip().lower()
    coincidencias = buscar_fichas_por_nombre(fichas, nombre_buscado)
    if not coincidencias:
        print("No se encontraron fichas con ese nombre.")
        return
    print(f"\nSe encontraron {len(coincidencias)} coincidencia/s:\n")
    for i, ficha in enumerate(coincidencias, start=1):
        print(f"Ficha [{i}]: {ficha}")
    if len(coincidencias) > 1:
        try:
            pos = int(input(f"Elige el número de la ficha a eliminar: (1 - {len(coincidencias)}): ").strip())
            eliminar_ficha = coincidencias[pos]
        except ValueError:
            print("Entrada no válida.")
            return
    else:
        eliminar_ficha = 0
    print(f"Ficha seleccionada:\n{eliminar_ficha}")
    confirmar = input("Esta acción no se puede deshacer. ¿Eliminar definitivamente la ficha? (s/n): ").strip().lower()
    if confirmar == "s":
        fichas.remove(eliminar_ficha)
        guardar_fichas(fichas, nombre_archivo)
        print("Ficha eliminada correctamente.")
    else:
        print("Acción cancelada.")