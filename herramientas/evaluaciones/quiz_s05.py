"""Genera 01-python/semana-05/quiz-calificado.ipynb (Quiz 5 de la plataforma) y prueba cada respuesta."""

import builtins
import contextlib
import io
import os
import tempfile
from itertools import permutations
from math import sqrt
from pathlib import Path

import nbformat
from nbformat.v4 import new_code_cell, new_markdown_cell, new_notebook, new_output

RAIZ = Path(__file__).resolve().parents[2]
DESTINO = RAIZ / "01-python/semana-05/quiz-calificado.ipynb"
S4 = "../semana-04/clase-2-greedy-divide-y-venceras"
C1 = "clase-1-programacion-dinamica-y-backtracking"
U = {
    30: f"{S4}/u30-enfoque-greedy.ipynb",
    31: f"{S4}/u31-divide-y-venceras.ipynb",
    32: f"{C1}/u32-programacion-dinamica.ipynb",
    33: f"{C1}/u33-backtracking.ipynb",
}
ESTADO = "**Entregado. Nota final: 100/100.**"
MARCA = "x"


def unidad(*nums):
    return ", ".join(f"[Unidad {n}]({U[n]})" for n in nums)


PESAR = '''def pesar(pesos, grupo_a, grupo_b):
    """Simula una pesada en la balanza: devuelve 'izquierda', 'derecha' o 'igual'."""
    a = sum(pesos[i] for i in grupo_a)
    b = sum(pesos[i] for i in grupo_b)
    if a > b:
        return "izquierda"
    if b > a:
        return "derecha"
    return "igual"


def buscar_pesada(pesos, candidatas=None):
    """Devuelve (indice de la moneda pesada, numero de pesadas usadas)."""
    if candidatas is None:
        candidatas = list(range(len(pesos)))
    if len(candidatas) == 1:
        return candidatas[0], 0
    tercio = -(-len(candidatas) // 3)            # techo de len/3: se divide en tres grupos
    g1 = candidatas[:tercio]
    g2 = candidatas[tercio:2 * tercio]
    g3 = candidatas[2 * tercio:]
    resultado = pesar(pesos, g1, g2)             # una pesada: grupo 1 contra grupo 2
    if resultado == "izquierda":
        moneda, usadas = buscar_pesada(pesos, g1)    # el lado que baja tiene la pesada
    elif resultado == "derecha":
        moneda, usadas = buscar_pesada(pesos, g2)
    else:
        moneda, usadas = buscar_pesada(pesos, g3)    # equilibrio: está en el grupo que no se pesó
    return moneda, usadas + 1

'''

CODIGO_Q33 = '''from math import sqrt, floor
import time


def is_square_digitsum(n):
    S = 0
    while n > 0:
        S += n % 10          # errata del enunciado: la variable se llama S, no s
        n //= 10             # errata del enunciado: el operador es //=, sin espacio
    if sqrt(S) == int(sqrt(S)):
        return True
    return False


def find_all_squares():
    sqrs = [[] for _ in range(5)]
    for i in range(1, floor(sqrt(10 ** 5)) + 1):
        n = i * i
        if not is_square_digitsum(n):
            continue
        s = str(n)
        if len(s) == 3 and s[1] != s[2]:
            continue
        if len(s) == 5 and s[2] != s[3]:
            continue
        if len(s) in [4, 5] and len(set(s)) != 4:
            continue
        sqrs[len(s) - 1].append(n)
    return sqrs


def promising(s, n, dic):
    for i in range(len(s)):
        digit = int(str(n)[i])
        for key, value in dic.items():
            if key == s[i] and value != digit:
                return False
            if value == digit and key != s[i]:
                return False
    return True


def solve(words, dic, squares):
    global solved
    if (len(words) == 0):
        solved = dic
    else:
        s = words[0]
        candidates = squares[len(s) - 1]
        for n in candidates:
            if promising(s, n, dic):
                newdic = dic.copy()
                for i in range(len(s)):
                    newdic[s[i]] = int(str(n)[i])
                solve(words[1:], newdic, squares)


def main():
    squares = find_all_squares()
    words = ['A', 'TO', 'ALL', 'XMAS', 'MERRY']
    dic = {}
    solve(words, dic, squares)
    for word in words:
        print(word, end=": ")
        for c in word:
            print(solved[c], end="")
        print()


start = time.time()
solved = {}
main()
end = time.time()
print("Elapsed Time:", end - start, "seconds")'''


