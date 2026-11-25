"""Genera semana-NN.ipynb, quiz.ipynb y repaso.ipynb de una semana y el glosario acumulado.

Uso (desde la raíz del curso): uv run python herramientas/construir_semana.py 2

Lee los aportes de herramientas/aportes/semana-NN/uXX.md (glosario, quiz, cheatsheet y errores comunes
de cada unidad) y los encabezados de los notebooks de unidad.
"""

import re
import sys
from pathlib import Path

import nbformat
from nbformat.v4 import new_code_cell, new_markdown_cell, new_notebook

sys.path.insert(0, str(Path(__file__).resolve().parent))
from cronograma import archivo_semana  # noqa: E402

RAIZ = Path(__file__).resolve().parent.parent
APORTES = Path(__file__).resolve().parent / "aportes"

SEMANAS = {
    0: {
        "aportes": APORTES / "semana-00",
        "checklist_completo": True,   # el usuario terminó la semana (2026-10-19)
        "titulo": "Fundamentos de programación con Python",
        "fechas": "Previa al inicio del programa",
        "capitulo": "1",
        "contenido": "Semana preparatoria: pensamiento computacional, algoritmos, Python, variables, operadores, "
        "condicionales y bucles",
        "unidades": [],  # se completa desde los encabezados de los notebooks
        "objetivos": [
            "Explicar la definición y necesidad del pensamiento computacional.",
            "Instalar Anaconda y Jupyter Notebook para programar en Python (en este cuaderno se usa `uv` + JupyterLab).",
            "Utilizar la función `print()` para mostrar cadenas y valores en pantalla.",
            "Distinguir entre error de sintaxis y error de tiempo de ejecución.",
        ],
        "contexto": "Python es un lenguaje popular y versátil, usado por empresas como Google, Netflix e Instagram, con "
        "una sintaxis sencilla y legible. Es una herramienta clave para la automatización, la ciencia de datos, la "
        "inteligencia artificial y el desarrollo web. La semana empieza por el pensamiento computacional, que permite "
        "descomponer problemas en pasos lógicos, y por los algoritmos y diagramas de flujo. Después se configura el "
        "entorno de desarrollo y se escriben los primeros programas: variables, tipos de datos, operadores, manejo "
        "básico de errores, sentencias condicionales y bucles.",
        "vocabulario": [
            ("Pensamiento computacional", "proceso de pensamiento para formular problemas y sus soluciones de manera que puedan ser ejecutadas eficazmente por un procesador de información."),
            ("Entorno virtual", "espacio aislado que permite gestionar dependencias y versiones de Python para diferentes proyectos."),
            ("Jupyter Notebook", "aplicación web interactiva para crear y compartir documentos con código ejecutable, ecuaciones, visualizaciones y texto narrativo."),
            ("Error de sintaxis", "error que ocurre cuando el código no sigue las reglas gramaticales del lenguaje de programación."),
            ("Error de tiempo de ejecución", "error que ocurre durante la ejecución del programa, a menudo por operaciones inválidas como la división por cero."),
        ],
        "nota_pdfs": "La semana 0 es un único PDF (`semana-00.pdf`, 543 págs.) con las unidades 1 a 9 del capítulo 1. "
        "Se dividió en dos bloques por tema: fundamentos (unidades 1–4) y control de flujo (unidades 5–9).",
        "repaso_extra": (
            "## Mapa rápido de la semana\n\n"
            "| Tema | Pregunta que responde | Herramienta |\n"
            "|---|---|---|\n"
            "| Pensamiento computacional | ¿Cómo convierto un problema en pasos que una computadora pueda seguir? | Descomposición, secuencia, selección, repetición |\n"
            "| Algoritmos | ¿Cómo describo la solución antes de programarla? | Diagrama de flujo, pseudocódigo |\n"
            "| Tipos y operadores | ¿Qué clase de dato tengo y qué puedo hacer con él? | `int`, `float`, `str`, `bool`, `type()`, conversión |\n"
            "| Variables | ¿Cómo guardo un valor para usarlo después? | `nombre = valor`, `input()` |\n"
            "| Comparación y lógica | ¿Cómo pregunto si algo es verdadero? | `==`, `!=`, `<`, `and`, `or`, `not` |\n"
            "| Condicionales | ¿Cómo hago que el programa elija un camino? | `if`, `else`, `elif` |\n"
            "| Bucles | ¿Cómo repito sin copiar código? | `for` con `range`, `while`, `break` |\n\n"
            "**Clave:** un error de sintaxis impide que el programa empiece; un error de tiempo de ejecución aparece "
            "mientras corre (por ejemplo `ZeroDivisionError`). La sangría define los bloques en Python."
        ),
    },
    1: {
        "aportes": APORTES / "semana-01",
        "checklist_completo": True,   # el usuario terminó la semana (2026-10-19)
        "titulo": "Secuencias de datos en Python",
        "fechas": "12/10/2026 – 17/10/2026",
        "capitulo": "2",
        "contenido": "Conceptos básicos de programación e iniciación con Python / Programación básica de Python "
        "- Secuencia de datos escrita en Python",
        "unidades": [
            (10, 1, "clase-1-listas-tuplas-diccionarios/u10-listas-y-tuplas.ipynb", "Tipos de datos de lista y tupla", "parte 1, págs. 5–88"),
            (11, 1, "clase-1-listas-tuplas-diccionarios/u11-diccionarios-y-json.ipynb", "Tipos de datos del diccionario", "parte 1, págs. 89–148"),
            (12, 1, "clase-1-listas-tuplas-diccionarios/u12-iteracion-y-busqueda.ipynb", "Tipos de datos de secuencia", "parte 1, págs. 149–208"),
            (13, 1, "clase-1-listas-tuplas-diccionarios/u13-listas-bidimensionales.ipynb", "Listas bidimensionales", "parte 1, págs. 209–281"),
            (14, 2, "clase-2-diccionarios-y-conjuntos/u14-diccionarios-crud.ipynb", "Diccionario, método 1: añadir, editar, borrar y guardar", "parte 2, págs. 5–64"),
            (15, 2, "clase-2-diccionarios-y-conjuntos/u15-diccionarios-avanzados.ipynb", "Diccionario, método 2: fromkeys, defaultdict, diccionario doble y copia", "parte 2, págs. 65–125"),
            (16, 2, "clase-2-diccionarios-y-conjuntos/u16-conjuntos.ipynb", "Establecer tipos de datos: conjuntos (set)", "parte 2, págs. 127–189"),
        ],
        "objetivos": [
            "Crear y manipular listas utilizando índices y métodos como `append`, `pop` y `remove`.",
            "Aplicar el rebanado (slicing) para extraer subconjuntos de datos de listas y tuplas.",
            "Construir y gestionar diccionarios para almacenar y acceder a datos mediante pares clave-valor.",
            "Diferenciar entre tipos de datos mutables (listas) e inmutables (tuplas) y sus usos.",
        ],
        "contexto": "La semana recorre las estructuras de datos fundamentales de Python. Empieza por las listas: varios "
        "valores en una sola variable, acceso por índice, métodos para modificarlas, rebanado y el operador `in`, "
        "aplicados al cálculo de la edad media de una base de datos personal. Sigue con los diccionarios, que asocian "
        "claves únicas a valores (por ejemplo, el menú de una cafetería con sus precios), y los compara con las listas. "
        "Introduce las tuplas, secuencias inmutables para datos que no deben cambiar, y termina con conjuntos.",
        "vocabulario": [
            ("Lista", "estructura de datos mutable que puede contener múltiples elementos de diferentes tipos, accesibles mediante un índice numérico."),
            ("Índice", "número entero que indica la posición de un elemento dentro de una secuencia, empezando desde 0."),
            ("Rebanar (slicing)", "operación para extraer una porción de una secuencia especificando inicio, fin y un paso opcional."),
            ("Diccionario", "estructura que almacena pares clave-valor, donde cada clave única se asocia a un valor."),
            ("Tupla", "secuencia inmutable; una vez creada, sus valores no pueden modificarse."),
        ],
        "nota_pdfs": "`semana-01-parte-2.pdf` es una copia de las unidades 14–16 de `semana-01-parte-1.pdf` "
        "(págs. 283–467). Las referencias de la clase 2 citan la parte 2.",
        "repaso_extra": (
            "## Lista, tupla, diccionario y conjunto\n\n"
            "| | Lista | Tupla | Diccionario | Conjunto |\n"
            "|---|---|---|---|---|\n"
            "| Sintaxis | `[1, 2]` | `(1, 2)` | `{'a': 1}` | `{1, 2}` |\n"
            "| Vacío | `[]` | `()` | `{}` | `set()` |\n"
            "| Mutable | Sí | No | Sí | Sí |\n"
            "| Ordenado | Sí | Sí | Sí, por inserción | No |\n"
            "| Acceso | Índice `l[0]` | Índice `t[0]` | Clave `d['a']` | Solo `in` |\n"
            "| Duplicados | Sí | Sí | Claves no | No |\n"
            "| Uso típico | Colección que cambia | Datos fijos, registros | Buscar por nombre | Quitar duplicados, operaciones de conjuntos |\n\n"
            "**Clave:** si necesitas buscar por posición, lista o tupla; si buscas por nombre, diccionario; "
            "si solo te importa si algo está o no, conjunto."
        ),
    },
    2: {
        "aportes": APORTES / "semana-02",
        "titulo": "Funciones, clausuras y clases",
        "fechas": "19/10/2026 – 24/10/2026",
        "capitulo": "3",
        "contenido": "Programación efectiva con Python - Function, Closure y Clases",
        "unidades": [],  # se completa desde los encabezados de los notebooks
        "objetivos": [
            "Definir funciones en Python utilizando parámetros, argumentos variables, por defecto y de palabra clave.",
            "Implementar funciones recursivas con condición de terminación para resolver problemas como factorial y Fibonacci.",
            "Aplicar funciones lambda junto con `filter`, `map` y `reduce` para procesar listas y otros iterables.",
            "Distinguir entre variables globales, locales y no locales, y utilizar las palabras clave `global` y `nonlocal`.",
            "Definir y utilizar funciones anidadas y clausuras para encapsular datos y comportamiento.",
            "Crear clases con atributos, métodos, constructores (`__init__`) y representación de cadenas (`__str__`).",
            "Aplicar el concepto de herencia para crear jerarquías de clases y reutilizar código.",
        ],
        "contexto": "Las funciones son los componentes básicos de un programa: bloques reutilizables que se definen con "
        "`def`, reciben argumentos de distintas formas y devuelven resultados con `return`, aplicados a un programa de "
        "cifrado César. La recursividad resuelve problemas dividiéndolos en subproblemas (factorial, Fibonacci, Torre "
        "de Hanoi), y las funciones de orden superior (`lambda`, `filter`, `map`, `reduce`) procesan datos sin bucles "
        "explícitos. La segunda clase profundiza en el ámbito de las variables, las funciones como objetos y las "
        "clausuras, e introduce la programación orientada a objetos: clases, instancias, `__init__`, `__str__` y "
        "herencia, con una cuenta bancaria como caso práctico.",
        "vocabulario": [
            ("Parámetro", "variable definida en la función que recibe un valor cuando la función es llamada."),
            ("Argumento", "valor real que se pasa a una función cuando es llamada."),
            ("Recursividad", "técnica donde una función se llama a sí misma para resolver un problema."),
            ("Lambda", "función anónima definida con la palabra clave `lambda`, usada para expresiones simples."),
            ("Variable global", "variable definida fuera de cualquier función, accesible en todo el código."),
            ("Ámbito (scope)", "regla que determina desde qué partes del código se puede acceder a una variable: local (L), envolvente (E) y global (G)."),
            ("Clausura (closure)", "función que recuerda y puede acceder a variables de su ámbito envolvente incluso después de que ese ámbito haya terminado su ejecución."),
            ("Clase", "plantilla que define los atributos (datos) y métodos (comportamientos) comunes a un tipo de objeto, como una cuenta bancaria."),
            ("Instancia", "objeto concreto creado a partir de una clase, por ejemplo `cuenta1` de la clase `BankAccount`."),
            ("Herencia", "mecanismo por el cual una subclase hereda atributos y métodos de una superclase, permitiendo reutilizar y extender código."),
        ],
        "nota_pdfs": "`semana-02-parte-2.pdf` repite las unidades 20–21 de `semana-02-parte-1.pdf` (desde la pág. 212). "
        "Las referencias de la clase 2 citan la parte 2.",
        "repaso_extra": (
            "## Mapa rápido de la semana\n\n"
            "| Tema | Pregunta que responde | Herramienta |\n"
            "|---|---|---|\n"
            "| Funciones | ¿Cómo reutilizo un bloque de código? | `def`, `return`, parámetros por defecto, `*args`, `**kwargs` |\n"
            "| Recursividad | ¿Cómo resuelvo un problema que contiene versiones más pequeñas de sí mismo? | Caso base + llamada recursiva |\n"
            "| Funciones de orden superior | ¿Cómo proceso una colección sin escribir el bucle? | `lambda`, `filter`, `map`, `reduce` |\n"
            "| Ámbito | ¿Desde dónde se ve una variable? | Regla LEGB, `global`, `nonlocal` |\n"
            "| Clausuras | ¿Cómo hago que una función recuerde datos? | Función anidada que usa variables de la externa |\n"
            "| Clases | ¿Cómo junto datos y comportamiento? | `class`, `__init__`, `self`, `__str__` |\n"
            "| Herencia | ¿Cómo reutilizo una clase existente? | `class Hija(Padre)`, `super()` |\n\n"
            "**Clave:** toda función recursiva necesita un caso base; sin él, `RecursionError`. "
            "Asignar a una variable dentro de una función la vuelve local salvo que se declare `global` o `nonlocal`."
        ),
    },
}


