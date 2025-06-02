from funciones.funciones_validaciones import *
from funciones.funciones_generales import *
# Función para mostrar el menú
def mostrar_menu(turnos, pacientes, medicos):
    """Función que muestra el menú principal y maneja las opciones seleccionadas por el usuario.	
    Args:
        turnos (list): Lista de turnos médicos.
        pacientes (dict): Diccionario de pacientes.
        medicos (dict): Diccionario de médicos.
    Returns:
        str: Opción seleccionada por el usuario.
    Logica:
    - Imprime el menú de opciones disponibles.
    - Solicita al usuario que seleccione una opción.
    - Dependiendo de la opción seleccionada, llama a la función correspondiente.
    - Si la opción es "0", finaliza el programa.
    - Si la opción es inválida, muestra un mensaje de error y vuelve a solicitar una opción.
    """
    print("\nMenú de Turnos Médicos")
    print("1. Ver lista de turnos")  
    print("2. Agregar turno")  
    print("3. Modificar turno")
    print("4. Eliminar turno") 
    print("5. Buscar paciente")
    print("6. Crear paciente")
    print("7. Eliminar paciente")
    print("8. Buscar médico")
    print("9. Eliminar médico")
    print("10. Agregar médico")
    print("11. Agenda médica")
    try:
        opcion = input("\nSeleccione una opción (0 para salir):")
        if opcion == "1":
            ver_turnos(turnos, pacientes, medicos)
        elif opcion == "2":
            agregar_turno(turnos, medicos, pacientes)
        elif opcion == "3":
            modificar_turno(turnos,medicos, pacientes)
        elif opcion == "4":
            eliminar_turno(turnos)
        elif opcion == "5":
            buscar_paciente(pacientes)
        elif opcion == "6":
            crear_paciente(pacientes)
        elif opcion == "7":
            eliminar_paciente(pacientes)
        elif opcion == "8":
            buscar_medico(medicos)
        elif opcion == "9":
            eliminar_medico(medicos, turnos, pacientes)
        elif opcion == "10":
            agregar_medico(medicos)
        elif opcion == "11":
            agenda_medico(medicos, turnos)
        elif opcion == "0":
            print("Saliendo del programa...")
            exit()
        else:
            print("Opción no válida. Intente de nuevo.")
        return opcion
    except ValueError as e:
        print(f"Error: {e}. Debe ingresar un número válido.")
# Función para mostrar turnos con información expandida
def ver_turnos(turnos, pacientes, medicos):
    """Función que muestra la lista de turnos con información detallada de pacientes y médicos.
    Args:
        turnos (list): Lista de turnos médicos.
        pacientes (dict): Diccionario de pacientes.
        medicos (dict): Diccionario de médicos.
    Returns:
        None
    Logica:
    - Itera sobre cada turno en la lista de turnos.
    - Intenta obtener el ID del médico y del paciente del turno.
    - Busca el nombre del paciente y del médico en sus respectivos diccionarios.
    - Si encuentra ambos, agrega la información del turno a una lista.
    - Determina el estado del turno comparando la fecha y hora actual con la del turno.
    - Imprime la lista de turnos en formato tabular.
    """
    info_turno = []
    for turno in turnos:
        try:
            id_medico = turno["medico"]
            id_paciente = turno["paciente"]
            # Obtener el nombre del paciente
            paciente = next((p for p in pacientes if p["id"] == id_paciente), None)
            paciente = paciente['nombre'] + " " + paciente['apellido'] if paciente else None
            # Obtener el nombre del médico
            medico = next((m for m in medicos if m["id"] == id_medico), None)
            medico = medico['nombre'] + " " + medico['apellido'] if medico else None
            # Agregar la información del turno a la lista
            # Agregar estado de turno como "Pendiente" o "Atendido" comparando fecha y hora actual
            if turno['fecha'] < datetime.now().strftime("%Y-%m-%d") or (turno['fecha'] == datetime.now().strftime("%Y-%m-%d") and turno['hora'] < datetime.now().strftime("%H:%M")):
                estado = "Atendido"
            else:
                estado = "Pendiente"
            if paciente and medico:
               info_turno.append([turno['fecha'], turno['hora'], paciente, medico, turno['consultorio'], estado])
            # Si el paciente y médico se encuentran, se agrega el turno a la lista
            # Si el paciente o médico no se encuentra, no se agrega el turno
            else:
                print("Datos incompletos para mostrar el turno.")
        # Se captura cualquier error de tipo o clave que pueda ocurrir al procesar el turno
        except ValueError as e:
            print(f"VALUE Error al procesar el turno: {e}")
        except TypeError as e:
            print(f"TYPE Error al procesar el turno: {e}")
        except KeyError as e:
            print(f"KEY Turno inválido. Falta la clave: {e}")
    #ordenar la lista de turnos por fecha y hora
    info_turno.sort(key=lambda x: (x[0], x[1]))  # Ordenar por fecha y hora
    print_tabla("Lista de Turnos", info_turno, ["Fecha", "Hora", "Paciente", "Medico", "Consultorio", "Estado"])

