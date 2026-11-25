"""Funciones de las semanas 5 y 6: programación dinámica, retroceso y pandas sobre los datos del proyecto.

Siguen los nombres y el estilo de las unidades del curso (u32 a u40). Los cargadores devuelven
objetos de pandas leídos de los CSV oficiales; nada de este módulo escribe archivos.
Los usan los notebooks s05 y s06.
"""
import pandas as pd

from penonome import COMPARACION, PAQUETE

# Paleta común de los gráficos del proyecto (azul, naranja, agua).
AZUL, NARANJA, AGUA = "#2a78d6", "#eb6834", "#1baf7a"
PALETA = (AZUL, NARANJA, AGUA)

MESES = (
    "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
    "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre",
)

# Réplicas acumuladas localizadas por el IGC-UP tras el sismo del 9-oct-2026, según la prensa
# (los mismos puntos de datos/analisis/replicas_acumuladas.csv). Son datos de prensa, no una tabla oficial.
REPLICAS = (
    ("2026-10-10", 135, "Panamá América"),
    ("2026-10-16", 746, "Infobae"),
    ("2026-11-02", 1271, "La Estrella"),
    ("2026-11-06", 1452, "Prensa Latina"),
    ("2026-11-09", 1483, "Crítica"),
    ("2026-11-17", 1656, "La Verdad"),
)

ORDEN_TRIMESTRES = ("abr-jun", "may-jul", "jun-ago", "jul-sep")
CLAVE_LARGA = ("provincia", "distrito", "corregimiento", "indicador", "unidad")


# --- Lectura (u35, u36) -------------------------------------------------------------------

def leer(nombre, carpeta=PAQUETE):
    """Lee un CSV del proyecto (UTF-8 con BOM) y devuelve un DataFrame."""
    return pd.read_csv(carpeta / nombre, encoding="utf-8-sig")


def poblacion_corregimientos():
    """Tabla 01 con id_corregimiento como índice."""
    return leer("01_censo2023_poblacion_corregimientos.csv").set_index("id_corregimiento")


def base_larga():
    """Tabla 99 con distrito y corregimiento vacíos como "" para que puedan formar parte de un índice."""
    larga = leer("99_base_larga_todo.csv")
    larga[["distrito", "corregimiento"]] = larga[["distrito", "corregimiento"]].fillna("")
    return larga


# --- Programación dinámica (u32) ------------------------------------------------------------

def maximum_subarray(S):
    """Mejor suma de valores consecutivos y las posiciones (inicio, fin) de ese tramo.

    Misma recurrencia de la u32: mejor_hasta = max(S[i], mejor_hasta + S[i]).
    """
    mejor_hasta, inicio_actual = S[0], 0
    mejor, inicio, fin = S[0], 0, 0
    for i in range(1, len(S)):
        if S[i] > mejor_hasta + S[i]:
            mejor_hasta, inicio_actual = S[i], i
        else:
            mejor_hasta = mejor_hasta + S[i]
        if mejor_hasta > mejor:
            mejor, inicio, fin = mejor_hasta, inicio_actual, i
    return mejor, inicio, fin


def golpe_restante(t, golpe, meses_media_vida, memo=None):
    """Parte del golpe que sigue presente t meses después, con memorización como fib_memo (u32).

    Recurrencia: G(0) = golpe; G(t) = G(t - 1) * 0.5 ** (1 / meses_media_vida).
    """
    if memo is None:
        memo = {0: golpe}
    if t in memo:
        return memo[t]
    memo[t] = golpe_restante(t - 1, golpe, meses_media_vida, memo) * 0.5 ** (1 / meses_media_vida)
    return memo[t]


def proyectar_desempleo(linea_base, golpe, meses_media_vida, meses):
    """Desempleo mes a mes: línea base más el golpe restante; todas las llamadas comparten la tabla memo."""
    memo = {0: golpe}
    return [linea_base + golpe_restante(t, golpe, meses_media_vida, memo) for t in range(meses)]


# --- Retroceso (u33) -------------------------------------------------------------------

def combinaciones_minimas(valores, objetivo):
    """Todas las combinaciones más pequeñas de posiciones cuyos valores suman al menos `objetivo`.

    Búsqueda en profundidad con poda: una rama se abandona si ni sumando todos los valores
    restantes llega al objetivo, o si ya necesitaría más elementos que la mejor encontrada.
    Devuelve (lista de tuplas de posiciones, número de nodos visitados).
    """
    orden = sorted(range(len(valores)), key=lambda i: valores[i], reverse=True)
    restante = [0] * (len(orden) + 1)
    for k in range(len(orden) - 1, -1, -1):
        restante[k] = restante[k + 1] + valores[orden[k]]
    mejores, tamanio = [], [len(valores) + 1]
    visitados = 0

    def promising(k, suma, elegidos):
        if len(elegidos) + 1 > tamanio[0]:
            return False
        return suma + restante[k] >= objetivo

    def buscar(k, suma, elegidos):
        nonlocal visitados
        visitados += 1
        if suma >= objetivo:
            if len(elegidos) < tamanio[0]:
                tamanio[0] = len(elegidos)
                mejores.clear()
            if len(elegidos) == tamanio[0]:
                mejores.append(tuple(sorted(elegidos)))
            return
        if k == len(orden) or not promising(k, suma, elegidos):
            return
        elegidos.append(orden[k])
        buscar(k + 1, suma + valores[orden[k]], elegidos)
        elegidos.pop()
        buscar(k + 1, suma, elegidos)

    buscar(0, 0, [])
    return sorted(mejores), visitados