def fuerza_bruta_q33():
    """Comprobación independiente: las 10! asignaciones de dígitos distintos a las 10 letras."""
    letras = "AMERYXSTOL"
    palabras = ["A", "TO", "ALL", "XMAS", "MERRY"]

    def cuadrado(n):
        return int(sqrt(n)) ** 2 == n

    soluciones = []
    for p in permutations(range(10)):
        d = dict(zip(letras, p))
        if any(d[w[0]] == 0 for w in palabras):
            continue
        valores = [int("".join(str(d[c]) for c in w)) for w in palabras]
        if all(cuadrado(v) and cuadrado(sum(map(int, str(v)))) for v in valores):
            soluciones.append(d)
    return soluciones


# (titulo, consigna, unidades, [(etiqueta, codigo, entradas, esperados)], explicacion)
PREGUNTAS = [
    ("Q 30-01 (20 puntos)",
     "Este es el problema del intercambio de monedas. Tienes una moneda de 400 wones. Escriba el resultado de cómo "
     "el algoritmo `coin_change()` determina el cambio de la moneda de 800 wones.\n\n"
     "```python\ncoins  = [500, 400, 100, 50, 10]\namount = int(input(\"Ingrese la cantidad: \"))\n"
     "changes= coin_change(coins, amount)\nprint(changes, len(changes))\n```\n\n"
     "```text\nIngrese la cantidad: 800\n```",
     unidad(30),
     [("Respuesta", '''# coin_change del curso (unidad 30): las monedas van de mayor a menor
def coin_change(coins, amount):
    changes = []
    largest = 0
    while amount > 0:
        if amount < coins[largest]:
            largest += 1
        else:
            changes.append(coins[largest])
            amount -= coins[largest]
    return changes


coins = [500, 400, 100, 50, 10]
texto = input("Ingrese la cantidad: ")
amount = int(texto) if texto and texto.strip().isdigit() else 800    # 800 si se cancela
changes = coin_change(coins, amount)
print(changes, len(changes))''', ["800"], ["[500, 100, 100, 100] 4"]),
      ("Complemento (no es necesario entregarlo): ¿era el mínimo?", '''# Complemento: el mínimo real de monedas para 800 con programación dinámica (unidad 32)
def minimo_monedas(monedas, importe):
    mejor = [None] * (importe + 1)
    mejor[0] = []
    for x in range(1, importe + 1):
        for moneda in monedas:
            if moneda <= x and mejor[x - moneda] is not None:
                candidata = mejor[x - moneda] + [moneda]
                if mejor[x] is None or len(candidata) < len(mejor[x]):
                    mejor[x] = candidata
    return mejor[importe]

print("Greedy:", coin_change(coins, 800), "-> 4 monedas")
print("Mínimo:", sorted(minimo_monedas(coins, 800), reverse=True), "-> 2 monedas")''', None,
       ["Mínimo: [400, 400] -> 2 monedas"])],
     "**Respuesta: `[500, 100, 100, 100] 4`.**\n\n"
     "Paso a paso: 800 ≥ 500, se toma 500 y quedan 300. Como 300 < 500, se pasa a 400; 300 < 400, se pasa a 100. "
     "Ahora se toma 100 tres veces (300 → 200 → 100 → 0). Resultado: cuatro monedas, `[500, 100, 100, 100]`.\n\n"
     "El resultado **no es el óptimo**: con la moneda de 400 bastaban dos monedas (400 + 400). El Greedy se "
     "queda con la moneda más grande que cabe (500) y no la corrige, igual que con `[11, 5, 1]` y el 15. Además, "
     "la función necesita monedas ordenadas de mayor a menor. La respuesta usa 800 si se cancela la ventana de "
     "`input()`."),

    ("Q 31-01 (20 puntos)",
     "Tienes 8 monedas idénticas numeradas del 1 al 8. De estas, solo una moneda es más pesada que la otra. "
     "Suponiendo que puede pesar monedas con una balanza equilibrada, diseñe un algoritmo que encuentre la moneda "
     "más pesada. En este momento, ¿cuántas veces se debe usar al menos la balanza?",
     unidad(31),
     [("Respuesta", PESAR + '''# Se prueba con cada una de las 8 monedas como la pesada (la numeración va de 1 a 8)
peor = 0
for pesada in range(8):
    pesos = [1] * 8
    pesos[pesada] = 2                            # la moneda pesada pesa más
    moneda, usadas = buscar_pesada(pesos)
    assert moneda == pesada
    peor = max(peor, usadas)
    print(f"Moneda pesada: {pesada + 1} -> encontrada: {moneda + 1}, pesadas usadas: {usadas}")
print("Máximo de pesadas necesarias con 8 monedas:", peor)''', None,
       ["Moneda pesada: 8 -> encontrada: 8, pesadas usadas: 2", "Máximo de pesadas necesarias con 8 monedas: 2"])],
     "**Respuesta: 2 veces.**\n\n"
     "**Algoritmo (3-3-2):**\n\n"
     "1. Se separan las monedas en tres grupos: {1, 2, 3}, {4, 5, 6} y {7, 8}. Primera pesada: {1, 2, 3} contra "
     "{4, 5, 6}.\n"
     "2. Si un lado baja, la pesada está en ese grupo de 3: segunda pesada, una moneda contra otra de ese grupo. "
     "Si una baja, es la pesada; si quedan equilibradas, es la tercera.\n"
     "3. Si la balanza queda equilibrada, la pesada está en {7, 8}: segunda pesada, 7 contra 8.\n\n"
     "**Por qué no basta con 1:** cada pesada tiene solo 3 resultados posibles (izquierda, derecha, igual), así que "
     "con 1 pesada se distinguen como máximo 3 monedas; con 8 no alcanza. Con 2 pesadas se distinguen 3² = 9 ≥ 8. "
     "El mínimo es ⌈log₃ 8⌉ = **2**. La simulación comprueba las 8 posibilidades: ninguna necesita más de 2 pesadas."),

    ("Q 31-02 (20 puntos)",
     "Hay nueve monedas idénticas numeradas del 1 al 9 en el problema anterior. Diseñe un algoritmo para encontrar "
     "una moneda pesada en este caso. En este momento, ¿cuántas veces se debe usar al menos la balanza?",
     unidad(31),
     [("Respuesta", PESAR + '''# Se prueba con cada una de las 9 monedas como la pesada (la numeración va de 1 a 9)
peor = 0
for pesada in range(9):
    pesos = [1] * 9
    pesos[pesada] = 2
    moneda, usadas = buscar_pesada(pesos)
    assert moneda == pesada
    peor = max(peor, usadas)
    print(f"Moneda pesada: {pesada + 1} -> encontrada: {moneda + 1}, pesadas usadas: {usadas}")
print("Máximo de pesadas necesarias con 9 monedas:", peor)''', None,
       ["Moneda pesada: 9 -> encontrada: 9, pesadas usadas: 2", "Máximo de pesadas necesarias con 9 monedas: 2"]),
      ("Complemento (no es necesario entregarlo): el mínimo es ⌈log₃ n⌉", '''# Complemento: el mínimo de pesadas coincide con el techo de log base 3 de n
for n in range(2, 28):
    k = 0
    while 3 ** k < n:          # menor k con 3^k >= n, es decir, el techo de log3(n)
        k += 1
    peor = 0
    for pesada in range(n):
        pesos = [1] * n
        pesos[pesada] = 2
        moneda, usadas = buscar_pesada(pesos)
        assert moneda == pesada
        peor = max(peor, usadas)
    assert peor == k, (n, peor, k)
print("Para n de 2 a 27, el peor caso del algoritmo es exactamente el techo de log3(n)")
print("n = 3 -> 1 pesada, n = 9 -> 2 pesadas, n = 27 -> 3 pesadas")''', None,
       ["exactamente el techo de log3(n)"])],
     "**Respuesta: 2 veces.**\n\n"
     "**Algoritmo (3-3-3):**\n\n"
     "1. Se separan las 9 monedas en tres grupos iguales: {1, 2, 3}, {4, 5, 6} y {7, 8, 9}. Primera pesada: "
     "{1, 2, 3} contra {4, 5, 6}.\n"
     "2. Si un lado baja, la pesada está en ese grupo; si hay equilibrio, está en {7, 8, 9}.\n"
     "3. Segunda pesada dentro del grupo de 3: una moneda contra otra. Si una baja, es la pesada; si hay "
     "equilibrio, es la tercera.\n\n"
     "Con 9 monedas el reparto es perfecto: 3² = 9, así que 2 pesadas son suficientes y también necesarias "
     "(⌈log₃ 9⌉ = **2**). En general, con n monedas hacen falta ⌈log₃ n⌉ pesadas, porque cada pesada triplica lo "
     "que se puede distinguir; el complemento lo comprueba para n de 2 a 27."),

    ("Q 32-01 (20 puntos)",
     "Analice el resultado de la ejecución del siguiente código y compárelo con el rendimiento de las funciones "
     "`fib1()`, `fib2()` y `fib3()`.\n\n"
     "```python\ndef fib4(n):\n    if n <= 1:\n        return n\n    else:\n        a,b = 0,1\n"
     "        for i in range(2, n + 1):\n            a,b = b,a+b\n        return b\n"
     "N = int(input(\"Ingrese un numero: \"))\nprint(fib4(N))\n```",
     unidad(32),
     [("Respuesta", '''def fib4(n):
    if n <= 1:
        return n
    else:
        a, b = 0, 1                     # solo se guardan los dos últimos términos
        for i in range(2, n + 1):
            a, b = b, a + b             # avanza un término por vuelta
        return b


N = int(input("Ingrese un numero: "))
print(fib4(N))

# Ejecución: entrada 8, salida 21.
# La salida corresponde a la entrada: fib4(8) es el término 8 de Fibonacci, contando
# desde F(0) = 0: F(0)..F(8) = 0, 1, 1, 2, 3, 5, 8, 13, 21, y F(8) = 21.
# Es el mismo valor que devuelven fib1(8), fib2(8) y fib3(F, 8); lo que cambia es el
# rendimiento.
#
# Análisis: fib4 calcula los términos de abajo hacia arriba (tabulación) con un bucle.
# Tiempo O(n): una vuelta por término. Memoria O(1): solo dos variables (a, b), sin lista,
# sin diccionario y sin recursión.
#
# Comparación de rendimiento:
# - fib1 (recursión simple): tiempo exponencial, O(2^n), porque recalcula los mismos
#   subproblemas una y otra vez (para n = 25 hace 242 785 llamadas). Memoria: la pila
#   de recursión, de profundidad n.
# - fib2 (memorización con diccionario): tiempo O(n), cada término se calcula una sola
#   vez (49 llamadas para n = 25). Memoria O(n): el diccionario más la pila de recursión.
# - fib3 (memorización con lista): igual que fib2, tiempo O(n) y memoria O(n) (la lista
#   de n + 1 elementos más la pila de recursión).
# - fib4 (bucle): tiempo O(n), como fib2 y fib3, pero memoria O(1), porque cada término
#   solo depende de los dos anteriores. Además, al no usar recursión no tiene el límite
#   de pila: fib2(3000) produce RecursionError y fib4(3000) se calcula sin problema.
# Conclusión: fib4 es la más eficiente de las cuatro.''', ["8"], ["21"]),
      ("Complemento (no es necesario entregarlo): comparación con fib1, fib2 y fib3", '''# Complemento: las funciones de la unidad 32 y cuántas llamadas hace cada una
import time

def fib1(n):                                   # recursión simple
    if n == 0 or n == 1:
        return n
    else:
        return fib1(n - 1) + fib1(n - 2)

F = {0: 0, 1: 1}

def fib2(n):                                   # memorización con diccionario
    if n in F:
        return F[n]
    else:
        F[n] = fib2(n - 1) + fib2(n - 2)
        return F[n]

def fib3(F, n):                                # memorización con lista inicializada en -1
    if n <= 1:
        return F[n]
    else:
        if F[n] < 0:
            F[n] = fib3(F, n - 1) + fib3(F, n - 2)
        return F[n]

def contar(f):
    """Envuelve una función para contar cuántas veces se llama (también las llamadas recursivas)."""
    def envoltura(*args):
        envoltura.llamadas += 1
        return f(*args)
    envoltura.llamadas = 0
    return envoltura

fib1, fib2, fib3 = contar(fib1), contar(fib2), contar(fib3)

n = 25
inicio = time.perf_counter(); r1 = fib1(n); t1 = time.perf_counter() - inicio
F = {0: 0, 1: 1}
inicio = time.perf_counter(); r2 = fib2(n); t2 = time.perf_counter() - inicio
lista = [0, 1] + [-1] * (n - 1)
inicio = time.perf_counter(); r3 = fib3(lista, n); t3 = time.perf_counter() - inicio
inicio = time.perf_counter(); r4 = fib4(n); t4 = time.perf_counter() - inicio

print(f"n = {n}: fib1 = {r1}, fib2 = {r2}, fib3 = {r3}, fib4 = {r4}")
print(f"llamadas: fib1 = {fib1.llamadas}, fib2 = {fib2.llamadas}, fib3 = {fib3.llamadas}, fib4 = 0 (bucle)")
print(f"tiempos (varían en cada ejecución): fib1 {t1:.4f} s, fib2 {t2:.6f} s, fib3 {t3:.6f} s, fib4 {t4:.6f} s")

# fib2 y fib3 usan recursión de profundidad n; con n grande se acaba la pila. fib4 no.
try:
    F = {0: 0, 1: 1}
    fib2(3000)
except RecursionError:
    print("fib2(3000): RecursionError (demasiadas llamadas anidadas)")
print("fib4(3000) tiene", len(str(fib4(3000))), "dígitos y se calcula sin problema")''', None,
       ["n = 25: fib1 = 75025, fib2 = 75025, fib3 = 75025, fib4 = 75025",
        "llamadas: fib1 = 242785, fib2 = 49, fib3 = 49, fib4 = 0 (bucle)",
        "fib2(3000): RecursionError", "fib4(3000) tiene 627 dígitos"])],
     "**El resultado de `fib4(N)` es el término N de Fibonacci** (con la entrada `8` imprime `21`), igual que fib1, fib2 y "
     "fib3. Lo que cambia es el rendimiento:\n\n"
     "| Función | Técnica | Tiempo | Memoria | Llamadas para n = 25 |\n|---|---|---|---|---|\n"
     "| `fib1` | recursión simple | exponencial, O(2ⁿ) | pila de n llamadas | 242 785 |\n"
     "| `fib2` | memorización (diccionario) | O(n) | O(n) más pila | 49 |\n"
     "| `fib3` | memorización (lista) | O(n) | O(n) más pila | 49 |\n"
     "| `fib4` | tabulación (bucle) | O(n) | **O(1)** | ninguna |\n\n"
     "`fib1` repite subproblemas (calcula una y otra vez los mismos términos); `fib2` y `fib3` los guardan y los "
     "calculan una sola vez; `fib4` ni siquiera necesita guardarlos todos, porque cada término solo depende de los "
     "dos anteriores. Por eso es la más eficiente y la única sin límite de recursión. Los tiempos del complemento "
     "dependen de la máquina; las llamadas y los resultados no."),

    ("Q 32-02 (20 puntos)",
     "Analice el resultado de la ejecución del siguiente código y compárelo con el rendimiento de las funciones "
     "`bin1()` y `bin2()`.\n\n"
     "```python\ndef bin3(n,k):\n    B = [0] * (n + 1)\n    for i in range(n + 1):\n"
     "        for j in range(n, -1, -1):\n            if j==0 or j==i:\n                B[j] = 1\n"
     "            else:\n                B[j] = B[j] B[j-1]\n    return B[k]\n"
     "for i in range(10):\n    for j in range(i+1):\n        print(bin3(i,j),end=\" \")\n    print()\n```\n\n"
     "**Nota sobre el enunciado:** en la línea `B[j] = B[j] B[j-1]` falta el operador. La versión correcta, por la "
     "recurrencia del coeficiente binomial, es `B[j] = B[j] + B[j-1]`.",
     unidad(32),
     [("Respuesta", '''def bin3(n, k):
    B = [0] * (n + 1)                       # una sola fila de n + 1 elementos
    for i in range(n + 1):
        for j in range(n, -1, -1):          # de derecha a izquierda: B[j-1] aún es de la fila anterior
            if j == 0 or j == i:
                B[j] = 1
            else:
                B[j] = B[j] + B[j - 1]      # errata corregida: faltaba el signo +
    return B[k]


for i in range(10):
    for j in range(i + 1):
        print(bin3(i, j), end=" ")
    print()

# Resultado: imprime el triángulo de Pascal de 10 filas; la fila i contiene los
# coeficientes binomiales C(i, 0), ..., C(i, i). Da los mismos valores que bin1 y bin2.
#
# Análisis: bin3 aplica la recurrencia C(i, j) = C(i-1, j-1) + C(i-1, j) de abajo hacia
# arriba, reutilizando una sola fila B. Recorre j de derecha a izquierda para que B[j-1]
# todavía tenga el valor de la fila anterior cuando se calcula B[j].
# Tiempo O(n^2): dos bucles anidados de n + 1 vueltas. Memoria O(n): n + 1 elementos.
#
# Comparación de rendimiento:
# - bin1 (recursión simple): tiempo exponencial, porque recalcula los mismos
#   subproblemas (hasta 2 * C(n, k) - 1 llamadas; bin1(9, 4) hace 251). Memoria: la pila
#   de recursión, de profundidad n.
# - bin2 (tabla bidimensional): tiempo O(n^2), cada C(i, j) se calcula una sola vez.
#   Memoria O(n^2): guarda todo el triángulo, (n + 1)(n + 2) / 2 celdas (55 para n = 9).
# - bin3 (una sola fila): tiempo O(n^2), igual que bin2, pero memoria O(n), porque cada
#   fila solo depende de la anterior (10 celdas para n = 9 frente a las 55 de bin2).
# Conclusión: bin3 es tan rápida como bin2 y usa mucha menos memoria; las dos son mucho
# más eficientes que bin1.''', None, ["1 9 36 84 126 126 84 36 9 1 "]),
      ("Complemento (no es necesario entregarlo): comprobación y comparación con bin1 y bin2", '''# Complemento: bin1 y bin2 de la unidad 32, y la comprobación de bin3
from math import comb

def bin1(n, k):
    if k == 0 or n == k:
        return 1
    else:
        return bin1(n - 1, k - 1) + bin1(n - 1, k)

def bin2(n, k):
    B = [[0] * (i + 1) for i in range(n + 1)]
    for i in range(n + 1):
        for j in range(i + 1):
            if j == 0 or j == i:
                B[i][j] = 1
            else:
                B[i][j] = B[i - 1][j - 1] + B[i - 1][j]
    return B[n][k]

todo_igual = all(bin1(i, j) == bin2(i, j) == bin3(i, j) == comb(i, j)
                 for i in range(10) for j in range(i + 1))
print("bin1, bin2 y bin3 coinciden con math.comb para todo 0 <= j <= i < 10:", todo_igual)

contador = 0
def bin1_contando(n, k):
    global contador
    contador += 1
    if k == 0 or n == k:
        return 1
    return bin1_contando(n - 1, k - 1) + bin1_contando(n - 1, k)

bin1_contando(9, 4)
print("bin1(9, 4): llamadas =", contador, "(2 * C(9, 4) - 1 =", 2 * comb(9, 4) - 1, ")")
print("celdas guardadas para n = 9: bin2 =", sum(range(1, 11)), ", bin3 =", 9 + 1)

# Por qué j va de derecha a izquierda: con el orden normal se pisa B[j-1] antes de usarlo
def bin3_al_reves(n, k):
    B = [0] * (n + 1)
    for i in range(n + 1):
        for j in range(n + 1):
            if j == 0 or j == i:
                B[j] = 1
            else:
                B[j] = B[j] + B[j - 1]
    return B[k]

print("bin3 con j de izquierda a derecha, bin3_al_reves(5, 3) =", bin3_al_reves(5, 3), "(debía ser 10)")''', None,
       ["math.comb para todo 0 <= j <= i < 10: True", "bin1(9, 4): llamadas = 251 (2 * C(9, 4) - 1 = 251 )",
        "celdas guardadas para n = 9: bin2 = 55 , bin3 = 10", "bin3_al_reves(5, 3) = 22 (debía ser 10)"])],
     "**Resultado:** el código imprime el **triángulo de Pascal** de 10 filas (el valor de cada fila `i` son los "
     "coeficientes binomiales C(i, j)):\n\n"
     "```text\n1\n1 1\n1 2 1\n1 3 3 1\n1 4 6 4 1\n1 5 10 10 5 1\n1 6 15 20 15 6 1\n1 7 21 35 35 21 7 1\n"
     "1 8 28 56 70 56 28 8 1\n1 9 36 84 126 126 84 36 9 1\n```\n\n"
     "**Comparación:**\n\n"
     "| Función | Técnica | Tiempo | Memoria |\n|---|---|---|---|\n"
     "| `bin1` | recursión simple | exponencial (hasta 2·C(n, k) − 1 llamadas) | pila de n llamadas |\n"
     "| `bin2` | tabla bidimensional (tabulación) | O(n²) | O(n²): (n + 1)(n + 2)/2 celdas |\n"
     "| `bin3` | una sola fila reutilizada | O(n²) | **O(n)**: n + 1 elementos |\n\n"
     "`bin3` conserva la rapidez de `bin2` pero guarda solo una fila: como cada fila depende únicamente de la "
     "anterior, se sobrescribe la misma lista. Funciona porque `j` recorre de **derecha a izquierda**: al calcular "
     "`B[j]`, `B[j-1]` todavía contiene el valor de la fila anterior (con el orden contrario daría resultados "
     "erróneos, como muestra el complemento).\n\n"
     "**Comprobación:** se verificó contra `math.comb` para todo `0 ≤ j ≤ i < 10` y coincide. Las posiciones con "
     "`j > i` guardan valores sin significado en cada vuelta, pero no afectan a los valores válidos, porque estos "
     "solo leen `B[j]` y `B[j-1]` con `j ≤ i`. Esas posiciones sobrantes hacen que `bin3` recorra n + 1 columnas "
     "por fila en lugar de i + 1: trabajo extra que no cambia el orden O(n²)."),

    ("Q 33-01 (Extra Point, hasta 20 puntos)",
     "Si reemplaza cada letra con un número en la siguiente letra, el número correspondiente a las cinco palabras "
     "son todos cuadrados. Para cada palabra, la suma de cada dígito también es un número cuadrado. Encuentra el "
     "número representado por cada letra.\n\n"
     "```text\nA   MERRY   XMAS   TO   ALL\n```\n\n"
     "Código de referencia de la plataforma (con sus erratas: `S` en lugar de `s` y `n // = 10`; las demás "
     "diferencias, como `floor (sqrt(...))` o `words [1:]`, son solo espacios y no afectan):\n\n"
     "```python\nfrom math import sqrt, floor\nimport time\n\ndef is_square_digitsum(n):\n    S = 0\n"
     "    while n > 0:\n        s += n % 10\n        n // = 10\n    if sqrt(s) == int(sqrt(s)):\n"
     "        return True\n    return False\n...\n```",
     unidad(33),
     [("Respuesta (código corregido)", CODIGO_Q33, None,
       ["A: 9\n", "TO: 81\n", "ALL: 900\n", "XMAS: 7396\n", "MERRY: 34225\n", "Elapsed Time:"]),
      ("Complemento (no es necesario entregarlo): comprobar las restricciones y que la solución es única", '''# Complemento: se recorre todo el retroceso reuniendo todas las soluciones, y se comprueban las reglas
soluciones = []

def solve_todas(words, dic, squares):
    if len(words) == 0:
        soluciones.append(dic)
    else:
        s = words[0]
        for n in squares[len(s) - 1]:
            if promising(s, n, dic):
                newdic = dic.copy()
                for i in range(len(s)):
                    newdic[s[i]] = int(str(n)[i])
                solve_todas(words[1:], newdic, squares)

palabras = ['A', 'TO', 'ALL', 'XMAS', 'MERRY']
solve_todas(palabras, {}, find_all_squares())
print("Soluciones encontradas:", len(soluciones))

letras = soluciones[0]
print("Valor de cada letra:", dict(sorted(letras.items())))
print("Todas las letras tienen un dígito distinto:", len(set(letras.values())) == len(letras))
for palabra in palabras:
    numero = int("".join(str(letras[c]) for c in palabra))
    suma = sum(int(d) for d in str(numero))
    print(f"{palabra} = {numero} = {int(sqrt(numero))}^2; suma de dígitos = {suma} = {int(sqrt(suma))}^2")''', None,
       ["Soluciones encontradas: 1", "Todas las letras tienen un dígito distinto: True",
        "MERRY = 34225 = 185^2; suma de dígitos = 16 = 4^2"])],
     "**Respuesta:** A = 9, M = 3, E = 4, R = 2, Y = 5, X = 7, S = 6, T = 8, O = 1, L = 0. Las cinco palabras "
     "valen:\n\n"
     "| Palabra | Número | Cuadrado de | Suma de dígitos |\n|---|---|---|---|\n"
     "| A | 9 | 3² | 9 = 3² |\n| TO | 81 | 9² | 9 = 3² |\n| ALL | 900 | 30² | 9 = 3² |\n"
     "| XMAS | 7396 | 86² | 25 = 5² |\n| MERRY | 34225 | 185² | 16 = 4² |\n\n"
     "**Cómo funciona (retroceso):** primero se generan los cuadrados perfectos de hasta 5 dígitos cuya suma de "
     "dígitos también es cuadrado, descartando los que no tienen la forma de la palabra (por ejemplo, ALL debe tener "
     "las dos últimas cifras iguales). Luego `solve` va asignando una palabra por vez; `promising` rechaza el "
     "candidato si una letra ya tenía otro dígito o si ese dígito ya lo usa otra letra, y entonces se retrocede y se "
     "prueba el siguiente cuadrado.\n\n"
     "**Unicidad:** la solución es única. Lo confirman dos comprobaciones independientes: el retroceso que reúne "
     "todas las soluciones (complemento) devuelve una sola, y una búsqueda por fuerza bruta sobre las 10! "
     "asignaciones de dígitos distintos a las 10 letras (sin cifras iniciales en 0) también encuentra exactamente "
     "una.\n\n"
     "**Nota sobre el enunciado:** la plataforma muestra 6 preguntas (\"0 de 6 respondidas\") sin marcar cuál es la "
     "adicional. Se trata como **Extra Point la Q 33-01**: es la última, no sigue el patrón de las demás (una por "
     "unidad, 30 a 32) y es la de mayor dificultad, que es lo habitual en una pregunta opcional. Es una deducción: "
     "si la plataforma indica otra, el resto del quiz no cambia. El PDF solo trae el planteamiento del problema "
     "(unidad 33, págs. 77 y 78, con la pista de T = 8 y O = 1); el código con las erratas es el de la plataforma. "
     "El tiempo (`Elapsed Time`) cambia en cada ejecución."),
]


