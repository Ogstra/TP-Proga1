from funciones.funciones_validaciones import *
from funciones.funciones_generales import *

# Cargar los datos desde los archivos JSON
pacientes = cargar_json("pacientes")
medicos = cargar_json("medicos")
turnos = cargar_json("turnos")
config = cargar_json("config")
consultorios = config["consultorios"]


def menu_roles(roles):
    """
    Función que muestra un menú para seleccionar un rol utilizando recursividad.

    Args:
        roles (list): Lista de roles disponibles.

    Returns:
        str: Rol seleccionado por el usuario o None si se elige salir.

    Lógica:
        - Muestra las opciones de roles disponibles.
        - Solicita al usuario que seleccione un rol.
        - Devuelve el rol seleccionado o finaliza el programa si se elige salir.
    """
    print('Seleccione rol:')
    for i in range(len(roles)):
        print(f'{i + 1}. {roles[i]}')
    print("0. Salir")

    try:
        opcion = mensajesTipoNumerico("\nSeleccione una opción: ")
        if opcion == 0:
            print("Saliendo del programa...")
            exit()
        elif 1 <= opcion <= len(roles):
            return roles[opcion - 1]
        else:
            print("Opción inválida. Intente nuevamente.")
            return menu_roles(roles)
    except ValueError:
        print("Debe ingresar un número válido.")
        return menu_roles(roles)

def mostrar_menu(rol, opciones):
    """
    Función que muestra el menú principal con las opciones disponibles en el json y maneja las opciones seleccionadas por el usuario.

    Args:
        turnos (list): Lista de turnos médicos.
        pacientes (dict): Diccionario de pacientes.
        medicos (dict): Diccionario de médicos.

    Returns:
        str: Opción seleccionada por el usuario.

    Lógica:
        - Imprime el menú de opciones disponibles.
        - Solicita al usuario que seleccione una opción.
        - Dependiendo de la opción seleccionada, llama a la función correspondiente.
        - Si la opción es "0", finaliza el programa.
        - Si la opción es inválida, muestra un mensaje de error y vuelve a solicitar una opción.
    """
    print(f"\n--- Menú para {rol} ---") 

    contexto = {
        "turnos": turnos,
        "pacientes": pacientes,
        "medicos": medicos,
        "rol": rol,
        "opciones": opciones
    }
    
    opciones_validas = [op for op in opciones if rol in op["roles"]]
    opciones_validas.sort(key=lambda op: op["clave"] == "editar_config_menu")

    for i, op in enumerate(opciones_validas, start=1):
        print(f"{i}. {op['texto']}")
    print("0. Salir")

    opcion = mensajesTipoNumerico("\nSeleccione una opción (0 para salir): ")
    
    if opcion == 0:
        print("Saliendo del programa...")
        exit()
    if 1 <= opcion <= len(opciones_validas):
        seleccionada = opciones_validas[opcion - 1]
        nombre_funcion = seleccionada['clave']
        argumentos = seleccionada.get('argumentos', [])

        args = [contexto[arg] for arg in argumentos if arg in contexto]
        ejecutar(nombre_funcion, *args)
    else:
        print("Opción no válida. Intente de nuevo.")
        
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
    info_turno.sort(key=lambda x: datetime.strptime(f"{x[0]} {x[1]}", "%Y-%m-%d %H:%M"))

    print_tabla("Lista de Turnos", info_turno, ["Fecha", "Hora", "Paciente", "Medico", "Consultorio", "Estado"], "horizontal")