SEMANAS[3] = {
    "aportes": APORTES / "semana-03",
    "titulo": "Pilas, colas, búsqueda y tablas hash",
    "fechas": "26/10/2026 – 31/10/2026",
    "checklist_completo": True,   # el usuario terminó la semana (2026-10-26)
    "capitulo": "4",
    "contenido": "Algoritmos de clasificación 1. Pilas, colas, búsqueda secuencial/binaria, tablas hash",
    "unidades": [],  # se completa desde los encabezados de los notebooks
    "objetivos": [
        "Implementar una pila (LIFO) con una lista y como clase, con las operaciones push y pop, manejando pilas vacías.",
        "Usar una pila para verificar paréntesis equilibrados en código fuente o HTML.",
        "Implementar una cola (FIFO) con las operaciones enqueue y dequeue y aplicarla al problema de Josephus.",
        "Aplicar la búsqueda secuencial para encontrar un valor o el mayor de una lista.",
        "Comprender el funcionamiento del algoritmo de búsqueda binaria.",
        "Aplicar la búsqueda binaria para resolver el problema de la caída de huevos.",
        "Entender el concepto y la implementación de una tabla hash.",
        "Utilizar un diccionario para construir un conversor de números romanos.",
    ],
    "contexto": "La semana introduce las estructuras de datos de pila y cola. Una pila es una colección LIFO (último en "
    "entrar, primero en salir) con push y pop, que permite verificar paréntesis equilibrados en código fuente o HTML; "
    "se implementa con una lista de Python y con una clase propia. Una cola es una colección FIFO (primero en entrar, "
    "primero en salir) con enqueue y dequeue, aplicada al problema histórico de Josephus. La búsqueda secuencial "
    "recorre una lista elemento por elemento, y la búsqueda binaria reduce el espacio de búsqueda a la mitad en cada "
    "paso (tiempo logarítmico); ambas se aplican al problema de la caída de huevos. Por último, las tablas hash dan "
    "acceso casi instantáneo a los valores mediante una función hash, y un diccionario de Python sirve para construir "
    "un conversor de números romanos a arábigos.",
    "vocabulario": [
        ("Pila (stack)", "estructura de datos LIFO que permite las operaciones push (añadir) y pop (eliminar)."),
        ("LIFO", "Last-In, First-Out: el último elemento añadido es el primero en ser removido."),
        ("Cola (queue)", "estructura de datos FIFO con las operaciones enqueue (añadir al final) y dequeue (remover del frente)."),
        ("FIFO", "First-In, First-Out: el primer elemento añadido es el primero en ser removido."),
        ("Búsqueda secuencial", "algoritmo que recorre una lista en orden, uno por uno, hasta encontrar el objetivo o llegar al final."),
        ("Búsqueda binaria", "algoritmo que encuentra un valor en un array ordenado dividiendo repetidamente el intervalo de búsqueda a la mitad."),
        ("Espacio de búsqueda", "rango de elementos (de un índice bajo a uno alto) dentro del cual se busca el objetivo."),
        ("Tiempo logarítmico", "complejidad O(log n): el tiempo de ejecución crece logarítmicamente con el tamaño de la entrada."),
        ("Tabla hash", "estructura de datos que implementa un array asociativo, mapeando claves a valores mediante una función hash."),
        ("Función hash", "función que convierte una clave (como una cadena) en un índice numérico (hashkey) para guardar o recuperar un valor."),
    ],
    "nota_pdfs": "Dos PDFs sin contenido repetido: la parte 1 tiene las unidades 22 a 24 (clase 1) y la parte 2 las "
    "unidades 25 y 26 (clase 2).",
    "repaso_extra": (
        "## Mapa rápido de la semana\n\n"
        "| Estructura o algoritmo | Idea | Operaciones clave | Costo típico |\n"
        "|---|---|---|---|\n"
        "| Pila | LIFO: sale primero lo último que entró | `push` (`append`), `pop` (`pop()`), `peek` (`[-1]`) | O(1) |\n"
        "| Cola | FIFO: sale primero lo primero que entró | `enqueue` (`append`), `dequeue` (`pop(0)` o `deque.popleft()`) | O(1) con `deque` |\n"
        "| Búsqueda secuencial | Revisar uno por uno | recorrer con `for` | O(n) |\n"
        "| Búsqueda binaria | Partir el rango a la mitad (lista ordenada) | `bajo`, `alto`, `medio` | O(log n) |\n"
        "| Tabla hash | Clave → función hash → posición | guardar y buscar por clave (`dict`) | O(1) promedio |\n\n"
        "**Clave:** la búsqueda binaria solo funciona sobre datos **ordenados**. Con 1 000 000 de elementos, la "
        "secuencial puede necesitar 1 000 000 de comparaciones y la binaria unas 20."
    ),
}


