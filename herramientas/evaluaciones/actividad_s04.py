"""Genera 01-python/semana-04/actividad-asincronica.ipynb y prueba cada respuesta."""

import builtins
import contextlib
import io
import os
import random
import tempfile
from pathlib import Path

import nbformat
from nbformat.v4 import new_code_cell, new_markdown_cell, new_notebook, new_output

RAIZ = Path(__file__).resolve().parents[2]
DESTINO = RAIZ / "01-python/semana-04/actividad-asincronica.ipynb"
C1 = "clase-1-algoritmos-de-ordenamiento"
U = {
    27: f"{C1}/u27-burbuja-seleccion-insercion.ipynb",
    29: f"{C1}/u29-ordenamiento-rapido.ipynb",
}
ESTADO = "**Entregada. Nota final: 100/100.**"
MARCA = "x"


def unidad(*nums):
    return ", ".join(f"[Unidad {n}]({U[n]})" for n in nums)


# (titulo, consigna, guia, [(etiqueta, codigo, entradas)], explicacion)
ACTIVIDADES = [
    ("Actividad 1 — Ordenamiento de burbuja",
     "1. Explique brevemente y en forma clara cómo funciona el algoritmo de ordenamiento de burbuja.\n"
     "2. Desarrolle una función donde se use el ordenamiento de burbuja aplicada a una lista de valores enteros.\n\n"
     "En la plataforma esta actividad tiene **dos recuadros**: el primero para la explicación y la función, y el "
     "segundo con un código de ejemplo (`agregado()`) sobre listas.",
     f"**Dónde se ve:** {unidad(27)} (ordenamiento por burbuja, intercambio y complejidad).\n\n"
     "**Error común:** decir que los **menores** quedan al final. En el ordenamiento ascendente, en cada pasada el "
     "**mayor** \"sube como una burbuja\" hasta el final de la lista y los menores van quedando al principio.",
     [("Respuesta (recuadro 1)", '''# Cómo funciona el ordenamiento de burbuja:
# Recorre la lista comparando cada par de elementos vecinos y los intercambia si están en el
# orden incorrecto. Al terminar una pasada, el mayor de los que faltan queda al final (sube
# como una burbuja). Se repite con la parte que falta hasta que no hay más intercambios.
# Complejidad: O(N^2) comparaciones en el peor caso.

def burbuja(lista):
    """Ordena la lista de enteros de menor a mayor (en el lugar) y la devuelve."""
    n = len(lista)
    for pasada in range(n - 1):
        hubo_intercambio = False
        # Los últimos 'pasada' elementos ya están en su lugar: no se revisan
        for i in range(n - 1 - pasada):
            if lista[i] > lista[i + 1]:
                lista[i], lista[i + 1] = lista[i + 1], lista[i]   # intercambio de vecinos
                hubo_intercambio = True
        print(f"Pasada {pasada + 1}: {lista}")
        if not hubo_intercambio:      # si no hubo cambios, la lista ya está ordenada
            break
    return lista


numeros = [2, 3, 4, 5, 6, 7, 3, 5, 66, 75, 23]
print("Original:", numeros)
print("Ordenada:", burbuja(numeros))''', None),
      ("Respuesta (recuadro 2: código de ejemplo de la plataforma)", '''lista = [2, 4, 5, 6]

def agregado():
    lista.append(2)     # modifica la lista global: las listas son mutables
    return lista

print(agregado())       # [2, 4, 5, 6, 2]
print(lista)            # [2, 4, 5, 6, 2]: es el mismo objeto, también cambió

# Comentario: la función no crea una copia; append modifica la lista original, por eso los dos
# print muestran lo mismo. Igual pasa con burbuja(): ordena la lista que recibe, "en el lugar".''', None)],
     "La función hace pasadas comparando vecinos y corta antes si una pasada no intercambió nada. El segundo "
     "recuadro trae un código de la plataforma: se deja tal cual y se explica por qué la lista global cambia, "
     "que es lo mismo que permite a `burbuja()` ordenar la lista que recibe."),

    ("Actividad 2 — Función swap",
     "Escriba una función que permita el intercambio de elementos en una lista. Los argumentos de esta función "
     "serán la lista y los índices de los elementos que se desean intercambiar. Agregue comentarios breves.",
     f"**Dónde se ve:** {unidad(27)} (operación de intercambio en Python).\n\n"
     "**Clave:** la consigna pide que la **lista sea un argumento**; una función que usa una lista global solo "
     "sirve para esa lista.",
     [("Respuesta", '''def swap(lista, i, j):
    """Intercambia los elementos en las posiciones i y j de la lista (la modifica en el lugar)."""
    if not (-len(lista) <= i < len(lista) and -len(lista) <= j < len(lista)):
        raise IndexError("Índice fuera de rango")
    lista[i], lista[j] = lista[j], lista[i]     # asignación simultánea de Python
    return lista


def swap_con_auxiliar(lista, i, j):
    """Mismo intercambio usando una variable auxiliar, como en otros lenguajes."""
    aux = lista[i]          # guarda el primero para no perderlo
    lista[i] = lista[j]     # copia el segundo en la posición del primero
    lista[j] = aux          # pone el primero en la posición del segundo
    return lista


numeros = [2, 3, 4, 5, 6, 7, 7]
print(swap(numeros, 0, 5))              # [7, 3, 4, 5, 6, 2, 7]
print(swap_con_auxiliar(numeros, 1, 3)) # [7, 5, 4, 3, 6, 2, 7]
print(swap(["a", "b", "c"], 0, -1))     # funciona con cualquier lista: ['c', 'b', 'a']

try:
    swap(numeros, 0, 10)
except IndexError as error:
    print("Error controlado:", error)''', None)],
     "`swap` recibe la lista y los dos índices, como pide la consigna, y sirve para cualquier lista. Se muestran "
     "las dos formas de intercambiar (simultánea y con variable auxiliar) y la validación de índices."),

    ("Actividad 3 — Quick Sort",
     "1. Explique brevemente el funcionamiento del algoritmo Quick Sort.\n"
     "2. Desarrolle el código para implementar el algoritmo Quick Sort.\n\n"
     "Revise la unidad 29, sección 1.1.",
     f"**Dónde se ve:** {unidad(29)} (`quicksort1` y `partition1`, pivote en el primer elemento).\n\n"
     "**Nota sobre el PDF:** la `partition1` de las diapositivas usa `while left < right:` y con algunas listas "
     "deja mal ubicado el pivote (por ejemplo `[1, 2, 3]`). Se usa la versión corregida con `<=`, como en la "
     "unidad 29.",
     [("Respuesta", '''# Cómo funciona Quick Sort (divide y vencerás):
# 1. Se elige un pivote (aquí, el primer elemento del tramo).
# 2. Partición: se reordena el tramo para que los menores o iguales al pivote queden a su izquierda y
#    los mayores a su derecha; el pivote queda en su posición definitiva.
# 3. Se aplica lo mismo, recursivamente, al tramo de la izquierda y al de la derecha.
# Promedio O(N log N); peor caso O(N^2) si el pivote siempre es el menor o el mayor.

def quicksort1(S, low, high):
    """Ordena S[low..high] en el lugar."""
    if low < high:                               # tramo de 0 o 1 elemento: ya está ordenado
        pivotpoint = partition1(S, low, high)
        quicksort1(S, low, pivotpoint - 1)       # parte izquierda (menores)
        quicksort1(S, pivotpoint + 1, high)      # parte derecha (mayores)


def partition1(S, low, high):
    """Ubica el pivote S[low] en su lugar y devuelve su posición."""
    pivot = S[low]
    left, right = low + 1, high
    while left <= right:                         # corrección del PDF: '<=' en lugar de '<'
        while left <= right and S[left] <= pivot:
            left += 1                            # busca desde la izquierda un mayor que el pivote
        while left <= right and S[right] >= pivot:
            right -= 1                           # busca desde la derecha un menor que el pivote
        if left < right:
            S[left], S[right] = S[right], S[left]
    S[low], S[right] = S[right], S[low]          # el pivote va entre las dos partes
    return right


S = [15, 10, 12, 20, 25, 13, 22]
quicksort1(S, 0, len(S) - 1)
print(S)                                         # [10, 12, 13, 15, 20, 22, 25]

prueba = [1, 2, 3]                               # caso que falla con la versión del PDF
quicksort1(prueba, 0, len(prueba) - 1)
print(prueba)''', None)],
     "Se usa el `quicksort1` del curso con la partición corregida. La prueba con `[1, 2, 3]` muestra que la "
     "corrección funciona en el caso donde la versión de las diapositivas falla."),

    ("Actividad 4 — Quick Sort con pivote aleatorio",
     "1. Explique brevemente el funcionamiento del Quick Sort con un valor de pivote aleatorio.\n"
     "2. Comente las ventajas de esta variación.\n"
     "3. Desarrolle el código necesario para este algoritmo, con comentarios sobre su funcionamiento.",
     f"**Dónde se ve:** {unidad(29)} (`quicksort2` y `partition2`, pivote aleatorio).\n\n"
     "**En la plataforma:** el resultado ordenado es siempre el mismo, pero las líneas intermedias cambian en cada "
     "ejecución porque el pivote es aleatorio. Aquí se fija `random.seed(42)` solo para que la salida de ejemplo "
     "sea reproducible.",
     [("Respuesta", '''# Funcionamiento: igual que Quick Sort, pero antes de partir cada tramo se elige al azar una
# posición entre low y high y ese elemento se usa como pivote (se lleva al inicio del tramo).
# Ventajas: evita el peor caso O(N^2) con listas ya ordenadas o invertidas, donde el primer
# elemento es siempre el menor o el mayor; en promedio da O(N log N) sin importar cómo vengan
# los datos, y ninguna entrada concreta lo hace lento siempre.

import random
from random import randint


def quicksort2(S, low, high):
    """Quick Sort con pivote aleatorio; ordena S[low..high] en el lugar."""
    if low < high:
        pivotpoint = partition2(S, low, high)
        quicksort2(S, low, pivotpoint - 1)
        quicksort2(S, pivotpoint + 1, high)


def partition2(S, low, high):
    rand = randint(low, high)                    # posición aleatoria del pivote
    S[low], S[rand] = S[rand], S[low]            # el pivote elegido pasa al inicio del tramo
    pivot, left, right = S[low], low, high
    print(S, left, right, "pivot = ", pivot)     # muestra cada partición
    while left < right:
        while left < high and S[left] <= pivot:
            left += 1
        while right > low and pivot <= S[right]:
            right -= 1
        if left < right:
            S[left], S[right] = S[right], S[left]
    S[low], S[right] = S[right], S[low]          # el pivote queda en su lugar definitivo
    return right


random.seed(42)                                  # solo para que este ejemplo sea reproducible
S = [25, 22, 20, 15, 13, 12, 10]                 # lista invertida: el peor caso con pivote fijo
quicksort2(S, 0, len(S) - 1)
print(S)''', None)],
     "Con la lista invertida, un pivote fijo en el primer elemento haría siempre la peor partición; el pivote "
     "aleatorio reparte mejor y la lista se ordena igual. Es el `quicksort2` de la unidad 29."),
]


