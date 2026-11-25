"""Genera 01-python/semana-01/actividad-asincronica.ipynb y prueba cada solución de referencia."""

import builtins
import contextlib
import io
import os
import tempfile
from pathlib import Path

import nbformat
from nbformat.v4 import new_code_cell, new_markdown_cell, new_notebook, new_output

RAIZ = Path(__file__).resolve().parents[2]
DESTINO = RAIZ / "01-python/semana-01/actividad-asincronica.ipynb"

S0 = "../semana-00"
U = {
    1: f"{S0}/clase-1-fundamentos/u01-pensamiento-computacional-y-entorno.ipynb",
    2: f"{S0}/clase-1-fundamentos/u02-algoritmos-y-diagramas-de-flujo.ipynb",
    3: f"{S0}/clase-1-fundamentos/u03-operadores-y-tipos-de-datos.ipynb",
    4: f"{S0}/clase-1-fundamentos/u04-variables.ipynb",
    5: f"{S0}/clase-2-control-de-flujo/u05-operadores-de-comparacion-y-logicos.ipynb",
    6: f"{S0}/clase-2-control-de-flujo/u06-sentencia-if.ipynb",
    7: f"{S0}/clase-2-control-de-flujo/u07-if-else-elif.ipynb",
    8: f"{S0}/clase-2-control-de-flujo/u08-bucle-for.ipynb",
    9: f"{S0}/clase-2-control-de-flujo/u09-bucle-while.ipynb",
    10: "clase-1-listas-tuplas-diccionarios/u10-listas-y-tuplas.ipynb",
    11: "clase-1-listas-tuplas-diccionarios/u11-diccionarios-y-json.ipynb",
    12: "clase-1-listas-tuplas-diccionarios/u12-iteracion-y-busqueda.ipynb",
    13: "clase-1-listas-tuplas-diccionarios/u13-listas-bidimensionales.ipynb",
    14: "clase-2-diccionarios-y-conjuntos/u14-diccionarios-crud.ipynb",
    15: "clase-2-diccionarios-y-conjuntos/u15-diccionarios-avanzados.ipynb",
    16: "clase-2-diccionarios-y-conjuntos/u16-conjuntos.ipynb",
}


def unidad(*nums):
    return ", ".join(f"[Unidad {n}]({U[n]})" for n in nums)


def solucion(codigo, explicacion):
    return (
        "<details><summary>Ver solución de referencia</summary>\n\n"
        f"```python\n{codigo.strip()}\n```\n\n{explicacion.strip()}\n</details>"
    )


def texto_modelo(texto):
    return f"<details><summary>Ver respuesta modelo</summary>\n\n{texto.strip()}\n</details>"


ACTIVIDADES = []  # (titulo, enunciado, guia, codigo_inicial, solucion_codigo | None, explicacion | texto_modelo, entradas)

ACTIVIDADES.append((
    "Actividad 1 — Concepto de algoritmo",
    "Escriba con sus propias palabras el concepto que tiene de algoritmo.\n\n"
    "**Algoritmos cotidianos:** escriba con detalles algún algoritmo que usted haya desarrollado continuamente "
    "durante sus actividades diarias.\n\n1-\n2-\n3-",
    f"**Dónde se ve:** {unidad(2)} (definición de algoritmo, diagrama de flujo y pseudocódigo).\n\n"
    "**Pista:** un algoritmo es una secuencia **finita**, **ordenada** y **sin ambigüedad** de pasos que resuelve "
    "un problema. Para el ejemplo cotidiano, elige algo que hagas siempre igual y escribe cada paso numerado, "
    "incluyendo alguna decisión (si pasa X, hago Y) y alguna repetición. La plataforma lo califica: redáctalo "
    "con tus palabras; la respuesta modelo es solo una referencia.",
    "# Escribe tu respuesta aquí (puede ir como comentarios).\n",
    None,
    "**Concepto de algoritmo (con mis palabras).** Para mí, un algoritmo es la receta que sigo para resolver un "
    "problema: una lista de pasos claros, en un orden fijo, que siempre termina y que, si cualquier persona (o una "
    "computadora) la sigue al pie de la letra, llega al mismo resultado. Tiene un punto de inicio (los datos o "
    "materiales que necesito), una serie de pasos donde a veces hay que decidir algo o repetir una acción, y un "
    "final con el resultado. Lo importante es que no puede haber pasos ambiguos: cada instrucción tiene que "
    "entenderse de una sola manera. Programar es escribir esos pasos en un lenguaje que la computadora entienda.\n\n"
    "**Lección aprendida:** en un primer intento esta pregunta sacó 6/10 porque la respuesta no incluyó la "
    "definición general con palabras propias. Escribe siempre las dos partes, cada una con su título.\n\n"
    "**Algoritmo cotidiano: preparar café por la mañana.**\n\n"
    "1. Llenar la cafetera con agua hasta la marca de dos tazas.\n"
    "2. Colocar el filtro y agregar dos cucharadas de café molido.\n"
    "3. Encender la cafetera y esperar hasta que termine de pasar el agua (repetición: revisar cada minuto).\n"
    "4. Servir el café en la taza.\n"
    "5. Si quiero el café dulce, agregar una cucharada de azúcar; si no, dejarlo como está (decisión).\n"
    "6. Apagar la cafetera.",
    None,
))