SEMANAS[4] = {
    "aportes": APORTES / "semana-04",
    "titulo": "Ordenamiento, greedy y divide y vencerás",
    "fechas": "2/11/2026 – 7/11/2026",
    "capitulo": "5 y 6",
    "contenido": "Estructuras de datos / Algoritmos de clasificación / Resolución de problemas con algoritmos",
    "unidades": [],  # se completa desde los encabezados de los notebooks
    "objetivos": [
        "Implementar los algoritmos de ordenamiento de burbuja, selección e inserción en Python.",
        "Explicar las diferencias entre los algoritmos de ordenamiento de burbuja, selección e inserción.",
        "Implementar el algoritmo de ordenamiento por fusión utilizando funciones recursivas.",
        "Implementar el algoritmo de ordenamiento rápido con diferentes estrategias de selección de pivote.",
        "Entender el enfoque greedy y aplicarlo a los problemas de intercambio de monedas y selección de actividades.",
        "Diseñar e implementar algoritmos greedy de forma recursiva.",
        "Comprender el método divide y vencerás y aplicarlo al problema de la ruta del triángulo.",
        "Diseñar e implementar recursivamente divide y vencerás, reconociendo su uso en búsqueda binaria, merge sort y quick sort.",
    ],
    "contexto": "La semana aborda el problema del ordenamiento. Primero los métodos básicos (burbuja, selección e "
    "inserción), que comparan e intercambian elementos o buscan el mínimo y tienen complejidad cuadrática O(N²) en "
    "el peor caso. Luego los algoritmos de divide y vencerás, ordenamiento por fusión y ordenamiento rápido, que "
    "llegan típicamente a O(N log N); se analiza cómo la elección del pivote afecta al quicksort y el uso de memoria "
    "de cada implementación. La segunda clase presenta técnicas de diseño para problemas de optimización: el enfoque "
    "greedy (cambio de monedas y selección de actividades en una sala de reuniones, con sus pasos de selección, "
    "verificación de viabilidad y verificación de solución) y la estrategia divide y vencerás aplicada a la ruta "
    "mínima en un triángulo, reconocida también en la búsqueda binaria, el merge sort y el quick sort.",
    "vocabulario": [
        ("Problema de ordenamiento", "tarea de reorganizar los elementos de una lista en un orden específico, típicamente ascendente o descendente."),
        ("Tiempo cuadrático", "complejidad O(N²): el tiempo de ejecución crece proporcionalmente al cuadrado del tamaño de la entrada."),
        ("Fusionar (merge)", "combinar dos listas ordenadas en una sola lista ordenada, como hace el ordenamiento por fusión."),
        ("Pivote", "elemento de referencia del ordenamiento rápido que divide la lista en elementos menores y mayores."),
        ("Partición", "reorganizar la lista alrededor del pivote: menores a la izquierda y mayores a la derecha."),
        ("Enfoque greedy (voraz)", "técnica que llega a una solución eligiendo en cada paso la mejor opción del momento, según criterios predefinidos."),
        ("Selección de actividades", "dadas actividades con hora de inicio y fin, elegir el máximo número de actividades que no se solapen."),
        ("Intercambio de monedas", "devolver una cantidad de cambio con el mínimo número de monedas de las denominaciones dadas."),
        ("Divide y vencerás", "estrategia que divide un problema en subproblemas más pequeños, los resuelve recursivamente y combina sus soluciones."),
        ("Ruta del triángulo", "dado un triángulo de enteros positivos, la suma mínima desde la cima hasta la base moviéndose solo a números adyacentes."),
    ],
    "nota_pdfs": "Dos PDFs sin contenido repetido (los archivos originales venían rotulados como semana 3): la parte 1 "
    "tiene las unidades 27 a 29 (clase 1) y la parte 2 las unidades 30 y 31 (clase 2).",
    "repaso_extra": (
        "## Mapa rápido de la semana\n\n"
        "| Algoritmo | Idea | Peor caso | Caso típico | Memoria extra |\n"
        "|---|---|---|---|---|\n"
        "| Burbuja | Intercambiar vecinos desordenados; el mayor \"sube\" al final | O(N²) | O(N²) | O(1) |\n"
        "| Selección | Buscar el mínimo y ponerlo al principio | O(N²) | O(N²) | O(1) |\n"
        "| Inserción | Insertar cada elemento en su lugar dentro de la parte ya ordenada | O(N²) | O(N) si casi ordenada | O(1) |\n"
        "| Fusión (merge sort) | Dividir a la mitad, ordenar cada mitad y fusionar | O(N log N) | O(N log N) | O(N) |\n"
        "| Rápido (quick sort) | Partir alrededor de un pivote y ordenar cada lado | O(N²) con mal pivote | O(N log N) | O(log N) in situ |\n\n"
        "| Técnica | Cuándo sirve | Ejemplo |\n|---|---|---|\n"
        "| Greedy | Cuando la mejor elección local lleva a la óptima global | Cambio de monedas, selección de actividades |\n"
        "| Divide y vencerás | Cuando el problema se parte en subproblemas del mismo tipo | Búsqueda binaria, merge sort, quick sort, ruta del triángulo |\n\n"
        "**Clave:** greedy no siempre da el óptimo (con monedas `[4, 3, 1]` y 6, greedy usa 3 monedas y lo óptimo son 2). "
        "Un pivote aleatorio evita el peor caso de quicksort con listas ya ordenadas."
    ),
}


