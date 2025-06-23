import json
from rich.console import Console
from rich.table import Table
from rich import box
from datetime import datetime, timedelta

def cargar_json(file_path):
    """
    Carga datos desde un archivo JSON.
    Args:
        file_path (str): Ruta del archivo JSON sin la extensión.
        Returns:
        dict: Datos cargados desde el archivo JSON.
    """
    try:
        with open("./datos/"+file_path+".json", 'r', encoding='utf-8') as file:
            data_json = json.load(file)
            data = data_json[file_path]
        save_log(f"Datos cargados desde {file_path}.json")
        return data
    except FileNotFoundError:
        print(f"Error: El archivo {file_path}.json no se encuentra.")
        save_log(f"Error al cargar datos desde {file_path}.json: Archivo no encontrado.")
        return {}
    except json.JSONDecodeError:
        print(f"Error: El archivo {file_path}.json no es un JSON válido.")
        save_log(f"Error al cargar datos desde {file_path}.json: JSON inválido.")
        return {}

def guardar_json(file_path, data):
    """
    Guarda datos en un archivo JSON.
    Args:
        file_path (str): Ruta del archivo JSON sin la extensión.
        data (dict): Datos a guardar en el archivo JSON.
    """
    try:
        with open("./datos/"+file_path+".json", 'w', encoding='utf-8') as file:
            json.dump({file_path: data}, file, indent=4, ensure_ascii=False)
            save_log(f"Datos guardados en {file_path}.json")
    except IOError as e:
        print(f"Error al guardar datos en {file_path}.json: {e}")
        save_log(f"Error al guardar datos en {file_path}.json: {e}")

def tieneTurnosAsignados(id, turnos, posicionDelId):
    """"Verifica si un ID tiene turnos asignados en la lista de turnos.
    Args:
        id (str): El ID a verificar.
        turnos (list): Lista de turnos, donde cada turno es un diccionario.
        posicionDelId (str): La clave del diccionario que contiene el ID.
    Returns:
        bool: True si el ID tiene turnos asignados, False en caso contrario.
    """
    return any(turno.get(posicionDelId) == id for turno in turnos)

def print_tabla(titulo, info, columnas, orientacion):
    """
    Imprime una tabla formateada en la consola.
    Args:
        titulo (str): Título de la tabla.
        info (list): Lista de diccionarios a imprimir.
        columnas (list): Lista de claves que se mostrarán como columnas.
        orientacion (str): Orientación de la tabla ("vertical" u "horizontal").
    Returns:
        None   
    """
    console = Console()
    table = Table()
    
    table = Table(
            box=box.ROUNDED,
            style="#8b8b8b",
            header_style="bold",
            row_styles=[],
            show_lines=True
        )
        
    if orientacion == "vertical":
        datos_transpuestos = list(zip(*info))
        table.add_column("Campo", justify="left")
        for i in range(len(info)):
            table.add_column(f"Registro {i+1}", justify="left")
        for idx, campo in enumerate(columnas):
            fila = [campo] + list(map(str, datos_transpuestos[idx]))
            table.add_row(*fila)
    else:
        for col in columnas:
            table.add_column(col, justify="center")
        for fila in info:
            table.add_row(*map(str, fila))
            
        indice_estado = columnas.index("Estado") if "Estado" in columnas else -1
        
    console.print(table)


def login_admin(admins):
    print("\n--- Inicio de sesión administrador ---")
    intentos = 3
    while intentos > 0:
        usuario = input("Usuario: ").strip()
        contrasena = input("Contraseña: ").strip()

        # Verificar credenciales
        admin = next((a for a in admins if a["usuario"] == usuario and a["contrasena"] == contrasena), None)

        if admin:
            print("Inicio de sesión exitoso.\n")
            save_log(f"Inicio de sesión exitoso para el usuario {usuario}.")
            return True
        else:
            intentos -= 1
            print(f"Credenciales incorrectas. Intentos restantes: {intentos}")

    print("Demasiados intentos fallidos. Acceso denegado.")
    save_log(f"Intentos fallidos de inicio de sesión para el usuario {usuario}.")
    return False

def save_log(message):
    """
    Guarda un mensaje en un archivo de log con la fecha y hora actual.
    Args:
        message (str): Mensaje a guardar en el log.
    """
    with open("./datos/log.txt", 'a', encoding='utf-8') as file:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        file.write(f"{timestamp} - {message}\n")