"""Genera 01-python/semana-05/actividad-asincronica.ipynb y prueba cada respuesta."""

import builtins
import contextlib
import io
import os
import tempfile
from pathlib import Path

import nbformat
from nbformat.v4 import new_code_cell, new_markdown_cell, new_notebook, new_output

RAIZ = Path(__file__).resolve().parents[2]
DESTINO = RAIZ / "01-python/semana-05/actividad-asincronica.ipynb"
S4 = "../semana-04/clase-2-greedy-divide-y-venceras"
C1 = "clase-1-programacion-dinamica-y-backtracking"
U = {
    30: f"{S4}/u30-enfoque-greedy.ipynb",
    31: f"{S4}/u31-divide-y-venceras.ipynb",
    32: f"{C1}/u32-programacion-dinamica.ipynb",
    33: f"{C1}/u33-backtracking.ipynb",
}
ESTADO = "**Entregada. Nota final: 100/100.**"
MARCA = "x"


def unidad(*nums):
    return ", ".join(f"[Unidad {n}]({U[n]})" for n in nums)


# (titulo, consigna, guia, [(etiqueta, codigo, entradas, esperados)], explicacion)
ACTIVIDADES = [
    ("Actividad 1 — Algoritmos Greedy",
     "Explique brevemente y en forma clara qué es un algoritmo Greedy y cómo funciona. Enumere algunas ventajas. "
     "Enumere algunas desventajas. Escriba el código desarrollado con el enfoque Greedy para el problema de cambio "
     "de monedas, haga diferentes pruebas cambiando las entradas (las entradas de este algoritmo son las monedas "
     "disponibles y la cantidad que se desea cubrir; con estas entradas el algoritmo debe retornar la combinación de "
     "monedas que cubre el monto solicitado, minimizando la cantidad de monedas usadas). Ahora pruebe los "
     "resultados con las siguientes entradas: `monedas_disponibles = [11, 5, 1]` para cubrir la cantidad de 15, "
     "observe los resultados y haga algún análisis de lo que pasaría con esta combinación de entradas.\n\n"
     "```python\n# Espacio disponible para desarrollar el código y agregar los comentarios necesarios.\n```",
     f"**Dónde se ve:** {unidad(30)} (enfoque Greedy y `coin_change`).\n\n"
     "**Clave:** con monedas `[11, 5, 1]` y el importe 15, el Greedy elige 11 y luego cuatro de 1 (5 monedas), pero "
     "la solución óptima es 5 + 5 + 5 (3 monedas). El criterio \"la moneda más grande que quepa\" no siempre da el "
     "mínimo.\n\n"
     "**Para redactar a tu manera:** la explicación del primer bloque es una respuesta modelo. Escríbela con tus "
     "propias palabras antes de entregar.",
     [("Respuesta", '''# ¿Qué es un algoritmo Greedy (voraz o ávido) y cómo funciona?
# Resuelve un problema por etapas. En cada etapa elige la opción que parece mejor en ese momento
# (la elección local óptima) y no vuelve atrás: nunca revisa una decisión ya tomada. Si el problema
# cumple la propiedad de elección Greedy, las elecciones locales llevan a la solución óptima global.
#
# Ventajas:
#   - Es simple de diseñar y de programar.
#   - Es rápido: casi siempre basta un recorrido, con poca memoria.
#   - Es fácil de explicar y de verificar paso a paso.
# Desventajas:
#   - No siempre encuentra la solución óptima: depende del problema y de los datos.
#   - Hay que demostrar (o comprobar) que el criterio de elección es correcto.
#   - Como no retrocede, una mala decisión temprana no se corrige.

# Código del curso (unidad 30): las monedas deben venir ordenadas de mayor a menor.
def coin_change(coins, amount):
    changes = []
    largest = 0                         # posición de la moneda más grande que se prueba
    while amount > 0:
        if amount < coins[largest]:     # la moneda no cabe: pasar a la siguiente
            largest += 1
        else:
            changes.append(coins[largest])   # elección Greedy: la moneda más grande que quepa
            amount -= coins[largest]
    return changes


# Diferentes pruebas cambiando las entradas
pruebas = [
    ([500, 100, 50, 10], 870),    # ejemplo del PDF
    ([25, 10, 5, 1], 63),         # monedas de un sistema monetario "normal"
    ([500, 100, 50, 10], 10),     # un solo valor
    ([200, 100, 50, 20, 10], 380),
]
for monedas, importe in pruebas:
    cambio = coin_change(monedas, importe)
    print(f"monedas {monedas}, importe {importe}: {cambio} -> {len(cambio)} monedas")

# Si el importe no se puede formar, el algoritmo del curso se pasa del final de la lista
try:
    coin_change([500, 100, 50, 10], 875)
except IndexError:
    print("monedas [500, 100, 50, 10], importe 875: IndexError (no se puede formar con esas monedas)")

# Caso pedido: monedas_disponibles = [11, 5, 1] para cubrir 15
monedas_disponibles = [11, 5, 1]
cambio = coin_change(monedas_disponibles, 15)
print("\\nmonedas", monedas_disponibles, "importe 15:", cambio, "->", len(cambio), "monedas")

# Análisis: el Greedy toma 11 (la más grande que cabe), quedan 4 y completa con cuatro monedas de 1:
# 11 + 1 + 1 + 1 + 1 = 15 con 5 monedas. Pero 5 + 5 + 5 = 15 usa solo 3 monedas. Por eso el
# resultado no es el óptimo: este sistema de monedas rompe la propiedad de elección Greedy.''',
       None, ["[11, 1, 1, 1, 1] -> 5 monedas", "[500, 100, 100, 100, 50, 10, 10] -> 7 monedas",
              "IndexError"]),
      ("Complemento (no es necesario entregarlo): comprobación con programación dinámica", '''# Complemento: calcula el mínimo real de monedas con programación dinámica (unidad 32) para
# comprobar el análisis anterior. Continúa el código de arriba.
def minimo_monedas_dp(monedas, importe):
    """Devuelve (cantidad mínima, combinación) o None si no se puede formar el importe."""
    mejor = [None] * (importe + 1)       # mejor[x] = combinación mínima para el importe x
    mejor[0] = []
    for x in range(1, importe + 1):
        for moneda in monedas:
            if moneda <= x and mejor[x - moneda] is not None:
                candidata = mejor[x - moneda] + [moneda]
                if mejor[x] is None or len(candidata) < len(mejor[x]):
                    mejor[x] = candidata
    return None if mejor[importe] is None else (len(mejor[importe]), sorted(mejor[importe], reverse=True))

for monedas, importe in [([11, 5, 1], 15), ([500, 100, 50, 10], 870), ([25, 10, 5, 1], 63)]:
    greedy = len(coin_change(monedas, importe))
    optimo = minimo_monedas_dp(monedas, importe)
    print(f"{monedas}, {importe}: Greedy usa {greedy}, el mínimo es {optimo[0]} {optimo[1]}")''',
       None, ["[11, 5, 1], 15: Greedy usa 5, el mínimo es 3 [5, 5, 5]",
              "[500, 100, 50, 10], 870: Greedy usa 7, el mínimo es 7"])],
     "El Greedy del curso devuelve `[11, 1, 1, 1, 1]` (5 monedas) para 15 con `[11, 5, 1]`, mientras que el "
     "mínimo es `[5, 5, 5]` (3 monedas): es el caso en que el criterio Greedy falla. Con los sistemas de monedas "
     "habituales (como `[500, 100, 50, 10]` o `[25, 10, 5, 1]`) sí da el óptimo. El complemento con programación "
     "dinámica lo confirma y anticipa por qué existe la unidad 32."),

    ("Actividad 2 — Trayectoria triangular mínima",
     "Replique el código de la búsqueda de la trayectoria triangular mínima. Instrucciones: replique el código "
     "mostrado en la unidad 31. Analice el código replicado y agregue una explicación sobre su funcionamiento. "
     "Haga diferentes pruebas cambiando la entrada.",
     f"**Dónde se ve:** {unidad(31)} (`find_minimum`, divide y vencerás sobre el triángulo).\n\n"
     "**Clave:** desde la casilla `(row, col)` solo se puede bajar a `(row + 1, col)` o a `(row + 1, col + 1)`. El "
     "costo mínimo desde una casilla es su valor más el menor de los dos costos mínimos de abajo.\n\n"
     "**Error común:** pensar que basta con elegir siempre el menor de los dos vecinos (eso es Greedy y puede "
     "fallar); la función compara los caminos completos.",
     [("Respuesta", '''# Código de la unidad 31
def find_minimum(row, col, triangle):
    # Caso base: se pasó de la última fila, no queda costo por pagar
    if row == len(triangle):
        return 0
    # Dividir: bajar a (row + 1, col) o a (row + 1, col + 1); cada opción es un subproblema
    # Conquistar: cada subproblema se resuelve con una llamada recursiva
    minimum = min(find_minimum(row + 1, col, triangle),
                  find_minimum(row + 1, col + 1, triangle))
    # Combinar: el costo de la casilla actual más el mejor camino que queda
    return triangle[row][col] + minimum


triangle = [
    [2],
    [3, 4],
    [6, 5, 7],
    [4, 1, 8, 3]
]
minimum = find_minimum(0, 0, triangle)
print("The minimum cost is ", minimum)       # 2 + 3 + 5 + 1 = 11

# Explicación: find_minimum(0, 0, triangle) pregunta cuánto cuesta el mejor camino desde la cima.
# Cada llamada se divide en dos (izquierda y derecha) hasta salir del triángulo (caso base, costo 0).
# Al volver, cada nivel suma su casilla al menor de los dos resultados. Como no recuerda lo ya
# calculado, repite subproblemas: hace 2^(n+1) - 1 llamadas para n filas (por eso es lento con
# triángulos grandes; la unidad 32 lo mejora con programación dinámica).

# Diferentes pruebas cambiando la entrada
pruebas = [
    [[5]],
    [[1], [9, 2]],
    [[3], [7, 4], [2, 4, 6], [8, 5, 9, 3]],
    [[1], [2, 3], [4, 5, 6], [7, 8, 9, 10], [1, 1, 1, 1, 1]],
]
for tri in pruebas:
    resultado = find_minimum(0, 0, tri)
    print(f"{tri} -> costo mínimo {resultado}")''', None, ["The minimum cost is  11", "[[5]] -> costo mínimo 5"]),
      ("Complemento (no es necesario entregarlo): comprobar con todos los caminos", '''# Complemento: se comprueba find_minimum contra la lista de todos los caminos posibles.
from itertools import product

def todos_los_caminos(tri):
    """Cada camino es una secuencia de pasos: 0 = bajar igual, 1 = bajar a la derecha."""
    n = len(tri)
    for pasos in product((0, 1), repeat=n - 1):
        col, costo = 0, tri[0][0]
        for fila, paso in enumerate(pasos, start=1):
            col += paso
            costo += tri[fila][col]
        yield costo

for tri in [triangle, [[5]], [[1], [9, 2]], [[3], [7, 4], [2, 4, 6], [8, 5, 9, 3]],
            [[1], [2, 3], [4, 5, 6], [7, 8, 9, 10], [1, 1, 1, 1, 1]]]:
    por_enumeracion = min(todos_los_caminos(tri))
    print(f"{find_minimum(0, 0, tri)} == {por_enumeracion}",
          find_minimum(0, 0, tri) == por_enumeracion)''', None, ["11 == 11 True"])],
     "Es el `find_minimum` de la unidad 31, copiado tal cual. En las pruebas, el costo mínimo del triángulo del PDF "
     "es 11 (camino 2, 3, 5, 1). Para no fiarse solo de la función, el complemento enumera todos los caminos y "
     "comprueba que el mínimo coincide en cada triángulo probado."),

    ("Actividad 3 — Búsqueda binaria con iteración",
     "Replique el código mostrado en la unidad 31. Analice el código replicado y agregue una explicación sobre su "
     "funcionamiento. Explique por qué es necesario usar una función recursiva. Haga diferentes pruebas cambiando "
     "la entrada.",
     f"**Dónde se ve:** {unidad(31)} (`bin_search` con iteración y `bin_search2` recursiva).\n\n"
     "**Nota sobre el enunciado:** el título dice \"con iteración\", pero la instrucción pide explicar \"por qué es "
     "necesario usar una función recursiva\". Es una contradicción: la unidad 31 muestra **las dos versiones**, y "
     "la recursión **no es estrictamente necesaria**; la búsqueda binaria se resuelve igual con un bucle `while`. La "
     "versión recursiva refleja mejor el esquema divide y vencerás (cada llamada trabaja con la mitad del rango), "
     "y por eso la unidad la presenta así. Se entregan ambas y se explica esta diferencia.",
     [("Respuesta", '''# Código de la unidad 31: versión con iteración
def bin_search(nums, x):
    low, high = 0, len(nums) - 1
    while low <= high:
        mid = (low + high) // 2           # posición central del rango
        if nums[mid] == x:
            return mid                    # encontrado
        elif nums[mid] > x:
            high = mid - 1                # descartar la mitad derecha
        else:
            low = mid + 1                 # descartar la mitad izquierda
    return -1                             # el rango quedó vacío: no está


# Código de la unidad 31: versión recursiva (divide y vencerás)
def bin_search2(nums, x, low, high):
    if low > high:                        # caso base: rango vacío
        return -1
    else:
        mid = (low + high) // 2
        if nums[mid] == x:
            return mid
        elif nums[mid] > x:
            return bin_search2(nums, x, low, mid - 1)     # buscar en la mitad izquierda
        else:
            return bin_search2(nums, x, mid + 1, high)    # buscar en la mitad derecha


# Funcionamiento: la lista debe estar ORDENADA. Se compara x con el elemento central: si es igual,
# se terminó; si el central es mayor que x, x solo puede estar a la izquierda; si es menor, a la
# derecha. En cada paso se descarta la mitad del rango, por eso hace O(log n) comparaciones.
#
# ¿Por qué una función recursiva? No es obligatorio: la versión iterativa hace lo mismo con un
# bucle. La recursiva expresa directamente la idea de divide y vencerás: el problema (buscar en
# [low, high]) se reduce a un problema idéntico más pequeño (buscar en la mitad), con un caso base
# (rango vacío). La iterativa ahorra la pila de llamadas, pero el razonamiento es el mismo.

S = [11, 17, 26, 28, 37, 45, 53, 59, 77]
print(bin_search(S, 26), bin_search2(S, 26, 0, len(S) - 1))     # 2 2
print(bin_search(S, 30), bin_search2(S, 30, 0, len(S) - 1))     # -1 -1

# Diferentes pruebas cambiando la entrada
for lista, x in [(S, 11), (S, 77), (S, 45), ([5], 5), ([5], 9), ([], 3), ([1, 3, 5, 7], 4)]:
    a = bin_search(lista, x)
    b = bin_search2(lista, x, 0, len(lista) - 1)
    print(f"lista {lista}, buscar {x}: iterativa {a}, recursiva {b}", "(coinciden)" if a == b else "(DIFIEREN)")''',
       None, ["2 2", "-1 -1", "lista [], buscar 3: iterativa -1, recursiva -1 (coinciden)"]),
      ("Complemento (no es necesario entregarlo): comprobación exhaustiva", '''# Complemento: se comprueban las dos versiones con todos los valores posibles de una lista.
S = [11, 17, 26, 28, 37, 45, 53, 59, 77]
correcto = True
for x in range(0, 90):
    esperado = S.index(x) if x in S else -1
    if bin_search(S, x) != esperado or bin_search2(S, x, 0, len(S) - 1) != esperado:
        correcto = False
print("Las dos versiones aciertan con todos los valores de 0 a 89:", correcto)''',
       None, ["valores de 0 a 89: True"])],
     "Se copian las dos versiones de la unidad 31 y se prueban con listas distintas (incluida la vacía y la de un "
     "elemento). La respuesta a \"por qué recursiva\" es que **no es necesaria**: sirve para expresar el esquema "
     "divide y vencerás; la versión con `while` es equivalente y evita la pila de llamadas."),

    ("Actividad 4 — Programación dinámica frente a divide y vencerás",
     "Comparación entre programación dinámica y la metodología divide y vencerás. Enumere las diferencias entre los "
     "dos enfoques. Nombre algunos casos donde funciona mejor la programación dinámica. Nombre ejemplos donde es "
     "suficiente usar el enfoque divide y vencerás.",
     f"**Dónde se ve:** {unidad(31)} (divide y vencerás) y {unidad(32)} (programación dinámica).\n\n"
     "**Clave:** la diferencia central es si los subproblemas **se repiten**. Si son independientes, divide y "
     "vencerás basta; si se solapan, conviene guardar los resultados (programación dinámica).\n\n"
     "**Para redactar a tu manera:** el texto de las diferencias y los ejemplos es una respuesta modelo. Escríbelo "
     "con tus propias palabras antes de entregar.",
     [("Respuesta", '''# Diferencias entre programación dinámica (PD) y divide y vencerás (DyV)
#
# 1. Subproblemas: en DyV son independientes (cada mitad se resuelve por separado y sin repetirse).
#    En PD se superponen: el mismo subproblema aparece muchas veces.
# 2. Memoria: DyV no guarda resultados de subproblemas. PD sí los guarda (tabla, lista o diccionario)
#    para calcular cada subproblema una sola vez (memorización o tabulación).
# 3. Dirección: DyV es de arriba hacia abajo (recursivo). PD puede ir de arriba hacia abajo con
#    memorización, o de abajo hacia arriba llenando una tabla.
# 4. Combinación: en DyV se combinan las soluciones de las partes (mezclar, sumar...). En PD se
#    construye la solución a partir de subproblemas más chicos ya resueltos (subestructura óptima).
# 5. Costo: sin memoria, un problema con subproblemas repetidos crece de forma exponencial; con PD
#    pasa a ser polinómico. En DyV, repetir no es un problema porque no hay repetición.
#
# Casos donde funciona mejor la PD: sucesión de Fibonacci, coeficiente binomial (triángulo de
# Pascal), camino mínimo en el triángulo o en una cuadrícula, cambio de monedas con el mínimo de
# monedas, problema de la mochila, subsecuencia común más larga, distancia de edición.
#
# Casos donde basta DyV: búsqueda binaria, merge sort, quick sort, suma o máximo de una lista por
# mitades, potencia por exponenciación rápida, cubrir un tablero con trominós.

# Demostración: cuántos subproblemas se repiten en cada enfoque
llamadas = []

def fib1(n):                       # recursión simple, como en la unidad 32
    llamadas.append(n)
    if n == 0 or n == 1:
        return n
    return fib1(n - 1) + fib1(n - 2)

llamadas_dp = []
F = {0: 0, 1: 1}

def fib2(n):                       # con memorización (programación dinámica)
    llamadas_dp.append(n)
    if n in F:
        return F[n]
    F[n] = fib2(n - 1) + fib2(n - 2)
    return F[n]

fib1(20)
fib2(20)
print(f"fib1(20): {len(llamadas)} llamadas, solo {len(set(llamadas))} subproblemas distintos")
print(f"fib2(20): {len(llamadas_dp)} llamadas, solo {len(set(llamadas_dp))} subproblemas distintos")

rangos = []

def merge_sort_rangos(lista, bajo, alto):
    """Divide y vencerás: registra qué rango resuelve cada llamada."""
    rangos.append((bajo, alto))
    if bajo == alto:
        return [lista[bajo]]
    medio = (bajo + alto) // 2
    izq = merge_sort_rangos(lista, bajo, medio)
    der = merge_sort_rangos(lista, medio + 1, alto)
    resultado, i, j = [], 0, 0
    while i < len(izq) and j < len(der):
        if izq[i] <= der[j]:
            resultado.append(izq[i]); i += 1
        else:
            resultado.append(der[j]); j += 1
    return resultado + izq[i:] + der[j:]

datos = [27, 10, 12, 20, 25, 13, 15, 22, 3, 8, 30, 1, 9, 16, 4, 6]
print(merge_sort_rangos(datos, 0, len(datos) - 1))
print(f"merge sort de 16 datos: {len(rangos)} llamadas, {len(set(rangos))} subproblemas distintos "
      "(ninguno se repite)")''', None,
       ["fib1(20): 21891 llamadas, solo 21 subproblemas distintos",
        "fib2(20): 39 llamadas, solo 21 subproblemas distintos",
        "merge sort de 16 datos: 31 llamadas, 31 subproblemas distintos"]),
      ("Complemento (no es necesario entregarlo): el triángulo de la unidad 31 con y sin memoria", '''# Complemento: el mismo problema del triángulo, con DyV simple y con programación dinámica
# (find_minimum_memo es la versión con memorización de la unidad 31).
llamadas_tri = 0

def find_minimum_contando(row, col, triangle):
    global llamadas_tri
    llamadas_tri += 1
    if row == len(triangle):
        return 0
    minimum = min(find_minimum_contando(row + 1, col, triangle),
                  find_minimum_contando(row + 1, col + 1, triangle))
    return triangle[row][col] + minimum

def find_minimum_memo_contando(triangle):
    memo = {}
    def C(row, col):
        if row == len(triangle):
            return 0
        if (row, col) not in memo:
            memo[(row, col)] = triangle[row][col] + min(C(row + 1, col), C(row + 1, col + 1))
        return memo[(row, col)]
    return C(0, 0), len(memo)

triangulo = [[1] * (fila + 1) for fila in range(15)]
resultado = find_minimum_contando(0, 0, triangulo)
memo_resultado, calculados = find_minimum_memo_contando(triangulo)
print(f"Triángulo de 15 filas: costo {resultado} == {memo_resultado}")
print(f"Sin memoria: {llamadas_tri} llamadas. Con memoria: {calculados} subproblemas calculados.")''',
       None, ["Triángulo de 15 filas: costo 15 == 15", "Sin memoria: 65535 llamadas. Con memoria: 120 subproblemas calculados."])],
     "La demostración lo hace visible: `fib1(20)` hace 21 891 llamadas pero solo hay 21 subproblemas distintos (se "
     "repite casi todo), mientras que el merge sort hace 31 llamadas y cada una resuelve un rango distinto. Donde "
     "hay repetición conviene guardar resultados; donde no, divide y vencerás es suficiente.\n\n"
     "**Nota sobre el enunciado:** el encabezado de la plataforma dice \"Capítulo 6. Algoritmos de clasificación\", "
     "pero el capítulo del PDF es \"Algorithm 3 – Problem Solving with Algorithms\" (resolución de problemas con "
     "algoritmos), que es lo que tratan las unidades 30 a 33."),
]


