"""Genera 01-python/semana-03/actividad-asincronica.ipynb y prueba cada respuesta."""

import builtins
import contextlib
import io
import os
import tempfile
from pathlib import Path

import nbformat
from nbformat.v4 import new_code_cell, new_markdown_cell, new_notebook, new_output

RAIZ = Path(__file__).resolve().parents[2]
DESTINO = RAIZ / "01-python/semana-03/actividad-asincronica.ipynb"
C1 = "clase-1-pilas-colas-busqueda-secuencial"
C2 = "clase-2-busqueda-binaria-tablas-hash"
U = {
    22: f"{C1}/u22-pilas.ipynb",
    24: f"{C1}/u24-busqueda-secuencial.ipynb",
    25: f"{C2}/u25-busqueda-binaria.ipynb",
    26: f"{C2}/u26-tablas-hash.ipynb",
}
ESTADO = "**Entregada. Nota final: 100/100.**"
MARCA = "x"


def unidad(*nums):
    return ", ".join(f"[Unidad {n}]({U[n]})" for n in nums)


# (titulo, consigna, guia, [(etiqueta, codigo, entradas)], explicacion)
ACTIVIDADES = [
    ("Actividad 1 — Implementación de una pila en Python",
     "Una pila sigue el principio LIFO: el último elemento que se agrega es el primero en ser eliminado.\n\n"
     "- `stack = []`: una pila es básicamente una lista.\n"
     "- `append`: agrega un elemento a la lista.\n"
     "- `pop`: elimina un elemento; si no se especifica el índice, elimina el último y lo devuelve.\n\n"
     "Revise los nombres de la lista `nombres_aleatorios` y guárdelos en diferentes listas según la inicial del "
     "nombre, usando esos comandos y recorriendo con `for nombre in nombres_aleatorios:`. Al final del proceso la "
     "lista inicial debe quedar vacía.",
     f"**Dónde se ve:** {unidad(22)} (pila con lista: `append` y `pop`).\n\n"
     "**Error común:** hacer `pop` sobre la misma lista que se está recorriendo con `for`. Al borrar mientras se "
     "recorre, Python se salta elementos y la lista no queda vacía. Por eso se recorre una **copia** "
     "(`nombres_aleatorios[::-1]`) y se hace `pop` sobre la original.",
     [("Respuesta", '''nombres_aleatorios = ["Ana", "Carlos", "David", "Elena", "Fernando", "Gabriela",
                      "Hugo", "Isabel", "Juan", "Luis", "Lucía",
                      "Lorena", "Manuel", "María", "Miguel", "Natalia",
                      "Nicolás", "Nora", "Óscar", "Olivia", "Pablo", "Paula",
                      "Pedro", "Raquel", "Rafael", "Renata", "Roberto", "Rosario",
                      "Sara", "Sergio", "Silvia", "Tomás", "Teresa", "Víctor", "Verónica",
                      "Ximena", "Xavier", "Yolanda", "Yenny", "Zaira", "Zoe", "Zacarías"]

import unicodedata

por_inicial = {}   # una lista (pila) por cada inicial: {"A": [...], "C": [...], ...}

# Se recorre una copia invertida: así cada pop() de la original saca justo el nombre que toca.
for nombre in nombres_aleatorios[::-1]:
    sacado = nombres_aleatorios.pop()                 # pop sin índice: saca el último (LIFO)
    # Inicial sin tilde, para que "Óscar" quede junto a "Olivia"
    inicial = unicodedata.normalize("NFD", sacado[0])[0].upper()
    if inicial not in por_inicial:
        por_inicial[inicial] = []                     # nueva pila para esa inicial
    por_inicial[inicial].append(sacado)               # append: apilar

for inicial in sorted(por_inicial):
    print(inicial, por_inicial[inicial])

print("Lista inicial al terminar:", nombres_aleatorios)   # []''', None)],
     "Cada nombre sale de la lista original con `pop()` y entra con `append()` en la pila de su inicial. Como los "
     "nombres salen desde el final, dentro de cada inicial quedan en orden inverso (efecto LIFO). Al terminar, "
     "`nombres_aleatorios` queda vacía, como pide la consigna."),

    ("Actividad 2 — Clase pila (presentación 36) y su uso (presentación 40)",
     "Replique el código de la presentación 36 del capítulo 4, que crea una clase para una pila:\n\n"
     "- `__init__`: creación de la pila.\n- `is_empty`: verifica si la pila está vacía.\n"
     "- `push`: agrega un elemento.\n- `pop`: si la pila no está vacía, elimina el último elemento.\n\n"
     "Use la notación de la presentación 40, realice varias operaciones y comente brevemente los resultados "
     "(máximo 3 líneas).",
     f"**Dónde se ve:** {unidad(22)} (pila como clase: PDF parte 1, págs. 36–40).",
     [("Respuesta", '''# Clase pila (presentación 36)
class Stack:

    def __init__(self):
        self.stack = []

    def is_empty(self):
        return True if len(self.stack) == 0 else False

    def push(self, item):
        self.stack.append(item)

    def pop(self):
        return None if self.is_empty() else self.stack.pop()


# Uso con la notación de la presentación 40: objeto.método()
stack = Stack()
print(stack.is_empty())          # True: recién creada
stack.push(1)
stack.push(2)
stack.push(3)
print(stack.stack)               # [1, 2, 3]
print(stack.pop())               # 3
print(stack.pop())               # 2
print(stack.pop())               # 1
print(stack.pop())               # None: ya estaba vacía
print(stack.is_empty())          # True

# Comentario: los elementos salen en orden inverso al que entraron (3, 2, 1), eso es LIFO.
# pop() sobre una pila vacía devuelve None en lugar de lanzar un error, gracias a is_empty().
# La notación stack.push(x) llama al método del objeto creado con Stack().''', None)],
     "Se replica la clase tal como está en el curso y se prueba con varias operaciones, incluida una extracción "
     "con la pila vacía, que es el caso que `is_empty()` protege."),

    ("Actividad 3 — Búsqueda secuencial",
     "Se tiene una lista de 10 ciudades organizadas en función de la densidad de población. Escriba una función "
     "que retorne la posición ocupada.",
     f"**Dónde se ve:** {unidad(24)} (búsqueda secuencial).\n\n"
     "**Para decidir:** la lista es un ranking, así que la \"posición ocupada\" se devuelve empezando en 1 "
     "(Seúl ocupa el puesto 5; su índice en la lista es 4). Si tu docente esperaba el índice, basta con "
     "devolver `i` en lugar de `i + 1`; está indicado en un comentario.",
     [("Respuesta", '''ciudades = [
    "Daca, Bangladés",
    "Karachi, Pakistán",
    "Nueva Delhi, India",
    "Manila, Filipinas",
    "Seúl, Corea del Sur",
    "Cantón, China",
    "Taipéi, Taiwán",
    "Chenaral, Chile",
    "Shenzhen, China",
    "Bombay, India"
]

def obtener_posicion(ciudades, ciudad):
    """Búsqueda secuencial: recorre la lista en orden hasta encontrar la ciudad."""
    posicion = -1                        # -1 si la ciudad no está en la lista
    for i in range(len(ciudades)):
        if ciudades[i] == ciudad:
            posicion = i + 1             # puesto en el ranking (1 = el primero); el índice es i
            break                        # ya se encontró: no hace falta seguir
    return posicion

posicion_ocupada = obtener_posicion(ciudades, "Seúl, Corea del Sur")
print(posicion_ocupada)                                  # 5
print(obtener_posicion(ciudades, "Lima, Perú"))          # -1: no está''', None)],
     "Se compara cada ciudad con la buscada, de la primera a la última; al encontrarla se corta con `break`. "
     "**Nota sobre el enunciado:** el código dado tiene `def obtener_posicion(ciudades, ciudad)` sin los dos "
     "puntos finales; así daría `SyntaxError`. Se agregan `:`."),

    ("Actividad 4 — Búsqueda binaria",
     "1. Escriba al menos una ventaja de la búsqueda binaria.\n"
     "2. Replique el código de la presentación 192.\n"
     "3. Explique brevemente el funcionamiento del código (máximo 3 líneas).\n"
     "4. Ingrese un piso de ruptura del huevo y calcule cuántas veces se realiza la revisión para encontrar el "
     "piso seguro (puede agregar un contador).",
     f"**Dónde se ve:** {unidad(25)} (la presentación 192 es la pág. 18 del PDF parte 2: "
     "`find_highest_safe_floor2`, caída de huevos con búsqueda binaria).\n\n"
     "**En la plataforma:** al ejecutar se abre una ventana para el piso de ruptura; si se cancela o se escribe "
     "algo que no es un número, usa el piso 37.",
     [("Respuesta", '''# Ventaja de la búsqueda binaria: en cada paso descarta la mitad de los pisos, así que necesita
# O(log n) revisiones; con 100 pisos bastan unas 7, mientras la secuencial puede necesitar 100.

# Código de la presentación 192 (caída de huevos con búsqueda binaria)
def do_experiment(floor, breaking):
    return floor >= breaking                  # True si el huevo se rompe desde ese piso

def find_highest_safe_floor2(height, breaking):
    low, high = 1, height
    while low < high:
        mid = (low + high) // 2
        if do_experiment(mid, breaking):
            high = mid
        else:
            low = mid + 1
    return low - 1

# Funcionamiento: se prueba el piso del medio del rango [low, high]; si el huevo se rompe, la
# ruptura está en mid o más abajo (high = mid), y si no, más arriba (low = mid + 1). Cuando
# low y high se juntan, low es el primer piso de ruptura y el piso seguro es low - 1.

# Misma búsqueda con un contador de revisiones
def find_highest_safe_floor2_contando(height, breaking):
    low, high = 1, height
    revisiones = 0
    while low < high:
        mid = (low + high) // 2
        revisiones += 1                       # cada llamada a do_experiment es una revisión
        if do_experiment(mid, breaking):
            high = mid
        else:
            low = mid + 1
    return low - 1, revisiones

texto = input("Ingrese el piso de ruptura del huevo (edificio de 100 pisos): ")
piso_ruptura = int(texto) if texto and texto.strip().isdigit() else 37
piso_seguro, revisiones = find_highest_safe_floor2_contando(100, piso_ruptura)
print(f"Piso de ruptura: {piso_ruptura}")
print(f"El huevo estará a salvo hasta el piso número {piso_seguro}")
print(f"Revisiones realizadas: {revisiones}")
print("Comprobación con la función original:", find_highest_safe_floor2(100, piso_ruptura))''', ["37"])],
     "Con 100 pisos y ruptura en el piso 37, la búsqueda binaria encuentra el piso seguro (36) en **7 "
     "revisiones**; la secuencial habría necesitado 37. La función con contador da el mismo piso que la "
     "original, así que el conteo es correcto."),

    ("Actividad 5 — Tabla hash tipo diccionario",
     "La celda muestra cómo crear un diccionario, agregar elementos, eliminarlos y verificar si una clave existe. "
     "Basándose en ese código, agregue otros elementos y comente los resultados (máximo 3 líneas).",
     f"**Dónde se ve:** {unidad(26)} (tabla hash con diccionario).",
     [("Respuesta", '''# Crear un diccionario vacío
mi_diccionario = {}

# Agregar elementos al diccionario
mi_diccionario["nombre"] = "Juan"
mi_diccionario["edad"] = 30
mi_diccionario["ciudad"] = "Nueva York"

# Acceder a los valores por clave
print("Nombre:", mi_diccionario["nombre"])
print("Edad:", mi_diccionario["edad"])
print("Ciudad:", mi_diccionario["ciudad"])

# Modificar un valor existente
mi_diccionario["edad"] = 31

# Eliminar un elemento del diccionario
del mi_diccionario["ciudad"]

# Verificar si una clave existe en el diccionario
if "ciudad" in mi_diccionario:
    print("La clave 'ciudad' está en el diccionario.")
else:
    print("La clave 'ciudad' no está en el diccionario.")

# --- Elementos agregados ---
mi_diccionario["profesion"] = "Ingeniero"
mi_diccionario["idiomas"] = ["español", "inglés"]     # el valor puede ser una lista
mi_diccionario["pais"] = "Panamá"
print("Diccionario actual:", mi_diccionario)
print("Profesión:", mi_diccionario.get("profesion"))
print("Teléfono:", mi_diccionario.get("telefono", "no registrado"))   # get no falla si falta la clave
print("Cantidad de claves:", len(mi_diccionario))

# Comentario: cada clave se ubica con su hash, por eso agregar, buscar o borrar es casi inmediato.
# Asignar a una clave existente reemplaza el valor (edad pasó a 31); a una clave nueva, la crea.
# Acceder con [] a una clave que no existe da KeyError; get() devuelve None o un valor por defecto.''', None)],
     "Se conserva el código dado y se agregan tres claves nuevas, una de ellas con una lista como valor, además "
     "de `get()` con valor por defecto y `len()`."),
]


