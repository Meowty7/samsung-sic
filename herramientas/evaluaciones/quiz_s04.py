"""Genera 01-python/semana-04/quiz-calificado.ipynb (Quiz 4 de la plataforma) y prueba cada respuesta."""

import builtins
import contextlib
import io
import os
import tempfile
from pathlib import Path

import nbformat
from nbformat.v4 import new_code_cell, new_markdown_cell, new_notebook, new_output

RAIZ = Path(__file__).resolve().parents[2]
DESTINO = RAIZ / "01-python/semana-04/quiz-calificado.ipynb"
C1 = "clase-1-algoritmos-de-ordenamiento"
U = {
    27: f"{C1}/u27-burbuja-seleccion-insercion.ipynb",
    29: f"{C1}/u29-ordenamiento-rapido.ipynb",
}
ESTADO = "**Entregado. Nota final: 100/100.**"
MARCA = "x"


def unidad(*nums):
    return ", ".join(f"[Unidad {n}]({U[n]})" for n in nums)


# (titulo, consigna, unidades, codigo, explicacion, entradas)
PREGUNTAS = [
    ("Q 27-01 (30 puntos)",
     "¿Cuántas comparaciones se ejecutaron en el siguiente proceso de ordenamiento de burbuja?\n\n"
     "```python\ndef bubbleSort(S):\n    n = len(S)\n    for i in range(n):\n        print(S)\n        for j in range(n-1):\n"
     "            if S[j] > S[j+1]:\n               S[j] , S[j+1] = S[j+1] , S[j]\n\n"
     "S = [50, 30, 40, 10, 20]\nbubbleSort(S)\nprint(S)\n```",
     unidad(27),
     "def bubbleSort(S):\n"
     "    n = len(S)\n"
     "    comparaciones = 0\n"
     "    for i in range(n):\n"
     "        print(S)\n"
     "        for j in range(n - 1):\n"
     "            comparaciones += 1            # se cuenta cada S[j] > S[j+1]\n"
     "            if S[j] > S[j + 1]:\n"
     "                S[j], S[j + 1] = S[j + 1], S[j]\n"
     "    return comparaciones\n\n\n"
     "S = [50, 30, 40, 10, 20]\n"
     "total = bubbleSort(S)\n"
     "print(S)\n"
     "print('Comparaciones:', total)",
     "**Respuesta: 20 comparaciones.** El bucle externo da n = 5 vueltas y el interno compara n − 1 = 4 pares en "
     "cada una: 5 × 4 = 20. Esta versión no se detiene antes aunque la lista ya esté ordenada (desde la tercera "
     "vuelta) y siempre compara n − 1 pares; por eso hace n(n − 1) comparaciones, no n(n − 1)/2. Se agregó un "
     "contador para comprobarlo; la salida impresa es la misma del enunciado.",
     None),
    ("Q 27-02 (30 puntos)",
     "¿Cuántas comparaciones se ejecutaron en el siguiente proceso de ordenamiento de inserción?\n\n"
     "```python\ndef insertionSort2(S):\n    n = len(S)\n    for i in range(1,n):\n        print(S)\n        x = S[i]\n"
     "        j = i - 1\n        while j >= 0 and S[j] > x:\n            S[j+1] = S[j]\n            j -= 1\n"
     "        S[j + 1] = x\n\nS = [50, 30, 40, 10, 20]\ninsertionSort2(S)\nprint(S)\n```",
     unidad(27),
     "def insertionSort2(S):\n"
     "    n = len(S)\n"
     "    comparaciones = 0\n"
     "    for i in range(1, n):\n"
     "        print(S)\n"
     "        x = S[i]\n"
     "        j = i - 1\n"
     "        while j >= 0:\n"
     "            comparaciones += 1            # se cuenta cada S[j] > x\n"
     "            if S[j] > x:\n"
     "                S[j + 1] = S[j]\n"
     "                j -= 1\n"
     "            else:\n"
     "                break\n"
     "        S[j + 1] = x\n"
     "    return comparaciones\n\n\n"
     "S = [50, 30, 40, 10, 20]\n"
     "total = insertionSort2(S)\n"
     "print(S)\n"
     "print('Comparaciones:', total)",
     "**Respuesta: 10 comparaciones** entre elementos (`S[j] > x`):\n\n"
     "| i | x | Comparaciones | Lista después |\n|---|---|---|---|\n"
     "| 1 | 30 | 1 (con 50) | [30, 50, 40, 10, 20] |\n"
     "| 2 | 40 | 2 (con 50 y 30) | [30, 40, 50, 10, 20] |\n"
     "| 3 | 10 | 3 (con 50, 40 y 30) | [10, 30, 40, 50, 20] |\n"
     "| 4 | 20 | 4 (con 50, 40, 30 y 10) | [10, 20, 30, 40, 50] |\n\n"
     "Total: 1 + 2 + 3 + 4 = 10. Cuando `j` llega a −1, `j >= 0` es falso y ya no se compara ningún elemento. "
     "El contador se agregó separando la condición del `while`, sin cambiar lo que hace el algoritmo.\n\n"
     "**Nota sobre el enunciado:** el \"Output\" que muestra es el de la Q 27-01 (burbuja), copiado por error. La "
     "salida real de este código es la de arriba: `[50, 30, 40, 10, 20]`, `[30, 50, 40, 10, 20]`, "
     "`[30, 40, 50, 10, 20]`, `[10, 30, 40, 50, 20]` y `[10, 20, 30, 40, 50]`.",
     None),
    ("Q 29-01 (40 puntos)",
     "Dada la lista a continuación, escriba la salida después de ejecutar la función `partition1()`.\n\n"
     "```python\nS = [15,10,12,20,25,13,22]\npartition1(S, 0, len(S)-1)\nprint(S)\n```\n\n"
     "Output\n\n```text\n[15,10,12,20,25,13,22] 0 6 pivot = 15\n...\n```",
     unidad(29),
     "def partition1(S, low, high):\n"
     "    pivot, left, right = S[low], low, high     # pivote: el primer elemento\n"
     "    while left < right:\n"
     '        print(S, left, right, "pivot = ", pivot)\n'
     "        while left < high and S[left] <= pivot:   # avanza mientras sea menor o igual al pivote\n"
     "            left += 1\n"
     "        while right > low and pivot <= S[right]:  # retrocede mientras sea mayor o igual al pivote\n"
     "            right -= 1\n"
     "        if left < right:\n"
     "            S[left], S[right] = S[right], S[left]\n"
     "    S[low], S[right] = S[right], S[low]          # el pivote va a su posición final\n"
     "    return right\n\n\n"
     "S = [15, 10, 12, 20, 25, 13, 22]\n"
     "pivotpoint = partition1(S, 0, len(S) - 1)\n"
     "print(S)\n"
     "print('Posición final del pivote:', pivotpoint)",
     "**Respuesta (salida):**\n\n```text\n[15, 10, 12, 20, 25, 13, 22] 0 6 pivot =  15\n"
     "[15, 10, 12, 13, 25, 20, 22] 3 5 pivot =  15\n[13, 10, 12, 15, 25, 20, 22]\n```\n\n"
     "Paso a paso con pivote 15: `left` avanza hasta el 20 (índice 3) y `right` retrocede hasta el 13 (índice 5); "
     "como `left < right`, se intercambian 20 y 13. En la segunda vuelta `left` llega al 25 (índice 4) y `right` "
     "al 13 (índice 3); ya se cruzaron, así que termina el bucle y el pivote se intercambia con `S[3]`. Resultado: "
     "**`[13, 10, 12, 15, 25, 20, 22]`**, con el 15 en su lugar definitivo (índice 3): a la izquierda los menores "
     "y a la derecha los mayores.\n\n"
     "**Nota sobre el enunciado:** el formato de salida que muestra (`lista left right pivot = valor`) es el de la "
     "partición de la unidad 29 con pivote fijo en el primer elemento; con la `partition1` de las diapositivas, "
     "que imprime solo la lista, el resultado final es el mismo `[13, 10, 12, 15, 25, 20, 22]`.",
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
    "# Quiz 4 — Semana 4 (plataforma)\n\n"
    "**Capítulo 5: algoritmos de ordenamiento** (unidades 27 a 29)\n\n"
    "[Índice de la semana](semana-04.ipynb)\n\n"
    f"## Estado\n\n{ESTADO}\n\n"
    "## Cómo se califica\n\n"
    "- 3 preguntas: la primera y la segunda valen 30 puntos y la tercera 40 (100). No tiene preguntas adicionales.\n"
    "- Se puede retomar una vez si se entregó por error; la nota de la nueva entrega es la que cuenta.\n\n"
    "## Cómo usar este notebook\n\n"
    "Cada pregunta trae la consigna, la unidad donde se explica, la **respuesta resuelta** (ya ejecutada, con su "
    "salida) y una explicación. La respuesta a escribir está en negrita en la explicación; el código la comprueba.\n\n"
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
    celdas.append(new_markdown_cell("**Explicación:** " + explicacion))

celdas.append(new_markdown_cell("[Índice de la semana](semana-04.ipynb)"))
nb = new_notebook()
nb.cells = celdas
nbformat.write(nb, DESTINO)
print("Escrito:", DESTINO)
