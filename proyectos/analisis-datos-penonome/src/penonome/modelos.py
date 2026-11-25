"""Clases del proyecto (semana 2, unidad 21): Corregimiento, CorregimientoNuevo y Fuente."""
from penonome.carga import PADRES_LEY_296, cargar_fuentes, cargar_ipm, cargar_poblacion, cargar_viviendas


class Corregimiento:
    """Un corregimiento del distrito de Penonomé con sus datos censales."""

    distrito = "Penonomé"  # variable de clase: la comparten todas las instancias
    total_creados = 0

    def __init__(self, id_corregimiento, nombre, superficie_km2, poblacion, viviendas=None, ipm=None):
        self.id_corregimiento = id_corregimiento
        self.nombre = nombre
        self.superficie_km2 = superficie_km2
        self.poblacion = dict(poblacion)  # {anio: personas}, solo los censos con dato
        self.viviendas = dict(viviendas or {})  # columnas de la tabla 02
        self.ipm = dict(ipm or {})  # columnas de la tabla 03 (pobreza multidimensional, PNUD)
        Corregimiento.total_creados += 1

    def poblacion_en(self, anio=2023):
        """Población del censo `anio`, o None si no hay dato."""
        return self.poblacion.get(anio)

    def densidad(self, anio=2023):
        """Habitantes por km² en el censo `anio`, redondeado a un decimal."""
        habitantes = self.poblacion_en(anio)
        if habitantes is None:
            return None
        return round(habitantes / self.superficie_km2, 1)

    def crecimiento(self, desde=2010, hasta=2023):
        """Crecimiento porcentual de la población entre dos censos, a un decimal."""
        inicio, fin = self.poblacion_en(desde), self.poblacion_en(hasta)
        if inicio is None or fin is None:
            return None
        return round((fin / inicio - 1) * 100, 1)

    def porcentaje_viviendas(self, columna):
        """Porcentaje de viviendas que cumplen `columna` (por ejemplo "sin_internet")."""
        return round(self.viviendas[columna] / self.viviendas["viviendas"] * 100, 1)

    def tasa_analfabetismo(self):
        """Analfabetas / población de 10 años y más del Censo 2023, en porcentaje."""
        return round(self.viviendas["analfabeta"] / self.viviendas["pob_10mas"] * 100, 1)

    def incidencia_pobreza(self):
        """Porcentaje de personas en pobreza multidimensional (incidencia H del PNUD), o None."""
        return self.ipm.get("incidencia_h")

    def __str__(self):
        return f"{self.nombre}: {self.poblacion_en(2023):,} habitantes en 2023"

    def __repr__(self):
        return f"Corregimiento({self.id_corregimiento!r})"

    def __lt__(self, otro):
        """Permite ordenar corregimientos por su población de 2023."""
        return self.poblacion_en(2023) < otro.poblacion_en(2023)


class CorregimientoNuevo(Corregimiento):
    """Corregimiento creado por la Ley 296 de 2022: sin datos comparables antes de 2023."""

    def __init__(self, id_corregimiento, nombre, superficie_km2, poblacion, viviendas=None,
                 padre=None, ipm=None):
        super().__init__(id_corregimiento, nombre, superficie_km2, poblacion, viviendas, ipm)
        self.padre = padre  # id del corregimiento del que se separó

    def crecimiento(self, desde=2010, hasta=2023):
        """No existe en 2010: el crecimiento no se puede calcular por sí solo."""
        return None

    def __repr__(self):
        return f"CorregimientoNuevo({self.id_corregimiento!r}, padre={self.padre!r})"


class Fuente:
    """Una fuente del estudio (una fila de fuentes.csv)."""

    TIPOS_OFICIALES = ("oficial", "organismo")

    def __init__(self, id_fuente, institucion, titulo, url, tipo, estado="sin revisar"):
        self.id_fuente = id_fuente
        self.institucion = institucion
        self.titulo = titulo
        self.url = url
        self.tipo = tipo
        self.estado = estado

    def es_oficial(self):
        """True si la fuente es estadística oficial o de un organismo internacional."""
        return self.tipo in Fuente.TIPOS_OFICIALES

    def esta_verificada(self):
        """True si la fuente se cotejó (estado "ok")."""
        return self.estado == "ok"

    def dominio(self):
        """Dominio de la URL, por ejemplo "www.inec.gob.pa"."""
        return self.url.split("//")[-1].split("/")[0]

    def __str__(self):
        return f"[{self.id_fuente}] {self.institucion}: {self.titulo}"

    def __repr__(self):
        return f"Fuente({self.id_fuente!r}, tipo={self.tipo!r})"


def padre_de(id_corregimiento):
    """Devuelve el corregimiento original de un corregimiento nuevo, o None."""
    for padre, hijos in PADRES_LEY_296.items():
        if id_corregimiento in hijos:
            return padre
    return None


def crear_corregimientos():
    """Crea un objeto por corregimiento uniendo las tablas 01, 02 y 03 por id_corregimiento."""
    viviendas = {fila["id_corregimiento"]: fila for fila in cargar_viviendas("corregimiento")}
    ipm = {fila["id_corregimiento"]: fila for fila in cargar_ipm()}
    corregimientos = []
    for fila in cargar_poblacion():
        clave = fila["id_corregimiento"]
        poblacion = {
            anio: fila[f"pob_{anio}"]
            for anio in (2000, 2010, 2023)
            if fila[f"pob_{anio}"] is not None
        }
        datos = (clave, fila["corregimiento"], fila["superficie_km2"], poblacion, viviendas[clave])
        padre = padre_de(clave)
        if padre is None:
            corregimientos.append(Corregimiento(*datos, ipm=ipm.get(clave)))
        else:
            corregimientos.append(CorregimientoNuevo(*datos, padre=padre, ipm=ipm.get(clave)))
    return corregimientos


def crear_fuentes():
    """Crea un objeto Fuente por fila de fuentes.csv."""
    return [
        Fuente(f["id"], f["institucion"], f["titulo"], f["url"], f["tipo"], f["estado"])
        for f in cargar_fuentes()
    ]