ACTIVIDADES.append((
    "Actividad 2 — Programación secuencial",
    "A continuación nombre las 3 estructuras básicas de programación.\n\n1-\n2-\n3-",
    f"**Dónde se ve:** {unidad(1)} (las 3 estructuras de la programación) y {unidad(6)} (estructuras de control).",
    "# Escribe tu respuesta aquí.\n",
    None,
    "1. **Secuencial (secuencia):** las instrucciones se ejecutan una tras otra, en el orden en que están escritas.\n"
    "2. **Selección (condicional):** el programa elige un camino según una condición (`if`, `elif`, `else`).\n"
    "3. **Repetición (iteración o bucle):** un bloque se repite mientras se cumpla una condición o para cada "
    "elemento de una secuencia (`for`, `while`).",
    None,
))

ACTIVIDADES.append((
    "Tipos de datos numéricos y operaciones matemáticas",
    "Ejecuta el código de la siguiente celda y verifica el tipo de dato retornado en cada una de las asignaciones. "
    "Para ello usa el comando `type(variable)` en combinación con el comando `print()`.",
    f"**Dónde se ve:** {unidad(3)} (cómo distinguir los tipos de datos con `type`).",
    "texto = 'Hola! bienvenido al mundo de la programación'\n"
    "# Escribe acá el código necesario para verificar el tipo de variable.\n\n\n"
    "entero = 4\n# Escribe acá el código necesario para verificar el tipo de variable.\n\n\n"
    "valor_flotante = 3.4\n# Escribe acá el código necesario para verificar el tipo de variable.\n\n\n"
    "ejemplo_de_lista = [1,2,3,4,4]\n# Escribe acá el código necesario para verificar el tipo de variable.\n\n\n"
    "ejemplo_de_diccionario = {'name':'Jhon Doe','edge':64}\n"
    "# Escribe acá el código necesario para verificar el tipo de variable.\n",
    """
texto = 'Hola! bienvenido al mundo de la programación'
print(type(texto))                   # <class 'str'>: cadena de texto

entero = 4
print(type(entero))                  # <class 'int'>: número entero

valor_flotante = 3.4
print(type(valor_flotante))          # <class 'float'>: número con decimales

ejemplo_de_lista = [1, 2, 3, 4, 4]
print(type(ejemplo_de_lista))        # <class 'list'>: lista (admite repetidos)

ejemplo_de_diccionario = {'name': 'Jhon Doe', 'edge': 64}
print(type(ejemplo_de_diccionario))  # <class 'dict'>: diccionario clave-valor
""",
    "`type()` devuelve la clase del objeto y `print()` la muestra. En Jupyter, si escribes solo `type(x)` en la "
    "última línea se ve `int`; con `print` se ve `<class 'int'>`.",
    None,
))

ACTIVIDADES.append((
    "Actividad 3 — Operaciones matemáticas en Python",
    "1. Crea una variable `numero1` y asígnale un número entero.\n"
    "2. Crea una variable `numero2` y asígnale otro número entero.\n"
    "3. Suma los valores de `numero1` y `numero2`, y almacena el resultado en una variable llamada `suma`.\n"
    "4. Resta `numero2` de `numero1` y almacena el resultado en `resta`.\n"
    "5. Multiplica `numero1` y `numero2`, y almacena el resultado en `multiplicacion`.\n"
    "6. Divide `numero1` entre `numero2` y almacena el resultado en `division`.\n\n"
    "Completa el código y luego imprime los valores de `suma`, `resta`, `multiplicacion` y `division`.",
    f"**Dónde se ve:** {unidad(3, 4)} (operadores aritméticos y variables).\n\n"
    "**Error común:** si `numero2` es 0, la división lanza `ZeroDivisionError`. `/` siempre devuelve `float`.",
    "# Desarrolla el código en la siguiente celda.\n",
    """
numero1 = 17                        # primer entero
numero2 = 5                         # segundo entero (distinto de 0 para poder dividir)

suma = numero1 + numero2            # 22
resta = numero1 - numero2           # 12
multiplicacion = numero1 * numero2  # 85
division = numero1 / numero2        # 3.4 (la división con / siempre devuelve float)

print("Suma:", suma)
print("Resta:", resta)
print("Multiplicación:", multiplicacion)
print("División:", division)
""",
    "Cada resultado se guarda en su variable antes de imprimirse, como pide el enunciado.",
    None,
))

