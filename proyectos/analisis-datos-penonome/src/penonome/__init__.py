"""Code of the Pulso Penonomé project: loaders, course techniques and the main analysis."""
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
DATOS = RAIZ / "datos"
PAQUETE = DATOS / "penonome"                 # official tables of Penonomé and Coclé
ANALISIS = DATOS / "analisis"                 # tables built for the main analysis (SINAPROC, press records)
INVESTIGACION = RAIZ / "investigacion"
FUENTES = INVESTIGACION / "fuentes.csv"