def agregar_turno(turnos, medicos, pacientes):
    """Función que permite agregar un nuevo turno médico.
    Args:
        turnos (list): Lista de turnos médicos.
        medicos (dict): Diccionario de médicos.
        pacientes (dict): Diccionario de pacientes.
    Returns:
        None
    Logica:
    - Solicita al usuario el ID del paciente y verifica si existe.
    - Solicita al usuario el ID del médico y verifica si existe.
    - Solicita el nombre del consultorio, la fecha y la hora del turno.
    - Valida la fecha y la hora ingresadas.
    - Genera un nuevo ID para el turno y lo agrega a la lista de turnos.
    """
    print("Agregar Turno:")
    
    # Verificar si hay pacientes registrados
    if not pacientes:
        print("No hay pacientes registrados. Por favor, registre un paciente antes de agregar un turno.")
        return
    
    # Verificar si hay médicos registrados
    if not medicos:
        print("No hay médicos registrados. Por favor, registre un médico antes de agregar un turno.")
        return

    while True:
        try:
            id_paciente = int(input("Ingrese el ID del paciente: "))
            if verificarSiExiste(id_paciente, pacientes, "paciente"):
                break
        except ValueError:
            print("Debe ingresar un número entero válido.")

    while True:
        try:
            id_medico = int(input("Ingrese el ID del médico: "))
            if verificarSiExiste(id_medico, medicos, "médico"):
                break
        except ValueError:
            print("Debe ingresar un número entero válido.")

    consultorio = input("Ingrese el numero del consultorio: ")

    while True:
        fecha = input("Ingrese la fecha (AAAA-MM-DD): ")
        if validarFecha(fecha):
            break
        else:
            print("Formato de fecha inválido. Intente de nuevo.")

    while True:
        hora = input("Ingrese la hora (HH:MM): ")
        if validarHora(hora):
            break
        else:
            print("Formato de hora inválido. Intente de nuevo.")

    # Generar un nuevo ID para el turno
    # Si la lista de turnos está vacía, el nuevo ID será 1
    # Si no, se toma el máximo ID existente y se le suma 1
    nuevo_id_turno = max(turnos, key=lambda x: x["id"])["id"] + 1 if turnos else 1
    nuevo_turno = {
        "id": nuevo_id_turno,
        "paciente": id_paciente,
        "medico": id_medico,
        "consultorio": consultorio,
        "fecha": fecha,
        "hora": hora
    }
    
    turnos.append(nuevo_turno)  # Agregar el nuevo turno a la lista de turnos
    guardar_json("turnos", turnos)  # Guardar los cambios en el archivo JSON
    # Imprimir el turno agregado en formato tabular
    print_tabla("Turno Agregado", [[nuevo_turno["fecha"], nuevo_turno["hora"], pacientes[id_paciente]["nombre"] + " " + pacientes[id_paciente]["apellido"], medicos[id_medico]["nombre"] + " " + medicos[id_medico]["apellido"], consultorio, "Pendiente"]], ["Fecha", "Hora", "Paciente", "Medico", "Consultorio", "Estado"])
    print(f"Turno agregado con éxito. ID del turno: {nuevo_id_turno}")

