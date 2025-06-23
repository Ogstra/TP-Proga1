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
    with open("./datos/"+file_path+".json", 'r', encoding='utf-8') as file:
        data_json = json.load(file)
        data = data_json[file_path]
    return data

def guardar_json(file_path, data):
    """
    Guarda datos en un archivo JSON.
    Args:
        file_path (str): Ruta del archivo JSON sin la extensión.
        data (dict): Datos a guardar en el archivo JSON.
    """
    with open("./datos/"+file_path+".json", 'w', encoding='utf-8') as file:
        json.dump({file_path: data}, file, indent=4, ensure_ascii=False)

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

def print_tabla(titulo, info, columnas, horientacion):
    """
    Imprime una tabla formateada en la consola.
    Args:
        titulo (str): Título de la tabla.
        info (list): Lista de diccionarios a imprimir.
        columnas (list): Lista de claves que se mostrarán como columnas.
        horientacion (str): Orientación de la tabla ("vertical" u "horizontal").
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
        
    if horientacion == "vertical":
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
            return True
        else:
            intentos -= 1
            print(f"Credenciales incorrectas. Intentos restantes: {intentos}")

    print("Demasiados intentos fallidos. Acceso denegado.")
    return False