ACTIVIDADES.append((
    "Operadores lógicos (práctica libre)",
    "| Operador | Descripción |\n|---|---|\n"
    "| `and` | Devuelve `True` si ambos operandos son `True`. |\n"
    "| `or` | Devuelve `True` si al menos uno de los operandos es `True`. |\n"
    "| `not` | Invierte el valor del operando; `True` se convierte en `False` y viceversa. |\n\n"
    "La plataforma deja un recuadro con la indicación «Desarrolla en la siguiente celda», sin consigna adicional: "
    "se espera que pruebes los tres operadores.",
    f"**Dónde se ve:** {unidad(5)} (operadores lógicos y tabla de verdad).",
    "# Desarrolla en la siguiente celda.\n",
    """
a = True
b = False

# and: verdadero solo si ambos lo son
print("True and False =", a and b)   # False
# or: verdadero si al menos uno lo es
print("True or False =", a or b)     # True
# not: invierte el valor
print("not True =", not a)           # False

# Uso práctico combinado con comparaciones
edad = 20
tiene_entrada = True
puede_entrar = edad >= 18 and tiene_entrada
print("¿Puede entrar?", puede_entrar)  # True

# Tabla de verdad completa de and y or
for x in (True, False):
    for y in (True, False):
        print(x, y, "-> and:", x and y, "| or:", x or y)
""",
    "La tabla de verdad recorre las cuatro combinaciones posibles; con ella se comprueban las definiciones.",
    None,
))

ACTIVIDADES.append((
    "Actividad 4 — Uso de operadores",
    "| Comparador | Descripción |\n|---|---|\n"
    "| `==` | Igual a |\n| `!=` | Diferente de |\n| `<` | Menor que |\n| `>` | Mayor que |\n"
    "| `<=` | Menor o igual que |\n| `>=` | Mayor o igual que |\n\n"
    "1. Generar un loop que revise cada uno de los elementos contenidos en la lista llamada `lista_de_elementos`.\n"
    "2. Revisar el tipo de elemento.\n"
    "3. Comparar si el valor está por debajo del umbral definido; en ese caso imprimir la palabra «aprobado», "
    "en caso contrario imprimir «Rechazado».\n"
    "4. Incluir dos contadores para contabilizar el número de aprobados y rechazados, y al final imprimir el total de cada uno.\n"
    "5. Contabilizar los elementos que son tipo string e imprimir el resultado al final del loop.",
    f"**Dónde se ve:** {unidad(5, 6, 7, 8)}.\n\n"
    "**Clave:** comparar un `str` con un número (`'7' < -10`) lanza `TypeError`. Por eso primero se revisa el "
    "tipo: los strings se cuentan y no se comparan.\n\n"
    "**Para decidir:** el enunciado no dice qué hacer con strings numéricos como `'7'` o `'2023'`. La solución "
    "los trata como texto (lo que son). Si tu docente esperaba convertirlos, se usa `float(elemento)` dentro de "
    "un `try/except`; explica tu decisión en un comentario.",
    "umbral = - 10\n"
    'lista_de_elementos = elementos = [10, 3.14, "7", -5, "2.718", 42, "Python", -8.9, "Hola", 100.5, "Mundo", '
    '-15, "GPT-3", 5.5, "AI", -20, "2023", 123, "OpenAI", -2.5, "Ejemplo"]\n\n'
    "# Desarrollo loop del código principal.\n"
    "# En este espacio debes escribir el código siguiendo las instrucción de la celda anterior.\n\n\n\n\n\n"
    'print("Total aprobados: ", aprobados)\n'
    'print("Total rechazados: , ", rechazados)\n'
    'print("Total de strings: ", conteo_strings)\n',
    """
umbral = - 10
lista_de_elementos = elementos = [10, 3.14, "7", -5, "2.718", 42, "Python", -8.9, "Hola", 100.5, "Mundo", -15, "GPT-3", 5.5, "AI", -20, "2023", 123, "OpenAI", -2.5, "Ejemplo"]

# Contadores
aprobados = 0
rechazados = 0
conteo_strings = 0

for elemento in lista_de_elementos:
    tipo = type(elemento)                      # paso 2: revisar el tipo
    print(f"{elemento!r} es de tipo {tipo.__name__}", end=" -> ")

    if tipo == str:
        # Un texto no se puede comparar con un número: se cuenta y se pasa al siguiente.
        conteo_strings += 1
        print("string (no se compara)")
        continue

    if elemento < umbral:                      # paso 3: comparar con el umbral
        print("aprobado")
        aprobados += 1
    else:
        print("Rechazado")
        rechazados += 1

print("Total aprobados: ", aprobados)
print("Total rechazados: , ", rechazados)
print("Total de strings: ", conteo_strings)
""",
    "Resultado esperado: 2 aprobados (-15 y -20 son los únicos menores que -10), 9 rechazados y 10 strings "
    "(21 elementos en total). `continue` salta al siguiente elemento sin ejecutar la comparación.\n\n"
    "**Nota sobre el enunciado:** el último `print` trae `\"Total rechazados: , \"` con una coma de más dentro "
    "del texto. Es parte del código dado; se puede dejar o corregir.",
    None,
))