def modificar_turno(turnos, medicos, pacientes):
    try:
        id_turno =mensajesTipoNumerico ("Ingrese el ID del turno que quiere modificar: ")
    except ValueError:
        print("Debe ingresar un número de ID válido.")
        return

    turnoAModificar = None
    for i in range(len(turnos)):
        if turnos[i]["id"] == id_turno:
            turnoAModificar = i
            break

    if turnoAModificar is None:
        print(f"No se encontró un turno con el ID {id_turno}.")
        return
    turno = turnos[turnoAModificar] # Convertimos la tupla en lista para poder modificarla

    # Pedir opción de modificación con validación
    while True:
        print("\n¿Qué desea modificar del turno?")
        print("1. Paciente")
        print("2. Médico")
        print("3. Consultorio")
        print("4. Fecha")
        print("5. Hora")
        print("6. Todo")
        try:
            opcion = int(input("Elija la opción (1-6): "))
            if opcion not in range(1, 7):
                print("Opción inválida. Debe ser un número entre 1 y 6.")
                continue
            break
        except ValueError:
            print("Debe ingresar un número entero.")


    if opcion == 1:
        while True:
            id_paciente = int(input("Ingrese el nuevo ID del paciente (o -1 para cancelar): "))
            if id_paciente == -1:
                print("Operación cancelada.")
                return
            if verificarSiExiste(id_paciente, pacientes, "paciente"):
                turno[1] = id_paciente
                print("ID del paciente modificado con éxito.")
                break

    elif opcion == 2:
        while True:
            id_medico = int(input("Ingrese el nuevo ID del médico (o -1 para cancelar): "))
            if id_medico == -1:
                print("Operación cancelada.")
                return
            if verificarSiExiste(id_medico, medicos, "médico"):
                turno[2] = id_medico
                print("ID del médico modificado con éxito.")
                break

    elif opcion == 3:
        consultorio = input("Ingrese el nuevo nombre del consultorio: ")
        turno['consultorio'] = consultorio
        print("El nombre del consultorio fue modificado con éxito.")
        
    elif opcion == 4:
        while True:
            fecha = input("Ingrese la nueva fecha (AAAA-MM-DD) (o -1 para cancelar): ")
            if fecha == "-1":
                print("Operación cancelada.")
                return
            if validarFecha(fecha):
                turno[4] = fecha
                print("La fecha fue modificada con éxito.")
                break
            else:
                print("Formato de fecha inválido. Intente de nuevo.")

    elif opcion == 5:
        while True:
            hora = input("Ingrese la nueva hora (HH:MM) (o -1 para cancelar): ")
            if hora == "-1":
                print("Operación cancelada.")
                return
            if validarHora(hora):
                turno[5] = hora
                print("La hora fue modificada con éxito.")
                break
            else:
                print("Formato de hora inválido. Intente de nuevo.")

    elif opcion == 6:
        while True:
            id_paciente = int(input("Ingrese el nuevo ID del paciente (o -1 para cancelar): "))
            if id_paciente == -1:
                print("Operación cancelada.")
                return
            if verificarSiExiste(id_paciente, pacientes, "paciente"):
                turno[1] = id_paciente
                break

        while True:
            id_medico = int(input("Ingrese el nuevo ID del médico (o -1 para cancelar): "))
            if id_medico == -1:
                print("Operación cancelada.")
                return
            if verificarSiExiste(id_medico, medicos, "médico"):
                turno[2] = id_medico
                break

        consultorio = input("Ingrese el nuevo nombre del consultorio: ")
        turno[3] = consultorio
        print("El nombre del consultorio fue modificado con éxito.")

        while True:
            fecha = input("Ingrese la nueva fecha (AAAA-MM-DD) (o -1 para cancelar): ")
            if fecha == "-1":
                print("Operación cancelada.")
                return
            if validarFecha(fecha):
                turno[4] = fecha
                break
            else:
                print("Formato de fecha inválido. Intente de nuevo.")

        while True:
            hora = input("Ingrese la nueva hora (HH:MM) (o -1 para cancelar): ")
            if hora == "-1":
                print("Operación cancelada.")
                return
            if validarHora(hora):
                turno[5] = hora
                break
            else:
                print("El formato de la hora es inválido. Intente de nuevo.")
        print("Toda la información fue modificada con éxito.")
        
    turnos[turnoAModificar] = turno # Volvemos a guardar como tupla
    guardar_json('turnos', turnos)
    
    print(f"\n Turno {id_turno} modificado con éxito.")

def eliminar_turno(turnos):
    id_turno= int(input("Ingrese el ID del turno que quiere eliminar: "))
    turnoAEliminar= None
    for turno in turnos:
        if turno[0] == id_turno:
            turnoAEliminar=turno
            break
    if turnoAEliminar:
        turnos.remove(turnoAEliminar)
        print(f"Turno {id_turno} eliminado con éxito.")
        return
    else:
        print("No existe un turno con ese ID.")
        return