# --- Datos ordenados (u37) ----------------------------------------------------------------------

def a_ancho(larga):
    """Tabla 99 larga -> ancha: una fila por indicador y una columna por fecha."""
    return larga.pivot(index=list(CLAVE_LARGA), columns="fecha", values="valor")


def a_largo(ancha):
    """Tabla ancha -> larga otra vez, sin las celdas vacías que creó el pivote."""
    larga = ancha.reset_index().melt(id_vars=list(CLAVE_LARGA), var_name="fecha", value_name="valor")
    return larga.dropna(subset=["valor"])


def ordenar_larga(larga):
    """Columnas clave y valor, ordenadas igual, para comparar dos tablas largas."""
    columnas = [*CLAVE_LARGA, "fecha", "valor"]
    return larga[columnas].sort_values(columnas[:-1]).reset_index(drop=True)


def eml_tidy():
    """Tabla 03 (una columna por periodo y sexo) como datos ordenados: area, indicador, valor, periodo, sexo."""
    ancha = leer("03_eml_condicion_actividad.csv")
    larga = ancha.melt(id_vars=["area", "indicador"], var_name="columna", value_name="valor")
    partes = larga["columna"].str.split("_", expand=True)
    larga["periodo"] = pd.to_datetime(partes[0].str[-4:] + "-" + partes[0].str[:3].map(
        {"oct": "10", "sep": "09"}), format="%Y-%m")
    larga["sexo"] = partes[1]
    return larga.drop(columns="columna")


# --- Series temporales (u38, u39) ---------------------------------------------------------------

def visitantes_mensuales():
    """Tabla 11 como DataFrame mensual (visitantes y divisas) con DatetimeIndex, 2024-2025."""
    ancha = leer("11_atp_visitantes_divisas_mensual.csv")
    ancha["num_mes"] = ancha["mes"].map({m: i for i, m in enumerate(MESES, start=1)})
    filas = []
    for anio in (2024, 2025):
        parte = pd.DataFrame({
            "fecha": pd.to_datetime({"year": anio, "month": ancha["num_mes"], "day": 1}),
            "visitantes": ancha[f"visitantes_{anio}"],
            "divisas_millones": ancha[f"divisas_{anio}_millones"],
        })
        filas.append(parte)
    return pd.concat(filas).set_index("fecha").sort_index()


def pib_anual():
    """Tabla 10 transpuesta: una fila por año (DatetimeIndex al cierre del año) y una columna por actividad."""
    pib = leer("10_pib_cocle_actividad_2018_2024.csv").set_index("actividad").T
    pib.index = pd.to_datetime(pib.index, format="%Y") + pd.offsets.YearEnd(0)
    pib.index.name = "anio"
    pib.columns.name = None
    return pib


def replicas():
    """Réplicas acumuladas como Serie con DatetimeIndex."""
    fechas = pd.to_datetime([fecha for fecha, _, _ in REPLICAS])
    return pd.Series([valor for _, valor, _ in REPLICAS], index=fechas, name="replicas_acumuladas")


def indice_base_100(datos):
    """Reescala una Serie o un DataFrame para que la primera fila valga 100."""
    return datos / datos.iloc[0] * 100


def variacion_pct(serie, periodos=1):
    """Cambio porcentual frente a `periodos` filas antes, con shift() como en la u39."""
    return (serie / serie.shift(periodos) - 1) * 100


def brecha_colombia():
    """Cambio medio del desempleo (pp) de las ciudades afectadas y de control por trimestre móvil."""
    geih = leer("20_colombia_geih_td_ciudades.csv", COMPARACION)
    grupos = geih[geih["grupo"].isin(["afectada", "control"])]
    tabla = grupos.groupby(["trimestre_movil", "grupo"])["cambio_pp"].mean().unstack()
    tabla = tabla.loc[list(ORDEN_TRIMESTRES)]
    tabla["brecha"] = tabla["afectada"] - tabla["control"]
    tabla.columns.name = None
    return tabla


# --- Gráficos (u35, u38, u40) ---------------------------------------------------------------

def estilo_eje(ax, titulo, xlabel, ylabel, fuente):
    """Estilo común: título a la izquierda, nombres de ejes, cuadrícula suave y línea de fuente al pie."""
    ax.set_title(titulo, loc="left", fontsize=12, fontweight="bold")
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.grid(True, axis="y", color="#e1e0d9", linewidth=0.6)
    ax.set_axisbelow(True)
    for lado in ("top", "right"):
        ax.spines[lado].set_visible(False)
    ax.figure.text(0.01, 0.005, f"Fuente: {fuente}", fontsize=8, color="#52514e")
    ax.figure.tight_layout(rect=(0, 0.04, 1, 1))
