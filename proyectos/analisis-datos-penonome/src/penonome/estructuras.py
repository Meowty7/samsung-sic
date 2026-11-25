"""Estructuras de datos de la semana 3 (unidades 22, 23 y 26) aplicadas al proyecto.

Las clases siguen la interfaz de las clases del curso:

- `Pila` es la `Stack` de la unidad 22 (`push`, `pop`, `is_empty`) con `peek` y `size`.
- `Cola` es la `Queue` de la unidad 23 (`enqueue`, `dequeue`, `is_empty`, `size`).
- `TablaHash` es la `HashTable` de la unidad 26 (`hash`, `put`, `get`) con cubos-lista.

Los alias `Stack`, `Queue` y `HashTable` permiten usar los nombres del curso.
"""


class Pila:
    """Pila (LIFO): el último elemento que entra es el primero que sale."""

    def __init__(self):
        self.stack = []

    def is_empty(self):
        return len(self.stack) == 0

    def push(self, item):
        self.stack.append(item)

    def pop(self):
        return None if self.is_empty() else self.stack.pop()

    def peek(self):
        return None if self.is_empty() else self.stack[-1]

    def size(self):
        return len(self.stack)


class Cola:
    """Cola (FIFO): el primer elemento que entra es el primero que sale."""

    def __init__(self):
        self.queue = []

    def is_empty(self):
        return len(self.queue) == 0

    def enqueue(self, item):
        self.queue.append(item)

    def dequeue(self):
        return None if self.is_empty() else self.queue.pop(0)

    def peek(self):
        return None if self.is_empty() else self.queue[0]

    def size(self):
        return len(self.queue)


def clave_ascii(texto):
    """Clave numérica de un texto: la suma de sus códigos ASCII, como en la unidad 26."""
    return sum(map(ord, texto))


class TablaHash:
    """Tabla hash con encadenamiento: cada ranura es una lista (cubo) de pares (clave, valor).

    A diferencia de la `HashTable` del PDF, que guarda solo valores y cuyo `get` devuelve
    el cubo completo, esta versión guarda la clave junto al valor para que `get` pueda
    devolver el valor exacto aunque varias claves compartan cubo.
    """

    def __init__(self, size):
        self.size = size
        self.table = {}
        for i in range(size):
            self.table[i] = []
        self.comparaciones = 0      # comparaciones de claves hechas por get

    def hash(self, key):
        """Posición de la clave: `clave % size`; los textos se convierten antes con `clave_ascii`."""
        if isinstance(key, str):
            key = clave_ascii(key)
        return key % self.size

    def put(self, key, value):
        """Guarda el valor; si la clave ya estaba, reemplaza su valor."""
        bucket = self.table[self.hash(key)]
        for i, (clave, _) in enumerate(bucket):
            if clave == key:
                bucket[i] = (key, value)
                return
        bucket.append((key, value))

    def get(self, key, default=None):
        """Devuelve el valor de la clave o `default` si no está."""
        for clave, valor in self.table[self.hash(key)]:
            self.comparaciones += 1
            if clave == key:
                return valor
        return default

    def bucket(self, key):
        """Cubo completo de la clave, como el `get` del PDF."""
        return self.table[self.hash(key)]

    def __len__(self):
        return sum(len(cubo) for cubo in self.table.values())

    def colisiones(self):
        """Cantidad de cubos que guardan más de una clave."""
        return sum(1 for cubo in self.table.values() if len(cubo) > 1)

    def cubo_mas_largo(self):
        return max(len(cubo) for cubo in self.table.values())


Stack = Pila
Queue = Cola
HashTable = TablaHash