ACTIVIDADES.append((
    "Actividad 5 — Creación de una base de datos en Python",
    "Crea un programa que permita a los usuarios:\n\n"
    "a. Agregar un nuevo estudiante (al menos nombre, número de identificación y edad).\n"
    "b. Mostrar la lista de estudiantes.\n"
    "c. Buscar un estudiante por su número de identificación y mostrar su información.\n"
    "d. Actualizar la información de un estudiante existente.\n"
    "e. Eliminar un estudiante.\n\n"
    "Usa listas de Python (por ejemplo, una lista de diccionarios), ofrece un menú interactivo e implementa la "
    "lógica de cada acción. Ejemplo:\n\n"
    "```python\nbase_de_datos = [\n    {\"nombre\": \"Juan\", \"id\": 1, \"edad\": 20},\n"
    "    {\"nombre\": \"María\", \"id\": 2, \"edad\": 22},\n    {\"nombre\": \"Carlos\", \"id\": 3, \"edad\": 21}\n]\n```\n\n"
    "Recuerda agregar comentarios que describan el funcionamiento de las diferentes secciones.",
    f"**Dónde se ve:** {unidad(9, 10, 11, 14)} (bucle `while` con menú, listas, diccionarios y CRUD).\n\n"
    "**Estructura recomendada:** una función por acción, un `while True` con el menú, y `break` al elegir salir. "
    "Valida que el id sea un número (`int(input(...))` dentro de `try/except`) y que no se repita.",
    "#Recuerde agregar comentarios donde se describa el funcionamiento de las diferentes secciones.\n",
    """
# ---------------------------------------------------------------
# Base de datos de estudiantes en memoria: lista de diccionarios.
# Cada estudiante: {"nombre": str, "id": int, "edad": int}
# ---------------------------------------------------------------
base_de_datos = [
    {"nombre": "Juan", "id": 1, "edad": 20},
    {"nombre": "María", "id": 2, "edad": 22},
    {"nombre": "Carlos", "id": 3, "edad": 21},
]


def pedir_entero(mensaje):
    \"\"\"Pide un número entero y repite la pregunta hasta que el dato sea válido.\"\"\"
    while True:
        try:
            return int(input(mensaje))
        except ValueError:
            print("Debe ingresar un número entero.")


def buscar_por_id(id_buscado):
    \"\"\"Devuelve el diccionario del estudiante con ese id, o None si no existe.\"\"\"
    for estudiante in base_de_datos:
        if estudiante["id"] == id_buscado:
            return estudiante
    return None


# a. Agregar
def agregar_estudiante():
    id_nuevo = pedir_entero("Número de identificación: ")
    if buscar_por_id(id_nuevo) is not None:
        print("Ya existe un estudiante con ese id.")
        return
    nombre = input("Nombre: ").strip()
    edad = pedir_entero("Edad: ")
    base_de_datos.append({"nombre": nombre, "id": id_nuevo, "edad": edad})
    print(f"Estudiante {nombre} agregado.")


# b. Mostrar
def mostrar_estudiantes():
    if not base_de_datos:
        print("La base de datos está vacía.")
        return
    print(f"{'ID':<5}{'Nombre':<15}{'Edad':>4}")
    for estudiante in base_de_datos:
        print(f"{estudiante['id']:<5}{estudiante['nombre']:<15}{estudiante['edad']:>4}")


# c. Buscar
def buscar_estudiante():
    estudiante = buscar_por_id(pedir_entero("Id a buscar: "))
    if estudiante is None:
        print("No se encontró el estudiante.")
    else:
        print(f"Nombre: {estudiante['nombre']} | Id: {estudiante['id']} | Edad: {estudiante['edad']}")


# d. Actualizar (Enter deja el valor actual)
def actualizar_estudiante():
    estudiante = buscar_por_id(pedir_entero("Id a actualizar: "))
    if estudiante is None:
        print("No se encontró el estudiante.")
        return
    nombre = input(f"Nuevo nombre [{estudiante['nombre']}]: ").strip()
    edad = input(f"Nueva edad [{estudiante['edad']}]: ").strip()
    if nombre:
        estudiante["nombre"] = nombre
    if edad.isdigit():
        estudiante["edad"] = int(edad)
    print("Estudiante actualizado.")


# e. Eliminar
def eliminar_estudiante():
    estudiante = buscar_por_id(pedir_entero("Id a eliminar: "))
    if estudiante is None:
        print("No se encontró el estudiante.")
    else:
        base_de_datos.remove(estudiante)
        print(f"Estudiante {estudiante['nombre']} eliminado.")


# Menú interactivo: se repite hasta elegir 6
def menu():
    acciones = {
        "1": agregar_estudiante,
        "2": mostrar_estudiantes,
        "3": buscar_estudiante,
        "4": actualizar_estudiante,
        "5": eliminar_estudiante,
    }
    while True:
        print("\\n--- Base de datos de estudiantes ---")
        print("1. Agregar  2. Mostrar  3. Buscar  4. Actualizar  5. Eliminar  6. Salir")
        opcion = input("Elija una opción: ").strip()
        if opcion == "6":
            print("Fin del programa.")
            break
        accion = acciones.get(opcion)
        if accion is None:
            print("Opción no válida.")
        else:
            accion()


menu()
""",
    "El diccionario `acciones` asocia cada opción con su función, así se evita una cadena larga de `elif`. "
    "`buscar_por_id` se reutiliza en buscar, actualizar y eliminar. Prueba de ejemplo: `1` (agregar id 4, Ana, 19), "
    "`2`, `4` (cambiar edad de 2), `5` (eliminar 1), `2`, `6`.",
    ["1", "4", "Ana", "19", "2", "3", "2", "4", "2", "", "23", "5", "1", "2", "9", "6"],
))

