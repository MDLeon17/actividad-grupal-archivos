"""
Grupo 5 Universidad: estudiantes, cursos, notas, observaciones académicas e
historial.
"""

"""
1. Registrar información.
2. Leer todos los registros.
3. Mostrar los datos recuperados correctamente.
4. Buscar un registro por su identificador.
5. Mostrar la posición inicial de cada registro.
6. Mostrar cuántos bytes ocupa cada registro.
7. Mostrar el tamaño total del archivo
"""

"""
Campos existentes en el archivo binario:
1. Carnet - int - fijo 8 bytes
2. Nombre - texto - variable
3. Fecha de nacimiento - fecha - fijo 3 bytes
4. Carrera - texto - variable
5. Curso - texto - variable
6. Observaciones - texto - variable
7. Estado académico - booleano - fijo 1 byte
8. Historial académico - texto - variable
9. Número de teléfono - número - fijo 8 bytes
10. nota final - float - fijo 4 bytes
"""

import struct

ARCHIVO = "datos.bin"

def guardar_texto(archivo, texto):
    # Convertimos el texto a bytes.
    texto_bytes = texto.encode("utf-8")

    # Calculamos la longitud real.
    longitud = len(texto_bytes)

    # Guardamos primero la longitud del texto.
    archivo.write(
        struct.pack("<I", longitud)
    )

    # Guardamos el texto.
    archivo.write(texto_bytes)

def leer_texto(archivo):
    # Leemos los 4 bytes donde está guardada
    # la longitud del texto.
    datos_longitud = archivo.read(4)

    if len(datos_longitud) != 4:
        return None

    # Recuperamos la longitud.
    longitud = struct.unpack(
        "<I",
        datos_longitud
    )[0]

    # Leemos exactamente la cantidad de bytes
    # que ocupa el texto.
    texto_bytes = archivo.read(longitud)

    if len(texto_bytes) != longitud:
        return None

    # Convertimos nuevamente los bytes a texto.
    texto = texto_bytes.decode("utf-8")

    return texto

def mostrar_tamanio_archivo():
    try:
        with open(ARCHIVO, "rb") as archivo:
            archivo.seek(0, 2)
            tamanio = archivo.tell()

            print("\nTamaño total del archivo:", tamanio, "bytes")

    except FileNotFoundError:
        print("\nEl archivo todavía no existe.")

def registrar_informacion():
    print("\nRegistrar información")
    carnet = int(input("Carnet: "))
    nombre = input("Nombre: ")
    print("\nFecha de nacimiento (solo enteros)")
    dia = int(input("Día: "))
    mes = int(input("Mes: "))
    anio = int(input("Año: "))
    carrera = input("Carrera: ")
    curso = input("Curso: ")
    observaciones = input("Observaciones académicas: ")
    estado = input("Estado académico (1 = activo, 0 = inactivo): ")
    historial = input("Historial académico (cursos asignados, desasignados): ")
    telefono = int(input("Número de teléfono: "))
    nota_final = float(input("Nota final: "))

    if estado == "1":
        estado_academico = True
    else:
        estado_academico = False

    with open(ARCHIVO, "ab") as archivo:
        # Guardamos la posición donde inicia el registro.
        posicion_inicial = archivo.tell()

        # Carnet - entero de 8 bytes.
        archivo.write(
            struct.pack("<q", carnet)
        )

        # Nombre - texto variable.
        guardar_texto(archivo, nombre)

        # Fecha de nacimiento - 3 bytes.
        archivo.write(
            struct.pack("<BBB", dia, mes, anio - 1900)
        )

        # Carrera - texto variable.
        guardar_texto(archivo, carrera)

        # Curso - texto variable.
        guardar_texto(archivo, curso)

        # Observaciones - texto variable.
        guardar_texto(archivo, observaciones)

        # Estado académico - booleano de 1 byte.
        archivo.write(
            struct.pack("<?", estado_academico)
        )

        # Historial - texto variable.
        guardar_texto(archivo, historial)

        # Telefono - entero de 8 bytes.
        archivo.write(
            struct.pack("<Q", telefono)
        )

        # Nota final - float de 4 bytes.
        archivo.write(
            struct.pack("<f", nota_final)
        )

        posicion_final = archivo.tell()

    tamanio_registro = posicion_final - posicion_inicial

    print("\nRegistro guardado correctamente.")
    print("Posición inicial:", posicion_inicial)
    print("Bytes utilizados:", tamanio_registro)

