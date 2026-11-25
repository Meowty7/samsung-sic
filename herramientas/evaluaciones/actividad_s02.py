"""Genera 01-python/semana-02/actividad-asincronica.ipynb y prueba cada respuesta."""

import builtins
import contextlib
import io
import os
import random
import tempfile
from pathlib import Path

import nbformat
from nbformat.v4 import new_code_cell, new_markdown_cell, new_notebook, new_output

RAIZ = Path(__file__).resolve().parents[2]
DESTINO = RAIZ / "01-python/semana-02/actividad-asincronica.ipynb"
C1 = "clase-1-funciones-recursividad-lambda"
C2 = "clase-2-ambito-clausuras-y-clases"
U = {
    11: "../semana-01/clase-1-listas-tuplas-diccionarios/u11-diccionarios-y-json.ipynb",
    13: "../semana-01/clase-1-listas-tuplas-diccionarios/u13-listas-bidimensionales.ipynb",
    17: f"{C1}/u17-funciones.ipynb",
    18: f"{C1}/u18-recursividad.ipynb",
    19: f"{C1}/u19-lambda-filter-map-reduce.ipynb",
    20: f"{C2}/u20-ambito-y-clausuras.ipynb",
}


def unidad(*nums):
    return ", ".join(f"[Unidad {n}]({U[n]})" for n in nums)


SETUP_ACT3 = '''import os
import random

def guardar_archivo(text_content, file_path):
    with open(file_path, 'w') as file:
        # Write the text content to the file
        file.write(text_content)


if os.path.exists("Carpeta_principal"):
    os.system(f'rm -r "Carpeta_principal"')

os.mkdir("Carpeta_principal")
# Inicialización



def crear_carpetas(ruta_actual):
    global numeracion_del_archivo, numero_de_sub_carpetas
    numero_de_archivos_o_carpetas = random.randint(0,15) # genración de numero aleatorio entre 0 y 15.
    print(ruta_actual)
    if numero_de_sub_carpetas < max_carpetas:
        for n in range(0, numero_de_archivos_o_carpetas):

            numero_aleatorio_2 = random.randint(0,2) # número aleatoria entre 0 y 1.
            if numero_aleatorio_2 == 0:
                os.mkdir(ruta_actual +'/'+ 'folder_{}'.format(n) )
                print(ruta_actual +'/'+ 'folder_{}'.format(n))
            else:
                contenido_del_archivo = "Contenido_{}".format(numeracion_del_archivo)
                ruta_del_archivo = ruta_actual + '/' + "archivo_{}.text".format(numeracion_del_archivo)
#                 print("ruta_del_archivo: ", ruta_del_archivo)
                guardar_archivo(contenido_del_archivo, ruta_del_archivo)
                numeracion_del_archivo += 1

        lista_de_nuevas_carpetas = [f.path for f in os.scandir(ruta_actual) if f.is_dir()] # Busqueda de nueva carpeta

        numero_de_sub_carpetas += 1
        for carpeta in lista_de_nuevas_carpetas:
            crear_carpetas(carpeta)

max_carpetas = 4
numeracion_del_archivo = 0
numero_de_sub_carpetas = 0
ruta_actual = "Carpeta_principal"
crear_carpetas(ruta_actual)'''