def crear_o_editar_turno(turnos, medicos, pacientes, id_turno=None):
    print("Asignación de Turno:")

    if not pacientes:
        print("No hay pacientes registrados.")
        return None

    if not medicos:
        print("No hay médicos registrados.")
        return None

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
            
    consultorio = input("Ingrese el número del consultorio: ").strip()

    while True:
        fecha = input("Ingrese la fecha (AAAA-MM-DD): ")
        if not validarFecha(fecha):
            print("Formato de fecha inválido.")
            continue
        break

    while True:
        hora = input("Ingrese la hora (HH:MM): ")
        if not validarHora(hora):
            print("Formato de hora inválido.")
            continue

        try:
            nueva_fecha_hora = datetime.strptime(f"{fecha} {hora}", "%Y-%m-%d %H:%M")
        except ValueError:
            print("Fecha y hora inválidas.")
            continue

        conflicto = False
        # Buscar consultorios ocupados en esa fecha y hora
        consultorios_ocupados = [
        turno['consultorio']
        for turno in turnos
        if turno['fecha'] == fecha and turno['hora'] == hora
        ]
        consultorios_disponibles = [
            c for c in consultorios if c not in consultorios_ocupados
        ]

        for turno in turnos:
            if id_turno is not None and turno["id"] == id_turno:
                continue  # Ignorar el mismo turno en caso de edición

            turno_fecha_hora = datetime.strptime(f"{turno['fecha']} {turno['hora']}", "%Y-%m-%d %H:%M")
            diferencia = abs((turno_fecha_hora - nueva_fecha_hora).total_seconds())

            if turno["medico"] == id_medico and diferencia < 600:
                print(f"Este médico ya tiene un turno dentro de 10 minutos.")
                
                conflicto = True
                break

            if turno["consultorio"] == consultorio and turno["fecha"] == fecha and turno["hora"] == hora:
                print("Consultorio ocupado en esa fecha y hora.")
                # Obtener disponibles
                consultorios_disponibles = [
                c for c in consultorios if c not in consultorios_ocupados
                ]
                conflicto = True
                if consultorios_disponibles:
                    print(f"\n *** Consultorios disponibles a las {hora or nueva_fecha_hora}: ***")
                    disponibles_por_piso = agrupar_consultorios_por_piso(consultorios)
                    print_tabla("Resultados de Médicos", [disponibles_por_piso], ["Piso 1","Piso 2","Piso 3","Piso 4","Piso 5"], "vertical")

                else:
                    print("No hay consultorios disponibles en esa fecha y hora.")
                break

        if conflicto:
            continue
        break
    
    
    return {
        "id": id_turno if id_turno is not None else (max([t["id"] for t in turnos], default=0) + 1),
        "paciente": id_paciente,
        "medico": id_medico,
        "consultorio": consultorio,
        "fecha": fecha,
        "hora": hora
    }

def agregar_turno(turnos, medicos, pacientes):
    nuevo_turno = crear_o_editar_turno(turnos, medicos, pacientes)
    if nuevo_turno:
        turnos.append(nuevo_turno)
        guardar_json("turnos", turnos)

        print_tabla("Turno Agregado", [[
            nuevo_turno["fecha"], nuevo_turno["hora"],
            pacientes[nuevo_turno["paciente"]]["nombre"] + " " + pacientes[nuevo_turno["paciente"]]["apellido"],
            medicos[nuevo_turno["medico"]]["nombre"] + " " + medicos[nuevo_turno["medico"]]["apellido"],
            nuevo_turno["consultorio"], "Pendiente"
        ]], ["Fecha", "Hora", "Paciente", "Medico", "Consultorio", "Estado"], "horizontal")

        print(f"Turno agregado con éxito. ID: {nuevo_turno['id']}")

def modificar_turno(turnos, medicos, pacientes):
    try:
        id_turno = mensajesTipoNumerico("Ingrese el ID del turno a modificar: ")
    except ValueError:
        print("ID inválido.")
        return

    for i, turno in enumerate(turnos):
        if turno["id"] == id_turno:
            turno_modificado = crear_o_editar_turno(turnos, medicos, pacientes, id_turno)
            if turno_modificado:
                turnos[i] = turno_modificado
                guardar_json("turnos", turnos)
                print(f"Turno {id_turno} modificado con éxito.")
            return

    print(f"No se encontró el turno con ID {id_turno}.")


def eliminar_medico(medicos, turnos, pacientes):
# La funcion busca primero el dni del medico y luego que si lo encuentra, verifica si tiene turnos asignados y si no lo elimina
# Una vez que ve que tiene turno, lo eliminara, despues te preguntara si quieres eliminar los turnos y el medico lo marcara como inactivo
    dni_medico = input("Ingrese el DNI del médico que desea eliminar: ").strip()
    # Buscar médico activo
    medico = next((m for m in medicos if m["dni"] == dni_medico and m.get("estado", "activo") == "activo"), None)
    if not medico:
        print(f"No se encontró un médico activo con DNI {dni_medico}.")
        return

    if tieneTurnosAsignados(dni_medico, turnos, "dni_medico"):
        print("Este médico tiene turnos asignados con pacientes.")
        
        
        turnos_medico = [t for t in turnos if t["dni_medico"] == dni_medico]
        for turno in turnos_medico:
            paciente = next((p for p in pacientes if p["dni"] == turno["dni_paciente"]), {})
            nombre = f"{paciente.get('nombre', 'Paciente')} {paciente.get('apellido', '')}"
            print(f"- Turno con {nombre} | Fecha: {turno['fecha']} | Hora: {turno['hora']}")

        confirmar = input("¿Deseás eliminar estos turnos y desactivar al médico? (s/n): ").strip().lower()
        if confirmar != "s":
            print("Operación cancelada.")
            return

        
        turnos[:] = [t for t in turnos if t["dni_medico"] != dni_medico]
        print("Turnos eliminados.")

   
    medico["estado"] = "inactivo"
    print("Médico marcado como inactivo.")

    # Guardar cambios
    guardar_json("medicos", medicos)
    guardar_json("turnos", turnos)