def buscar_paciente(pacientes):
    """
    Busca pacientes en una lista según un campo específico (nombre, apellido, DNI, etc.).

    Parámetros:
        pacientes (list[dict]): Lista de diccionarios con los datos de los pacientes.

    Comportamiento:
        - Pide al usuario que elija un campo para buscar.
        - Solicita el valor a buscar (ignorando mayúsculas y acentos).
        - Si hay un resultado, lo muestra.
        - Si hay varios, muestra un submenú para elegir.
        - Si no hay coincidencias, lo informa.

    Retorna:
        None
    """
    
    campos = ("nombre", "apellido", "dni", "mail", "grupo_sanguineo")
    opcion = int(input("Buscar por:\n1) Nombre\n2) Apellido\n3) DNI\n4) Mail\n5) Grupo Sanguíneo\nOpción: "))

    while opcion < 1 or opcion > len(campos):
        opcion = int(input("Opcion no valida\nBuscar por:\n1) Nombre\n2) Apellido\n3) DNI\n4) Mail\n5) Grupo Sanguíneo\nOpción: "))

    campo_seleccionado = campos[opcion - 1]
    valor_buscado = quitar_acentos(input(f"Ingrese {campo_seleccionado}: ").lower())
    
    resultados = []
    
    for i in range(len(pacientes)):
        valor_actual = quitar_acentos(str(pacientes[i][f"{campo_seleccionado}"]).lower())
        if valor_actual == valor_buscado:
            resultados.append(pacientes[i])

    if len(resultados) == 1:
        paciente = resultados[0]
        for i in paciente:
            print(f"{i.replace('_', ' ').capitalize()}: {paciente[i]}")

    elif len(resultados) > 1:
        print("\nSe encontraron varios pacientes:")
        
        campos_orden = ["nombre", "apellido", "dni"] # Campos que se mostraran en el resultado (ordenados)
        
        for i, paciente in enumerate(resultados, start=1):
            print(f"Paciente {i}:")
            for i in campos_orden:
                print(f"{i.replace('_', ' ').capitalize()}: {paciente[i]}")
            print("-" * 30)
            
        pacienteElegido = int(input("Seleccione paciente: "))
        while pacienteElegido < 1 or pacienteElegido > len(resultados):
            pacienteElegido = int(input(f"Opción inválida: "))
            
        print("\nPaciente seleccionado:")
        paciente = resultados[pacienteElegido - 1]
        for i in paciente:
            print(f"{i.replace('_', ' ').capitalize()}: {paciente[i]}")
    else:
        print("No se encontraron pacientes.")
        return




def crear_paciente(pacientes):
    """Función que permite crear un nuevo paciente y agregarlo a la lista de pacientes.	
    Args:
        pacientes (list): Lista de pacientes.
    Returns:
        None
    Logica:
    - Solicita al usuario los datos del paciente, asegurándose de que no queden campos vacíos.
    - Valida el formato de la fecha de nacimiento.
    - Genera un nuevo ID para el paciente.
    - Crea un diccionario con los datos del paciente y lo agrega a la lista de pacientes.
    """
    nombre = validar_campo_vacio("Nombre: ")
    apellido = validar_campo_vacio("Apellido: ")
    dni = validar_campo_vacio("DNI: ")
    fecha_nac = input("Ingrese la fecha (AAAA-MM-DD): ")
    while not validarFecha(fecha_nac):
        print("El formato de la fecha es inválido.")
        fecha_nac = input("Ingrese la fecha de nacimiento(AAAA-MM-DD): ")  
    domicilio = validar_campo_vacio("Domicilio: ")
    mail = validar_campo_vacio("Mail: ")
    num_tel = validar_campo_vacio("Número de Teléfono: ")
    obra_social = validar_campo_vacio("Obra Social: ")
    nacionalidad = validar_campo_vacio("Nacionalidad: ")
    grupo_sanguineo = validar_campo_vacio("Grupo Sanguíneo: ")
    nuevo_id_paciente = max(pacientes, key=lambda x: x["id"])["id"] + 1 if pacientes else 1
    paciente = {
        "id": nuevo_id_paciente,
        "nombre": nombre,
        "apellido": apellido,
        "dni": dni,
        "fecha_nac": fecha_nac,
        "domicilio": domicilio,
        "mail": mail,
        "num_tel": num_tel,
        "obra_social": obra_social,
        "nacionalidad": nacionalidad,
        "grupo_sanguineo": grupo_sanguineo 
    }
    pacientes.append(paciente)  # Agregar el nuevo paciente a la lista de pacientes
    guardar_json("pacientes", pacientes)  # Guardar los cambios en el archivo JSON
    print_tabla("Paciente Agregado", [[paciente["id"], paciente["nombre"], paciente["apellido"], paciente["dni"], paciente["fecha_nac"], paciente["domicilio"], paciente["mail"], paciente["num_tel"], paciente["obra_social"], paciente["nacionalidad"], paciente["grupo_sanguineo"]]], ["ID", "Nombre", "Apellido", "DNI", "Fecha Nac.", "Domicilio", "Mail", "Teléfono", "Obra Social", "Nacionalidad", "Grupo Sanguíneo"])
    print(f"Paciente agregado con éxito.")
    print(f"ID asignado: {nuevo_id_paciente}")

