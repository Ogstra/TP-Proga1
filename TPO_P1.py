from funciones.funciones_generales import *
from funciones.funciones_principales import *

# Cargar los datos desde los archivos JSON
archivos_vitales = {
    "pacientes": cargar_json("pacientes"),
    "medicos": cargar_json("medicos"),
    "turnos": cargar_json("turnos"),
    "config": cargar_json("config"),
}

try:
    errores = list(filter(lambda item: "ERROR" in str(item[1]), archivos_vitales.items()))
    # errores devuelve algo asi:[('medicos', 'ERROR: El archivo medicos.json no se encuentra.')]
    if errores:
        nombre = errores[0][0]
        print("ERROR al cargar los datos. Asegúrese de que los archivos JSON existan y sean válidos.")
        save_log(f"ERROR al cargar datos desde {nombre}.json: Archivo no encontrado o inválido.")
        exit()
except Exception as e:
    print(f"Ocurrió un ERROR inesperado al verificar los datos: {e}")
    save_log(f"ERROR inesperado al cargar archivos JSON: {e}")
    exit()

# Extrae los datos correctamente cargados
pacientes = archivos_vitales["pacientes"]
medicos = archivos_vitales["medicos"]
turnos = archivos_vitales["turnos"]
config = archivos_vitales["config"]

# Cargar roles y menú desde config.json
try:
    roles = config["roles"]
    opciones_menu = config["opciones_menu"]
except FileNotFoundError:
    print("ERROR: El archivo de configuración no se encuentra.")
    exit()
except KeyError as e:
    print(f"ERROR: Falta la clave {e} en el archivo de configuración.")
    exit()
except Exception as e:
    print(f"ERROR inesperado: {e}")
    exit()

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

# Bucle principal para mantener el programa en ejecucion
continuar = 's'
while continuar in ('', 's'):
    mostrar_menu(rol, opciones_menu)
    continuar = input("\n¿Desea continuar? (Enter / s = sí, n / 0 = no): ").strip().lower()
    if continuar in ('n', '0'):
        print("Saliendo del sistema. ¡Hasta luego!")
        save_log(f"Saliendo del sistema. {rol} con DNI {dni_actual} ha cerrado sesión.")
    elif continuar not in ('', 's'):
        print("*** Opción no válida ***")
        continuar = 's'  # vuelve a mostrar menú
