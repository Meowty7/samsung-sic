"""Reparte las viviendas evaluadas por SINAPROC (EDAN) en Coclé por distrito y por corregimiento de Penonomé.

Fuentes:
- SINAPROC publica un punto por vivienda evaluada en la capa `Sismo9oct_EDAN_Conteos` (sin nombres ni cédulas).
- Los límites de los corregimientos son los del Censo 2023, publicados por Esri Panamá (Living Atlas).

Cada punto se asigna al polígono que lo contiene. Solo se guardan totales: ninguna coordenada sale de este script.

Uso (desde la carpeta del proyecto): uv run python investigacion/edan_por_zona.py
"""
import collections
import csv
import json
import urllib.parse
import urllib.request
from pathlib import Path

EDAN = "https://sig.sinaproc.gob.pa/server/rest/services/Hosted/Sismo9oct_EDAN_Conteos/FeatureServer/0"
LIMITES = ("https://ags.esri.co/arcgis/rest/services/PanamaLivingAtlas/"
           "Censo_Poblacion_Corregimiento_Panama_2023/MapServer/0")
SALIDA = Path(__file__).resolve().parents[1] / "datos" / "analisis"
CORTE = "2026-11-15"
NIVELES = ["total", "moderado", "parcial", "leve", "menor"]
MINIMO = 5  # conteos de 1 a 4 personas con discapacidad o embarazadas no se publican

# Nombres de la capa de Esri -> clave del catálogo del proyecto (datos/penonome/00_catalogo_corregimientos.csv)
CLAVES = {"Penonomé (Cabecera)": "penonome_cabecera", "Cañaveral": "canaveral", "Coclé": "cocle",
          "Chiguirí Arriba": "chiguiri_arriba", "El Coco": "el_coco", "Pajonal": "pajonal",
          "Río Grande": "rio_grande", "Río Indio": "rio_indio", "Toabré": "toabre", "Tulú": "tulu",
          "Tucue": "boca_de_tucue", "Candelario Ovalle": "candelario_ovalle",
          "Victoriano Lorenzo": "general_victoriano_lorenzo", "Las Minas": "las_minas", "Reicito": "riecito",
          "San Miguel": "san_miguel"}


def consultar(url, **params):
    datos = urllib.parse.urlencode({**params, "f": params.get("f", "json")}).encode()
    pedido = urllib.request.Request(f"{url}/query", data=datos, headers={"User-Agent": "analisis-penonome"})
    with urllib.request.urlopen(pedido, timeout=120) as r:
        return json.load(r)


def viviendas_cocle():
    filas, salto = [], 0
    while True:  # el servidor entrega como máximo 1,000 filas por consulta
        d = consultar(EDAN, where="provincia='cocle'", outFields="*", returnGeometry="true", outSR="4326",
                      orderByFields="objectid", resultOffset=salto, resultRecordCount=1000)
        filas += d["features"]
        if len(d["features"]) < 1000:
            return filas
        salto += 1000


def dentro(x, y, anillo):
    c, j = False, len(anillo) - 1
    for i in range(len(anillo)):
        (xi, yi), (xj, yj) = anillo[i][:2], anillo[j][:2]
        if (yi > y) != (yj > y) and x < (xj - xi) * (y - yi) / (yj - yi) + xi:
            c = not c
        j = i
    return c


def poligonos(geom):
    return geom["coordinates"] if geom["type"] == "MultiPolygon" else [geom["coordinates"]]


def ubicar(x, y, zonas):
    for (x0, x1, y0, y1), props, geom in zonas:
        if x0 <= x <= x1 and y0 <= y <= y1:
            for p in poligonos(geom):
                if dentro(x, y, p[0]) and not any(dentro(x, y, h) for h in p[1:]):
                    return props
    return None


def resumir(grupo):
    c = collections.Counter(v["nivel"] for v in grupo)
    rep = collections.Counter(v["xy"] for v in grupo)
    return {"viviendas_evaluadas": len(grupo), **{f"dano_{n}": c.get(n, 0) for n in NIVELES},
            "personas": sum(v["personas"] for v in grupo), "adultos_mayores": sum(v["mayores"] for v in grupo),
            "discapacidad": sum(v["discapacidad"] for v in grupo), "embarazadas": sum(v["embarazadas"] for v in grupo),
            "viviendas_con_coordenada_compartida": sum(1 for v in grupo if rep[v["xy"]] > 1)}