def eliminar_paciente(pacientes):
    dni_paciente = input("Ingrese el DNI del paciente que desea eliminar: ")
    paciente_a_eliminar = None
    for id_paciente, datos_paciente in pacientes.items():
        if datos_paciente["dni"] == dni_paciente:
            paciente_a_eliminar = id_paciente
            break

    if paciente_a_eliminar:
        del pacientes[paciente_a_eliminar]
        print(f"Paciente con DNI {dni_paciente} eliminado con éxito.")
    else:
        print(f"No se encontró un paciente con DNI {dni_paciente}.")

def buscar_medico(medicos):
    campos = ("nombre", "apellido", "dni", "mail", "grupo_sanguineo")
    opcion = int(input("Buscar por:\n1) Nombre\n2) Apellido\n3) DNI\n4) Mail\nOpción: "))
    while opcion < 1 or opcion > len(campos):
        opcion = int(input("Opción no válida\nBuscar por:\n1) Nombre\n2) Apellido\n3) DNI\n4) Mail\nOpción: "))

    campo_seleccionado = campos[opcion - 1]
    valor_buscado = input(f"Ingrese {campo_seleccionado}: ").lower()
    resultados = []
    for id_medico, datos_medico in medicos.items():
        valor_actual = str(datos_medico[campo_seleccionado]).lower()
        if valor_actual == valor_buscado:
            resultados.append((id_medico, datos_medico))
    if resultados:
        for id_medico, datos in resultados:
            print(f"\nID: {id_medico}")
            for clave, valor in datos.items():
                print(f"{clave.capitalize()}: {valor}")
    else:
        print("No se encontraron médicos con ese dato.")

def eliminar_medico(medicos, turnos, pacientes):
    id_medico = mensajesTipoNumerico("Ingrese el ID del médico que desea eliminar: ")
    
    if not verificarSiExiste(id_medico, medicos, "médico"):
        return 
    
    if tieneTurnosAsignados(id_medico, turnos, 2):
        print("No se puede eliminar el médico porque tiene turnos asignados.")
        print("Primero elimine los turnos asignados que tiene el médico. (Use la opción 4 del menú.)")
        
        print("\nTurnos asignados:")
        for turno in turnos:
            if turno[2] == id_medico:
                id_paciente = turno[1]
                print(f"- Turno {turno[0]} | Paciente: {pacientes[id_paciente]['nombre']} {pacientes[id_paciente]['apellido']} | Médico: {medicos[id_medico]['nombre']} {medicos[id_medico]['apellido']}")
        return
    
    confirmacion = input(f"¿Está seguro de que desea eliminar al médico {medicos[id_medico]['nombre']} {medicos[id_medico]['apellido']}? (si/no): ").strip().lower()
    if confirmacion == "si":
        nombre_medico = medicos[id_medico]['nombre']
        apellido_medico = medicos[id_medico]['apellido']
        del medicos[id_medico]
        print(f"Médico {nombre_medico} {apellido_medico} eliminado con éxito.")
    else:
        print("Se ha cancelado la eliminación del médico.")
        