ACTIVIDADES.append((
    "Actividad 6 — Rebanado de listas",
    "Revisa la unidad 10, sección 5.3 (resumen de los comandos para tomar secciones de una lista) y aplica los "
    "comandos en la siguiente lista:\n\n`list_notas = [15, 21, 24, 40, 13, 14, 18, 17, 14.5]`",
    f"**Dónde se ve:** {unidad(10)} (sección de rebanado; en el PDF, Unidad 10, sección 5.3).\n\n"
    "**Clave:** `lista[inicio:fin:paso]`; `fin` no se incluye; los índices negativos cuentan desde el final.",
    "# Espacio para desarrollar las pruebas, si tienes alguna duda o comentario adicional\n"
    "# lo puedes dejar planteado acá.\n\nlist_notas = [15, 21, 24, 40, 13, 14, 18, 17, 14.5]\nlist_notas[::2]\n",
    """
list_notas = [15, 21, 24, 40, 13, 14, 18, 17, 14.5]

print(list_notas[:])      # copia completa
print(list_notas[2:5])    # índices 2, 3 y 4: [24, 40, 13]
print(list_notas[:3])     # desde el inicio hasta el índice 2: [15, 21, 24]
print(list_notas[4:])     # desde el índice 4 hasta el final: [13, 14, 18, 17, 14.5]
print(list_notas[-3:])    # los tres últimos: [18, 17, 14.5]
print(list_notas[:-2])    # todos menos los dos últimos
print(list_notas[::2])    # uno sí, uno no (índices pares): [15, 24, 13, 18, 14.5]
print(list_notas[1::2])   # índices impares: [21, 40, 14, 17]
print(list_notas[::-1])   # lista invertida
print(list_notas[-1])     # último elemento (indexación, no rebanado): 14.5
""",
    "El rebanado siempre devuelve una lista nueva; la original no cambia.",
    None,
))