SEMANAS[5] = {
    "aportes": APORTES / "semana-05",
    "titulo": "Programación dinámica, backtracking y primeros pasos con pandas",
    "fechas": "9/11/2026 – 14/11/2026",
    "capitulo": "6 y 7",
    "contenido": "Algoritmo 2 - Resolución de problemas con algoritmos / Procesamiento de datos, estadísticas "
    "descriptivas y visualización de datos",
    "unidades": [],  # se completa desde los encabezados de los notebooks
    "objetivos": [
        "Entender la programación dinámica y calcular la secuencia de Fibonacci utilizándola.",
        "Calcular el coeficiente binomial utilizando el triángulo de Pascal.",
        "Resolver problemas de optimización utilizando relaciones recursivas de forma ascendente.",
        "Comprender las técnicas de backtracking y resolver el problema de las N-Reinas.",
        "Importar y utilizar módulos estándar (random, time, datetime) y externos (pandas, matplotlib) en Python.",
        "Crear y manipular objetos Series de pandas a partir de listas, diccionarios y arrays de NumPy.",
        "Construir y modificar DataFrames de pandas desde diccionarios, archivos CSV, Excel y JSON.",
        "Aplicar operaciones aritméticas y estadísticas descriptivas básicas en Series y DataFrames.",
        "Visualizar datos mediante gráficos de líneas, barras y dispersión con matplotlib.",
    ],
    "contexto": "La primera clase presenta técnicas avanzadas de diseño de algoritmos. La programación dinámica aborda "
    "problemas con subestructura óptima y subproblemas superpuestos, almacenando soluciones parciales para evitar "
    "cálculos redundantes; se aplica a la secuencia de Fibonacci y al triángulo de Pascal, comparando la recursión "
    "simple con la memorización y el cálculo ascendente. El backtracking es una búsqueda en profundidad que construye "
    "soluciones candidatas paso a paso y retrocede cuando una candidata no puede llevar a una solución válida; se "
    "aplica al problema de las N-Reinas, podando las ramas no prometedoras. La segunda clase extiende Python con "
    "módulos: los estándar (random, time, datetime) en la misión del juego de dados, y los externos pandas y "
    "matplotlib. Con pandas se trabaja con Series (estructura unidimensional que asocia índices a datos) y "
    "DataFrames (tablas bidimensionales), cargando datos desde CSV, Excel y JSON, filtrando, seleccionando y "
    "calculando estadísticas; con matplotlib se grafican, por ejemplo, la densidad de población de ciudades o la "
    "correlación entre variables musicales.",
    "vocabulario": [
        ("Programación dinámica", "técnica que resuelve problemas con subproblemas superpuestos guardando las "
         "soluciones parciales para no recalcularlas."),
        ("Memorización (memoization)", "guardar el resultado de una llamada recursiva para reutilizarlo cuando se "
         "repiten los mismos argumentos."),
        ("Cálculo ascendente (bottom-up)", "resolver primero los subproblemas más pequeños y construir con ellos la "
         "solución de los más grandes."),
        ("Backtracking (retroceso)", "búsqueda en profundidad que construye candidatas paso a paso y retrocede cuando "
         "una no puede llevar a una solución válida."),
        ("Poda", "descartar ramas no prometedoras del espacio de búsqueda para no explorarlas."),
        ("Módulo", "archivo de código Python (.py) que agrupa funciones, clases y variables para su reutilización; "
         "puede ser estándar (incluido en Python) o externo (instalado por el usuario)."),
        ("Serie (pandas)", "estructura de datos unidimensional de pandas que almacena datos asociados a un índice."),
        ("DataFrame (pandas)", "estructura de datos bidimensional de pandas, similar a una hoja de cálculo, compuesta "
         "por filas y columnas; cada columna es una Serie."),
        ("Índice", "etiqueta o posición que identifica cada elemento de una Serie o cada fila de un DataFrame."),
        ("API", "conjunto de reglas que permite a distintas aplicaciones comunicarse; en el curso se usa para obtener "
         "datos de servicios remotos."),
    ],
    "nota_pdfs": "Dos PDFs sin contenido repetido: la parte 1 (capítulo 6) tiene las unidades 32 y 33 (clase 1) y la "
    "parte 2 (capítulo 7) las unidades 34 a 36 (clase 2). La parte 2 termina en la programación en pareja de la "
    "unidad 36, sin la diapositiva de cierre.",
    "repaso_extra": (
        "## Mapa rápido de la semana\n\n"
        "| Técnica | Idea | Ejemplo del curso |\n"
        "|---|---|---|\n"
        "| Recursión simple | Recalcula los mismos subproblemas | Fibonacci recursivo: O(2^n) |\n"
        "| Memorización | Recursión que guarda resultados | Fibonacci con diccionario: O(n) |\n"
        "| Ascendente (bottom-up) | Tabla de lo pequeño a lo grande | Triángulo de Pascal para el coeficiente binomial |\n"
        "| Backtracking | Probar, verificar si es prometedor y retroceder | N-Reinas |\n\n"
        "| Estructura de pandas | Dimensiones | Se crea con |\n"
        "|---|---|---|\n"
        "| Series | 1 (índice → valor) | `pd.Series([...], index=[...])` |\n"
        "| DataFrame | 2 (filas × columnas) | `pd.DataFrame({...})`, `pd.read_csv()`, `pd.read_excel()`, `pd.read_json()` |\n\n"
        "**Clave:** divide y vencerás parte en subproblemas independientes; la programación dinámica sirve cuando los "
        "subproblemas se repiten. `df['col']` es una Series y `df[['col']]` un DataFrame."
    ),
}