# (titulo, consigna, guia, [(etiqueta, codigo)], explicacion)
ACTIVIDADES = [
    ("Actividad 1 — Creación de funciones",
     "1. Defina en forma breve el concepto de función.\n"
     "2. Cree una función para realizar la suma de los números impares en el rango de 0 a 100; dentro de la "
     "función imprima los valores sumados y al final retorne el resultado de la sumatoria.",
     f"**Dónde se ve:** {unidad(17)} (`def`, parámetros, `return`).",
     [("Respuesta", '''# Concepto: una función es un bloque de código con nombre que realiza una tarea concreta.
# Se define una vez con def, puede recibir datos (parámetros) y devolver un resultado con
# return, y se reutiliza llamándola las veces que haga falta.

def suma_impares(inicio=0, fin=100):
    """Suma los números impares entre inicio y fin (incluido) e imprime cada uno."""
    total = 0
    for numero in range(inicio, fin + 1):
        if numero % 2 != 0:          # impar: el resto de dividir entre 2 no es 0
            print(numero, end=" ")   # valores que se van sumando
            total += numero
    print()                          # salto de línea al terminar la lista
    return total                     # resultado de la sumatoria


resultado = suma_impares()
print("Suma de los impares de 0 a 100:", resultado)''')],
     "Los impares de 0 a 100 son 1, 3, ..., 99 (50 números) y suman **2500**. `print` dentro de la función "
     "muestra los valores; `return` entrega el total a quien la llamó, que lo guarda en `resultado`."),

    ("Actividad 2 — Funciones para codificar y decodificar strings",
     "Diseñe una función para codificar strings y otra para decodificarlos.\n\n"
     "- Revise documentación sobre encriptación y explique brevemente cómo funciona.\n"
     "- Ambas funciones reciben un string y una \"clave\"; la clave se usa para codificar y decodificar.\n"
     "- La actividad admite múltiples soluciones: sea original.",
     f"**Dónde se ve:** {unidad(17)} (el proyecto de la unidad es el cifrado César).\n\n"
     "**Idea:** la solución combina tres piezas: la clave se repite a lo largo del mensaje (como en el cifrado "
     "Vigenère), cada byte se mezcla con un byte de la clave usando XOR, y el resultado se pasa a Base64 para que "
     "sea texto imprimible. Funciona con tildes, ñ y cualquier carácter.",
     [("Respuesta", '''# Cómo funciona la encriptación (resumen):
# Encriptar es transformar un mensaje legible (texto plano) en uno ilegible (texto cifrado)
# usando un algoritmo y una clave. Solo quien conoce la clave puede revertir el proceso.
# Cuando la misma clave sirve para cifrar y descifrar, se llama cifrado simétrico
# (por ejemplo César, Vigenère o AES). Aquí se usa XOR: aplicar XOR dos veces con la
# misma clave devuelve el valor original, (a ^ k) ^ k == a, por eso una sola operación
# sirve para codificar y decodificar.

import base64


def _mezclar_con_clave(datos, clave):
    """Aplica XOR byte a byte entre los datos y la clave repetida (estilo Vigenère)."""
    bytes_clave = clave.encode("utf-8")
    return bytes(b ^ bytes_clave[i % len(bytes_clave)] for i, b in enumerate(datos))


def codificar(texto, clave):
    """Devuelve el texto cifrado con la clave, en Base64 para que sea imprimible."""
    if not clave:
        raise ValueError("La clave no puede estar vacía.")
    mezclado = _mezclar_con_clave(texto.encode("utf-8"), clave)
    return base64.b64encode(mezclado).decode("ascii")


def decodificar(texto_cifrado, clave):
    """Revierte codificar(): Base64 -> XOR con la misma clave -> texto original."""
    if not clave:
        raise ValueError("La clave no puede estar vacía.")
    mezclado = base64.b64decode(texto_cifrado)
    return _mezclar_con_clave(mezclado, clave).decode("utf-8")


mensaje = "Nos vemos en la biblioteca a las 3. ¡No faltes!"
clave = "Samsung2026"

cifrado = codificar(mensaje, clave)
print("Original:   ", mensaje)
print("Codificado: ", cifrado)
print("Decodificado:", decodificar(cifrado, clave))

# Con una clave incorrecta no se recupera el mensaje
try:
    intento = decodificar(cifrado, "otra-clave")
except UnicodeDecodeError:
    intento = None   # los bytes resultantes ni siquiera forman un texto válido
print("¿Se recupera con una clave incorrecta?", intento == mensaje)''')],
     "`codificar` y `decodificar` reciben un string y una clave, como pide la consigna. La misma clave produce "
     "siempre el mismo cifrado y lo revierte; con otra clave el resultado es ilegible o inválido. "
     "**Aclaración:** XOR con una clave corta sirve para aprender, pero no es seguro para datos reales; en la "
     "práctica se usan algoritmos como AES."),

    ("Actividad 3 — Función que recorre carpetas",
     "Diseñe una función que revise el contenido de una carpeta: debe revisar todas las carpetas existentes y "
     "obtener los nombres de los archivos contenidos. Dentro de cada carpeta pueden existir otras carpetas, y "
     "todas deben ser revisadas. La celda de la plataforma crea las carpetas y los archivos. Es posible que "
     "deba usar una función recursiva.",
     f"**Dónde se ve:** {unidad(18)} (recursividad: caso base y llamada recursiva).\n\n"
     "**Orden en la plataforma:** primero se ejecuta la celda que ya viene (crea `Carpeta_principal`) y después "
     "la respuesta. La estructura es aleatoria: cada ejecución crea otra cantidad de archivos.",
     [("Código de la plataforma (crea las carpetas)", SETUP_ACT3),
      ("Respuesta", '''import os


def listar_archivos(ruta):
    """Devuelve la ruta de todos los archivos dentro de ruta, revisando cada subcarpeta.

    Es recursiva: si encuentra una carpeta, se llama a sí misma con esa carpeta.
    El caso base es una carpeta sin subcarpetas: solo devuelve sus archivos.
    """
    archivos = []
    for nombre in sorted(os.listdir(ruta)):
        ruta_completa = os.path.join(ruta, nombre)
        if os.path.isdir(ruta_completa):
            archivos.extend(listar_archivos(ruta_completa))   # llamada recursiva
        else:
            archivos.append(ruta_completa)
    return archivos


archivos = listar_archivos("Carpeta_principal")
for ruta in archivos:
    print(os.path.basename(ruta), "->", ruta)
print("Total de archivos encontrados:", len(archivos))

# Comprobación con os.walk, que recorre todo el árbol sin recursión explícita
total_walk = sum(len(nombres) for _, _, nombres in os.walk("Carpeta_principal"))
print("Comprobación con os.walk:", total_walk)''')],
     "`listar_archivos` revisa cada elemento de la carpeta: si es archivo lo guarda y si es carpeta se llama a sí "
     "misma, así llega a cualquier profundidad. Al final se compara el total con `os.walk`, que debe dar lo mismo. "
     "La salida de arriba corresponde a una ejecución de prueba; en la plataforma los nombres y la cantidad cambian "
     "porque las carpetas se crean al azar."),

    ("Actividad 4 — Crear diccionarios y guardarlos como archivo JSON",
     "De la unidad 11, sección 4.6, revise el ejemplo. Genere un diccionario con la información que desee guardar "
     "como base de datos, el código para generar el archivo JSON y el código para cargar la información del archivo.",
     f"**Dónde se ve:** {unidad(11)} (JSON: `json.dump` y `json.load`).",
     [("Respuesta", '''import json

# Diccionario con la información a guardar: inventario de una tienda
inventario = {
    "tienda": "Minisúper La Esquina",
    "productos": [
        {"codigo": "P001", "nombre": "Café molido", "precio": 4.25, "stock": 30},
        {"codigo": "P002", "nombre": "Azúcar 1 kg", "precio": 1.10, "stock": 50},
        {"codigo": "P003", "nombre": "Leche entera", "precio": 1.35, "stock": 24},
    ],
}

# Guardar el diccionario en un archivo JSON
with open("inventario.json", "w", encoding="utf-8") as archivo:
    json.dump(inventario, archivo, ensure_ascii=False, indent=2)
print("Archivo inventario.json creado.")

# Cargar la información desde el archivo JSON
with open("inventario.json", "r", encoding="utf-8") as archivo:
    datos = json.load(archivo)

print("Tienda:", datos["tienda"])
for producto in datos["productos"]:
    print(f"{producto['codigo']} | {producto['nombre']:<13} | ${producto['precio']:.2f} | stock {producto['stock']}")

valor_total = sum(p["precio"] * p["stock"] for p in datos["productos"])
print(f"Valor total del inventario: ${valor_total:.2f}")''')],
     "`json.dump` escribe el diccionario en el archivo y `json.load` lo lee de vuelta como diccionario de Python. "
     "`ensure_ascii=False` conserva las tildes e `indent=2` deja el archivo legible."),

    ("Actividad 5 — Uso de la función lambda",
     "1. Escriba una función regular donde se realice una operación.\n"
     "2. Escriba la misma función usando una expresión lambda.\n"
     "3. Explique brevemente las ventajas de usar la función lambda.",
     f"**Dónde se ve:** {unidad(19)} (sintaxis de la función regular frente a lambda).",
     [("Respuesta", '''# 1. Función regular: calcula el precio con impuesto (7 %)
def precio_con_impuesto(precio):
    return round(precio * 1.07, 2)


# 2. La misma operación con una expresión lambda
precio_con_impuesto_lambda = lambda precio: round(precio * 1.07, 2)

print(precio_con_impuesto(100))         # 107.0
print(precio_con_impuesto_lambda(100))  # 107.0

# Donde lambda resulta más útil: como argumento de otra función, sin definirla aparte
precios = [100, 25.5, 10]
print(list(map(lambda p: round(p * 1.07, 2), precios)))      # aplicar a cada precio
print(sorted(["kiwi", "uva", "banano"], key=lambda f: len(f)))  # ordenar por longitud

# 3. Ventajas de lambda:
# - Es concisa: una operación simple se escribe en una sola línea.
# - Se puede escribir justo donde se usa, como argumento de map, filter, sorted o reduce,
#   sin tener que crear y nombrar una función aparte que solo se usa una vez.
# - Hace el código más legible cuando la operación es corta.
# Límite: solo admite una expresión; para lógica con varias líneas conviene def.''')],
     "Las dos versiones dan el mismo resultado. La ventaja de lambda aparece al pasarla directamente a `map` o "
     "`sorted`: la operación queda escrita en el mismo lugar donde se usa."),

    ("Actividad Extra Point — Duplicar valores con map",
     "1. Describa brevemente el funcionamiento y las ventajas de usar la función `map`.\n"
     "2. Escriba el código para duplicar el valor de cada uno de los elementos.\n\n"
     "Es opcional: solo suma (hasta 20 puntos) si la nota es menor que 50.",
     f"**Dónde se ve:** {unidad(19)} (`map`).",
     [("Respuesta", '''# Funcionamiento: map(funcion, iterable) aplica la función a cada elemento del iterable
# y devuelve un objeto map (un iterador) con los resultados; se convierte con list().
# Ventajas: evita escribir el bucle y el append a mano, deja el código más corto y claro,
# combina bien con lambda y procesa los elementos a medida que se necesitan.

numeros = [1, 2, 3, 4, 5, 10, 25]

duplicados = list(map(lambda x: x * 2, numeros))
print("Original:  ", numeros)
print("Duplicados:", duplicados)

# Equivalente con un bucle, para comparar
con_bucle = []
for x in numeros:
    con_bucle.append(x * 2)
print("Con bucle: ", con_bucle)''')],
     "`map` aplica `lambda x: x * 2` a cada número; el resultado es igual al del bucle, pero en una sola línea."),
]


