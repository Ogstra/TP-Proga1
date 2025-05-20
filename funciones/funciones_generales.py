import json
import unicodedata
from datetime import datetime

def cargar_json(file_path):
    """
    Carga el json que le pasemos como argumento y lo devuelve como un diccionario.
    """
    with open("./datos/"+file_path+".json", 'r') as file:
        data_json = json.load(file)
        data = data_json[file_path]
    return data

def tieneTurnosAsignados(id, turnos, posicionDelId):

    return any(turno[posicionDelId] == id for turno in turnos)





