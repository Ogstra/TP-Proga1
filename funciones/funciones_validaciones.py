import funciones.funciones_principales as funciones_principales
import unicodedata
from datetime import datetime, timedelta

def ejecutar(nombre_funcion, *args, **kwargs):
    """
    Ejecuta dinámicamente una función por su nombre desde el módulo funciones_principales.

    Parámetros:
        nombre_funcion (str): Nombre de la función a ejecutar.
        *args: Argumentos posicionales que se le pasarán a la función.
        **kwargs: Argumentos nombrados que se le pasarán a la función.

    Retorna:
        El resultado de la función si existe y es ejecutable.
        None si la función no existe o no es callable.
    """
    funcion = getattr(funciones_principales, nombre_funcion, None)
    if callable(funcion):
        return funcion(*args, **kwargs)
    else:
        print(f"*** La función '{nombre_funcion}' no existe o no es ejecutable. ***")

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

def pedir_dos_horarios(turno_nombre):
    while True:
        entrada = input(f"Ingresá el horario para {turno_nombre} (formato HH:MM-HH:MM): ").strip()

        if "-" not in entrada:
            print("Formato inválido. Debe estar separado por un guion (-).")
            continue

        partes = entrada.split("-")
        if len(partes) != 2:
            print("Debe ingresar exactamente una hora de inicio y una de fin.")
            continue

        inicio_str, fin_str = partes

        try:
            inicio = datetime.strptime(inicio_str.strip(), "%H:%M").time()
            fin = datetime.strptime(fin_str.strip(), "%H:%M").time()

            if inicio >= fin:
                print("La hora de inicio debe ser menor que la hora de fin.")
                continue

            return f"{inicio_str.strip()}-{fin_str.strip()}"

        except ValueError:
            print("Horas inválidas. Asegurate de usar el formato HH:MM.")

def pedir_horarios_medico():
    print("Configuración de horarios del médico:")
    horario_mañana = pedir_dos_horarios("turno mañana")
    horario_tarde = pedir_dos_horarios("turno tarde")
    return [horario_mañana, horario_tarde]

def agrupar_consultorios_por_piso(consultorios):
    por_piso = {str(piso): [] for piso in range(1, 6)}
    for c in consultorios:
        piso = str(c)[0]
        if piso in por_piso:
            por_piso[piso].append(c)
    return list(por_piso.values())