def ejecutar(bloques):
    """Ejecuta los bloques en orden en una carpeta temporal; devuelve la salida de cada uno."""
    previo = os.getcwd()
    original = builtins.input
    salidas = []
    entorno = {"__name__": "__main__"}
    with tempfile.TemporaryDirectory() as tmp:
        os.chdir(tmp)
        try:
            for codigo, entradas in bloques:
                cola = list(entradas or [])

                def falso_input(msg=""):
                    valor = cola.pop(0)
                    print(msg + valor)
                    return valor

                builtins.input = falso_input
                buffer = io.StringIO()
                with contextlib.redirect_stdout(buffer):
                    exec(compile(codigo, "<respuesta>", "exec"), entorno)
                salidas.append(buffer.getvalue())
        finally:
            builtins.input = original
            os.chdir(previo)
    return salidas


celdas = [new_markdown_cell(
    "# Actividad asincrónica — Semana 3\n\n"
    "**Capítulo 4: estructuras de datos** (unidades 22 a 26)\n\n"
    "[Índice de la semana](semana-03.ipynb)\n\n"
    f"## Estado\n\n{ESTADO}\n\n"
    "## Cómo se califica\n\n"
    "- 5 preguntas de 20 puntos cada una (100). No tiene pregunta adicional.\n"
    "- Se puede retomar una vez si se entregó por error; la nota de la nueva entrega es la que cuenta.\n\n"
    "## Cómo usar este notebook\n\n"
    "Cada actividad trae la consigna, la unidad donde se explica, la **respuesta resuelta** (ya ejecutada, con su "
    "salida) y una explicación. Para entregar, copia el código de la respuesta en el recuadro de la plataforma y "
    "pulsa «Ejecutar».\n\n"
    "## Checklist de entrega\n\n" + "\n".join(f"- [{MARCA}] {a[0]}" for a in ACTIVIDADES)
    + f"\n- [{MARCA}] Revisar todo y pulsar «Entregar»"
)]

numero = 0
for titulo, consigna, guia, bloques, explicacion in ACTIVIDADES:
    salidas = ejecutar([(codigo, entradas) for _, codigo, entradas in bloques])
    celdas.append(new_markdown_cell(f"## {titulo}\n\n### Consigna\n\n{consigna}\n\n### Guía\n\n{guia}"))
    for (etiqueta, codigo, _), salida in zip(bloques, salidas):
        print(f"--- {titulo}\n{salida.rstrip()[-700:]}")
        numero += 1
        celdas.append(new_markdown_cell(f"### {etiqueta}"))
        celdas.append(new_code_cell(codigo, execution_count=numero,
                                    outputs=[new_output("stream", name="stdout", text=salida)]))
    celdas.append(new_markdown_cell("**Explicación:** " + explicacion))

celdas.append(new_markdown_cell("[Índice de la semana](semana-03.ipynb)"))
nb = new_notebook()
nb.cells = celdas
nbformat.write(nb, DESTINO)
print("Escrito:", DESTINO)