def buscar_paciente(pacientes):
    """
    Busca pacientes en una lista según un campo específico (nombre, apellido, DNI, etc.).
    Muestra los resultados en formato tabular.
    """
    campos = ("nombre", "apellido", "dni", "mail", "grupo_sanguineo")
    opcion = mensajesTipoNumerico("Buscar por:\n1) Nombre\n2) Apellido\n3) DNI\n4) Mail\n5) Grupo Sanguíneo\nOpción: ")
    if opcion == 0:
        return None
    while opcion < 1 or opcion > len(campos):
        opcion = mensajesTipoNumerico("Opcion no valida\nBuscar por:\n1) Nombre\n2) Apellido\n3) DNI\n4) Mail\n5) Grupo Sanguíneo\nOpción: ")

    campo_seleccionado = campos[opcion - 1]
    valor_buscado = quitar_acentos(input(f"Ingrese {campo_seleccionado}: ").lower())

    resultados = []
    for paciente in pacientes:
        valor_actual = quitar_acentos(str(paciente.get(campo_seleccionado, "")).lower())
        if valor_actual == valor_buscado:
            resultados.append(paciente)

    if resultados:
        columnas = ["ID", "Nombre", "Apellido", "DNI", "Fecha Nac.", "Domicilio", "Mail", "Teléfono", "Obra Social", "Nacionalidad", "Grupo Sanguíneo"]
        filas = [[p.get("id"), p.get("nombre"), p.get("apellido"), p.get("dni"), p.get("fecha_nac"), p.get("domicilio"), p.get("mail"), p.get("num_tel"), p.get("obra_social"), p.get("nacionalidad"), p.get("grupo_sanguineo")] for p in resultados]
        print_tabla("Resultados de Pacientes", filas, columnas, "vertical")
    else:
        print("No se encontraron pacientes.")

