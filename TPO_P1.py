from funciones.funciones_generales import *
from funciones.funciones_principales import *

# Cargar los datos desde los archivos JSON
pacientes = cargar_json("pacientes")
medicos = cargar_json("medicos")
turnos = cargar_json("turnos")
config = cargar_json("config")

roles = config["roles"]
opciones_menu = config["opciones_menu"]

# Mostrar el menú y manejar las opciones
print("Bienvenido al sistema de gestión de turnos médicos\n")
rol = menu_roles(roles)
mostrar_menu(turnos, pacientes, medicos, rol, opciones_menu)

# Bucle principal para mantener el programa en ejecución
while True:
    continuar = input("\n¿Desea continuar? (Enter / s = sí, n / 0 = no): ").strip().lower()
    
    if continuar in ('', 's'):
        mostrar_menu(turnos, pacientes, medicos, rol, opciones_menu)
    elif continuar in ('n', '0'):
        print("Saliendo del sistema. ¡Hasta luego!")
        break
    else:
        print("*** Opción no válida ***")
