"""Funciones de las semanas 5 y 6: programación dinámica, retroceso y pandas sobre los datos del proyecto.

Siguen los nombres y el estilo de las unidades del curso (u32 a u40). Los cargadores devuelven
objetos de pandas leídos de los CSV oficiales; nada de este módulo escribe archivos.
Los usan los notebooks s05 y s06.
"""
import pandas as pd

from penonome import ANALISIS, PAQUETE

# Paleta común de los gráficos del proyecto (azul, naranja, agua).
AZUL, NARANJA, AGUA = "#2a78d6", "#eb6834", "#1baf7a"
PALETA = (AZUL, NARANJA, AGUA)

MESES = (
    "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
    "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre",
)

CLAVE_LARGA = ("provincia", "distrito", "corregimiento", "indicador", "unidad")


# --- Lectura (u35, u36) -------------------------------------------------------------------

def leer(nombre, carpeta=PAQUETE):
    """Lee un CSV del proyecto (UTF-8 con BOM) y devuelve un DataFrame."""
    return pd.read_csv(carpeta / nombre, encoding="utf-8-sig")


def poblacion_corregimientos():
    """Tabla 01 con id_corregimiento como índice."""
    return leer("01_censo2023_poblacion_corregimientos.csv").set_index("id_corregimiento")


def afectaciones():
    """Afectaciones del sismo en Coclé (EDAN de SINAPROC) como DataFrame en formato largo."""
    return leer("afectaciones_sinaproc_cocle.csv", ANALISIS)


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



def mochila_01(valores, costos, capacidad):
    """Mochila 0/1 con memorización: el mayor valor total que cabe en `capacidad`.

    Recurrencia (misma idea de `fib_memo` en la u32): mejor(i, cap) es el mayor valor usando solo
    los elementos desde la posición i con `cap` de capacidad restante:
    mejor(i, cap) = max(mejor(i + 1, cap), valores[i] + mejor(i + 1, cap - costos[i])).
    Cada par (i, cap) se calcula una vez y se guarda en `memo`.
    Los costos deben ser enteros positivos. Devuelve (mejor valor, posiciones elegidas, memo).
    """
    memo = {}

    def mejor(i, cap):
        if i == len(valores):
            return 0
        if (i, cap) not in memo:
            sin = mejor(i + 1, cap)
            con = valores[i] + mejor(i + 1, cap - costos[i]) if costos[i] <= cap else -1
            memo[(i, cap)] = max(sin, con)
        return memo[(i, cap)]

    total = mejor(0, capacidad)
    elegidos, cap = [], capacidad
    for i in range(len(valores)):
        if mejor(i, cap) != mejor(i + 1, cap):       # si no da lo mismo sin i, se tomó i
            elegidos.append(i)
            cap -= costos[i]
    return total, elegidos, memo






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
    larga = larga.dropna(subset=["valor"])
    larga["fecha"] = larga["fecha"].infer_objects()      # melt deja object aunque las fechas sean años enteros
    return larga


def ordenar_larga(larga):
    """Columnas clave y valor, ordenadas igual, para comparar dos tablas largas."""
    columnas = [*CLAVE_LARGA, "fecha", "valor"]
    return larga[columnas].sort_values(columnas[:-1]).reset_index(drop=True)




# --- Series temporales (u38, u39) ---------------------------------------------------------------





def replicas():
    """Réplicas acumuladas del sismo del 9-oct-2026 como Serie con DatetimeIndex.

    Lee datos/analisis/replicas_acumuladas.csv: cortes de prensa con datos del IGC-UP, sin
    frecuencia fija. El último corte (20-nov) es aproximado según la fuente.
    """
    tabla = leer("replicas_acumuladas.csv", ANALISIS)
    return pd.Series(tabla["replicas_acumuladas"].to_numpy(), index=pd.to_datetime(tabla["fecha"]),
                     name="replicas_acumuladas")


def indice_base_100(datos):
    """Reescala una Serie o un DataFrame para que la primera fila valga 100."""
    return datos / datos.iloc[0] * 100


def variacion_pct(serie, periodos=1):
    """Cambio porcentual frente a `periodos` filas antes, con shift() como en la u39."""
    return (serie / serie.shift(periodos) - 1) * 100




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