SEMANAS[6] = {
    "aportes": APORTES / "semana-06",
    "titulo": "Datos ordenados, series temporales y mini proyectos",
    "fechas": "16/11/2026 – 21/11/2026",
    "capitulo": "7 y 8",
    "contenido": "Procesamiento de datos, estadísticas descriptivas y visualización de datos / Mini proyecto de "
    "análisis y visualización de datos",
    "unidades": [],  # se completa desde los encabezados de los notebooks
    "objetivos": [
        "Identificar y manejar datos faltantes (NaN) en un DataFrame de Pandas.",
        "Aplicar estadísticas descriptivas (media, mediana, moda, varianza, desviación estándar) a datos organizados.",
        "Visualizar datos utilizando histogramas, diagramas de caja y diagramas de dispersión con Matplotlib/Seaborn.",
        "Convertir y manipular datos de series temporales utilizando Timestamp, Period y DatetimeIndex.",
        "Adquirir y procesar datos financieros de repositorios remotos.",
        "Visualizar datos de precios y volúmenes de acciones en series temporales.",
        "Calcular métricas financieras como cambio porcentual diario, rendimiento acumulado y volatilidad.",
        "Analizar la correlación entre diferentes activos financieros.",
        "Visualizar datos de una pandemia global en un mapa interactivo usando Folium.",
    ],
    "contexto": "En el análisis de datos real, los conjuntos de datos rara vez están listos para su análisis: contienen "
    "valores faltantes, formatos inconsistentes o están desorganizados. La ordenación de datos (Tidy Data) consume una "
    "gran parte del tiempo del científico de datos y sigue principios como «cada variable en su columna» y «cada "
    "observación en su fila». Con Pandas se detectan los NaN con isnull(), se eliminan con dropna() o se reemplazan "
    "con fillna(), usando valores como la media o la moda. Los datos de series temporales son secuencias de puntos "
    "indexados en el tiempo, como precios de acciones o producción anual: Pandas ofrece Timestamp para puntos "
    "específicos y Period para intervalos, y convertir una columna de fechas a datetime64 y usarla como índice "
    "(DatetimeIndex) permite cortes temporales intuitivos; rolling().mean() suaviza fluctuaciones y revela tendencias. "
    "La segunda clase aplica todo en dos mini proyectos: el análisis de datos financieros del mercado estadounidense "
    "(índices, bonos, materias primas y oro obtenidos de Yahoo Finance; cambio porcentual diario, rendimiento "
    "acumulado, volatilidad y correlación entre activos, incluido el periodo de la pandemia de COVID-19) y el análisis "
    "de datos públicos de la pandemia de coronavirus, con estadísticas de vacunación por país y un mapa coroplético "
    "interactivo de casos acumulados creado con Folium.",
    "vocabulario": [
        ("NaN", "Not a Number; valor utilizado en Pandas para representar datos faltantes u omitidos en un DataFrame."),
        ("Datos ordenados (Tidy Data)", "forma estándar de estructurar datos donde cada variable es una columna, cada "
         "observación es una fila y cada valor tiene su propia celda."),
        ("Estadísticas descriptivas", "métricas como media, mediana, moda, varianza y desviación estándar que resumen y "
         "describen las características principales de un conjunto de datos."),
        ("Timestamp", "un punto específico en el tiempo (por ejemplo, una fecha y hora exactas), representado en Pandas "
         "con el tipo datetime64."),
        ("Media móvil", "cálculo estadístico de series temporales que suaviza fluctuaciones a corto plazo y revela "
         "tendencias a largo plazo, calculado como la media de una ventana deslizante de datos."),
        ("Ticker", "código único que identifica un valor negociado públicamente en una bolsa (por ejemplo, SPY para el "
         "ETF del S&P 500)."),
        ("Serie temporal", "conjunto de datos recolectados en intervalos de tiempo sucesivos, como los precios de cierre "
         "diarios de una acción."),
        ("Cambio porcentual diario", "variación relativa de un valor de un día para otro: ((precio hoy - precio ayer) / "
         "precio ayer) * 100."),
        ("Coeficiente de correlación", "medida de la fuerza y dirección de la relación lineal entre dos variables; en "
         "Pandas se calcula con .corr()."),
        ("Mapa coroplético", "mapa temático donde las áreas geográficas se colorean en proporción a un valor "
         "estadístico, como la tasa de infección por país."),
    ],
    "nota_pdfs": "Dos PDFs sin contenido repetido: la parte 1 (capítulo 7) tiene las unidades 37 y 38 (clase 1) y la "
    "parte 2 (capítulo 8) las unidades 39 y 40 (clase 2). La portada del capítulo 7 lista también las unidades 34 a 36, "
    "que corresponden a la semana 5.",
    "repaso_extra": (
        "## Mapa rápido de la semana\n\n"
        "| Tarea | Herramienta en Pandas | Ejemplo |\n"
        "|---|---|---|\n"
        "| Detectar faltantes | `isnull()` / `isna()` | `df.isnull().sum()` |\n"
        "| Eliminar faltantes | `dropna()` | `df.dropna(subset=['col'])` |\n"
        "| Reemplazar faltantes | `fillna()` | `df['col'] = df['col'].fillna(df['col'].mean())` |\n"
        "| Resumen estadístico | `describe()`, `mean()`, `median()`, `mode()`, `var()`, `std()` | `df.describe()` |\n"
        "| Fechas | `pd.to_datetime()`, `pd.Timestamp`, `pd.Period` | `df.index = pd.to_datetime(df['fecha'])` |\n"
        "| Ventana móvil | `rolling(n).mean()` | `s.rolling(20).mean()` |\n"
        "| Cambio porcentual | `pct_change()` | `precios.pct_change() * 100` |\n"
        "| Rendimiento acumulado | `cumprod()` | `(1 + precios.pct_change()).cumprod() - 1` |\n"
        "| Correlación | `corr()` | `rendimientos.corr()` |\n"
        "| Mapa coroplético | `folium.Choropleth` | capa coloreada por país sobre `folium.Map` |\n\n"
        "**Clave:** `df[['col']]` devuelve un DataFrame y `df['col']` una Series. `describe()` no incluye la moda: "
        "se obtiene con `mode()`."
    ),
}