def buscar_medico(medicos):
    if not medicos:
        print("No hay médicos registrados.")
        return

    campos = ("nombre", "apellido", "dni", "mail", "grupo_sanguineo")
    try:
        opcion = int(input("Buscar por:\n1) Nombre\n2) Apellido\n3) DNI\n4) Mail\nOpción: "))
        while opcion < 1 or opcion > len(campos):
            opcion = int(input("Opción no válida\nBuscar por:\n1) Nombre\n2) Apellido\n3) DNI\n4) Mail\nOpción: "))
    except ValueError:
        print("Debe ingresar un número válido.")
        return

    campo_seleccionado = campos[opcion - 1]
    if campo_seleccionado == "dni":
        while True:
            valor_buscado = input("Ingrese DNI (8 dígitos): ").strip()
            if validarDNI(valor_buscado):
                break
            print("DNI inválido. Debe contener exactamente 8 dígitos numéricos.")
    elif campo_seleccionado == "mail":
        while True:
            valor_buscado = input("Ingrese mail: ").strip().lower()
            if validarMail(valor_buscado):
                break
            print("Mail inválido. Debe tener un formato válido (ej: nombre@dominio.com).")
    else:
        valor_buscado = quitar_acentos(input(f"Ingrese {campo_seleccionado}: ").lower())

    resultados = []
    for medico in medicos:
        valor_actual = quitar_acentos(str(medico.get(campo_seleccionado, "")).lower())
        if valor_actual == valor_buscado:
            resultados.append(medico)
    if resultados:
        columnas = ["ID", "Nombre", "Apellido", "Especialidad", "DNI", "Fecha Nac.", "Domicilio", "Mail", "Teléfono", "Nacionalidad", "Título", "Matrícula", "Horario", "Estado"]
        filas = [
            [
                m.get("id"),
                m.get("nombre"),
                m.get("apellido"),
                m.get("especialidad"),
                m.get("dni"),
                m.get("fecha_nac"),
                m.get("domicilio"),
                m.get("mail"),
                m.get("num_tel"),
                m.get("nacionalidad"),
                m.get("titulo"),
                m.get("matricula"),
                m.get("horario"),
                m.get("estado")
            ] for m in resultados
        ]
        print_tabla("Resultados de Médicos", filas, columnas, "vertical")
    else:
        print("No se encontraron médicos con ese dato.")

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
    while True:
        dni = validar_campo_vacio("DNI: ")
        if validarDNI(dni):
            break
    print("DNI inválido. Debe contener 8 dígitos numéricos.")

    fecha_nac = input("Ingrese la fecha (AAAA-MM-DD): ")
    while not validarFecha(fecha_nac):
        print("El formato de la fecha es inválido.")
        fecha_nac = input("Ingrese la fecha de nacimiento(AAAA-MM-DD): ")  
    domicilio = validar_campo_vacio("Domicilio: ")
    mail = validar_campo_vacio("Mail: ")
    while True:
        mail = validar_campo_vacio("Mail: ")
        if validarMail(mail):
            break
    print("Correo electrónico inválido.")

    num_tel = validar_campo_vacio("Número de Teléfono: ")
    while True:
        num_tel = validar_campo_vacio("Número de Teléfono (formato XXXX-XXXX): ")
        if validarTelefono(num_tel):
            break
    print("Teléfono inválido. Use el formato XXXX-XXXX.")

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
    print_tabla("Paciente Agregado", [[paciente["id"], paciente["nombre"], paciente["apellido"], paciente["dni"], paciente["fecha_nac"], paciente["domicilio"], paciente["mail"], paciente["num_tel"], paciente["obra_social"], paciente["nacionalidad"], paciente["grupo_sanguineo"]]], ["ID", "Nombre", "Apellido", "DNI", "Fecha Nac.", "Domicilio", "Mail", "Teléfono", "Obra Social", "Nacionalidad", "Grupo Sanguíneo"], "vertical")
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
        
        
def eliminar_medico(medicos, turnos, pacientes):
    # La funcion busca primero el dni del medico y luego que si lo encuentra, verifica si tiene turnos asignados y si no lo elimina
    # Una vez que ve que tiene turno, lo eliminara, despues te preguntara si quieres eliminar los turnos y el medico lo marcara como inactivo

    dni_medico = input("Ingrese el DNI del médico que desea eliminar: ").strip()

    # Buscar médico activo (normalizando el estado a minúsculas)
    medico = next((m for m in medicos if m["dni"] == dni_medico and m.get("estado", "activo").lower() == "activo"), None)
    
    if not medico:
        print(f"No se encontró un médico activo con DNI {dni_medico}.")
        return

    # Verificar si tiene turnos
    if tieneTurnosAsignados(dni_medico, turnos, "dni_medico"):
        print("Este médico tiene turnos asignados con pacientes.")
        
        # Mostrar pacientes afectados
        turnos_medico = [t for t in turnos if t["dni_medico"] == dni_medico]
        for turno in turnos_medico:
            paciente = next((p for p in pacientes if p["dni"] == turno["dni_paciente"]), {})
            nombre = f"{paciente.get('nombre', 'Paciente')} {paciente.get('apellido', '')}"
            print(f"- Turno con {nombre} | Fecha: {turno['fecha']} | Hora: {turno['hora']}")

        confirmar = input("¿Deseás eliminar estos turnos y desactivar al médico? (s/n): ").strip().lower()
        if confirmar != "s":
            print("Operación cancelada.")
            return

        # Eliminar turnos del médico
        turnos[:] = [t for t in turnos if t["dni_medico"] != dni_medico]
        print("El turno fue eliminado.")

    # Marcar médico como inactivo (guardando el mismo formato que en JSON)
    medico["estado"] = "Inactivo"
    print("Médico marcado como inactivo.")

    # Guardar cambios
    guardar_json("medicos", medicos)
    guardar_json("turnos", turnos)
        
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
    while True:
        mail = validar_campo_vacio("Mail: ")
        if validarMail(mail):
            break
        print("Correo electrónico inválido.")
    dni = validar_campo_vacio("DNI: ")
    while True:
        dni = validar_campo_vacio("DNI: ")
        if validarDNI(dni):
            break
        print("DNI inválido. Debe contener 8 dígitos numéricos.")
    fecha_nac = input("Ingrese la fecha (AAAA-MM-DD): ")
    while not validarFecha(fecha_nac):
        print("El formato de la fecha es inválido.")
        fecha_nac = input("Ingrese la fecha (AAAA-MM-DD): ") 
    num_tel = validar_campo_vacio("Número de Teléfono: ")
    while True:
        num_tel = validar_campo_vacio("Número de Teléfono (formato XXXX-XXXX): ")
        if validarTelefono(num_tel):
            break
        print("Teléfono inválido. Use el formato XXXX-XXXX.")

    domicilio = validar_campo_vacio("Domicilio: ")
    nacionalidad = validar_campo_vacio("Nacionalidad: ")
    titulo = validar_campo_vacio("Título: ")
    matricula = validar_campo_vacio("Matrícula: ")
    # Generar un nuevo ID para el médico
    nuevo_id = max(medicos, key=lambda x: x["id"])["id"] + 1 if medicos else 1
    horarios = pedir_horarios_medico()

    
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
        "matricula": matricula,
        "horario": horarios,
        "estado": "Activo"
    }

    medicos.append(medico)  # Agregar el nuevo médico a la lista de médicos
    guardar_json("medicos", medicos)  # Guardar los cambios en el archivo JSON
    print_tabla("Médico Agregado", [[medico["id"], medico["nombre"], medico["apellido"], medico["especialidad"], medico["dni"], medico["fecha_nac"], medico["domicilio"], medico["mail"], medico["num_tel"], medico["nacionalidad"], medico["titulo"], medico["matricula"], medico["horario"]]], ["ID", "Nombre", "Apellido", "Especialidad", "DNI", "Fecha Nac.", "Domicilio", "Mail", "Teléfono", "Nacionalidad", "Título", "Matrícula", "Horario"], "vertical")
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
    print_tabla("Lista de Médicos", info_medicos, ["ID", "Nombre", "Apellido", "Especialidad"], "horizontal")
    try:
        id_medico = int(input("Ingrese el ID del médico para ver su agenda: "))
    except ValueError:
        print("Debe ingresar un número válido.")
        return
    if not verificarSiExiste(id_medico, medicos, "médico"):
        return
    print(f"\nAgenda del Médico {medicos[id_medico]['nombre']} {medicos[id_medico]['apellido']}:")
    agenda = []
    for turno in turnos:
        if turno["medico"] == id_medico:
            #sacar el id del medico del turno para no mostrarlo en la agenda
            agenda.append({
                "fecha": turno["fecha"],
                "hora": turno["hora"],
                "paciente": turno["paciente"],
                "consultorio": turno["consultorio"]
            })
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

    print_tabla("Agenda del Médico", tabla_agenda, ["Fecha", "Hora", "Paciente", "Consultorio"], "horizontal")
  