def ejecutar(bloques):
    """Ejecuta los bloques de una actividad (comparten espacio de nombres); devuelve la salida de cada uno."""
    previo = os.getcwd()
    original = builtins.input
    salidas = []
    ns = {"__name__": "__main__"}
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
                    exec(compile(codigo, "<respuesta>", "exec"), ns)
                salidas.append(buffer.getvalue())
        finally:
            builtins.input = original
            os.chdir(previo)
    return salidas


celdas = [new_markdown_cell(
    "# Actividad asincrónica — Semana 5\n\n"
    "**Capítulo 6: resolución de problemas con algoritmos** (unidades 30 a 33)\n\n"
    "[Índice de la semana](semana-05.ipynb)\n\n"
    f"## Estado\n\n{ESTADO}\n\n"
    "## Cómo se califica\n\n"
    "- 3 preguntas: la primera y la segunda valen 30 puntos y la tercera 40 (100). No tiene pregunta adicional. "
    "La nota máxima es 100.\n"
    "- Al entregar, la plataforma la califica pregunta por pregunta y muestra cuánto sacaste en cada una.\n"
    "- Se puede corregir cualquier pregunta y volver a entregar hasta que el docente la revise: pulsar «Corregir "
    "mi entrega», cambiar lo necesario y entregar de nuevo; la nota que cuenta es la de la última entrega. Cuando "
    "el docente la revisa ya no se puede modificar, salvo que habilite otro intento.\n\n"
    "**Nota sobre el enunciado:** el texto de calificación habla de 3 preguntas, pero la página muestra **4 "
    "actividades** (\"0 de 4 respondidas\"). Se responden las 4: conviene entregarlas todas.\n\n"
    "## Cómo usar este notebook\n\n"
    "Cada actividad trae la consigna, la unidad donde se explica, la **respuesta resuelta** (ya ejecutada, con su "
    "salida) y una explicación. Para entregar, copia el código de la respuesta en el recuadro de la plataforma y "
    "pulsa «Ejecutar». Los bloques marcados como **Complemento** son opcionales y no hace falta entregarlos. Los "
    "textos de las actividades 1 y 4 son respuestas modelo: redáctalos a tu manera.\n\n"
    "## Checklist de entrega\n\n" + "\n".join(f"- [{MARCA}] {a[0]}" for a in ACTIVIDADES)
    + f"\n- [{MARCA}] Revisar todo y pulsar «Entregar»"
)]

numero = 0
for titulo, consigna, guia, bloques, explicacion in ACTIVIDADES:
    salidas = ejecutar([(codigo, entradas) for _, codigo, entradas, _ in bloques])
    celdas.append(new_markdown_cell(f"## {titulo}\n\n### Consigna\n\n{consigna}\n\n### Guía\n\n{guia}"))
    for (etiqueta, codigo, _, esperados), salida in zip(bloques, salidas):
        for texto in esperados:
            assert texto in salida, f"{titulo} / {etiqueta}: falta {texto!r} en la salida:\n{salida}"
        print(f"--- {titulo} / {etiqueta}\n{salida.rstrip()[-900:]}")
        numero += 1
        celdas.append(new_markdown_cell(f"### {etiqueta}"))
        celdas.append(new_code_cell(codigo, execution_count=numero,
                                    outputs=[new_output("stream", name="stdout", text=salida)]))
    celdas.append(new_markdown_cell("**Explicación:** " + explicacion))

celdas.append(new_markdown_cell("[Índice de la semana](semana-05.ipynb)"))
nb = new_notebook()
nb.cells = celdas
nbformat.validate(nb)
nbformat.write(nb, DESTINO)
print("Escrito:", DESTINO)
