"""Genera 01-python/semana-01/quiz-calificado.ipynb (Quiz 1 de la plataforma) y prueba cada respuesta."""

import builtins
import contextlib
import io
import os
import tempfile
from pathlib import Path

import nbformat
from nbformat.v4 import new_code_cell, new_markdown_cell, new_notebook, new_output

RAIZ = Path(__file__).resolve().parents[2]
DESTINO = RAIZ / "01-python/semana-01/quiz-calificado.ipynb"
S0 = "../semana-00"
U = {
    1: f"{S0}/clase-1-fundamentos/u01-pensamiento-computacional-y-entorno.ipynb",
    2: f"{S0}/clase-1-fundamentos/u02-algoritmos-y-diagramas-de-flujo.ipynb",
    3: f"{S0}/clase-1-fundamentos/u03-operadores-y-tipos-de-datos.ipynb",
    5: f"{S0}/clase-2-control-de-flujo/u05-operadores-de-comparacion-y-logicos.ipynb",
    7: f"{S0}/clase-2-control-de-flujo/u07-if-else-elif.ipynb",
    8: f"{S0}/clase-2-control-de-flujo/u08-bucle-for.ipynb",
    9: f"{S0}/clase-2-control-de-flujo/u09-bucle-while.ipynb",
    11: "clase-1-listas-tuplas-diccionarios/u11-diccionarios-y-json.ipynb",
    13: "clase-1-listas-tuplas-diccionarios/u13-listas-bidimensionales.ipynb",
    14: "clase-2-diccionarios-y-conjuntos/u14-diccionarios-crud.ipynb",
    15: "clase-2-diccionarios-y-conjuntos/u15-diccionarios-avanzados.ipynb",
    16: "clase-2-diccionarios-y-conjuntos/u16-conjuntos.ipynb",
}


def unidad(*nums):
    return ", ".join(f"[Unidad {n}]({U[n]})" for n in nums)