def leer_registro(archivo):
    # Carnet
    datos_carnet = archivo.read(8)

    if not datos_carnet:
        return None

    if len(datos_carnet) != 8:
        return None

    carnet = struct.unpack(
        "<q",
        datos_carnet
    )[0]

    # Nombre
    nombre = leer_texto(archivo)

    if nombre is None:
        return None

    # Fecha de nacimiento
    datos_fecha = archivo.read(3)

    if len(datos_fecha) != 3:
        return None

    dia, mes, anio_guardado = struct.unpack(
        "<BBB",
        datos_fecha
    )

    anio = anio_guardado + 1900

    # Carrera
    carrera = leer_texto(archivo)

    if carrera is None:
        return None

    # Curso
    curso = leer_texto(archivo)

    if curso is None:
        return None

    # Observaciones
    observaciones = leer_texto(archivo)

    if observaciones is None:
        return None

    # Estado académico
    datos_estado = archivo.read(1)

    if len(datos_estado) != 1:
        return None

    estado_academico = struct.unpack(
        "<?",
        datos_estado
    )[0]

    # Historial academico
    historial = leer_texto(archivo)

    if historial is None:
        return None

    # Telefono
    datos_telefono = archivo.read(8)

    if len(datos_telefono) != 8:
        return None

    telefono = struct.unpack(
        "<Q",
        datos_telefono
    )[0]

    # Nota final
    datos_nota = archivo.read(4)

    if len(datos_nota) != 4:
        return None

    nota_final = struct.unpack(
        "<f",
        datos_nota
    )[0]

    return (
        carnet,
        nombre,
        dia,
        mes,
        anio,
        carrera,
        curso,
        observaciones,
        estado_academico,
        historial,
        telefono,
        nota_final
    )

def leer_todos_registros():
    try:
        with open(ARCHIVO, "rb") as archivo:

            while True:
                registro = leer_registro(archivo)

                if registro is None:
                    break

                print(registro)

    except FileNotFoundError:
        print("\nEl archivo todavía no existe.")
        
def mostrar_datos_recuperados():
    try:
        with open(ARCHIVO, "rb") as archivo:
            numero_registro = 1

            while True:
                registro = leer_registro(archivo)

                if registro is None:
                    break

                carnet = registro[0]
                nombre = registro[1]
                dia = registro[2]
                mes = registro[3]
                anio = registro[4]
                carrera = registro[5]
                curso = registro[6]
                observaciones = registro[7]
                estado_academico = registro[8]
                historial = registro[9]
                telefono = registro[10]
                nota_final = registro[11]

                if estado_academico:
                    estado = "Activo"
                else:
                    estado = "Inactivo"

                print("\nRegistro", numero_registro)
                print("Carnet:", carnet)
                print("Nombre:", nombre)
                print("Fecha de nacimiento:", dia, "/", mes, "/", anio)
                print("Carrera:", carrera)
                print("Curso:", curso)
                print("Observaciones académicas:", observaciones)
                print("Estado académico:", estado)
                print("Historial académico:", historial)
                print("Número de teléfono:", telefono)
                print("Nota final:", nota_final)

                numero_registro += 1

    except FileNotFoundError:
        print("\nEl archivo todavía no existe.")
        
def buscar_registro(carnet_buscado):
    try:
        with open(ARCHIVO, "rb") as archivo:

            while True:
                # Guardamos la posición donde inicia el registro.
                posicion = archivo.tell()

                registro = leer_registro(archivo)

                if registro is None:
                    break

                carnet = registro[0]

                if carnet == carnet_buscado:
                    nombre = registro[1]
                    dia = registro[2]
                    mes = registro[3]
                    anio = registro[4]
                    carrera = registro[5]
                    curso = registro[6]
                    observaciones = registro[7]
                    estado_academico = registro[8]
                    historial = registro[9]
                    telefono = registro[10]
                    nota_final = registro[11]

                    if estado_academico:
                        estado = "Activo"
                    else:
                        estado = "Inactivo"

                    print("\nRegistro encontrado")
                    print("Posición inicial:", posicion)
                    print("Carnet:", carnet)
                    print("Nombre:", nombre)
                    print("Fecha de nacimiento:", dia, "/", mes, "/", anio)
                    print("Carrera:", carrera)
                    print("Curso:", curso)
                    print("Observaciones académicas:", observaciones)
                    print("Estado académico:", estado)
                    print("Historial académico:", historial)
                    print("Número de teléfono:", telefono)
                    print("Nota final:", nota_final)

                    return

            print("\nRegistro no encontrado.")

    except FileNotFoundError:
        print("\nEl archivo todavía no existe.")

while True:
    print("\nMenú de opciones:")
    print("1. Registrar información.")
    print("2. Leer todos los registros.")
    print("3. Mostrar los datos recuperados correctamente.")
    print("4. Buscar un registro por su identificador.")
    print("5. Mostrar la posición inicial de cada registro.")
    print("6. Mostrar cuántos bytes ocupa cada registro.")
    print("7. Mostrar el tamaño total del archivo.")
    print("8. Salir.")
    
    opcion_usuario = input("Ingrese el número de la opción deseada: ")
    
    match opcion_usuario:
        case "1":
            registrar_informacion()
        
        case "2":
            print("\nLeer todos los registros")
            leer_todos_registros()
        
        case "3":
            print("\nMostrar los datos recuperados correctamente")
            mostrar_datos_recuperados()
        
        case "4":
            print("\nBuscar un registro por su identificador")
            carnet_buscado = int(input("Ingrese el carnet que desea buscar: "))
            buscar_registro(carnet_buscado)
        
        case "5":
            print("\nMostrar la posición inicial de cada registro")
        
        case "6":
            print("\nMostrar cuántos bytes ocupa cada registro")
        
        case "7":
            print("\nMostrar el tamaño total del archivo")
        
        case "8":
            print("\nSaliendo del programa...")
            break
        
        case _:
            print("\nOpción inválida, intente de nuevo")