def probar(bloques):
    """Ejecuta los bloques de una pregunta (comparten espacio de nombres) con entradas simuladas."""
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
                salida = io.StringIO()
                with contextlib.redirect_stdout(salida):
                    exec(compile(codigo, "<respuesta>", "exec"), ns)
                salidas.append(salida.getvalue())
        finally:
            builtins.input = original
            os.chdir(previo)
    return salidas


# Comprobación independiente de la Q 33-01 antes de escribir nada
SOL = fuerza_bruta_q33()
assert len(SOL) == 1 and SOL[0] == dict(A=9, M=3, E=4, R=2, Y=5, X=7, S=6, T=8, O=1, L=0), SOL
print("Fuerza bruta Q 33-01:", len(SOL), "solución", SOL[0])

celdas = [new_markdown_cell(
    "# Quiz 5 — Semana 5 (plataforma)\n\n"
    "**Capítulo 6: resolución de problemas con algoritmos** (unidades 30 a 33)\n\n"
    "[Índice de la semana](semana-05.ipynb)\n\n"
    f"## Estado\n\n{ESTADO}\n\n"
    "## Cómo se califica\n\n"
    "- 5 preguntas principales de 20 puntos cada una (100). La pregunta adicional (Extra Point) es opcional: si "
    "sacas menos de 50, suma hasta 20 puntos. La nota máxima es 100.\n"
    "- Al entregar, la plataforma califica pregunta por pregunta y muestra cuánto sacaste en cada una.\n"
    "- Se puede corregir cualquier pregunta y volver a entregar hasta que el docente la revise: pulsar «Corregir "
    "mi entrega», cambiar lo necesario y entregar de nuevo; la nota que cuenta es la de la última entrega. Cuando "
    "el docente la revisa ya no se puede modificar, salvo que habilite otro intento.\n\n"
    "**Nota sobre el enunciado:** la página muestra 6 preguntas (\"0 de 6 respondidas\") y no indica cuál es la "
    "adicional. Aquí se trata como Extra Point la **Q 33-01** (ver su explicación). Conviene entregar las 6.\n\n"
    "## Cómo usar este notebook\n\n"
    "Cada pregunta trae la consigna, la unidad donde se explica, la **respuesta resuelta** (ya ejecutada, con su "
    "salida) y una explicación. La respuesta a escribir está en negrita en la explicación; el código la comprueba. "
    "Los bloques marcados como **Complemento** son opcionales y no hace falta entregarlos. Las preguntas con "
    "`input()` usan un valor por defecto si se cancela la ventana.\n\n"
    "## Checklist de entrega\n\n" + "\n".join(f"- [{MARCA}] {p[0]}" for p in PREGUNTAS)
    + f"\n- [{MARCA}] Revisar todo y pulsar «Entregar»"
)]