def editar_config_menu(): 
    roles_no_eliminables = ["Admin", "Paciente", "Médico"]
    config = cargar_json("config")
    roles = config["roles"]
    opciones = config["opciones_menu"]
    
    def guardar_config():
        guardar_json('config', {
            "roles": roles,
            "consultorios": consultorios,
            "opciones_menu": opciones,
        })

    while True:
        print("\n--- Editor de Configuración ---")
        print("1. Ver roles disponibles")
        print("2. Agregar rol")
        print("3. Eliminar rol")
        print("4. Ver permisos de opciones")
        print("5. Modificar permisos de una opción")
        print("0. Volver")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            print("\nRoles disponibles:", ", ".join(roles))

        elif opcion == "2":
            nuevo_rol = input("Ingrese el nombre del nuevo rol: ").strip()
            if nuevo_rol and nuevo_rol not in roles:
                roles.append(nuevo_rol)
                print(f"Rol '{nuevo_rol}' agregado.")
                guardar_config()  # Guardar configuración inmediatamente
            else:
                print("Rol inválido o ya existe.")

        elif opcion == "3":
            if not roles:
                print("No hay roles disponibles para eliminar.")
            else:
                print("\n--- Seleccione un rol para eliminar ---")
                for i, rol in enumerate(roles, start=1):
                    print(
                        f"{i}. {rol} {'(No eliminable)' if rol in roles_no_eliminables else ''}")
                rol_a_eliminar = input(
                    "Ingrese el número del rol a eliminar: ")
                try:
                    rol_a_eliminar = int(rol_a_eliminar)
                    if 1 <= rol_a_eliminar <= len(roles):
                        rol_eliminado = roles[rol_a_eliminar - 1]
                        if rol_eliminado not in roles_no_eliminables:
                            roles.pop(rol_a_eliminar - 1)
                            for opcion in opciones:
                                if rol_eliminado in opcion["roles"]:
                                    opcion["roles"].remove(rol_eliminado)
                            print(f"Rol '{rol_eliminado}' eliminado.")
                            guardar_config()  # Guardar configuración inmediatamente
                        else:
                            print(
                                f"No se puede eliminar el rol '{rol_eliminado}'.")
                    else:
                        print("Número de rol inválido.")
                except ValueError:
                    print("Debe ingresar un número válido.")

        elif opcion == "4":
            print("\n--- Permisos por opción ---")
            for o in opciones:
                print(f"{o['clave']} ({o['texto']}): {', '.join(o['roles'])}")

        elif opcion == "5":
            while True:
                print("\n--- Submenú de Roles ---")
                print("Funciones disponibles:")
                for i, opcion in enumerate(opciones, start=1):
                    print(
                        f"{i}. {opcion['texto']} (Roles: {', '.join(opcion['roles'])})")

                print("0. Volver")

                sub_opcion = input("Seleccione una opción: ")

                if sub_opcion == "0":
                    break

                try:
                    sub_opcion = int(sub_opcion)
                    if 1 <= sub_opcion <= len(opciones):
                        funcion_seleccionada = opciones[sub_opcion - 1]
                        print(
                            f"\nFunciones seleccionada: {funcion_seleccionada['texto']}")
                        while True:
                            print("\n--- Opciones para el rol ---")
                            print("1. Agregar rol")
                            print("2. Quitar rol")
                            print("0. Volver")

                            rol_opcion = input("Seleccione una opción: ")

                            if rol_opcion == "0":
                                break

                            elif rol_opcion == "1":
                                while True:
                                    print("\n--- Submenú de Roles ---")
                                    print("Roles disponibles:")
                                    for i, rol in enumerate(roles, start=1):
                                        print(f"{i}. {rol}")
                                    print("0. Volver")

                                    rol_seleccionado = input(
                                        "Seleccione un rol para agregar a la función: ")

                                    if rol_seleccionado == "0":
                                        break

                                    try:
                                        rol_seleccionado = int(
                                            rol_seleccionado)
                                        if 1 <= rol_seleccionado <= len(roles):
                                            nuevo_rol = roles[rol_seleccionado - 1]
                                            if nuevo_rol not in funcion_seleccionada["roles"]:
                                                funcion_seleccionada["roles"].append(
                                                    nuevo_rol)
                                                print(
                                                    f"Rol '{nuevo_rol}' agregado a la función '{funcion_seleccionada['texto']}'.")
                                                guardar_config()  # Guardar configuración inmediatamente
                                                break
                                            else:
                                                print(
                                                    "El rol ya existe en la función.")
                                        else:
                                            print("Número de rol inválido.")
                                    except ValueError:
                                        print("Debe ingresar un número válido.")

                            elif rol_opcion == "2":
                                if not funcion_seleccionada["roles"]:
                                    print(
                                        "No hay roles disponibles para eliminar.")
                                else:
                                    print(
                                        "\n--- Seleccione un rol para eliminar ---")
                                    for j, rol in enumerate(funcion_seleccionada["roles"], start=1):
                                        print(
                                            f"{j}. {rol} {'(No eliminable)' if rol in roles_no_eliminables else ''}")
                                    rol_a_eliminar = input(
                                        "Ingrese el número del rol a eliminar: ")
                                    try:
                                        rol_a_eliminar = int(rol_a_eliminar)
                                        if 1 <= rol_a_eliminar <= len(funcion_seleccionada["roles"]):
                                            rol_eliminado = funcion_seleccionada["roles"][rol_a_eliminar - 1]
                                            if rol_eliminado not in roles_no_eliminables:
                                                funcion_seleccionada["roles"].remove(
                                                    rol_eliminado)
                                                print(
                                                    f"Rol '{rol_eliminado}' eliminado de la función '{funcion_seleccionada['texto']}'.")
                                                guardar_config()  # Guardar configuración inmediatamente
                                            else:
                                                print(
                                                    f"No se puede eliminar el rol '{rol_eliminado}'.")
                                        else:
                                            print("Número de rol inválido.")
                                    except ValueError:
                                        print("Debe ingresar un número válido.")

                            elif rol_opcion == "0":
                                break
                            else:
                                print("Opción inválida.")
                    else:
                        print("Número de opción inválido.")
                except ValueError:
                    print("Debe ingresar un número válido.")
        
        elif opcion == "0":
            break
        else:
            print("Opción inválida.")