def agregar_medico(medicos):
    """Función que permite agregar un nuevo médico a la lista de médicos.
    Args:
        medicos (list): Lista de médicos.
    Returns:
        None
    Logica:
    - Solicita al usuario los datos del médico, asegurándose de que no queden campos vacíos.
    - Valida el formato de la fecha de nacimiento.
    - Genera un nuevo ID para el médico.
    - Crea un diccionario con los datos del médico y lo agrega a la lista de médicos.
    """
    print(f"Agregar Médico: ")

    nombre = validar_campo_vacio("Nombre: ")
    apellido = validar_campo_vacio("Apellido: ")
    especialidad = validar_campo_vacio("Especialidad: ")
    mail = validar_campo_vacio("Mail: ")
    dni = validar_campo_vacio("DNI: ")
    fecha_nac = input("Ingrese la fecha (AAAA-MM-DD): ")
    while not validarFecha(fecha_nac):
        print("El formato de la fecha es inválido.")
        fecha_nac = input("Ingrese la fecha (AAAA-MM-DD): ") 
    num_tel = validar_campo_vacio("Número de Teléfono: ")
    domicilio = validar_campo_vacio("Domicilio: ")
    nacionalidad = validar_campo_vacio("Nacionalidad: ")
    titulo = validar_campo_vacio("Título: ")
    matricula = validar_campo_vacio("Matrícula: ")
    # Generar un nuevo ID para el médico
    nuevo_id = max(medicos, key=lambda x: x["id"])["id"] + 1 if medicos else 1
    medico = {
        "id": nuevo_id,
        "nombre": nombre,
        "apellido": apellido,
        "especialidad": especialidad,
        "dni": dni,
        "fecha_nac": fecha_nac,
        "domicilio": domicilio,
        "mail": mail,
        "num_tel": num_tel,
        "nacionalidad": nacionalidad,
        "titulo": titulo,
        "matricula": matricula
    }

    medicos.append(medico)  # Agregar el nuevo médico a la lista de médicos
    guardar_json("medicos", medicos)  # Guardar los cambios en el archivo JSON
    print_tabla("Médico Agregado", [[medico["id"], medico["nombre"], medico["apellido"], medico["especialidad"], medico["dni"], medico["fecha_nac"], medico["domicilio"], medico["mail"], medico["num_tel"], medico["nacionalidad"], medico["titulo"], medico["matricula"]]], ["ID", "Nombre", "Apellido", "Especialidad", "DNI", "Fecha Nac.", "Domicilio", "Mail", "Teléfono", "Nacionalidad", "Título", "Matrícula"])
    print(f"Médico agregado con éxito.")
    print(f"ID asignado: {nuevo_id}")

def agenda_medico(medicos, turnos):
    """Función que muestra la agenda de un médico específico.	
    Args:
        medicos (list): Lista de médicos.
        turnos (list): Lista de turnos médicos.
    Returns:
        None
    Logica:
    - Imprime la lista de médicos disponibles.
    - Solicita al usuario que ingrese el ID del médico cuya agenda desea ver.
    - Verifica si el ID del médico existe.
    - Si el médico existe, filtra los turnos asignados a ese médico.
    - Si no hay turnos asignados, muestra un mensaje indicando que no hay turnos para ese médico.
    - Si hay turnos, ordena la agenda por fecha y hora.
    - Imprime la agenda del médico en formato tabular.
    """
    print("Agenda Médica:")
    if not medicos:
        print("No hay médicos registrados.")
        return
    print("Médicos disponibles:")
    info_medicos = []
    for medico in medicos:
        info_medicos.append([medico["id"], medico["nombre"], medico["apellido"], medico["especialidad"]])
    print_tabla("Lista de Médicos", info_medicos, ["ID", "Nombre", "Apellido", "Especialidad"])
    id_medico = int(input("Ingrese el ID del médico para ver su agenda: "))
    if not verificarSiExiste(id_medico, medicos, "médico"):
        return
    print(f"\nAgenda del Médico {medicos[id_medico]['nombre']} {medicos[id_medico]['apellido']}:")
    agenda = []
    for turno in turnos:
        if turno["medico"] == id_medico:
            #sacar el id del medico del turno para no mostrarlo en la agenda
            turno.pop("medico", None)
            turno.pop("id", None)
            agenda.append(turno)
    # Si no hay turnos asignados, se muestra un mensaje indicando que no hay turnos para ese médico
    if not agenda:
        print("No hay turnos asignados para este médico.")
        return
    # Ordenar la agenda por fecha y hora
    agenda.sort(key=lambda x: (x["fecha"], x["hora"]))
    tabla_agenda = []
    for item in agenda:
        paciente = item["paciente"]
        tabla_agenda.append([item["fecha"], item["hora"], paciente, item["consultorio"]])

    print_tabla("Agenda del Médico", tabla_agenda, ["Fecha", "Hora", "Paciente", "Consultorio"])
    