def secciones(texto):
    partes, actual = {}, None
    for linea in texto.splitlines():
        if linea.startswith("## "):
            actual = linea[3:].strip()
            partes[actual] = []
        elif actual:
            partes[actual].append(linea)
    return partes


def leer_aporte(carpeta, n):
    ruta = carpeta / f"u{n:02d}.md"
    if not ruta.exists():
        ruta = carpeta / f"u{n}.md"
    s = secciones(ruta.read_text())
    glosario = []
    for l in s["Glosario"]:
        m = re.match(r"^\s*-?\s*\*\*(.+?)\*\*\s*:\s*(.+)$", l)
        if m:
            glosario.append((m.group(1), m.group(2)))
    cheat = [l for l in s["Cheatsheet"] if l.strip() and not l.strip().startswith("```")]
    errores = [l.strip()[2:] for l in s["Errores comunes"] if l.strip().startswith("- ")]
    preguntas = []
    for trozo in re.split(r"\n(?=P: )", "\n".join(s["Quiz"])):
        trozo = trozo.strip()
        if not trozo.startswith("P:"):
            continue
        campos, opciones = {}, {}
        for l in trozo.splitlines():
            l = l.strip()
            if l.startswith("P:"):
                campos["pregunta"] = l[2:].strip()
            elif re.match(r"^[A-D]\)", l):
                opciones[l[0]] = l[2:].strip()
            elif l.startswith("Correcta:"):
                campos["correcta"] = l.split(":", 1)[1].strip()[0]
            elif l.startswith("Por qué:"):
                campos["porque"] = l.split(":", 1)[1].strip()
            elif l.startswith("Referencia:"):
                campos["referencia"] = l.split(":", 1)[1].strip()
        campos["opciones"] = opciones
        assert len(opciones) == 4 and "correcta" in campos, (n, trozo)
        preguntas.append(campos)
    return glosario, cheat, errores, preguntas