ACTIVIDADES.append((
    "Actividad 7 — Diferentes métodos usados en listas",
    "De la unidad 10, sección 6.3, revisa los métodos disponibles para usar sobre las listas y aplícalos sobre la "
    "lista de la siguiente celda.\n\n**Nota:** usando el método `sort()` ordena de mayor a menor y viceversa.",
    f"**Dónde se ve:** {unidad(10)} (agregar, borrar, ordenar y otros métodos; en el PDF, sección 6.3).\n\n"
    "**Clave:** `sort()` ordena la lista en el lugar y devuelve `None`; de mayor a menor con `sort(reverse=True)`. "
    "**Error común:** `lista = lista.sort()` deja la variable en `None`.",
    "# Aplique los métodos disponibles y agregue comentarios breves sobre su funcinamiento.\n\n"
    "list_notas = [15, 21, 24, 40, 13, 14, 18, 13, 17, 14.5]\n\n\n# Espacio para desarrollo del código y comentarios.\n",
    """
list_notas = [15, 21, 24, 40, 13, 14, 18, 13, 17, 14.5]

list_notas.append(20)          # agrega 20 al final
print("append:", list_notas)

list_notas.extend([11, 19])    # agrega cada elemento de otra lista
print("extend:", list_notas)

list_notas.insert(0, 10)       # inserta 10 en la posición 0
print("insert:", list_notas)

list_notas.remove(13)          # borra la primera aparición de 13
print("remove:", list_notas)

ultimo = list_notas.pop()      # quita y devuelve el último elemento
print("pop:", ultimo, list_notas)

print("index de 40:", list_notas.index(40))   # posición de la primera aparición
print("count de 13:", list_notas.count(13))   # cuántas veces aparece

list_notas.sort()              # ordena de menor a mayor (en el lugar)
print("sort ascendente:", list_notas)

list_notas.sort(reverse=True)  # ordena de mayor a menor
print("sort descendente:", list_notas)

list_notas.reverse()           # invierte el orden actual
print("reverse:", list_notas)

copia = list_notas.copy()      # copia independiente
copia.clear()                  # vacía la copia; la original no cambia
print("clear en la copia:", copia, "| original:", len(list_notas), "elementos")
""",
    "`sort()` funciona aquí porque todos los elementos son números (`int` y `float` se pueden comparar). Si la "
    "lista mezclara números y textos, lanzaría `TypeError`.",
    None,
))

ACTIVIDADES.append((
    "Actividad 8 — Crear diccionarios y guardarlos como archivo JSON",
    "De la unidad 11, sección 4.6, revisa el ejemplo mostrado. Genera un diccionario con la información que "
    "desees guardar como base de datos, desarrolla el código necesario para generar el archivo JSON y también el "
    "código para cargar la información del archivo JSON.",
    f"**Dónde se ve:** {unidad(11)} (sección de JSON; en el PDF, Unidad 11, sección 4.6).\n\n"
    "**Clave:** `json.dump(objeto, archivo)` escribe y `json.load(archivo)` lee. Abre con `'w'` para escribir y "
    "`'r'` para leer. `ensure_ascii=False` conserva las tildes y `indent=2` deja el archivo legible.",
    "# Espacio para desarrollar el código.\n",
    """
import json

# Diccionario con la información a guardar
biblioteca = {
    "nombre": "Biblioteca personal",
    "libros": [
        {"titulo": "Cien años de soledad", "autor": "Gabriel García Márquez", "anio": 1967},
        {"titulo": "Rayuela", "autor": "Julio Cortázar", "anio": 1963},
    ],
    "total": 2,
}

# Guardar el diccionario en un archivo JSON
with open("biblioteca.json", "w", encoding="utf-8") as archivo:
    json.dump(biblioteca, archivo, ensure_ascii=False, indent=2)
print("Archivo biblioteca.json creado.")

# Cargar la información desde el archivo JSON
with open("biblioteca.json", "r", encoding="utf-8") as archivo:
    datos = json.load(archivo)

print(type(datos))              # <class 'dict'>: vuelve como diccionario
for libro in datos["libros"]:
    print(f"{libro['titulo']} - {libro['autor']} ({libro['anio']})")
""",
    "`with` cierra el archivo solo al salir del bloque. Lo que se carga es otra vez un diccionario de Python, "
    "así que se recorre igual que el original.",
    None,
))

ACTIVIDADES.append((
    "Actividad 9 — Creación y manejo de tuplas",
    "1. Escriba una diferencia entre las tuplas y las listas.\n"
    "2. Crear una tupla con varios elementos.\n"
    "3. Usar el operador `in` para verificar si la tupla contiene determinado elemento.",
    f"**Dónde se ve:** {unidad(10, 12)} (tuplas, inmutabilidad y operador `in`).",
    "# Espacio para desarrollar el código siguiendo las instrucciones.\n\ntup = (1, 2, 3, 4, 5)\n",
    """
# 1. Diferencia: la lista es mutable (se puede modificar después de creada) y la tupla
#    es inmutable (una vez creada, sus elementos no se pueden cambiar, agregar ni borrar).

# 2. Crear una tupla
tup = (1, 2, 3, 4, 5)
colores = ("rojo", "verde", "azul")
print(tup, colores)

# 3. Verificar pertenencia con in / not in
print(3 in tup)               # True
print(10 in tup)              # False
print("verde" in colores)     # True
print("negro" not in colores) # True

# Demostración de la inmutabilidad
try:
    tup[0] = 100
except TypeError as error:
    print("No se puede modificar una tupla:", error)
""",
    "El `try/except` muestra el `TypeError` sin detener el programa; es la evidencia práctica de la diferencia.",
    None,
))

