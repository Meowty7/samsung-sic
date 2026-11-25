"""Genera 01-python/semana-03/quiz-calificado.ipynb (Quiz 3 de la plataforma) y prueba cada respuesta."""

import builtins
import contextlib
import io
import os
import tempfile
from pathlib import Path

import nbformat
from nbformat.v4 import new_code_cell, new_markdown_cell, new_notebook, new_output

RAIZ = Path(__file__).resolve().parents[2]
DESTINO = RAIZ / "01-python/semana-03/quiz-calificado.ipynb"
C1 = "clase-1-pilas-colas-busqueda-secuencial"
C2 = "clase-2-busqueda-binaria-tablas-hash"
U = {
    22: f"{C1}/u22-pilas.ipynb",
    23: f"{C1}/u23-colas.ipynb",
    24: f"{C1}/u24-busqueda-secuencial.ipynb",
    25: f"{C2}/u25-busqueda-binaria.ipynb",
    26: f"{C2}/u26-tablas-hash.ipynb",
}
ESTADO = "**Entregado. Nota final: 100/100.**"
MARCA = "x"


def unidad(*nums):
    return ", ".join(f"[Unidad {n}]({U[n]})" for n in nums)


STACK = '''class Stack:

    def __init__(self):
        self.stack = []

    def is_empty(self):
        return True if len(self.stack) == 0 else False

    def push(self, item):
        self.stack.append(item)

    def pop(self):
        return None if self.is_empty() else self.stack.pop()
'''

QUEUE = '''class Queue:

    def __init__(self):
        self.queue = []

    def is_empty(self):
        return True if len(self.queue) == 0 else False

    def enqueue(self, item):
        self.queue.append(item)

    def dequeue(self):
        return None if self.is_empty() else self.queue.pop(0)
'''

HASHTABLE = '''class HashTable:

    def __init__(self, size):
        self.size = size
        self.table = {}
        for i in range(size):
            self.table[i] = []

    def hash(self, key):
        return key % self.size

    def get(self, key):
        return self.table[self.hash(key)]

    def put(self, key, value):
        bucket = self.table[self.hash(key)]
        if value not in bucket:
            bucket.append(value)
'''

CLASE_PILA = "Para ejecutarlo se incluye la clase `Stack` de la unidad 22 (la misma del curso)."
CLASE_COLA = "Para ejecutarlo se incluye la clase `Queue` de la unidad 23 (la misma del curso)."
CLASE_HASH = "Para ejecutarlo se incluye la clase `HashTable` de la unidad 26 (la misma del curso)."

