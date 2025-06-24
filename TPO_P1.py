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
if rol.lower() == "admin":
    try:
        admins = cargar_json("admins")
    except FileNotFoundError:
        print("Error: No se encontró el archivo de administradores.")
        exit()

    if not login_admin(admins):
        print("No autorizado. Saliendo del sistema.")
        exit()
        
    mostrar_menu(rol, opciones_menu)
elif rol.lower() in ["médico", "medico", "paciente"]:
    # Solicitar DNI para médicos y pacientes
    if rol.lower() in ("médico", "medico"):
        lista = medicos
    else:
        lista = pacientes
    dni_ingresado = input("Ingrese su DNI: ").strip()
    while not any(persona["dni"] == dni_ingresado for persona in lista):
        print("DNI no encontrado. Intente nuevamente.")
        dni_ingresado = input("Ingrese su DNI: ").strip()
    establecer_sesion(rol, dni_ingresado)
    mostrar_menu(rol, opciones_menu)
else:
        establecer_sesion(rol, dni=None)
        mostrar_menu(rol, opciones_menu)

# Bucle principal para mantener el programa en ejecución
while True:
    continuar = input("\n¿Desea continuar? (Enter / s = sí, n / 0 = no): ").strip().lower()  
    if continuar in ('', 's'):
        mostrar_menu(rol, opciones_menu)
    elif continuar in ('n', '0'):
        print("Saliendo del sistema. ¡Hasta luego!")
        save_log(f"Saliendo del sistema. {rol} con DNI {dni_actual} ha cerrado sesión.")
        break
    else:
        print("*** Opción no válida ***")