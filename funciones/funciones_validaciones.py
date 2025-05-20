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
        valor = input(mensaje)
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

#Funcion para verificar si existe ese id
def verificarSiExiste(id, diccionario, nombre_objeto):
    if id not in diccionario:
        print(f"No existe un {nombre_objeto} con ese ID.")
        return False
    return True