def estado_evaluacion(ruta):
    """(existe, nota) de un notebook de evaluación; nota es "100/100" si su sección Estado dice "Nota final"."""
    if not ruta.exists():
        return False, None
    m = re.search(r"Nota final: (\d+/\d+)", nbformat.read(ruta, 4).cells[0].source)
    return True, m.group(1) if m else None


def carpeta_semana(num):
    return RAIZ / f"01-python/semana-{num:02d}"


def unidades_desde_notebooks(num):
    """Lee número, clase, título y fuente del encabezado de cada notebook de unidad."""
    unidades = []
    for ruta in sorted(carpeta_semana(num).glob("clase-*/u*.ipynb")):
        primera = nbformat.read(ruta, 4).cells[0].source.splitlines()
        m = re.match(r"# Unidad (\d+) — (.+)", primera[0])
        fuente = next(l for l in primera if "Fuente:" in l)
        clase = int(re.search(r"Clase (\d)", fuente).group(1))
        pdf = fuente.split("Fuente: PDF ")[1].strip()
        unidades.append((int(m.group(1)), clase, str(ruta.relative_to(carpeta_semana(num))), m.group(2).strip(), pdf))
    return unidades


def navegacion(num):
    partes = ["[Inicio del curso](../../00-inicio.ipynb)"]
    if num > 0:
        partes.append(f"[Semana anterior](../semana-{num - 1:02d}/semana-{num - 1:02d}.ipynb)")
    partes.append(f"[Semana siguiente](../semana-{num + 1:02d}/semana-{num + 1:02d}.ipynb)")
    return " | ".join(partes)


def semana_nb(num, cfg, datos):
    hecho = "x" if cfg.get("checklist_completo") else " "   # unidades, tutoría y repaso
    nav = navegacion(num)
    indice = f"semana-{num:02d}.ipynb"
    filas = ["| Clase | Unidad | Tema | Fuente |", "|---|---|---|---|"]
    for n, clase, ruta, titulo, fuente in cfg["unidades"]:
        filas.append(f"| {clase} | [Unidad {n}]({ruta}) | {titulo} | PDF {fuente} |")
    nb = new_notebook()
    nb.cells = [
        new_markdown_cell(
            f"# Semana {num} — {cfg['titulo']}\n\n"
            f"**Fechas:** {cfg['fechas']}  \n**Capítulo:** {cfg['capitulo']}  \n**Contenido:** {cfg['contenido']}\n\n" + nav
        ),
        new_markdown_cell(
            "## Objetivos de aprendizaje\n\n" + "\n".join(f"- {o}" for o in cfg["objetivos"])
            + "\n\n## Contexto\n\n" + cfg["contexto"]
        ),
        new_markdown_cell(
            "## Vocabulario clave\n\n" + "\n".join(f"- **{t}:** {d}" for t, d in cfg["vocabulario"])
            + "\n\nGlosario completo: [glosario.ipynb](../../glosario.ipynb)"
        ),
        new_markdown_cell("## Clases\n\n" + "\n".join(filas)),
        new_markdown_cell(
            "## Nota sobre los PDFs\n\n" + cfg["nota_pdfs"] + "\n\n"
            "Los PDFs tienen errores de traducción automática: nombres de funciones y métodos traducidos al español, "
            "código que no ejecuta y salidas incorrectas. Cada notebook los corrige y los señala con **Nota sobre el PDF:**. "
            "Ante la duda, vale el código que corre."
        ),
        new_markdown_cell(
            "## Actividades\n\n"
            f"- [Tutoría]({archivo_semana(num, 'tutoria')}): notas de la clase de tutoría.\n"
            f"- [Quiz de práctica]({archivo_semana(num, 'quiz')}): práctica interactiva y repaso de preguntas de las "
            f"{len(cfg['unidades'])} unidades.\n"
            + (
                f"- [Quiz calificado]({archivo_semana(num, 'quiz-calificado')}): quiz de la plataforma, con las "
                "respuestas resueltas.\n"
                if (carpeta_semana(num) / archivo_semana(num, "quiz-calificado")).exists()
                else ""
            )
            + (
                f"- [Actividad asincrónica]({archivo_semana(num, 'actividad-asincronica')}): actividad calificada "
                "de la plataforma, con guía y solución de referencia.\n"
                if (carpeta_semana(num) / archivo_semana(num, "actividad-asincronica")).exists()
                else ""
            )
            + f"- [Repaso]({archivo_semana(num, 'repaso')}): cheatsheet y errores comunes en una sola página."
        ),
        new_markdown_cell(
            "## Checklist de la semana\n\n"
            + "\n".join(f"- [{hecho}] Unidad {n}: leer, ejecutar los ejemplos y resolver la práctica" for n, *_ in cfg["unidades"])
            + f"\n- [{hecho}] Tutoría: anotar dudas y respuestas"
            + "".join(
                f"\n- [{'x' if nota else ' '}] {titulo}" + (f": {entregado}, {nota}" if nota else ": pendiente de entrega")
                for nombre, titulo, entregado in (("quiz-calificado", "Quiz calificado", "entregado"),
                                                  ("actividad-asincronica", "Actividad asincrónica", "entregada"))
                for existe, nota in [estado_evaluacion(carpeta_semana(num) / archivo_semana(num, nombre))]
                if existe
            )
            + f"\n- [{hecho}] Repaso final"
        ),
        new_markdown_cell(nav),
    ]
    return nb