# (titulo, consigna, unidades, codigo, explicacion, entradas)
PREGUNTAS = [
    ("Q 22-01",
     "La siguiente es la implementación de una pila. ¿Cuál será el resultado del siguiente código?\n\n"
     "```python\nstack = Stack()\nstack.push(\"Banana\")\nstack.push(\"Apple\")\nstack.push(\"Tomato\")\nstack.pop()\n"
     "stack.push(\"Strawberry\")\nstack.push(\"Grapes\")\nstack.pop()\nprint(stack.stack)\n```",
     unidad(22),
     STACK + '\n\nstack = Stack()\nstack.push("Banana")\nstack.push("Apple")\nstack.push("Tomato")\nstack.pop()\n'
     'stack.push("Strawberry")\nstack.push("Grapes")\nstack.pop()\nprint(stack.stack)',
     "**Respuesta:** `['Banana', 'Apple', 'Strawberry']`.\n\n"
     "La pila saca siempre el último que entró (LIFO): el primer `pop` quita `Tomato` y el segundo quita `Grapes`. "
     + CLASE_PILA,
     None),
    ("Q 22-02",
     "La siguiente es la implementación de una pila. ¿Cuál será el resultado del siguiente código?\n\n"
     "```python\nstack = Stack()\nitems = [10 * i for i in range(1,10)]\nfor item in items:\n    stack.push(item)\n"
     "    if (item // 10) % 2 == 0:\n        stack.pop()\nprint(stack.stack)\n```",
     unidad(22),
     STACK + "\n\nstack = Stack()\nitems = [10 * i for i in range(1, 10)]\nfor item in items:\n    stack.push(item)\n"
     "    if (item // 10) % 2 == 0:\n        stack.pop()\nprint(stack.stack)",
     "**Respuesta:** `[10, 30, 50, 70, 90]`.\n\n"
     "`items` es `[10, 20, ..., 90]`. Cuando `item // 10` es par (20, 40, 60, 80), el `pop` quita justo ese "
     "número, que es el último que entró. Quedan los de decena impar. " + CLASE_PILA,
     None),
    ("Q 23-01",
     "La siguiente es la implementación de una cola. ¿Cuál será el resultado del siguiente código?\n\n"
     "```python\nqueue = Queue()\nqueue.enqueue(\"Banana\")\nqueue.enqueue(\"Apple\")\nqueue.enqueue(\"Tomato\")\n"
     "queue.dequeue()\nqueue.enqueue(\"Strawberry\")\nqueue.enqueue(\"Grapes\")\nqueue.dequeue()\nprint(queue.queue)\n```",
     unidad(23),
     QUEUE + '\n\nqueue = Queue()\nqueue.enqueue("Banana")\nqueue.enqueue("Apple")\nqueue.enqueue("Tomato")\n'
     'queue.dequeue()\nqueue.enqueue("Strawberry")\nqueue.enqueue("Grapes")\nqueue.dequeue()\nprint(queue.queue)',
     "**Respuesta:** `['Tomato', 'Strawberry', 'Grapes']`.\n\n"
     "La cola saca siempre el primero que entró (FIFO): el primer `dequeue` quita `Banana` y el segundo `Apple`.\n\n"
     "**Nota sobre el enunciado:** dice \"implementación de una pila\" pero el código usa una cola (`Queue`). "
     + CLASE_COLA,
     None),
    ("Q 23-02",
     "La siguiente es la implementación de una cola. ¿Cuál será el resultado del siguiente código?\n\n"
     "```python\nqueue = Queue()\nitems = [10 * i for i in range(1,10)]\nfor item in items:\n    queue.enqueue(item)\n"
     "    if (item // 10) % 2 == 0:\n        queue.dequeue()\nprint(queue.queue)\n```",
     unidad(23),
     QUEUE + "\n\nqueue = Queue()\nitems = [10 * i for i in range(1, 10)]\nfor item in items:\n"
     "    queue.enqueue(item)\n    if (item // 10) % 2 == 0:\n        queue.dequeue()\nprint(queue.queue)",
     "**Respuesta:** `[50, 60, 70, 80, 90]`.\n\n"
     "A diferencia de la pila, cada `dequeue` quita el **más antiguo**: al llegar 20 sale 10, al llegar 40 sale 20, "
     "al llegar 60 sale 30 y al llegar 80 sale 40. Entran 9 y salen 4, quedan 5. " + CLASE_COLA,
     None),
    ("Q 24-01",
     "¿Cuál es el algoritmo de la siguiente función `find_two()`? Analice el código y escriba el resultado.\n\n"
     "```python\ndef find_two():\n    x = y = 0\n    for i in range(1, len(nums)):\n        if nums[x] < nums[i]:\n"
     "            x = i\n        elif nums[y] > nums[i]:\n            y = i\n    return x,y\n\n"
     "nums = [11, 37, 45, 26, 59, 28, 17, 53]\ni,j = find_two(nums)\nprint(nums[i], nums[j])\n```",
     unidad(24),
     "def find_two(nums):\n"
     "    x = y = 0                          # x: índice del mayor, y: índice del menor\n"
     "    for i in range(1, len(nums)):\n"
     "        if nums[x] < nums[i]:\n"
     "            x = i\n"
     "        elif nums[y] > nums[i]:\n"
     "            y = i\n"
     "    return x, y\n\n\n"
     "nums = [11, 37, 45, 26, 59, 28, 17, 53]\n"
     "i, j = find_two(nums)\n"
     "print(nums[i], nums[j])",
     "**Algoritmo:** búsqueda secuencial que encuentra **a la vez el máximo y el mínimo** en un solo recorrido; "
     "devuelve sus índices.\n\n**Resultado:** `59 11` (59 es el mayor y 11 el menor).\n\n"
     "**Nota sobre el enunciado:** la función se define sin parámetros, `def find_two():`, pero se llama con "
     "`find_two(nums)`; así daría `TypeError`. Se agrega el parámetro `nums`.",
     None),
    ("Q 24-02",
     "¿Cuántas comparaciones debe realizar la función `find_two()` de la pregunta anterior (24-01)?",
     unidad(24),
     "def find_two_contando(nums):\n"
     "    x = y = 0\n"
     "    comparaciones = 0\n"
     "    for i in range(1, len(nums)):\n"
     "        comparaciones += 1                 # nums[x] < nums[i]\n"
     "        if nums[x] < nums[i]:\n"
     "            x = i\n"
     "        else:\n"
     "            comparaciones += 1             # nums[y] > nums[i] (solo si la primera fue falsa)\n"
     "            if nums[y] > nums[i]:\n"
     "                y = i\n"
     "    return x, y, comparaciones\n\n\n"
     "nums = [11, 37, 45, 26, 59, 28, 17, 53]\n"
     "x, y, total = find_two_contando(nums)\n"
     "print('Comparaciones con esta lista:', total)\n"
     "print('Mínimo posible (n - 1):', len(nums) - 1)\n"
     "print('Máximo posible 2(n - 1):', 2 * (len(nums) - 1))",
     "**Respuesta:** con esta lista hace **11 comparaciones**. En general, para n elementos hace entre "
     "**n − 1 = 7** (si cada número es un nuevo máximo, el `elif` nunca se evalúa) y **2(n − 1) = 14** (si la "
     "primera comparación siempre es falsa). Recorrido: i = 1, 2 y 4 encuentran un nuevo máximo (1 comparación "
     "cada uno); i = 3, 5, 6 y 7 hacen 2 comparaciones cada uno: 3 × 1 + 4 × 2 = 11.",
     None),
    ("Q 25-01",
     "Código del juego de adivinar el número. Si el máximo es 100 y el número es 51, ¿cuál es la salida de "
     "`count`?\n\n"
     "```python\nmaximo = int(input(\"Ingrese el número maximo: \"))\nnumero = int(input(\"Ingrese tu intento de adivinar el numero: \"))\n"
     "low, high = 1, maximo\ncount = 0\nwhile low < high:\n    count += 1\n    mid = (low + high) // 2\n"
     "    if mid == numero:\n        print(f\"El número es {numero}\")\n        break\n    elif mid > numero:\n"
     "        high = mid - 1\n    else:\n        low  = mid + 1\n\nprint(f\"Total {count} veces fue buscado.\")\n```",
     unidad(25),
     'maximo = int(input("Ingrese el número maximo: "))\n'
     'numero = int(input("Ingrese tu intento de adivinar el numero: "))\n'
     "low, high = 1, maximo\n"
     "count = 0\n"
     "while low < high:\n"
     "    count += 1\n"
     "    mid = (low + high) // 2\n"
     "    print(f\"Intento {count}: low={low}, high={high}, mid={mid}\")   # traza para ver cada paso\n"
     "    if mid == numero:\n"
     '        print(f"El número es {numero}")\n'
     "        break\n"
     "    elif mid > numero:\n"
     "        high = mid - 1\n"
     "    else:\n"
     "        low = mid + 1\n\n"
     'print(f"Total {count} veces fue buscado.")',
     "**Respuesta:** `count` = **6** (\"Total 6 veces fue buscado.\"). Los valores de `mid` son 50, 75, 62, 56, "
     "53 y 51. La línea de traza (`print` de cada intento) se agregó solo para mostrar los pasos; el valor de "
     "`count` es el mismo sin ella.",
     ["100", "51"]),
    ("Q 25-02",
     "En el mismo código, si el máximo es 100 y el número es 25, ¿cuál es el resultado del conteo?",
     unidad(25),
     "def contar_busqueda(maximo, numero):\n"
     "    low, high = 1, maximo\n"
     "    count = 0\n"
     "    while low < high:\n"
     "        count += 1\n"
     "        mid = (low + high) // 2\n"
     "        print(f\"Intento {count}: mid={mid}\")\n"
     "        if mid == numero:\n"
     "            break\n"
     "        elif mid > numero:\n"
     "            high = mid - 1\n"
     "        else:\n"
     "            low = mid + 1\n"
     "    return count\n\n\n"
     "print('Total', contar_busqueda(100, 25), 'veces fue buscado.')",
     "**Respuesta:** `count` = **2**. Primer intento: `mid` = (1 + 100) // 2 = 50, mayor que 25, entonces "
     "`high` = 49. Segundo intento: `mid` = (1 + 49) // 2 = 25, lo encuentra.",
     None),
    ("Q 26-01",
     "Usando la función hash de la clase `HashTable`, calcule la clave y la clave hash de \"Alice in Wonderland\" "
     "(el valor clave es 1763).\n\n"
     "```python\ntable = HashTable(8)\nbook  = \"Alice in Wonderland\"\nkey = sum(map(ord, book))\nprint(key, table.hash(key))\n```",
     unidad(26),
     HASHTABLE + '\n\ntable = HashTable(8)\nbook  = \"Alice in Wonderland\"\nkey = sum(map(ord, book))\n'
     "print(key, table.hash(key))\n\n"
     "# Valor clave indicado en el enunciado\n"
     "key = 1763\nprint(key, table.hash(key))",
     "**Respuesta:** `1763 3` (la clave que da el enunciado y su clave hash). El código copia la consigna tal cual y "
     "además muestra el cálculo con el valor indicado: 1763 % 8 = 3 (8 × 220 = 1760).\n\n"
     "**Nota sobre el enunciado:** el texto \"Alice in Wonderland\" suma 1795, no 1763; el 1763 corresponde a "
     "\"Alice in WonderLand\" (con L mayúscula), como aparece en el PDF de la unidad 26. La clave hash es 3 en los "
     "dos casos. Por eso la respuesta muestra las dos líneas: la del código literal (`1795 3`) y la del valor "
     "indicado (`1763 3`). " + CLASE_HASH
     + "\n\n**Corrección del docente:** primera entrega, \"Alice in WonderLand\" con salida `1763 3`: 3/10 por "
     "cambiar el texto. Segunda entrega, texto literal con salida `1795 3`: 5/10, porque se esperaba `1763 3`. "
     "**Clave:** el docente quiere el texto literal **y** el resultado que anuncia el enunciado; cuando no coinciden, "
     "se muestran ambos y se explica la diferencia. Tercera entrega, con esta respuesta: 10/10.",
     None),
    ("Q 26-02",
     "Si la nueva estantería tiene 10 compartimentos, use el siguiente código para averiguar qué libro hay en cada "
     "compartimento.\n\n"
     "```python\ntable = HashTable(10)\nbooks = [\n    \"The Little Prince\",\n    \"The Old Man and the Sea\",\n"
     "    \"The Little Memaid\",\n    \"Beauty and the Beast\",\n    \"The Last Leaf\",\n    \"Alice in Wonderland\",\n]\n\n"
     "for book in books:\n    key = sum(map(ord, book))\n    table.put(key, book)\n\n"
     "for key in table.table.key():\n    print(key, table.table[key])\n```",
     unidad(26),
     HASHTABLE + "\n\ntable = HashTable(10)\nbooks = [\n"
     '    "The Little Prince",\n    "The Old Man and the Sea",\n    "The Little Memaid",\n'
     '    "Beauty and the Beast",\n    "The Last Leaf",\n    "Alice in Wonderland",\n]\n\n'
     "for book in books:\n    key = sum(map(ord, book))\n    table.put(key, book)\n\n"
     "for key in table.table.keys():\n    print(key, table.table[key])",
     "Cada libro va al compartimento `suma ASCII % 10`. Los títulos se copian **tal como los da la consigna** "
     "(\"The Little Memaid\" y \"Alice in Wonderland\", con sus erratas): el docente descuenta si se cambian. "
     "La salida a entregar es esta:\n\n"
     "```text\n0 []\n1 []\n2 []\n3 ['The Last Leaf']\n4 ['The Little Prince', 'The Little Memaid']\n"
     "5 ['Alice in Wonderland']\n6 []\n7 ['Beauty and the Beast']\n8 []\n9 ['The Old Man and the Sea']\n```\n\n"
     "Los compartimentos vacíos aparecen como `[]`; en el 4 hay una colisión: dos libros comparten la lista.\n\n"
     "**Nota sobre el enunciado:** `table.table.key()` no existe (da `AttributeError`); el método del diccionario "
     "es `keys()`, y es el único cambio que se hace al código de la consigna. Con los títulos del PDF de la unidad 26 "
     "(\"The Little Mermaid\" y \"Alice in WonderLand\") las claves cambian: Mermaid iría al 8 y Alice al 3. "
     + CLASE_HASH
     + "\n\n**Corrección del docente (8/10):** la tabla, la inserción y el recorrido estaban bien, pero se descontó "
     "por no incluir la salida concreta y por cambiar la escritura de los títulos respecto al enunciado. Esta "
     "respuesta ya está corregida en los dos puntos y, entregada de nuevo, obtuvo 10/10.",
     None),
]


