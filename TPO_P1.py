from funciones.funciones_generales import *
from funciones.funciones_principales import *

# Cargar los datos desde los archivos JSON
try:
    config = cargar_json("config")
    roles = config["roles"]
    opciones_menu = config["opciones_menu"]
except FileNotFoundError:
    print("Error: El archivo de configuración no se encuentra.")
    exit()
except KeyError as e:
    print(f"Error: Falta la clave {e} en el archivo de configuración.")
    exit()
except Exception as e:
    print(f"Error inesperado: {e}")
    exit()

roles = config["roles"]
opciones_menu = config["opciones_menu"]

# Mostrar el menú y manejar las opciones
print("Bienvenido al sistema de gestión de turnos médicos\n")
rol = menu_roles(roles)
mostrar_menu(rol, opciones_menu)

# Bucle principal para mantener el programa en ejecución
while True:
    continuar = input("\n¿Desea continuar? (Enter / s = sí, n / 0 = no): ").strip().lower()  
    if continuar in ('', 's'):
        mostrar_menu(rol, opciones_menu)
    elif continuar in ('n', '0'):
        print("Saliendo del sistema. ¡Hasta luego!")
        break
    else:
        print("*** Opción no válida ***")
