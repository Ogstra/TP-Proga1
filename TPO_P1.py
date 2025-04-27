
# Definir la matriz de turnos de ejemplo (id, paciente, médico, consultorio, fecha, hora)
# Diccionario de pacientes
from datetime import datetime
pacientes = {
    1: {
        "nombre": "Juan",
        "apellido": "Pérez",
        "dni": "12345678",
        "fecha_nac": "1980-05-12",
        "domicilio": "Av. Siempre Viva 123",
        "mail": "juan.perez@email.com",
        "num_tel": "555-1234",
        "obra_social": "OSDE",
        "nacionalidad": "Argentina",
        "grupo_sanguineo": "O+"
    },
    2: {
        "nombre": "Ana",
        "apellido": "López",
        "dni": "23456789",
        "fecha_nac": "1992-07-24",
        "domicilio": "Calle Falsa 456",
        "mail": "ana.lopez@email.com",
        "num_tel": "555-5678",
        "obra_social": "Swiss Medical",
        "nacionalidad": "Argentina",
        "grupo_sanguineo": "A-"
    },
    3: {
        "nombre": "Ana",
        "apellido": "Perez",
        "dni": "28486789",
        "fecha_nac": "1998-07-24",
        "domicilio": "Calle Falsa 486",
        "mail": "ana.lopez@email.com",
        "num_tel": "555-5278",
        "obra_social": "Swiss Medical",
        "nacionalidad": "Argentina",
        "grupo_sanguineo": "A+"
    }
}

# Diccionario de médicos
medicos = {
    1: {
        "nombre": "María",
        "apellido": "Rodríguez",
        "especialidad": "Cardiología",
        "mail": "maria.rodriguez@email.com",
        "dni": "87654321",
        "fecha_nac": "1975-03-20",
        "num_tel": "555-9876",
        "domicilio": "Av. Salud 789",
        "nacionalidad": "Argentina",
        "titulo": "Doctor en Medicina",
        "matricula": "12345"
    },
    2: {
        "nombre": "Carlos",
        "apellido": "Martínez",
        "especialidad": "Dermatología",
        "mail": "carlos.martinez@email.com",
        "dni": "76543210",
        "fecha_nac": "1985-09-10",
        "num_tel": "555-5432",
        "domicilio": "Calle Piel 101",
        "nacionalidad": "Argentina",
        "titulo": "Doctor en Medicina",
        "matricula": "67890"
    }
}

# Matriz de turnos con referencia a los IDs
turnos = [
    (1, 1, 1, "Consultorio 101", "2025-04-15", "10:00"),  # Juan Pérez con Dra. Rodríguez
    (2, 2, 2, "Consultorio 202", "2025-04-16", "11:30")   # Ana López con Dr. Martínez
]   

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

# Función para mostrar turnos con información expandida
def ver_turnos(turnos):
    print("\nLista de turnos:")
    for turno in turnos:
        id_turno, id_paciente, id_medico, consultorio, fecha, horario = turno
        paciente = pacientes[id_paciente]
        medico = medicos[id_medico]
        print(f"Turno {id_turno}: {fecha} a las {horario}")
        print(f"  Paciente: {paciente['nombre']} {paciente['apellido']} ({paciente['dni']})")
        print(f"  Médico: {medico['nombre']} {medico['apellido']} - {medico['especialidad']}")
        print(f"  Consultorio: {consultorio}\n")

def crear_paciente(pacientes):
    paciente = {
    "nombre": input("Nombre: "),
    "apellido": input("Apellido: "),
    "dni": input("DNI: "),
    "fecha_nac": input("Fecha de Nacimento: "),
    "domicilio": input("Domicilio: "),
    "mail": input("Mail: "),
    "num_tel": input("Numero de Telefono: "),
    "obra_social": input("Obra Social: "),
    "nacionalidad": input("Nacionalidad: "),
    "grupo_sanguineo": input("Grupo Sanguineo: ")
    }
    pacientes.update(paciente)
    
    print(f"--- Paciente agregado ---")
"""     for clave, valor in paciente.items():
        print(clave, ": " ,valor)
 """
 
