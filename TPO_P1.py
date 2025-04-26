# Definir la matriz de turnos de ejemplo (id, paciente, médico, consultorio, fecha, hora)
# Diccionario de pacientes
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

    id_paciente = int(input("Ingrese el ID del paciente: "))

    if id_paciente not in pacientes:
        print("No existe un paciente con ese ID.")
        return
    if id_paciente in pacientes:
        id_medico = int(input("Ingrese el ID del médico: "))
        if id_medico in medicos:
            ids = [turno[0] for turno in turnos] #recorro toda la lista de turnos y guardo los id en una lista
            if ids:
                id_turno = max(ids) + 1
            else:
                id_turno = 1
            consultorio = input("Ingrese el nombre del consultorio: ")
            fecha = input("Ingrese la fecha (AAAA-MM-DD): ")
            hora = input("Ingrese la hora (HH:MM): ")
            turnos.append((len(turnos) + 1, id_paciente, id_medico, consultorio, fecha, hora))
            print(f"Turno {len(turnos)} agregado con éxito.")
            return
        else:
            print("No existe un médico con ese ID.")
            return
    else:
        print("No existe un paciente con ese ID.")
        return
    
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
    id_turno= int(input("Ingrese el ID del turno que quiere modificar: "))
    for turno in turnos:
        if turno[0]== id_turno:
            turnoAModificar=turno
            break
    if turnoAModificar is not None:
        print("¿Que desea modificar del turno?")
        print("1. Paciente")
        print("2. Médico")
        print("3. Consultorio")
        print("4. Fecha")
        print("5. Hora")
        print("6. Todo")
        opcion=int(input("Eliga la opcion que desea modificar: "))

        turno = list(turnos[turnoAModificar]) # Convertir la tupla a lista para poder modificarla
        if opcion == 1:
            id_paciente=int(input("Ingrese el nuevo ID del paciente: "))
            if id_paciente in pacientes:
                turnoAModificar[1]=id_paciente
                print("ID del paciente modificado con éxito.")
        elif opcion ==2:
            id_medico=int(input("Ingrese el nuevo ID del médico: "))
            if id_medico in medicos:
                turnoAModificar[2]=id_medico
                print("ID del médico modificado con éxito.")
            else:
                print("No existe un médico con ese ID.")
        elif opcion ==3:
            consultorio=input("Ingrese el nuevo nombre del consultorio: ")
            turnoAModificar[3]=consultorio
            print("El nuevo nombre del consultorio fue modificado con éxito.")
        elif opcion ==4:
            fecha=input("Ingrese la nueva fecha (AAAA-MM-DD): ")
            turnoAModificar[4]=fecha
            print("La nueva fecha fue modificada con éxito.")
        elif opcion ==5:
            hora=input("Ingrese la nueva hora (HH:MM): ")
            turnoAModificar[5]=hora
            print("La nueva hora fue modificada con éxito.")
        elif opcion ==6:
            id_paciente=int(input("Ingrese el nuevo ID del paciente: "))
            if id_paciente in pacientes:
                turnoAModificar[1]=id_paciente
            else: 
                print("No existe un paciente con ese ID.")
                return
            id_medico=int(input("Ingrese el nuevo ID del médico: "))
            if id_medico in medicos:
                turnoAModificar[2]=id_medico
                print("ID del médico modificado con éxito.")
            else:
                print("No existe un médico con ese ID.")
                return
            consultorio=input("Ingrese el nuevo nombre del consultorio: ")
            turnoAModificar[3]=consultorio
            print("El nuevo nombre del consultorio fue modificado con éxito.")
            fecha=input("Ingrese la nueva fecha (AAAA-MM-DD): ")
            turnoAModificar[4]=fecha
            print("La nueva fecha fue modificada con éxito.")
            hora=input("Ingrese la nueva hora (HH:MM): ")
            turnoAModificar[5]=hora
            print("La nueva hora fue modificada con éxito.")
        else:
            print("Opción no válida. Intente de nuevo.")
            return
        turnos[turnoAModificar] = tuple(turno)  # Guardamos de nuevo como tupla
        print(f"Turno {id_turno} modificado con éxito.")
    else:
        print(f"No se encontró un turno con el ID {id_turno}.")

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
        
