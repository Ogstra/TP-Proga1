import unicodedata
from datetime import datetime
def quitar_acentos(texto):
     texto = unicodedata.normalize('NFD', texto)
     texto = ''.join(c for c in texto if unicodedata.category(c) != 'Mn')
     return texto
 
def validar_campo_vacio(texto):
     valor = input(texto).strip()
     while valor == "":
         print("*** Este campo es obligatorio ***")
         valor = input(texto).strip()
     return valor

def mensajesTipoNumerico(mensaje):
    while True:
        valor = input(mensaje).strip()
        if valor.isdigit():
            return int(valor)
        else:
            print("Error: Debe ingresar un número.")
    
def validarFecha(fecha):
    try:
        datetime.strptime(fecha, "%Y-%m-%d")
        return True
    except ValueError:
        return False

def validarHora(hora):
    try:
        datetime.strptime(hora, "%H:%M")
        return True
    except ValueError:
        return False

#Funcion para verificar si existe ese id en el json
def verificarSiExiste(id, json, nombre_objeto):
    """
    Verifica si un ID existe en una lista de diccionarios.
    Args:
        id (str): El ID a verificar.
        json (list): Lista de diccionarios donde se buscará el ID.
        nombre_objeto (str): Nombre del objeto para mostrar en el mensaje de error.
    Returns:
        bool: True si el ID existe, False en caso contrario.
    Logica:
        Recorre la lista de diccionarios y compara el campo 'id' con el ID proporcionado.
        Si encuentra una coincidencia, retorna True. Si no, imprime un mensaje de error y retorna False.    
    """
    for item in json:
        if item['id'] == id:
            return True
    print(f"El {nombre_objeto} con ID {id} no existe.")
    return False
