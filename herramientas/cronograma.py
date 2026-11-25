"""Cronograma oficial SIC 2026 (fuente: recursos/cronograma-sic-2026.jpg).

Única fuente de datos para generar el índice del curso y el esqueleto de cada semana.
"""

MODULOS = {
    "01-python": "Python",
    "02-ia": "Inteligencia Artificial",
    "03-ia-generativa": "IA Generativa",
}

# (semana, fechas, capítulos / actividad, contenido)
SEMANAS = [
    (0, "Previa al inicio del programa", "Capítulo 1",
     "Semana preparatoria: pensamiento computacional, algoritmos, Python, variables, operadores, condicionales y bucles"),
    (1,"12/10/2026 – 17/10/2026", "Capítulo 2",
     "Conceptos básicos de programación e iniciación con Python / Programación básica de Python - Secuencia de datos escrita en Python"),
    (2, "19/10/2026 – 24/10/2026", "Capítulo 3",
     "Programación efectiva con Python - Function, Closure y Clases"),
    (3, "26/10/2026 – 31/10/2026", "Capítulo 4",
     "Algoritmos de clasificación 1. Pilas, colas, búsqueda secuencial/binaria, tablas hash"),
    (4, "2/11/2026 – 7/11/2026", "Capítulo 5, Capítulo 6",
     "Estructuras de datos / Algoritmos de clasificación / Resolución de problemas con algoritmos"),
    (5, "9/11/2026 – 14/11/2026", "Capítulo 6, Capítulo 7",
     "Algoritmo 2 - Resolución de problemas con algoritmos / Procesamiento de datos, estadísticas descriptivas y visualización de datos"),
    (6, "16/11/2026 – 21/11/2026", "Capítulo 7, Capítulo 8",
     "Procesamiento de datos, estadísticas descriptivas y visualización de datos / Mini proyecto de análisis y visualización de datos"),
    (7, "23/11/2026 – 28/11/2026", "Desarrollo Proyecto Python", "Desarrollo de proyectos"),
    (8, "30/11/2026 – 5/12/2026", "PROYECTO PYTHON", "Entrega del Proyecto Python"),
    (9, "7/12/2026 – 12/12/2026", "Capítulo 1, Capítulo 2",
     "(Cap. 1) Introducción a IA / (Cap. 2) Matemática básica para ciencias de datos / (Cap. 3) Análisis exploratorio de datos (P1)"),
    (10, "14/12/2026 – 19/12/2026", "Capítulo 3, Capítulo 4, Capítulo 5",
     "Probabilidad y estadística / Machine Learning / Aprendizaje supervisado"),
    (11, "21/12/2026 – 26/12/2026", "Capítulo 5", "Machine Learning / Aprendizaje supervisado"),
    (12, "28/12/2026 – 2/1/2027", "Capítulo 5 y 6", "Machine Learning / Aprendizaje no supervisado"),
    (13, "4/1/2027 – 9/1/2027", "Capítulo 6 y 7",
     "Procesamiento del lenguaje natural y modelos lingüísticos: para la minería de textos"),
    (14, "11/1/2027 – 16/1/2027", "Capítulo 7 y 8", "Fundamentos de las redes neuronales, Deep Learning"),
    (15, "18/1/2027 – 23/1/2027", "Capítulo 8 y 9", "Fundamentos de las redes neuronales, Deep Learning"),
    (16, "25/1/2027 – 30/1/2027", "Capítulo 10 y 11",
     "Tutorial del proyecto final de IA e inicio de un proyecto de IA"),
    (17, "1/2/2027 – 6/2/2027", "Desarrollo Proyecto IA", "Desarrollo de proyectos"),
    (18, "8/2/2027 – 13/2/2027", "PROYECTO IA", "Entrega del Proyecto IA"),
    (19, "15/2/2027 – 20/2/2027", "Capítulo 1, Capítulo 2",
     "Introducción a la IA Generativa / Conceptos básicos de ingeniería de prompts"),
    (20, "22/2/2027 – 26/2/2027", "Capítulo 2, Capítulo 3", "Conceptos básicos de ingeniería de prompts"),
    (21, "1/3/2027 – 5/3/2027", "Capítulo 4", "Ética y responsabilidad de la IA"),
    (22, "8/3/2027 – 12/3/2027", "PROYECTO FINAL MINI HANDS PROJECT",
     "Semana de desarrollo del proyecto final Mini Hands Project"),
    (23, "15/3/2027 – 19/3/2027", "Semana preparativa Hackathon", "Semana de preparación al Hackathon"),
    (24, "22/3/2027 – 26/3/2027", "Cierre del programa", "Semana del Hackathon"),
]


def modulo_de(semana: int) -> str:
    """Devuelve la carpeta del módulo al que pertenece una semana."""
    if semana <= 8:
        return "01-python"
    if semana <= 18:
        return "02-ia"
    return "03-ia-generativa"


def carpeta_de(semana: int) -> str:
    """Ruta relativa a la raíz del curso de la carpeta de una semana."""
    return f"{modulo_de(semana)}/semana-{semana:02d}"


def archivo_semana(semana: int, nombre: str) -> str:
    """Nombre de un notebook propio de la semana, por ejemplo quiz.ipynb.

    No lleva prefijo: el sitio usa `folders: true` (myst.yml), así que la dirección ya incluye la carpeta de la
    semana (/python/semana-01/quiz/). Se centraliza aquí para cambiar el esquema en un solo lugar.
    """
    return f"{nombre}.ipynb"


def datos_de(semana: int) -> tuple:
    """Devuelve la fila del cronograma de una semana."""
    for fila in SEMANAS:
        if fila[0] == semana:
            return fila
    raise ValueError(f"La semana {semana} no está en el cronograma")