def ejecutar(bloques):
    """Ejecuta los bloques en orden en una carpeta temporal; devuelve la salida de cada uno."""
    previo = os.getcwd()
    original = builtins.input
    salidas = []
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
                    exec(compile(codigo, "<respuesta>", "exec"), {"__name__": "__main__"})
                salidas.append(buffer.getvalue())
        finally:
            builtins.input = original
            os.chdir(previo)
    return salidas


celdas = [new_markdown_cell(
    "# Actividad asincrónica — Semana 4\n\n"
    "**Capítulo 5: algoritmos de ordenamiento** (unidades 27 a 29)\n\n"
    "[Índice de la semana](semana-04.ipynb)\n\n"
    f"## Estado\n\n{ESTADO}\n\n"
    "## Cómo se califica\n\n"
    "- 4 preguntas de 25 puntos cada una (100). No tiene pregunta adicional.\n"
    "- Se puede retomar una vez si se entregó por error; la nota de la nueva entrega es la que cuenta.\n\n"
    "## Cómo usar este notebook\n\n"
    "Cada actividad trae la consigna, la unidad donde se explica, la **respuesta resuelta** (ya ejecutada, con su "
    "salida) y una explicación. Para entregar, copia el código de la respuesta en el recuadro de la plataforma y "
    "pulsa «Ejecutar». La plataforma tiene 5 recuadros: la actividad 1 usa dos.\n\n"
    "## Checklist de entrega\n\n" + "\n".join(f"- [{MARCA}] {a[0]}" for a in ACTIVIDADES)
    + f"\n- [{MARCA}] Revisar todo y pulsar «Entregar»"
)]

numero = 0
for titulo, consigna, guia, bloques, explicacion in ACTIVIDADES:
    salidas = ejecutar([(codigo, entradas) for _, codigo, entradas in bloques])
    celdas.append(new_markdown_cell(f"## {titulo}\n\n### Consigna\n\n{consigna}\n\n### Guía\n\n{guia}"))
    for (etiqueta, codigo, _), salida in zip(bloques, salidas):
        print(f"--- {titulo} / {etiqueta}\n{salida.rstrip()[-700:]}")
        numero += 1
        celdas.append(new_markdown_cell(f"### {etiqueta}"))
        celdas.append(new_code_cell(codigo, execution_count=numero,
                                    outputs=[new_output("stream", name="stdout", text=salida)]))
    celdas.append(new_markdown_cell("**Explicación:** " + explicacion))

celdas.append(new_markdown_cell("[Índice de la semana](semana-04.ipynb)"))
nb = new_notebook()
nb.cells = celdas
nbformat.write(nb, DESTINO)
print("Escrito:", DESTINO)