def probar(codigo, entradas):
    """Ejecuta una respuesta en una carpeta temporal, con entradas simuladas si las necesita."""
    previo = os.getcwd()
    original = builtins.input
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
                exec(compile(codigo, "<respuesta>", "exec"), {"__name__": "__main__"})
        finally:
            builtins.input = original
            os.chdir(previo)
    return salida.getvalue()


celdas = [new_markdown_cell(
    "# Quiz 3 — Semana 3 (plataforma)\n\n"
    "**Capítulo 4: estructuras de datos** (unidades 22 a 26)\n\n"
    "[Índice de la semana](semana-03.ipynb)\n\n"
    f"## Estado\n\n{ESTADO}\n\n"
    "## Cómo se califica\n\n"
    "- 10 preguntas de 10 puntos cada una (100). No tiene preguntas adicionales.\n"
    "- Se puede corregir y volver a entregar las veces que haga falta hasta que el docente la revise; la nota nueva reemplaza a la anterior.\n\n"
    "## Cómo usar este notebook\n\n"
    "Cada pregunta trae la consigna, la unidad donde se explica, la **respuesta resuelta** (ya ejecutada, con su "
    "salida) y una explicación. En las preguntas que piden \"el resultado\", la respuesta a escribir es la que "
    "aparece en negrita en la explicación; el código sirve para comprobarla.\n\n"
    "**Nota sobre el enunciado:** la cabecera del quiz lista \"Unidad 17. Pila\", \"18. Cola\", etc.; en el curso "
    "son las unidades 22 a 26.\n\n"
    "## Checklist de entrega\n\n" + "\n".join(f"- [{MARCA}] {p[0]}" for p in PREGUNTAS)
    + f"\n- [{MARCA}] Revisar todo y pulsar «Entregar»"
)]

numero = 0
for titulo, consigna, unidades, codigo, explicacion, entradas in PREGUNTAS:
    salida = probar(codigo, entradas)
    print(f"--- {titulo}\n{salida.rstrip()}")
    numero += 1
    celdas += [
        new_markdown_cell(f"## {titulo}\n\n### Consigna\n\n{consigna}\n\n**Dónde se ve:** {unidades}"),
        new_markdown_cell("### Respuesta"),
        new_code_cell(codigo, execution_count=numero,
                      outputs=[new_output("stream", name="stdout", text=salida)]),
    ]
    nota = ""
    if entradas:
        nota = ("\n\nUsa `input()`: la salida de arriba es una prueba respondiendo "
                + ", ".join(f"`{e}`" for e in entradas) + ". En la plataforma se abre una ventana para cada dato.")
    celdas.append(new_markdown_cell("**Explicación:** " + explicacion + nota))

celdas.append(new_markdown_cell("[Índice de la semana](semana-03.ipynb)"))
nb = new_notebook()
nb.cells = celdas
nbformat.write(nb, DESTINO)
print("Escrito:", DESTINO)