ACTIVIDADES.append((
    "Actividad 10 — Revisión y manejo de listas bidimensionales",
    "1. Describa brevemente qué entiende por lista bidimensional.\n"
    "2. Crear una lista bidimensional.\n"
    "3. Generar un doble loop para acceder a la lista bidimensional.\n"
    "4. Sumar todos los elementos de esta lista bidimensional.",
    f"**Dónde se ve:** {unidad(13)} (listas bidimensionales y doble bucle).",
    "# Espacio para desarrollar el código, escriba comentarias breves para explicar su funcionamiento.\n",
    """
# 1. Una lista bidimensional es una lista cuyos elementos son otras listas: se organiza
#    como una tabla de filas y columnas, y se accede con dos índices: matriz[fila][columna].

# 2. Crear la lista bidimensional (3 filas x 4 columnas)
matriz = [
    [1, 2, 3, 4],
    [5, 6, 7, 8],
    [9, 10, 11, 12],
]
print("Elemento fila 1, columna 2:", matriz[1][2])   # 7

# 3. y 4. Doble loop: el externo recorre filas y el interno los elementos de cada fila
suma_total = 0
for i in range(len(matriz)):
    for j in range(len(matriz[i])):
        print(f"matriz[{i}][{j}] = {matriz[i][j]}")
        suma_total += matriz[i][j]

print("Suma de todos los elementos:", suma_total)    # 78

# Comprobación con funciones integradas
print("Comprobación:", sum(sum(fila) for fila in matriz))
""",
    "Usar `range(len(...))` permite mostrar los índices; si solo importa el valor, también vale "
    "`for fila in matriz: for valor in fila:`.",
    None,
))

ACTIVIDADES.append((
    "Actividad Extra Point — Métodos de diccionarios",
    "1. Crear un diccionario.\n"
    "2. Testear los métodos `get()`, `keys()`, `values()`, `items()`, `pop()`, `clear()`.\n"
    "3. Agregar un breve comentario sobre su funcionamiento.\n\n"
    "Es opcional: solo suma (hasta 10 puntos) si la nota es menor que 60.",
    f"**Dónde se ve:** {unidad(11, 14)} (métodos de diccionario).",
    "# Espacio para desarrollar el código.\n",
    """
estudiante = {"nombre": "Ana", "edad": 21, "carrera": "Ingeniería"}

# get: devuelve el valor de la clave; si no existe, devuelve None o el valor por defecto (no lanza error)
print(estudiante.get("nombre"))           # Ana
print(estudiante.get("ciudad", "Sin dato"))  # Sin dato

# keys: vista con todas las claves
print(estudiante.keys())                  # dict_keys(['nombre', 'edad', 'carrera'])

# values: vista con todos los valores
print(estudiante.values())                # dict_values(['Ana', 21, 'Ingeniería'])

# items: vista con los pares (clave, valor); útil para recorrer
for clave, valor in estudiante.items():
    print(clave, "->", valor)

# pop: elimina la clave y devuelve su valor
edad = estudiante.pop("edad")
print("Se quitó la edad:", edad, "|", estudiante)

# clear: vacía el diccionario por completo
estudiante.clear()
print("Después de clear:", estudiante)    # {}
""",
    "Diferencia clave: `estudiante['ciudad']` lanzaría `KeyError`; `get` devuelve `None` o el valor por defecto.",
    None,
))


def probar(codigo, entradas):
    """Ejecuta una solución en una carpeta temporal, con entradas simuladas si las necesita."""
    previo = os.getcwd()
    original_input = builtins.input
    cola = list(entradas or [])

    def falso_input(msg=""):
        valor = cola.pop(0)
        print(msg + valor)
        return valor

    salida = io.StringIO()
    with tempfile.TemporaryDirectory() as tmp:
        os.chdir(tmp)
        builtins.input = falso_input
        try:
            with contextlib.redirect_stdout(salida):
                exec(compile(codigo, "<solucion>", "exec"), {"__name__": "__main__"})
        finally:
            builtins.input = original_input
            os.chdir(previo)
    return salida.getvalue()


