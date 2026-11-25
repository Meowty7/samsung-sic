"""Búsquedas de la semana 3 (unidades 24 y 25) y su versión recursiva (unidad 31).

Cada función de búsqueda acepta `clave`, una función que extrae de cada elemento el valor
que se compara (por defecto, el elemento mismo). Las versiones `_contando` devuelven
`(posición, comparaciones)` para medir el costo.
"""


def _identidad(x):
    return x


def seq_search(nums, x, clave=_identidad):
    """Búsqueda secuencial (unidad 24): posición de la primera coincidencia o -1."""
    for i in range(len(nums)):
        if x == clave(nums[i]):
            return i
    return -1


def seq_search_contando(nums, x, clave=_identidad):
    """Como `seq_search`, pero devuelve `(posición, comparaciones)`."""
    comparaciones = 0
    for i in range(len(nums)):
        comparaciones += 1
        if x == clave(nums[i]):
            return i, comparaciones
    return -1, comparaciones


def bin_search(nums, x, clave=_identidad):
    """Búsqueda binaria (unidad 25). `nums` debe estar ordenada por `clave` de menor a mayor."""
    low, high = 0, len(nums) - 1
    while low <= high:
        mid = (low + high) // 2
        valor = clave(nums[mid])
        if valor == x:
            return mid
        elif valor > x:
            high = mid - 1
        else:
            low = mid + 1
    return -1


def bin_search_contando(nums, x, clave=_identidad):
    """Como `bin_search`, pero devuelve `(posición, comparaciones)`.

    Se cuenta una comparación por cada elemento del medio que se examina (una vuelta del ciclo).
    """
    comparaciones = 0
    low, high = 0, len(nums) - 1
    while low <= high:
        mid = (low + high) // 2
        valor = clave(nums[mid])
        comparaciones += 1
        if valor == x:
            return mid, comparaciones
        elif valor > x:
            high = mid - 1
        else:
            low = mid + 1
    return -1, comparaciones


def bin_search2(nums, x, low, high, clave=_identidad):
    """Búsqueda binaria recursiva de la unidad 31 (divide y vencerás)."""
    if low > high:
        return -1
    mid = (low + high) // 2
    valor = clave(nums[mid])
    if valor == x:
        return mid
    elif valor > x:
        return bin_search2(nums, x, low, mid - 1, clave)
    else:
        return bin_search2(nums, x, mid + 1, high, clave)


def find_largest(nums, clave=_identidad):
    """Índice del mayor (unidad 24)."""
    largest = 0
    for i in range(1, len(nums)):
        if clave(nums[largest]) < clave(nums[i]):
            largest = i
    return largest


def find_two(nums, clave=_identidad):
    """Índices del mayor y del menor en una sola pasada (unidad 24), con sus comparaciones.

    Devuelve `(indice_mayor, indice_menor, comparaciones)`.
    """
    x = y = 0
    comparaciones = 0
    for i in range(1, len(nums)):
        comparaciones += 1
        if clave(nums[x]) < clave(nums[i]):
            x = i
        else:
            comparaciones += 1
            if clave(nums[y]) > clave(nums[i]):
                y = i
    return x, y, comparaciones