def buscar_paciente(pacientes):
    campos = ("nombre", "apellido", "dni", "mail", "grupo_sanguineo")
    opcion = int(input("Buscar por:\n1) Nombre\n2) Apellido\n3) DNI\n4) Mail\n5) Grupo Sanguíneo\nOpción: "))

    while opcion < 1 or opcion > len(campos):
        opcion = int(input("Opcion no valida\nBuscar por:\n1) Nombre\n2) Apellido\n3) DNI\n4) Mail\n5) Grupo Sanguíneo\nOpción: "))



    campo_seleccionado = campos[opcion - 1]
    valor_buscado = input(f"Ingrese {campo_seleccionado}: ").lower()

    resultados = []
    for id_paciente, datos_paciente in pacientes.items():
        valor_actual = str(datos_paciente[campo_seleccionado]).lower()
        if valor_actual == valor_buscado:
            resultados.append((id_paciente, datos_paciente))

    if resultados:
        for id_paciente, datos in resultados:
            print(f"\nID: {id_paciente}")
            for clave, valor in datos.items():
                print(f"{clave.capitalize()}: {valor}")
    else:
        print("No se encontraron pacientes con ese dato.")

def agenda_medico(medicos, turnos):
    while True:
        print("\n=== Lista de Médicos ===")
        for id_medico, datos in medicos.items():
            print(f"{id_medico}. {datos['nombre']} {datos['apellido']}")
        print("0. Atras")

        id_elegido = input("Ingrese el ID del médico para ver sus turnos (0 para salir): ")

        if not id_elegido.isdigit():
            print("❌ ID inválido. Debe ser un número.")
            continue

        id_elegido = int(id_elegido)

        if id_elegido == 0:
            print("Saliendo del listado de turnos por médico.")
            break

        if id_elegido not in medicos:
            print("❌ No existe un médico con ese ID.")
            continue

        print(f"\nTurnos asignados al Dr/a. {medicos[id_elegido]['nombre']} {medicos[id_elegido]['apellido']}:")

        turnos_medico = []
        for turno in turnos:
            if turno[2] == id_elegido:
                turnos_medico.append(turno)

        if not turnos_medico:
            print("No hay turnos asignados.")
            continue

        for turno in turnos_medico:
            id_paciente = turno[1]
            paciente = pacientes.get(id_paciente, {"nombre": "Desconocido", "apellido": ""})
            print(f"- {paciente['nombre']} {paciente['apellido']} | Consultorio: {turno[3]} | Fecha: {turno[4]} | Hora: {turno[5]}")

def agregar_turno(turnos, medicos, pacientes):

    print("\n=== Agregar Turno ===")

    id_paciente = mensajesTipoNumerico("Ingrese el ID del paciente: ")
    if not verificarSiExiste(id_paciente, pacientes, "paciente"):
        return
    id_medico = mensajesTipoNumerico("Ingrese el ID del médico: ")
    if not verificarSiExiste(id_medico, medicos, "médico"):
        return
   
    consultorio = input("Ingrese el nombre del consultorio: ")
    fecha = input("Ingrese la fecha (AAAA-MM-DD): ")
    if not validarFecha(fecha):
        print("El formato de la fecha es inválido.")
        return
    hora = input("Ingrese la hora (HH:MM): ")
    if not validarHora(hora):
        print("El formato de la hora es inválido.")
        return
    id_turno = max([turno[0] for turno in turnos], default=0) + 1
    turnos.append((id_turno, id_paciente, id_medico, consultorio, fecha, hora))
    print(f"Turno {len(turnos)} agregado con éxito.")
           
    
    
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

def modificar_turno(turnos, medicos, pacientes):
    try:
        id_turno =mensajesTipoNumerico ("Ingrese el ID del turno que quiere modificar: ")
    except ValueError:
        print("Debe ingresar un número de ID válido.")
        return

    turnoAModificar = None
    for i in range(len(turnos)):
        if turnos[i][0] == id_turno:
            turnoAModificar = i
            break

    if turnoAModificar is None:
        print(f"No se encontró un turno con el ID {id_turno}.")
        return

    turno = list(turnos[turnoAModificar])  # Convertimos la tupla en lista para poder modificarla

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
        turno[3] = consultorio
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
    turnos[turnoAModificar] = tuple(turno)  # Volvemos a guardar como tupla
    print(f"\n Turno {id_turno} modificado con éxito.")

# Función para mostrar el menú
def mostrar_menu():
    print("\nMenú de Turnos Médicos")
    print("1. Ver lista de turnos")  
    print("2. Agregar turno")  
    print("3. Modificar turno")
    print("4. Eliminar turno") 
    print("5. Buscar paciente")
    print("6. Crear paciente")
    print("7. Eliminar paciente")
    print("8. Buscar médico")
    print("9. Ver agenda de médico")
    print("10. Salir")

# Lógica para el menú
while True:
    mostrar_menu()
    opcion = input("\nSeleccione una opción: ")
    if opcion == "1":
        ver_turnos(turnos)
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
    elif opcion == "9":
        agenda_medico(medicos, turnos)
    elif opcion == "10":
        print("Saliendo del programa.")
        break
    else:
        print("Opción no válida. Intente de nuevo.")
        