# (titulo, consigna, unidades, codigo, explicacion, entradas)
PREGUNTAS = [
    ("Q 01-01",
     "El código que imprime los valores numéricos del 1 al 3 utilizando la función `print()` es `print(1+2+3)`.\n\n"
     "Con referencia a este código, imprima los valores de 1 a 5 de forma similar.",
     unidad(1, 3),
     "print(1+2+3+4+5)",
     "Siguiendo el modelo `print(1+2+3)`, se escriben los valores de 1 a 5 unidos con `+`; Python calcula la "
     "suma y muestra `15`.\n\n**Nota sobre el enunciado:** la traducción dice que `print(1+2+3)` \"imprime los "
     "valores del 1 al 3\", pero en realidad imprime su suma (6). Se responde \"de forma similar\", como pide.",
     None),
    ("Q 02-01",
     "Un programa que reciba un número entero positivo del usuario e indique si es un número par o impar. "
     "Complete el pseudocódigo apropiado para `___`.\n\n"
     "```python\nprint(\"Ingrese un entero:\")\nn = input()\nif ___:\n    print(\"Es par\")\nelse:\n    print(\"Es impar\")\n```",
     unidad(3, 7),
     'print("Ingrese un entero:")\nn = input()\nif int(n) % 2 == 0:\n    print("Es par")\nelse:\n    print("Es impar")',
     "El espacio en blanco es **`int(n) % 2 == 0`**. `input()` devuelve texto, así que se convierte con `int()`; "
     "un número es par si el resto de dividirlo entre 2 (`%`) es 0.",
     ["8"]),
    ("Q 03-01",
     "Escribe el resultado del siguiente código.\n\n"
     "```python\nx = 1\ny = 0\nprint(x and y)\nprint(x or y)\nprint(not x)\nprint(not y)\n```",
     unidad(5),
     "x = 1\ny = 0\nprint(x and y)\nprint(x or y)\nprint(not x)\nprint(not y)",
     "Resultado:\n\n```text\n0\n1\nFalse\nTrue\n```\n\n"
     "- `x and y`: `and` devuelve el primer valor falso que encuentra; 1 es verdadero, así que devuelve `y`, que es **0**.\n"
     "- `x or y`: `or` devuelve el primer valor verdadero; `x` es 1, así que devuelve **1**.\n"
     "- `not x`: 1 es verdadero, su negación es **False**.\n"
     "- `not y`: 0 es falso, su negación es **True**.\n\n"
     "**Clave:** `and` y `or` no devuelven `True`/`False` sino uno de los operandos; `not` siempre devuelve un booleano.",
     None),
    ("Q 04-01",
     "Escriba un programa que realice las siguientes funciones utilizando una expresión condicional compuesta de "
     "una sentencia if. Guía: el código se ejecuta de forma diferente según la respuesta a la primera pregunta sea 0 o 1.\n\n"
     "Ejemplo:\n\n```text\n¿Eres un adulto? (1 si es mayor de edad, 0 si es menor de edad): 1\n"
     "¿Está casado? (1 si es casado, 0 si es soltero): 1\nUsted es un adulto que está casado.\n```\n\n"
     "Las tres salidas posibles son: Usted es un adulto que está casado. / Usted es un adulto que está soltero. / "
     "Usted es menor de edad.",
     unidad(7),
     'adulto = int(input("¿Eres un adulto? (1 si es mayor de edad, 0 si es menor de edad): "))\n\n'
     "if adulto == 1:\n"
     '    casado = int(input("¿Está casado? (1 si es casado, 0 si es soltero): "))\n'
     "    if casado == 1:\n"
     '        print("Usted es un adulto que está casado.")\n'
     "    else:\n"
     '        print("Usted es un adulto que está soltero.")\n'
     "else:\n"
     '    print("Usted es menor de edad.")',
     "Es un `if` anidado: solo si la primera respuesta es 1 se hace la segunda pregunta. Si es 0, se imprime "
     "directamente \"Usted es menor de edad.\" sin preguntar el estado civil. La salida mostrada corresponde a las "
     "respuestas 1 y 1.",
     ["1", "1"]),
    ("Q 05-01",
     "Entre los números naturales positivos distintos del 1, un número que no es primo se llama número compuesto. "
     "Escribe los números primos y compuestos del 2 al 12 (`2 : Primo`, `3 : Primo`, `4 : Compuesto`, ...).\n\n"
     "Pauta: use la instrucción `for`. Con un `for` anidado, el lazo interno debe determinar si el número es primo.",
     unidad(8, 9),
     "for n in range(2, 13):\n"
     "    es_primo = True\n"
     "    for divisor in range(2, n):      # lazo interno: busca un divisor\n"
     "        if n % divisor == 0:\n"
     "            es_primo = False\n"
     "            break\n"
     "    if es_primo:\n"
     '        print(n, ": Primo")\n'
     "    else:\n"
     '        print(n, ": Compuesto")',
     "El lazo externo recorre del 2 al 12. El interno prueba los divisores de 2 a n-1: si alguno divide exacto, "
     "el número es compuesto y `break` corta la búsqueda. Si ninguno divide, sigue siendo primo. "
     "`print(n, \": Primo\")` separa con un espacio, igual que el formato pedido.",
     None),
    ("Q 06-01",
     "Un número de Armstrong es un número entero de tres dígitos que es igual a la suma de los cubos de cada dígito. "
     "Encuentre todos los números de Armstrong de tres dígitos e imprímalos.\n\n"
     "Pauta: todos los números del 100 al 999 deben buscarse utilizando la instrucción `for`.",
     unidad(3, 8),
     "for numero in range(100, 1000):\n"
     "    centenas = numero // 100\n"
     "    decenas = (numero // 10) % 10\n"
     "    unidades = numero % 10\n"
     "    if centenas ** 3 + decenas ** 3 + unidades ** 3 == numero:\n"
     "        print(numero)",
     "Cada dígito se obtiene con división entera (`//`) y resto (`%`). Los números de Armstrong de tres dígitos "
     "son **153, 370, 371 y 407** (por ejemplo, 1³ + 5³ + 3³ = 1 + 125 + 27 = 153).\n\n"
     "**Nota sobre el enunciado:** dice \"imprímalos de la siguiente manera\" pero no muestra el formato; se "
     "imprime uno por línea.",
     None),
    ("Q 07-01",
     "Si hay dos listas `l1` y `l2` con las siguientes cadenas, use su combinación para imprimir:\n\n"
     "```python\nl1 = ['I like','I love']\nl1 = ['pancake.','kiwi juice.','espresso.']\n```\n\n"
     "```text\nI like pancake.\nI like kiwi juice.\nI like espresso.\nI love pancake.\nI love kiwi juice.\nI love espresso.\n```\n\n"
     "Pauta: use bucles anidados.",
     unidad(8, 13),
     "l1 = ['I like', 'I love']\n"
     "l2 = ['pancake.', 'kiwi juice.', 'espresso.']\n\n"
     "for inicio in l1:          # bucle externo: 'I like', luego 'I love'\n"
     "    for final in l2:       # bucle interno: cada comida o bebida\n"
     "        print(inicio, final)",
     "Por cada elemento de `l1` se recorre toda `l2`: 2 × 3 = 6 líneas.\n\n"
     "**Nota sobre el enunciado:** la segunda lista aparece como `l1` por error; se llama `l2`. Si se dejara `l1` "
     "dos veces, la segunda asignación reemplazaría a la primera.",
     None),
    ("Q 08-01",
     "Agregue un nuevo elemento al diccionario `person` con la clave `'Padre'` y el valor `'John Doe'`.\n\n"
     "Pauta: después de definir el diccionario, escriba el código para agregar el nuevo elemento.\n\n"
     "```python\nperson = {'Name':'David Doe', 'Age':26, 'Weight':82, 'Job':'Data Scientist'}\n```",
     unidad(11, 14),
     "person = {'Name': 'David Doe', 'Age': 26, 'Weight': 82, 'Job': 'Data Scientist'}\n\n"
     "person['Padre'] = 'John Doe'   # asignar a una clave nueva la agrega al diccionario\n"
     "print(person)",
     "Asignar a una clave que no existe la crea. Si la clave ya existiera, se reemplazaría su valor.",
     None),
    ("Q 09-01",
     "La matriz bidimensional `a` contiene `[[1, 2], [3, 4], [5, 6]]`. Cámbiela a una matriz unidimensional como "
     "`[1, 2, 3, 4, 5, 6]` e imprímala.\n\n"
     "Pauta: use un bucle `for`. Defina una nueva matriz y coloque los elementos de `a` en ella.",
     unidad(13),
     "a = [[1, 2], [3, 4], [5, 6]]\n"
     "b = []                    # nueva matriz unidimensional\n\n"
     "for fila in a:\n"
     "    for valor in fila:\n"
     "        b.append(valor)   # se agrega cada elemento en orden\n\n"
     "print(b)",
     "El bucle externo toma cada fila y el interno cada valor de la fila; `append` los va colocando en `b`.",
     None),
    ("Q 10-01",
     "El diccionario `maria` contiene las puntuaciones de 'coreano', 'inglés', 'matemáticas' y 'ciencia'. "
     "Imprima el puntaje promedio.\n\nGuía: utilice el método de diccionario `values()` y la función `len()`.\n\n"
     "```python\nmaria = { 'korean':94, 'english':91, 'maths':89, 'science':83 }\n```",
     unidad(11, 14),
     "maria = {'korean': 94, 'english': 91, 'maths': 89, 'science': 83}\n\n"
     "promedio = sum(maria.values()) / len(maria)\n"
     "print('Puntaje promedio:', promedio)",
     "`values()` da los cuatro puntajes, `sum` los suma (357) y `len(maria)` cuenta las asignaturas (4): "
     "357 / 4 = **89.25**.",
     None),
    ("Q 11-01",
     "Declare una variable `school` con un diccionario anidado:\n\n"
     "```python\nschool = {\n    'kim':{ 'age':16, 'hei':170, grade:3 },\n    'lee':{ 'age':15, 'hei':165, grade:2 },\n"
     "    'cho':{ 'age':14, 'hei':167, grade:1 },\n}\n```\n\n"
     "Luego, use `deepcopy()` del módulo `copy` para copiarlo a otra variable, `school2`, y verifique con el operador "
     "`is` que son variables diferentes.\n\nPauta: imprima el resultado de `school is school2`, que debe ser falso.",
     unidad(15),
     "import copy\n\n"
     "school = {\n"
     "    'kim': {'age': 16, 'hei': 170, 'grade': 3},\n"
     "    'lee': {'age': 15, 'hei': 165, 'grade': 2},\n"
     "    'cho': {'age': 14, 'hei': 167, 'grade': 1},\n"
     "}\n\n"
     "school2 = copy.deepcopy(school)   # copia profunda: también copia los diccionarios internos\n\n"
     "print(school is school2)              # False: son objetos distintos\n"
     "print(school == school2)              # True: tienen el mismo contenido\n"
     "print(school['kim'] is school2['kim'])  # False: los internos también son copias",
     "`is` compara identidad (si es el mismo objeto en memoria), no contenido. `deepcopy` crea objetos nuevos "
     "en todos los niveles, por eso incluso `school['kim'] is school2['kim']` es `False`.\n\n"
     "**Nota sobre el enunciado:** `grade` aparece sin comillas; así daría `NameError`, porque Python lo toma como "
     "una variable. Se escribe `'grade'`.",
     None),
    ("Q 12-01",
     "Hay una tupla de puntuaciones (nombre, inglés, matemáticas, ciencias):\n\n"
     "```python\nscores = (\n    ('DongKyu Park' , 88, 95, 90),\n    ('YoungMin Kang', 85, 90, 95),\n"
     "    ('DongMin Park' , 70, 90, 80),\n    ('Seungloo Hong', 90, 90, 95),\n)\n```\n\n"
     "Extraiga solo los puntajes de matemáticas desempaquetando con la función `zip` y calcule su promedio.\n\n"
     "Pauta: use la función `zip`.",
     unidad(16),
     "scores = (\n"
     "    ('DongKyu Park', 88, 95, 90),\n"
     "    ('YoungMin Kang', 85, 90, 95),\n"
     "    ('DongMin Park', 70, 90, 80),\n"
     "    ('Seungloo Hong', 90, 90, 95),\n"
     ")\n\n"
     "# zip(*scores) agrupa por posición: nombres, inglés, matemáticas y ciencias\n"
     "nombres, ingles, matematicas, ciencias = zip(*scores)\n\n"
     "print('Puntajes de matemáticas:', matematicas)\n"
     "promedio = sum(matematicas) / len(matematicas)\n"
     "print('Promedio de matemáticas:', promedio)",
     "`*scores` pasa cada tupla de estudiante como argumento separado, y `zip` junta los primeros elementos, los "
     "segundos, etc. Así se obtiene la \"columna\" de matemáticas: (95, 90, 90, 90). Promedio: 365 / 4 = **91.25**.",
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
    "# Quiz 1 — Semana 1 (plataforma)\n\n"
    "**Capítulos 1 y 2: conceptos básicos de programación y secuencias de datos en Python** (unidades 1 a 16)\n\n"
    "[Índice de la semana](semana-01.ipynb)\n\n"
    "## Estado\n\n**Entregado. Nota final: 100/100.**\n\n"
    "## Cómo se califica\n\n"
    "- Se responden 10 de las 12 preguntas, de 10 puntos cada una (100).\n"
    "- Las 2 adicionales (Extra Point) son opcionales: si la nota es menor que 60, cada una suma hasta 5 puntos. "
    "La nota máxima es 100.\n"
    "- Se puede retomar una vez si se entregó por error; la nota de la nueva entrega es la que cuenta.\n\n"
    "## Cómo usar este notebook\n\n"
    "Cada pregunta trae la consigna, la unidad donde se explica, la **respuesta resuelta** (ya ejecutada, con su "
    "salida) y una explicación. Aquí están respondidas las 12: conviene entregarlas todas.\n\n"
    "## Checklist de entrega\n\n" + "\n".join(f"- [x] {p[0]}" for p in PREGUNTAS)
    + "\n- [x] Revisar todo y pulsar «Entregar»"
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
                + ", ".join(f"`{e}`" for e in entradas) + ". En la plataforma se abre una ventana para escribir el dato.")
    celdas.append(new_markdown_cell("**Explicación:** " + explicacion + nota))

celdas.append(new_markdown_cell("[Índice de la semana](semana-01.ipynb)"))
nb = new_notebook()
nb.cells = celdas
nbformat.write(nb, DESTINO)
print("Escrito:", DESTINO)
