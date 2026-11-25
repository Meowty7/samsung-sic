"""Main analysis of the project: what happened in Penonomé before and after the 9-oct-2026 earthquake.

Loads every table the analysis needs, builds the priority index by corregimiento and draws the
charts with one style. The charts are saved to documento/img/ so the study and the deck use the
same images the notebook produces.
"""
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

from penonome import ANALISIS, PAQUETE, RAIZ

DATOS = ANALISIS
IMG = RAIZ / "documento" / "img"

AZUL, NARANJA, AGUA = "#2a78d6", "#eb6834", "#1baf7a"
TINTA, TINTA2, GRIS, REJILLA = "#0b0b0b", "#52514e", "#898781", "#e1e0d9"
FONDO = "#fcfcfb"

plt.rcParams.update({
    "font.family": "sans-serif", "font.size": 11, "text.color": TINTA, "axes.labelcolor": TINTA2,
    "xtick.color": TINTA2, "ytick.color": TINTA2, "axes.edgecolor": "#c3c2b7", "figure.facecolor": FONDO,
    "axes.facecolor": FONDO, "savefig.facecolor": FONDO, "figure.dpi": 110,
})


# ---- loading ---------------------------------------------------------------------------------------------------

def leer(nombre, carpeta=PAQUETE):
    """Read one CSV of the project with the encoding its files use."""
    return pd.read_csv(carpeta / nombre, encoding="utf-8-sig")


def cargar_todo():
    """Every table of the main analysis in a dict, keyed by a short name."""
    viviendas = leer("02_censo2023_viviendas_caracteristicas.csv")
    ipm = leer("03_pnud_ipm_corregimientos_2023.csv")[["corregimiento", "incidencia_h"]]
    return {
        "catalogo": leer("00_catalogo_corregimientos.csv"),
        "poblacion": leer("01_censo2023_poblacion_corregimientos.csv"),
        "viviendas": viviendas[viviendas["nivel"] == "corregimiento"].copy(),
        "viviendas_totales": viviendas[viviendas["nivel"] != "corregimiento"].copy(),
        "ipm": ipm.rename(columns={"incidencia_h": "ipm"}),
        "danos": leer("danos_sinaproc_cocle.csv", DATOS),
        "afectaciones": leer("afectaciones_sinaproc_cocle.csv", DATOS),
        "provincias": leer("afectaciones_sinaproc_provincias.csv", DATOS),
        "registros": leer("registros_danos_corregimiento.csv", DATOS),
        "replicas": leer("replicas_acumuladas.csv", DATOS),
        "poblacion_proy": leer("poblacion_proyeccion_2023_2026.csv", DATOS),
        "situacion": leer("situacion_actual_2026.csv", DATOS),
    }


# ---- priority index --------------------------------------------------------------------------------------------

PESOS = {"pobreza": 0.5, "carencias": 0.3, "danos": 0.2}


def tabla_corregimientos(t):
    """One row per corregimiento: population, poverty, housing gaps and reported damage."""
    pob = t["poblacion"].merge(t["catalogo"][["id_corregimiento", "corregimiento"]], on="id_corregimiento",
                               suffixes=("", "_cat"))
    v = t["viviendas"]
    carencias = (v["piso_tierra"] + v["sin_agua_potable"] + v["sin_luz"]) / (3 * v["viviendas"]) * 100
    v = v.assign(carencias_pct=carencias.round(1), sin_internet_pct=(v["sin_internet"] / v["viviendas"] * 100).round(1))
    tabla = (pob[["id_corregimiento", "corregimiento", "pob_2023"]]
             .merge(v[["id_corregimiento", "viviendas", "carencias_pct", "sin_internet_pct"]], on="id_corregimiento")
             .merge(t["ipm"], on="corregimiento")
             .merge(t["registros"][["id_corregimiento", "registros_danos"]], on="id_corregimiento"))
    # One corregimiento of the district is also called Coclé, like the province: label it so charts are not ambiguous
    tabla["corregimiento"] = tabla["corregimiento"].replace({"Coclé": "Coclé (corregimiento)"})
    return tabla


def indice_prioridad(tabla, pesos=PESOS):
    """Score from 0 to 100: poverty (IPM), housing gaps scaled to the worst corregimiento, and reported damage
    as yes/no (press coverage concentrates in the town centre, so counting records would reward visibility)."""
    pobreza = tabla["ipm"] / 100
    carencias = tabla["carencias_pct"] / tabla["carencias_pct"].max()
    danos = (tabla["registros_danos"] > 0).astype(float)
    puntaje = pesos["pobreza"] * pobreza + pesos["carencias"] * carencias + pesos["danos"] * danos
    return (puntaje / sum(pesos.values()) * 100).round(1)


# ---- charts ----------------------------------------------------------------------------------------------------

def figura(ancho=10, alto=5.4):
    fig, ax = plt.subplots(figsize=(ancho, alto))
    return fig, ax


def estilo(ax, titulo, fuente, xlabel="", ylabel="", rejilla="y"):
    """Title on the left, quiet axes and grid, source line at the bottom."""
    ax.set_title(titulo, loc="left", fontsize=14, fontweight="bold", pad=12)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    if rejilla:
        ax.grid(True, axis=rejilla, color=REJILLA, linewidth=0.7)
    ax.set_axisbelow(True)
    for lado in ("top", "right"):
        ax.spines[lado].set_visible(False)
    ax.tick_params(length=0)
    ax.figure.text(0.01, 0.012, f"Fuente: {fuente}", fontsize=8.5, color=TINTA2)
    ax.figure.tight_layout(rect=(0, 0.045, 1, 1))


def guardar(fig, nombre):
    """Save the chart for the study and the deck (documento/img/<nombre>.png)."""
    IMG.mkdir(parents=True, exist_ok=True)
    ruta = IMG / f"{nombre}.png"
    fig.savefig(ruta, dpi=170)
    return ruta
