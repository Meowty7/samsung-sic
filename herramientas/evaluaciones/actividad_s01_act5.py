# ---------------------------------------------------------------
# Base de datos de estudiantes en memoria: lista de diccionarios.
# Cada estudiante: {"nombre": str, "id": int, "edad": int}
#
# Pensado para ejecutarse en el navegador: ahí input() abre una ventana
# emergente y lo impreso con print() recién se ve al terminar. Por eso el
# menú y el resultado de cada acción se muestran dentro de la ventana, y
# "Cancelar" (o dejar vacío) termina el programa.
# ---------------------------------------------------------------
base_de_datos = [
    {"nombre": "Juan", "id": 1, "edad": 20},
    {"nombre": "María", "id": 2, "edad": 22},
    {"nombre": "Carlos", "id": 3, "edad": 21},
]

MENU = (
    "BASE DE DATOS DE ESTUDIANTES\n"
    "1. Agregar\n"
    "2. Mostrar\n"
    "3. Buscar\n"
    "4. Actualizar\n"
    "5. Eliminar\n"
    "6. Salir\n"
    "Elija una opción (Cancelar para salir):"
)


def leer(mensaje):
    """Lee un texto. Devuelve None si el usuario cancela la ventana."""
    try:
        valor = input(mensaje)
    except (EOFError, KeyboardInterrupt):
        return None
    if valor is None:
        return None
    return valor.strip()


def leer_entero(mensaje):
    """Lee un entero. Devuelve None si el usuario cancela o deja vacío."""
    while True:
        valor = leer(mensaje)
        if not valor:
            return None
        if valor.isdigit():
            return int(valor)
        mensaje = "Debe ingresar un número entero.\n" + mensaje


def buscar_por_id(id_buscado):
    """Devuelve el diccionario del estudiante con ese id, o None si no existe."""
    for estudiante in base_de_datos:
        if estudiante["id"] == id_buscado:
            return estudiante
    return None


def ficha(estudiante):
    """Texto con los datos de un estudiante."""
    return f"Id: {estudiante['id']} | Nombre: {estudiante['nombre']} | Edad: {estudiante['edad']}"


# Cada acción devuelve un mensaje con su resultado para mostrarlo en la siguiente ventana.

# a. Agregar
def agregar_estudiante():
    id_nuevo = leer_entero("Número de identificación:")
    if id_nuevo is None:
        return "Operación cancelada."
    if buscar_por_id(id_nuevo) is not None:
        return "Ya existe un estudiante con ese id."
    nombre = leer("Nombre:")
    if not nombre:
        return "Operación cancelada."
    edad = leer_entero("Edad:")
    if edad is None:
        return "Operación cancelada."
    base_de_datos.append({"nombre": nombre, "id": id_nuevo, "edad": edad})
    return f"Estudiante {nombre} agregado."


# b. Mostrar
def mostrar_estudiantes():
    if not base_de_datos:
        return "La base de datos está vacía."
    return "Estudiantes registrados:\n" + "\n".join(ficha(e) for e in base_de_datos)


# c. Buscar
def buscar_estudiante():
    id_buscado = leer_entero("Id a buscar:")
    if id_buscado is None:
        return "Operación cancelada."
    estudiante = buscar_por_id(id_buscado)
    return ficha(estudiante) if estudiante else "No se encontró el estudiante."


# d. Actualizar (dejar vacío conserva el valor actual)
def actualizar_estudiante():
    id_buscado = leer_entero("Id a actualizar:")
    if id_buscado is None:
        return "Operación cancelada."
    estudiante = buscar_por_id(id_buscado)
    if estudiante is None:
        return "No se encontró el estudiante."
    nombre = leer(f"Nuevo nombre (vacío conserva '{estudiante['nombre']}'):")
    edad = leer(f"Nueva edad (vacío conserva {estudiante['edad']}):")
    if nombre:
        estudiante["nombre"] = nombre
    if edad and edad.isdigit():
        estudiante["edad"] = int(edad)
    return "Estudiante actualizado: " + ficha(estudiante)


# e. Eliminar
def eliminar_estudiante():
    id_buscado = leer_entero("Id a eliminar:")
    if id_buscado is None:
        return "Operación cancelada."
    estudiante = buscar_por_id(id_buscado)
    if estudiante is None:
        return "No se encontró el estudiante."
    base_de_datos.remove(estudiante)
    return f"Estudiante {estudiante['nombre']} eliminado."


# Menú interactivo: se repite hasta elegir 6, cancelar o dejar vacío
def menu():
    acciones = {
        "1": agregar_estudiante,
        "2": mostrar_estudiantes,
        "3": buscar_estudiante,
        "4": actualizar_estudiante,
        "5": eliminar_estudiante,
    }
    resultado = ""
    while True:
        # El resultado de la acción anterior aparece arriba del menú
        opcion = leer((resultado + "\n\n" if resultado else "") + MENU)
        if not opcion or opcion == "6":
            break
        accion = acciones.get(opcion)
        resultado = accion() if accion else "Opción no válida."
        print(resultado)          # también queda en la salida al terminar
    print("Fin del programa.")
    print(mostrar_estudiantes())


menu()
