"""Cargadores de los CSV del paquete con el módulo csv (sin pandas).

Cada función devuelve una lista de diccionarios, una fila por diccionario, con los
números ya convertidos. Las usan los notebooks de las semanas 1 y 2.
"""
import csv

from penonome import FUENTES, PAQUETE

# Ley 296 de 26-abr-2022 (nota 53 del Cuadro 4 del Censo 2023):
# corregimiento original -> corregimientos nuevos creados a partir de él.
PADRES_LEY_296 = {
    "chiguiri_arriba": ("candelario_ovalle",),
    "pajonal": ("general_victoriano_lorenzo",),
    "rio_indio": ("riecito",),
    "toabre": ("boca_de_tucue", "san_miguel"),
    "tulu": ("las_minas",),
}


def a_numero(texto):
    """Convierte el texto de una celda en int o float; devuelve None si está vacía.

    Los valores enteros, aunque estén escritos como "15841.0", se devuelven como int.
    Si el texto no es un número, se devuelve tal cual.
    """
    texto = texto.strip()
    if texto == "":
        return None
    try:
        numero = float(texto)
    except ValueError:
        return texto
    if numero.is_integer():
        return int(numero)
    return numero


def leer_csv(ruta, numericas=()):
    """Lee un CSV en UTF-8 con BOM y devuelve una lista de diccionarios.

    Las columnas nombradas en `numericas` se convierten con `a_numero`.
    """
    with open(ruta, encoding="utf-8-sig", newline="") as archivo:
        filas = list(csv.DictReader(archivo))
    for fila in filas:
        for columna in numericas:
            fila[columna] = a_numero(fila[columna])
    return filas


def cargar_catalogo():
    """Tabla 00: los 16 corregimientos con su clave y la nota de cambio de límites."""
    return leer_csv(PAQUETE / "00_catalogo_corregimientos.csv")


def cargar_poblacion():
    """Tabla 01: superficie y población 2000, 2010 y 2023 por corregimiento."""
    return leer_csv(
        PAQUETE / "01_censo2023_poblacion_corregimientos.csv",
        numericas=("superficie_km2", "pob_2000", "pob_2010", "pob_2023", "densidad_2023"),
    )


def cargar_viviendas(nivel=None):
    """Tabla 02: viviendas y población con características (Censo 2023, Cuadro 1).

    `nivel` filtra las filas: "corregimiento", "distrito" o "provincia".
    Sin `nivel` se devuelven todas.
    """
    ruta = PAQUETE / "02_censo2023_viviendas_caracteristicas.csv"
    with open(ruta, encoding="utf-8-sig", newline="") as archivo:
        encabezado = next(csv.reader(archivo))
    texto = ("id_corregimiento", "nivel", "area")
    numericas = [columna for columna in encabezado if columna not in texto]
    filas = leer_csv(ruta, numericas=numericas)
    if nivel is None:
        return filas
    return [fila for fila in filas if fila["nivel"] == nivel]


def cargar_condicion_actividad():
    """Tabla 03: condición de actividad de la EML (República y Coclé), oct-2024 y sep-2025."""
    columnas = (
        "oct2024_total", "oct2024_hombres", "oct2024_mujeres",
        "sep2025_total", "sep2025_hombres", "sep2025_mujeres",
    )
    return leer_csv(PAQUETE / "03_eml_condicion_actividad.csv", numericas=columnas)


def cargar_informalidad():
    """Tabla 06: empleo informal no agrícola, República y Coclé."""
    columnas = (
        "ocupada_no_agricola", "empleo_informal", "en_empresas_formales",
        "en_empresas_informales", "en_hogares", "pct_informal",
    )
    return leer_csv(PAQUETE / "06_eml_informalidad.csv", numericas=columnas)


def cargar_pib():
    """Tabla 10: PIB de Coclé por actividad, 2018 a 2024 (millones de B/.)."""
    anios = tuple(str(anio) for anio in range(2018, 2025))
    return leer_csv(PAQUETE / "10_pib_cocle_actividad_2018_2024.csv", numericas=anios)


def cargar_base_larga():
    """Tabla 99: todas las tablas en formato largo, una fila por dato."""
    return leer_csv(PAQUETE / "99_base_larga_todo.csv", numericas=("valor",))


def cargar_fuentes():
    """fuentes.csv: cada fuente del estudio una sola vez."""
    return leer_csv(FUENTES)
