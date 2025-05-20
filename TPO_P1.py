from funciones.funciones_generales import *
from funciones.funciones_principales import *

# Cargar los datos desde los archivos JSON
pacientes = cargar_json("pacientes")
medicos = cargar_json("medicos")
turnos = cargar_json("turnos")
# Lógica para el menú
while True:
    mostrar_menu()
    opcion = input("\nSeleccione una opción: ")
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
    elif opcion == "12":
        print("Saliendo del programa.")
        break
    else:
        print("Opción no válida. Intente de nuevo.")