numero = 0
for titulo, consigna, unidades, bloques, explicacion in PREGUNTAS:
    salidas = probar([(codigo, entradas) for _, codigo, entradas, _ in bloques])
    celdas.append(new_markdown_cell(f"## {titulo}\n\n### Consigna\n\n{consigna}\n\n**Dónde se ve:** {unidades}"))
    entradas_usadas = []
    for (etiqueta, codigo, entradas, esperados), salida in zip(bloques, salidas):
        for texto in esperados:
            assert texto in salida, f"{titulo} / {etiqueta}: falta {texto!r} en la salida:\n{salida}"
        print(f"--- {titulo} / {etiqueta}\n{salida.rstrip()[-900:]}")
        numero += 1
        celdas += [
            new_markdown_cell("### " + ("Respuesta" if etiqueta.startswith("Respuesta") and "(" not in etiqueta
                                         else etiqueta)),
            new_code_cell(codigo, execution_count=numero,
                          outputs=[new_output("stream", name="stdout", text=salida)]),
        ]
        if entradas:
            entradas_usadas = entradas
    nota = ""
    if entradas_usadas:
        nota = ("\n\nUsa `input()`: la salida de arriba es una prueba respondiendo "
                + ", ".join(f"`{e}`" for e in entradas_usadas)
                + ". En la plataforma se abre una ventana para escribir el dato.")
    celdas.append(new_markdown_cell("**Explicación:** " + explicacion + nota))

celdas.append(new_markdown_cell("[Índice de la semana](semana-05.ipynb)"))
nb = new_notebook()
nb.cells = celdas
nbformat.validate(nb)
nbformat.write(nb, DESTINO)
print("Escrito:", DESTINO)
