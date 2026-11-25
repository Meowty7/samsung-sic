"""Genera 01-python/semana-02/quiz-calificado.ipynb (Quiz 2 de la plataforma) y prueba cada respuesta."""

import builtins
import contextlib
import io
import os
import tempfile
from pathlib import Path

import nbformat
from nbformat.v4 import new_code_cell, new_markdown_cell, new_notebook, new_output

RAIZ = Path(__file__).resolve().parents[2]
DESTINO = RAIZ / "01-python/semana-02/quiz-calificado.ipynb"
C1 = "clase-1-funciones-recursividad-lambda"
C2 = "clase-2-ambito-clausuras-y-clases"
U = {
    17: f"{C1}/u17-funciones.ipynb",
    18: f"{C1}/u18-recursividad.ipynb",
    19: f"{C1}/u19-lambda-filter-map-reduce.ipynb",
    20: f"{C2}/u20-ambito-y-clausuras.ipynb",
    21: f"{C2}/u21-clases-y-objetos.ipynb",
}


def unidad(*nums):
    return ", ".join(f"[Unidad {n}]({U[n]})" for n in nums)


# (titulo, consigna, unidades, codigo, explicacion, entradas)
PREGUNTAS = [
    ("Q 17-01",
     "Reciba las coordenadas (x1, y1), (x2, y2) de dos puntos del usuario e imprima la distancia entre los dos "
     "puntos. Para hacer esto, implemente la función `distancia(x1, y1, x2, y2)`.\n\n"
     "Pauta: consulte la fórmula para encontrar la distancia entre dos puntos.",
     unidad(17),
     "import math\n\n\n"
     "def distancia(x1, y1, x2, y2):\n"
     '    """Distancia euclidiana entre los puntos (x1, y1) y (x2, y2)."""\n'
     "    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)\n\n\n"
     'x1 = float(input("x1: "))\n'
     'y1 = float(input("y1: "))\n'
     'x2 = float(input("x2: "))\n'
     'y2 = float(input("y2: "))\n\n'
     'print("La distancia entre ({}, {}) y ({}, {}) es {}".format(x1, y1, x2, y2, distancia(x1, y1, x2, y2)))',
     "Fórmula: d = √((x2 − x1)² + (y2 − y1)²). Con los puntos (0, 0) y (3, 4) la distancia es 5.0. "
     "`float()` convierte el texto de `input()` en número y acepta decimales.\n\n"
     "**Nota sobre el enunciado:** dice \"de la siguiente manera\" pero no muestra el formato; se imprime una "
     "frase con los dos puntos y la distancia.",
     ["0", "0", "3", "4"]),
    ("Q 18-01",
     "Un palíndromo es una oración, palabra o cadena que se lee igual en ambos sentidos (level, kayak, salas, somos, "
     "radar, reconocer). Defina una función recursiva `is_palindrome` y escriba un programa que reciba una cadena "
     "del usuario e imprima si es palíndromo o no.\n\n"
     "Pauta: llame a la función `is_palindrome` dentro de la función `is_palindrome`.",
     unidad(18),
     "def is_palindrome(texto):\n"
     '    """True si texto se lee igual al derecho y al revés (recursiva)."""\n'
     "    if len(texto) <= 1:                     # caso base: 0 o 1 carácter siempre es palíndromo\n"
     "        return True\n"
     "    if texto[0] != texto[-1]:               # los extremos no coinciden: no es palíndromo\n"
     "        return False\n"
     "    return is_palindrome(texto[1:-1])       # llamada recursiva sin los extremos\n\n\n"
     'cadena = input("Ingrese una cadena: ")\n'
     'limpia = cadena.lower().replace(" ", "")      # ignora mayúsculas y espacios\n\n'
     "if is_palindrome(limpia):\n"
     '    print(cadena, "es un palíndromo.")\n'
     "else:\n"
     '    print(cadena, "no es un palíndromo.")\n\n'
     "# Pruebas rápidas con los ejemplos del enunciado\n"
     'for palabra in ["level", "kayak", "salas", "somos", "radar", "reconocer", "python"]:\n'
     "    print(palabra, \"->\", is_palindrome(palabra))",
     "Cada llamada compara el primer y el último carácter y, si coinciden, se llama a sí misma con la cadena sin "
     "ellos (`texto[1:-1]`). Termina cuando quedan 0 o 1 caracteres (caso base) o cuando encuentra una diferencia. "
     "La entrada se pasa a minúsculas y sin espacios para que \"Reconocer\" también cuente.",
     ["Reconocer"]),
    ("Q 19-01",
     "Indique el contenido de las variables `twice` y `triple`:\n\n"
     "```python\nn_list = [10,20,30]\ntwice  = list(map(lambda x: x*2, n_list))\ntriple = list(map(lambda x: x*3, n_list))\n```",
     unidad(19),
     "n_list = [10, 20, 30]\n"
     "twice = list(map(lambda x: x * 2, n_list))\n"
     "triple = list(map(lambda x: x * 3, n_list))\n\n"
     'print("twice =", twice)    # [20, 40, 60]\n'
     'print("triple =", triple)  # [30, 60, 90]',
     "**Respuesta:** `twice = [20, 40, 60]` y `triple = [30, 60, 90]`. `map` aplica la lambda a cada elemento de "
     "`n_list` y `list()` convierte el resultado en lista.",
     None),
    ("Q 20-01",
     "En el siguiente código, ¿qué valor se incluye finalmente en `num_list`? Calcule el resultado esperado a mano "
     "(el `for` se ejecuta 5 veces).\n\n"
     "```python\ndef calc_digit(n):\n    def findal(digit):\n        return digit**n\n    return final\n\n"
     "num_list = []\nfor num in range(1,6):\n    num_list.append( calc_digit(num) )\n    print( num_list[num-1](num) )\n```",
     unidad(20),
     "def calc_digit(n):\n"
     "    def final(digit):          # función interna: recuerda n (clausura)\n"
     "        return digit ** n\n"
     "    return final\n\n\n"
     "num_list = []\n"
     "for num in range(1, 6):\n"
     "    num_list.append(calc_digit(num))\n"
     "    print(num_list[num - 1](num))\n\n"
     "print(len(num_list), \"funciones en num_list\")   # 5 clausuras, una por cada n de 1 a 5\\n"
     "print(num_list[2](2))   # la tercera recuerda n = 3: 2 ** 3 = 8",
     "**Resultado esperado (a mano):** en cada vuelta se guarda la función que eleva a la potencia `num` y se "
     "llama con ese mismo `num`, así que se imprime num elevado a num:\n\n"
     "| Vuelta | Cálculo | Imprime |\n|---|---|---|\n"
     "| 1 | 1¹ | 1 |\n| 2 | 2² | 4 |\n| 3 | 3³ | 27 |\n| 4 | 4⁴ | 256 |\n| 5 | 5⁵ | 3125 |\n\n"
     "Al final, `num_list` contiene **5 funciones** (clausuras), no números: cada una recuerda su propio `n` "
     "(1, 2, 3, 4 y 5). Por ejemplo, `num_list[2](2)` devolvería 2³ = 8.\n\n"
     "**Nota sobre el enunciado:** la función interna se llama `findal` pero se devuelve `final`; así daría "
     "`NameError`. Se corrige usando el mismo nombre en los dos lugares.",
     None),
    ("Q 21-01",
     "Implemente la multiplicación (`*`) y la división (`/`) de dos vectores usando los métodos `__mul__` y "
     "`__truediv__` de la unidad 21. Con v1 = (30, 40) y v2 = (10, 20), escriba la salida de la multiplicación y "
     "la división de los dos vectores.\n\n"
     "Pauta: amplíe la funcionalidad de la clase `Vector2D` aprendida en este capítulo.",
     unidad(21),
     "class Vector2D:\n"
     "    def __init__(self, x, y):\n"
     "        self.x = x\n"
     "        self.y = y\n\n"
     "    def __add__(self, other):        # v1 + v2\n"
     "        return Vector2D(self.x + other.x, self.y + other.y)\n\n"
     "    def __sub__(self, other):        # v1 - v2\n"
     "        return Vector2D(self.x - other.x, self.y - other.y)\n\n"
     "    def __mul__(self, other):        # v1 * v2: multiplica componente a componente\n"
     "        return Vector2D(self.x * other.x, self.y * other.y)\n\n"
     "    def __truediv__(self, other):    # v1 / v2: divide componente a componente\n"
     "        return Vector2D(self.x / other.x, self.y / other.y)\n\n"
     "    def __str__(self):\n"
     '        return "({}, {})".format(self.x, self.y)\n\n\n'
     "v1 = Vector2D(30, 40)\n"
     "v2 = Vector2D(10, 20)\n\n"
     "print('v1 + v2 =', v1 + v2)\n"
     "print('v1 - v2 =', v1 - v2)\n"
     "print('v1 * v2 =', v1 * v2)\n"
     "print('v1 / v2 =', v1 / v2)",
     "Se parte de la `Vector2D` de la unidad 21 (`__init__`, `__add__`, `__sub__`, `__str__`) y se agregan "
     "`__mul__` y `__truediv__`. Python llama a `v1.__mul__(v2)` al escribir `v1 * v2` y a `v1.__truediv__(v2)` "
     "con `v1 / v2`. Resultado: `v1 * v2 = (300, 800)` y `v1 / v2 = (3.0, 2.0)` (la división con `/` devuelve float).\n\n"
     "**Nota sobre el enunciado:** dice \"el siguiente resultado\" pero no lo muestra; se usa la operación "
     "componente a componente, que es la extensión natural de `__add__` y `__sub__` de la unidad.",
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
    "# Quiz 2 — Semana 2 (plataforma)\n\n"
    "**Capítulo 3: función, clausura y clase** (unidades 17 a 21)\n\n"
    "[Índice de la semana](semana-02.ipynb)\n\n"
    "## Estado\n\n**Entregado. Nota final: 100/100.**\n\n"
    "## Cómo se califica\n\n"
    "- 5 preguntas de 20 puntos cada una (100). No tiene preguntas adicionales.\n"
    "- Se puede retomar una vez si se entregó por error; la nota de la nueva entrega es la que cuenta.\n\n"
    "## Cómo usar este notebook\n\n"
    "Cada pregunta trae la consigna, la unidad donde se explica, la **respuesta resuelta** (ya ejecutada, con su "
    "salida) y una explicación. Para entregar, copia el código de la respuesta en el recuadro de la plataforma y "
    "pulsa «Ejecutar».\n\n"
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
                + ", ".join(f"`{e}`" for e in entradas) + ". En la plataforma se abre una ventana para cada dato.")
    celdas.append(new_markdown_cell("**Explicación:** " + explicacion + nota))

celdas.append(new_markdown_cell("[Índice de la semana](semana-02.ipynb)"))
nb = new_notebook()
nb.cells = celdas
nbformat.write(nb, DESTINO)
print("Escrito:", DESTINO)