def ejecutar(bloques):
    """Ejecuta los bloques en orden, en una carpeta temporal compartida; devuelve la salida de cada uno."""
    previo = os.getcwd()
    salidas = []
    entorno = {"__name__": "__main__"}
    with tempfile.TemporaryDirectory() as tmp:
        os.chdir(tmp)
        random.seed(7)   # estructura de carpetas reproducible para la salida de ejemplo
        try:
            for codigo in bloques:
                buffer = io.StringIO()
                with contextlib.redirect_stdout(buffer):
                    exec(compile(codigo, "<respuesta>", "exec"), entorno)
                salidas.append(buffer.getvalue())
        finally:
            os.chdir(previo)
    return salidas


celdas = [new_markdown_cell(
    "# Actividad asincrónica — Semana 2\n\n"
    "**Capítulo 3: función, clausura y clase** (unidades 17 a 21)\n\n"
    "[Índice de la semana](semana-02.ipynb)\n\n"
    "## Estado\n\n**Entregada. Nota final: 100/100.**\n\n"
    "## Cómo se califica\n\n"
    "- Se responden 5 de las 6 preguntas, de 20 puntos cada una (100).\n"
    "- La pregunta adicional (Extra Point) es opcional: si la nota es menor que 50, suma hasta 20 puntos. "
    "La nota máxima es 100.\n"
    "- Se puede retomar una vez si se entregó por error; la nota de la nueva entrega es la que cuenta.\n\n"
    "## Cómo usar este notebook\n\n"
    "Cada actividad trae la consigna, la unidad donde se explica, la **respuesta resuelta** (ya ejecutada, con su "
    "salida) y una explicación. Para entregar, copia el código de la respuesta en el recuadro de la plataforma y "
    "pulsa «Ejecutar». Aquí están respondidas las 6: conviene entregarlas todas.\n\n"
    "## Checklist de entrega\n\n" + "\n".join(f"- [x] {a[0]}" for a in ACTIVIDADES)
    + "\n- [x] Revisar todo y pulsar «Entregar»"
)]

numero = 0
for titulo, consigna, guia, bloques, explicacion in ACTIVIDADES:
    salidas = ejecutar([codigo for _, codigo in bloques])
    celdas.append(new_markdown_cell(f"## {titulo}\n\n### Consigna\n\n{consigna}\n\n### Guía\n\n{guia}"))
    for (etiqueta, codigo), salida in zip(bloques, salidas):
        print(f"--- {titulo} / {etiqueta}\n{salida.rstrip()[-600:]}")
        numero += 1
        celdas.append(new_markdown_cell(f"### {etiqueta}"))
        celdas.append(new_code_cell(codigo, execution_count=numero,
                                    outputs=[new_output("stream", name="stdout", text=salida)]))
    celdas.append(new_markdown_cell("**Explicación:** " + explicacion))

celdas.append(new_markdown_cell("[Índice de la semana](semana-02.ipynb)"))
nb = new_notebook()
nb.cells = celdas
nbformat.write(nb, DESTINO)
print("Escrito:", DESTINO)