def guardar(nombre, filas):
    with open(SALIDA / nombre, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=list(filas[0]), lineterminator="\n")
        w.writeheader()
        w.writerows(filas)
    print(f"{nombre}: {len(filas)} filas")


def main():
    limites = consultar(LIMITES, where="LMPR_NOMB='Provincia de Coclé'", outFields="LMDI_NOMB,LMCO_NOMB",
                        returnGeometry="true", outSR="4326", f="geojson")["features"]
    zonas = []
    for f in limites:
        pts = [p for poly in poligonos(f["geometry"]) for p in poly[0]]
        caja = (min(p[0] for p in pts), max(p[0] for p in pts), min(p[1] for p in pts), max(p[1] for p in pts))
        zonas.append((caja, f["properties"], f["geometry"]))

    viviendas = []
    for p in viviendas_cocle():
        a, g = p["attributes"], p["geometry"]
        props = ubicar(g["x"], g["y"], zonas)
        viviendas.append({
            "distrito": props["LMDI_NOMB"].replace("Distrito de ", "") if props else "(ubicación fuera de Coclé)",
            "corregimiento": props["LMCO_NOMB"].replace("Corregimiento ", "") if props else None,
            "nivel": a["t_afectacion"], "personas": a["t_miembros"] or 0,
            "mayores": (a["m_a_mayores"] or 0) + (a["f_a_mayores"] or 0),
            "discapacidad": a["c_discapacitados"] or 0, "embarazadas": a["c_embarazadas"] or 0,
            "xy": (round(g["x"], 5), round(g["y"], 5))})

    total = resumir(viviendas)
    assert (total["viviendas_evaluadas"], total["personas"], total["discapacidad"], total["embarazadas"]) == \
        (2531, 10199, 431, 21), f"No coincide con la ficha de Coclé: {total}"

    fuente = "SINAPROC, capa pública de la EDAN (un punto por vivienda evaluada); límites: Esri Panamá, Censo 2023"
    nota_d = ("Cálculo propio: cada vivienda evaluada se asigna al distrito que contiene su coordenada. "
              "La EDAN cuenta viviendas evaluadas, no todas las dañadas")
    por_d = collections.defaultdict(list)
    for v in viviendas:
        por_d[v["distrito"]].append(v)
    distritos = [{"provincia": "Coclé", "distrito": d, **resumir(g), "corte": CORTE, "fuente": fuente,
                  "url": EDAN, "nota": nota_d if not d.startswith("(") else
                  "Viviendas de la EDAN de Coclé cuya coordenada cae fuera de la provincia (error de ubicación)"}
                 for d, g in sorted(por_d.items(), key=lambda t: (t[0].startswith("("), -len(t[1])))]
    guardar("edan_sinaproc_distritos_cocle.csv", distritos)

    por_c = collections.defaultdict(list)
    for v in viviendas:
        if v["distrito"] == "Penonomé":
            por_c[CLAVES[v["corregimiento"]]].append(v)
    catalogo = list(csv.DictReader(open(SALIDA.parent / "penonome" / "00_catalogo_corregimientos.csv",
                                        encoding="utf-8-sig")))
    nota_c = ("Cálculo propio y aproximado: la coordenada puede ser el lugar donde se llenó la ficha y no la vivienda "
              f"(ver viviendas_con_coordenada_compartida). Discapacidad y embarazadas en blanco cuando son de 1 a "
              f"{MINIMO - 1}, para proteger la privacidad; los totales del distrito están en edan_sinaproc_distritos_cocle.csv")
    corregimientos = []
    for c in catalogo:
        fila = resumir(por_c.get(c["id_corregimiento"], []))
        for k in ("discapacidad", "embarazadas"):
            if 0 < fila[k] < MINIMO:
                fila[k] = ""
        corregimientos.append({"id_corregimiento": c["id_corregimiento"], "corregimiento": c["corregimiento"], **fila,
                               "corte": CORTE, "fuente": fuente, "url": EDAN, "nota": nota_c})
    assert sum(f["viviendas_evaluadas"] for f in corregimientos) == len(por_d["Penonomé"])
    guardar("edan_sinaproc_corregimientos_penonome.csv", corregimientos)


if __name__ == "__main__":
    main()