def quiz_nb(num, cfg, datos):
    indice = f"[Índice de la semana](semana-{num:02d}.ipynb)"
    preguntas = [{"unidad": n, **p} for n, *_ in cfg["unidades"] for p in datos[n][3]]
    primera = cfg["unidades"][0][0]
    nb = new_notebook()
    nb.cells = [
        new_markdown_cell(
            f"# Quiz — Semana {num}\n\n{indice}\n\n"
            f"{len(preguntas)} preguntas de opción múltiple, 6 por unidad.\n\n"
            "Dos formas de usarlo:\n\n"
            "1. **Práctica interactiva:** ejecuta las celdas de código, quita el comentario de la llamada a `hacer_quiz` "
            "y responde con A, B, C o D. Al final se muestra el puntaje y las preguntas falladas.\n"
            "2. **Repaso rápido:** más abajo están todas las preguntas con la respuesta plegada. Intenta responder antes de abrirla."
        ),
        new_code_cell("PREGUNTAS = " + repr(preguntas).replace("}, {", "},\n    {")),
        new_code_cell(
            'import random\n\n\n'
            'def hacer_quiz(unidad=None, cantidad=10):\n'
            '    """Hace preguntas al azar. unidad=None mezcla todas las unidades."""\n'
            '    banco = [p for p in PREGUNTAS if unidad is None or p["unidad"] == unidad]\n'
            '    seleccion = random.sample(banco, min(cantidad, len(banco)))\n'
            '    falladas = []\n'
            '    for i, p in enumerate(seleccion, 1):\n'
            '        print(f"\\nPregunta {i} de {len(seleccion)} (Unidad {p[\'unidad\']})")\n'
            '        print(p["pregunta"])\n'
            '        for letra, texto in p["opciones"].items():\n'
            '            print(f"  {letra}) {texto}")\n'
            '        respuesta = input("Tu respuesta (A-D): ").strip().upper()[:1]\n'
            '        if respuesta == p["correcta"]:\n'
            '            print("Correcto.")\n'
            '        else:\n'
            '            print(f"Incorrecto. La respuesta es {p[\'correcta\']}: {p[\'porque\']}")\n'
            '            falladas.append(p)\n'
            '    aciertos = len(seleccion) - len(falladas)\n'
            '    print(f"\\nResultado: {aciertos} de {len(seleccion)}")\n'
            '    for p in falladas:\n'
            '        print(f"- Repasar: {p[\'pregunta\']} ({p.get(\'referencia\', \'\')})")\n\n\n'
            'print(f"{len(PREGUNTAS)} preguntas cargadas.")'
        ),
        new_code_cell(
            "# Para hacer el quiz, quita el comentario de una de estas líneas y ejecuta la celda.\n"
            "# hacer_quiz()                  # 10 preguntas de todas las unidades\n"
            f"# hacer_quiz(unidad={primera})         # solo la Unidad {primera}\n"
            f"# hacer_quiz(cantidad={len(preguntas)})       # el banco completo"
        ),
    ]
    for n, clase, ruta, titulo, _ in cfg["unidades"]:
        partes = [f"## Unidad {n} — {titulo}\n\n[Ir a la unidad]({ruta})"]
        for i, p in enumerate(datos[n][3], 1):
            ops = "\n".join(f"- {k}) {v}" for k, v in p["opciones"].items())
            partes.append(
                f"**{i}. {p['pregunta']}**\n\n{ops}\n\n<details><summary>Ver respuesta</summary>\n\n"
                f"**{p['correcta']}.** {p['porque']}\n\n**Referencia:** {p.get('referencia', '')}\n</details>"
            )
        nb.cells.append(new_markdown_cell("\n\n".join(partes)))
    nb.cells.append(new_markdown_cell(indice))
    return nb


def repaso_nb(num, cfg, datos):
    indice = f"[Índice de la semana](semana-{num:02d}.ipynb)"
    ultima = cfg["unidades"][-1]
    nb = new_notebook()
    nb.cells = [
        new_markdown_cell(
            f"# Repaso — Semana {num}\n\n{indice} | [Anterior: Unidad {ultima[0]}]({ultima[2]})\n\n"
            "Todo lo de la semana en una página: mapa de temas, cheatsheet por unidad y errores comunes."
        ),
        new_markdown_cell(cfg["repaso_extra"]),
    ]
    for n, clase, ruta, titulo, _ in cfg["unidades"]:
        _, cheat, errores, _ = datos[n]
        nb.cells.append(
            new_markdown_cell(
                f"## Unidad {n} — {titulo}\n\n[Ir a la unidad]({ruta})\n\n"
                "```python\n" + "\n".join(cheat) + "\n```\n\n"
                "**Errores comunes**\n\n" + "\n".join(f"- {e}" for e in errores)
            )
        )
    nb.cells.append(new_markdown_cell(indice))
    return nb


def glosario_nb(todas):
    nb = new_notebook()
    nb.cells = [
        new_markdown_cell(
            "# Glosario del curso\n\n[Inicio del curso](00-inicio.ipynb)\n\n"
            "Términos acumulados semana a semana, con la unidad donde se explican."
        )
    ]
    for num, cfg, datos in todas:
        partes = [f"## Semana {num} — {cfg['titulo']}"]
        for n, clase, ruta, titulo, _ in cfg["unidades"]:
            enlace = f"01-python/semana-{num:02d}/{ruta}"
            partes.append(f"### [Unidad {n} — {titulo}]({enlace})\n\n"
                          + "\n".join(f"- **{t}:** {d}" for t, d in datos[n][0]))
        nb.cells.append(new_markdown_cell("\n\n".join(partes)))
    return nb


def cargar(num):
    cfg = SEMANAS[num]
    if not cfg["unidades"]:
        cfg["unidades"] = unidades_desde_notebooks(num)
    datos = {n: leer_aporte(cfg["aportes"], n) for n, *_ in cfg["unidades"]}
    return cfg, datos


if __name__ == "__main__":
    num = int(sys.argv[1])
    cfg, datos = cargar(num)
    carpeta = carpeta_semana(num)
    nbformat.write(semana_nb(num, cfg, datos), carpeta / f"semana-{num:02d}.ipynb")
    nbformat.write(quiz_nb(num, cfg, datos), carpeta / archivo_semana(num, "quiz"))
    nbformat.write(repaso_nb(num, cfg, datos), carpeta / archivo_semana(num, "repaso"))
    todas = [(s, *cargar(s)) for s in sorted(SEMANAS)]  # all built weeks, so rebuilding an old one keeps the rest
    nbformat.write(glosario_nb(todas), RAIZ / "glosario.ipynb")
    print("ok", {n: [len(x) for x in d] for n, d in datos.items()})
    from actualizar_toc import actualizar_toc  # índice del sitio (myst.yml) con la semana ya construida

    actualizar_toc()
