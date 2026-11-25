"""Algoritmos de ordenamiento de la semana 4 (unidades 27, 28 y 29) aplicados al proyecto.

Todas las funciones:

- reciben una lista y `clave`, una función que extrae el valor por el que se ordena;
- no modifican la lista original (trabajan sobre una copia);
- devuelven `(lista_ordenada, comparaciones)`, donde `comparaciones` cuenta cada vez que
  se comparan dos claves.

Ordenan de menor a mayor. Para ordenar de mayor a menor se usa una clave negada, por
ejemplo `clave=lambda fila: -fila["pct"]`.
"""
import time


def _identidad(x):
    return x


def burbuja(lista, clave=_identidad):
    """Burbuja (unidad 27) que excluye la parte ya ordenada y se detiene si no hubo intercambios."""
    S = list(lista)
    n = len(S)
    comparaciones = 0
    for i in range(n - 1):
        hubo_intercambio = False
        for j in range(n - 1 - i):
            comparaciones += 1
            if clave(S[j]) > clave(S[j + 1]):
                S[j], S[j + 1] = S[j + 1], S[j]
                hubo_intercambio = True
        if not hubo_intercambio:
            break
    return S, comparaciones


def seleccion(lista, clave=_identidad):
    """Selección (`selectionsort2` de la unidad 27): busca el menor y lo pone en la posición i."""
    S = list(lista)
    n = len(S)
    comparaciones = 0
    for i in range(n - 1):
        smallest = i
        for j in range(i + 1, n):
            comparaciones += 1
            if clave(S[j]) < clave(S[smallest]):
                smallest = j
        S[i], S[smallest] = S[smallest], S[i]
    return S, comparaciones


def insercion(lista, clave=_identidad):
    """Inserción (`insertionsort2` de la unidad 27): desplaza los mayores e inserta x en su lugar."""
    S = list(lista)
    comparaciones = 0
    for i in range(1, len(S)):
        x = S[i]
        j = i - 1
        while j >= 0:
            comparaciones += 1          # se evalúa S[j] > x
            if not clave(S[j]) > clave(x):
                break
            S[j + 1] = S[j]
            j -= 1
        S[j + 1] = x
    return S, comparaciones


def fusion(lista, clave=_identidad):
    """Fusión o merge sort (unidad 28): divide en mitades, ordena cada una y las mezcla."""
    contador = [0]

    def mezclar(a, b):
        resultado = []
        i = j = 0
        while i < len(a) and j < len(b):
            contador[0] += 1
            if clave(a[i]) <= clave(b[j]):
                resultado.append(a[i])
                i += 1
            else:
                resultado.append(b[j])
                j += 1
        resultado.extend(a[i:])
        resultado.extend(b[j:])
        return resultado

    def merge_sort(S):
        if len(S) <= 1:
            return list(S)
        mitad = len(S) // 2
        return mezclar(merge_sort(S[:mitad]), merge_sort(S[mitad:]))

    return merge_sort(list(lista)), contador[0]


def rapido(lista, clave=_identidad):
    """Ordenamiento rápido o quicksort (unidad 29), in situ sobre una copia.

    Usa la partición `partition1` corregida de la unidad 29 (`while left <= right`) con el
    elemento del medio como pivote, para no caer en el peor caso O(n^2) con datos que ya
    vienen casi ordenados.
    """
    S = list(lista)
    contador = [0]

    def partition(low, high):
        medio = (low + high) // 2
        S[low], S[medio] = S[medio], S[low]
        pivot = clave(S[low])
        left, right = low + 1, high
        while left <= right:
            while left <= right:
                contador[0] += 1
                if clave(S[left]) <= pivot:
                    left += 1
                else:
                    break
            while left <= right:
                contador[0] += 1
                if clave(S[right]) >= pivot:
                    right -= 1
                else:
                    break
            if left < right:
                S[left], S[right] = S[right], S[left]
        S[low], S[right] = S[right], S[low]
        return right

    def quicksort(low, high):
        if low < high:
            pivotpoint = partition(low, high)
            quicksort(low, pivotpoint - 1)
            quicksort(pivotpoint + 1, high)

    quicksort(0, len(S) - 1)
    return S, contador[0]


ALGORITMOS = {
    "burbuja": burbuja,
    "selección": seleccion,
    "inserción": insercion,
    "fusión": fusion,
    "rápido": rapido,
}


def medir(funcion, lista, clave=_identidad, repeticiones=3):
    """Ejecuta `funcion(lista, clave)` varias veces.

    Devuelve `(ordenada, comparaciones, mejor_tiempo_en_segundos)`.
    """
    mejor = None
    for _ in range(repeticiones):
        inicio = time.perf_counter()
        ordenada, comparaciones = funcion(lista, clave)
        transcurrido = time.perf_counter() - inicio
        if mejor is None or transcurrido < mejor:
            mejor = transcurrido
    return ordenada, comparaciones, mejor
