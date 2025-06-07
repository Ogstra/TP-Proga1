import json
import tabulate  
from datetime import datetime

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
    return any(turno[posicionDelId] == id for turno in turnos)

def print_tabla(titulo, info, columnas):
    """
    Imprime una tabla formateada en la consola.
    Args:
        titulo (str): Título de la tabla.
        lista (list): Lista de diccionarios a imprimir.
        columnas (list): Lista de claves que se mostrarán como columnas.
    Returns:
        None   
    """
    # Imprimir el título de la tabla
    nombre_tabla = tabulate.tabulate([[titulo]], tablefmt="grid", stralign="center", numalign="center")
    print(nombre_tabla)
    # Imprimir la tabla
    tabla = tabulate.tabulate(info, columnas, tablefmt="grid", stralign="center", numalign="center")
    print(tabla)