# Actividad 5: versión adaptada al navegador de la plataforma (input() abre una ventana emergente)
_i = next(i for i, a in enumerate(ACTIVIDADES) if a[0].startswith("Actividad 5"))
_a = list(ACTIVIDADES[_i])
_a[4] = Path(__file__).with_name("actividad_s01_act5.py").read_text()
_a[5] = (
    "En la plataforma el código corre en el navegador: `input()` abre una ventana emergente y lo que se imprime "
    "con `print()` recién se ve cuando el programa termina. Por eso el menú y el resultado de cada acción van "
    "**dentro del texto de la ventana**, y **Cancelar** (o dejar vacío) termina el programa en lugar de "
    "repetir la pregunta para siempre. Al terminar se imprime la base de datos final.\n\n"
    "Cada acción devuelve un mensaje en lugar de imprimirlo; así el menú lo muestra en la siguiente ventana. "
    "`leer()` devuelve `None` si se cancela y `leer_entero()` vuelve a preguntar si el dato no es un número."
)
_a[6] = ["1", "4", "Ana", "19", "2", "3", "2", "4", "2", "", "23", "5", "1", "9", "6"]
ACTIVIDADES[_i] = tuple(_a)

celdas = [
    new_markdown_cell(
        "# Actividad asincrónica — Semana 1\n\n"
        "**Capítulos 1 y 2: programación básica e inicio con Python** (unidades 1 a 16)\n\n"
        "[Índice de la semana](semana-01.ipynb)\n\n"
        "## Estado\n\n"
        "**Entregada. Nota final: 100/100.**\n\n"
        "## Cómo se califica\n\n"
        "- 10 preguntas principales de 10 puntos cada una (100).\n"
        "- La pregunta adicional (Extra Point) es opcional: si la nota es menor que 60, suma hasta 10 puntos. "
        "La nota máxima es 100.\n"
        "- La plataforma califica pregunta por pregunta. Si se entregó por error, se puede retomar una vez; la nota "
        "de la nueva entrega es la que cuenta. Después, solo el docente puede dar otro intento.\n\n"
        "## Cómo se resuelve en la plataforma\n\n"
        "Cada pregunta se responde en su recuadro. Si es código, «Ejecutar» lo prueba (Tab mete la sangría). "
        "El borrador se guarda solo en ese navegador; al final se pulsa «Entregar». Hay 13 recuadros.\n\n"
        "## Cómo usar este notebook\n\n"
        "Cada actividad trae la consigna, una guía con link a la unidad donde se explica, la **respuesta resuelta** "
        "(ya ejecutada, con su salida) y una explicación. Para entregar, copia el código de la respuesta en el "
        "recuadro de la plataforma y pulsa «Ejecutar» para comprobarlo. En las actividades 1 y 2 la plataforma "
        "pide tus propias palabras: usa la respuesta como base y redáctala a tu manera.\n\n"
        "## Checklist de entrega\n\n"
        + "\n".join(f"- [x] {a[0]}" for a in ACTIVIDADES)
        + "\n- [x] Revisar todo y pulsar «Entregar»"
    )
]

numero = 0
for titulo, enunciado, guia, inicial, sol, explicacion, entradas in ACTIVIDADES:
    celdas.append(new_markdown_cell(f"## {titulo}\n\n### Consigna\n\n{enunciado}\n\n### Guía\n\n{guia}"))
    if sol is None:
        celdas.append(new_markdown_cell(
            "### Respuesta\n\n" + explicacion.strip()
            + "\n\n**Importante:** la plataforma pide tus propias palabras. Usa esta respuesta como base y redáctala a tu manera."
        ))
        continue
    salida = probar(sol, entradas)
    print(f"OK {titulo}: {len(salida.splitlines())} líneas de salida")
    celdas.append(new_markdown_cell("### Respuesta"))
    numero += 1
    celdas.append(new_code_cell(
        sol.strip(),
        execution_count=numero,
        outputs=[new_output("stream", name="stdout", text=salida)],
    ))
    nota = ""
    if entradas:
        nota = ("\n\nEs un programa interactivo: la salida de arriba es una prueba con estas respuestas escritas en "
                "orden: " + ", ".join(f"`{e}`" if e else "(Enter)" for e in entradas) + ". En la plataforma, al pulsar "
                "«Ejecutar» te pedirá los datos uno por uno.")
    celdas.append(new_markdown_cell("**Explicación:** " + explicacion.strip() + nota))

celdas.append(new_markdown_cell("[Índice de la semana](semana-01.ipynb)"))
nb = new_notebook()
nb.cells = celdas
nbformat.write(nb, DESTINO)
print("Escrito:", DESTINO)
