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
 
def buscar_paciente_nombre(pacientes, nombre):
    for clave, valor in pacientes.items():
        if pacientes[clave]["nombre"] == nombre:
            print("\n" ,pacientes[clave]["nombre"], pacientes[clave]["apellido"], pacientes[clave]["dni"])



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
    print("9. Salir")

# Lógica para el menú
while True:
    mostrar_menu()
    opcion = input("\nSeleccione una opción: ")
    if opcion == "1":
        ver_turnos(turnos)
    elif opcion == "2":
        print("Función para agregar turno en construcción...")
    elif opcion == "3":
        print("Función para modificar turno en construcción...")
    elif opcion == "4":
        print("Función para eliminar turno en construcción...")
    elif opcion == "5":
        nombre = input("Ingrese nombre a buscar: ")
        buscar_paciente_nombre(pacientes, nombre)
    elif opcion == "6":
        crear_paciente(pacientes)
    elif opcion == "9":
        print("Saliendo del programa.")
    else:
        print("Opción no válida. Intente de nuevo.")
        
