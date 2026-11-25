"""Build the project deck on the official SIC template, keeping its masters, layouts and art untouched.

Run from the project folder: uv run --with python-pptx --with defusedxml --with lxml --with pillow \
    python presentacion/generar_presentacion.py
"""
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path
from xml.sax.saxutils import escape

HERE = Path(__file__).resolve().parent
PROJ = HERE.parent
PLANTILLA = HERE / "plantillas" / "plantilla-presentacion-sic.pptx"
DESTINO = HERE / "entrega" / "RacoonCity - Pulso Penonome.pptx"
ADD_SLIDE = Path(sys.argv[1]) if len(sys.argv) > 1 else None  # path to the pptx skill's add_slide.py

PROYECTO = "Pulso Penonomé"
EQUIPO = "Equipo RacoonCity"

BLUE, INK, INK2, CARD, WHITE = "193EB0", "262626", "595959", "EEF1FA", "FFFFFF"
EMU = 914400


def E(inches):
    return int(round(inches * EMU))


# ---- shape builders --------------------------------------------------------------------------------------------

class Ids:
    def __init__(self):
        self.n = 100

    def __call__(self):
        self.n += 1
        return self.n


def run(text, size=None, bold=False, color=None, font="Arial"):
    attrs = f' lang="es-PA"' + (f' sz="{int(size * 100)}"' if size else "") + (' b="1"' if bold else ' b="0"')
    fill = f'<a:solidFill><a:srgbClr val="{color}"/></a:solidFill>' if color else ""
    face = f'<a:latin typeface="{font}"/><a:ea typeface="{font}"/><a:cs typeface="{font}"/>' if font else ""
    return f'<a:r><a:rPr{attrs} dirty="0">{fill}{face}</a:rPr><a:t xml:space="preserve">{escape(text)}</a:t></a:r>'


def para(runs, align="l", space_after=0, bullet=False, level=0, line=100):
    if bullet:
        mar = 228600 + level * 228600
        bu = (f'<a:buClr><a:srgbClr val="{BLUE}"/></a:buClr><a:buSzPct val="100000"/>'
              f'<a:buFont typeface="Arial"/><a:buChar char="&#8226;"/>')
        ppr = f'<a:pPr marL="{mar}" indent="-228600" lvl="{level}" algn="{align}">'
    else:
        bu, ppr = "<a:buNone/>", f'<a:pPr marL="0" indent="0" algn="{align}">'
    return (f'<a:p>{ppr}<a:lnSpc><a:spcPct val="{line * 1000}"/></a:lnSpc><a:spcBef><a:spcPts val="0"/></a:spcBef>'
            f'<a:spcAft><a:spcPts val="{int(space_after * 100)}"/></a:spcAft>{bu}</a:pPr>{"".join(runs)}</a:p>')


def textbox(ids, x, y, w, h, paragraphs, anchor="t", name="Texto", inset=0.0, autofit=False):
    i = E(inset)
    fit = "<a:normAutofit/>" if autofit else "<a:noAutofit/>"
    return (f'<p:sp><p:nvSpPr><p:cNvPr id="{ids()}" name="{name}"/><p:cNvSpPr txBox="1"/><p:nvPr/></p:nvSpPr>'
            f'<p:spPr><a:xfrm><a:off x="{E(x)}" y="{E(y)}"/><a:ext cx="{E(w)}" cy="{E(h)}"/></a:xfrm>'
            f'<a:prstGeom prst="rect"><a:avLst/></a:prstGeom><a:noFill/><a:ln><a:noFill/></a:ln></p:spPr>'
            f'<p:txBody><a:bodyPr wrap="square" lIns="{i}" tIns="{i}" rIns="{i}" bIns="{i}" anchor="{anchor}">{fit}'
            f'</a:bodyPr><a:lstStyle/>{"".join(paragraphs)}</p:txBody></p:sp>')


def shape(ids, x, y, w, h, fill, paragraphs=(), prst="roundRect", anchor="ctr", name="Forma", inset=0.12, adj=None):
    av = f'<a:gd name="adj" fmla="val {adj}"/>' if adj is not None else ""
    i = E(inset)
    body = (f'<p:txBody><a:bodyPr wrap="square" lIns="{i}" tIns="{i}" rIns="{i}" bIns="{i}" anchor="{anchor}">'
            f'<a:noAutofit/></a:bodyPr><a:lstStyle/>{"".join(paragraphs) or "<a:p><a:endParaRPr/></a:p>"}</p:txBody>')
    return (f'<p:sp><p:nvSpPr><p:cNvPr id="{ids()}" name="{name}"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr>'
            f'<p:spPr><a:xfrm><a:off x="{E(x)}" y="{E(y)}"/><a:ext cx="{E(w)}" cy="{E(h)}"/></a:xfrm>'
            f'<a:prstGeom prst="{prst}"><a:avLst>{av}</a:avLst></a:prstGeom>'
            f'<a:solidFill><a:srgbClr val="{fill}"/></a:solidFill><a:ln><a:noFill/></a:ln></p:spPr>{body}</p:sp>')


def picture(ids, rid, x, y, w, h, descr):
    return (f'<p:pic><p:nvPicPr><p:cNvPr id="{ids()}" name="Imagen" descr="{escape(descr)}"/>'
            f'<p:cNvPicPr><a:picLocks noChangeAspect="1"/></p:cNvPicPr><p:nvPr/></p:nvPicPr>'
            f'<p:blipFill><a:blip r:embed="{rid}"/><a:stretch><a:fillRect/></a:stretch></p:blipFill>'
            f'<p:spPr><a:xfrm><a:off x="{E(x)}" y="{E(y)}"/><a:ext cx="{E(w)}" cy="{E(h)}"/></a:xfrm>'
            f'<a:prstGeom prst="rect"><a:avLst/></a:prstGeom></p:spPr></p:pic>')


def band_title(ids, text):
    """White section label inside the template's blue band (same box as the template's 'Slide Title')."""
    return textbox(ids, 0.4916, 0.3362, 9.34, 0.47, [para([run(text, 28, False, WHITE)])], name="Seccion")


def slide_title(ids, text):
    """The template's title placeholder, filled by the layout's own style."""
    return (f'<p:sp><p:nvSpPr><p:cNvPr id="{ids()}" name="Titulo"/><p:cNvSpPr txBox="1"/><p:nvPr><p:ph type="title"/>'
            f'</p:nvPr></p:nvSpPr><p:spPr><a:xfrm><a:off x="449468" y="1440000"/><a:ext cx="8541300" cy="369300"/>'
            f'</a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom><a:noFill/><a:ln><a:noFill/></a:ln></p:spPr>'
            f'<p:txBody><a:bodyPr anchor="t" lIns="0" tIns="0" rIns="0" bIns="0" wrap="square"><a:spAutoFit/>'
            f'</a:bodyPr><a:lstStyle/><a:p><a:pPr indent="0" lvl="0" marL="0" algn="l"><a:buNone/></a:pPr>'
            f'<a:r><a:rPr lang="es-PA" sz="2400" b="1" dirty="0"/><a:t>{escape(text)}</a:t></a:r></a:p></p:txBody></p:sp>')


def stat_card(ids, x, y, w, h, value, label, source=None):
    ps = [para([run(value, 30, True, BLUE)], space_after=3), para([run(label, 14, False, INK)], line=105)]
    if source:
        ps.append(para([run(" ", 6)], line=100))
        ps.append(para([run(source, 10, False, INK2)], line=100))
    return shape(ids, x, y, w, h, CARD, ps, anchor="t", inset=0.18, adj=8000, name="Cifra")


def bullets(ids, x, y, w, h, items, size=15, gap=8):
    ps = []
    for it in items:
        if isinstance(it, tuple):  # (bold lead, rest)
            ps.append(para([run(it[0], size, True, INK), run(it[1], size, False, INK)], bullet=True,
                           space_after=gap, line=108))
        else:
            ps.append(para([run(it, size, False, INK)], bullet=True, space_after=gap, line=108))
    return textbox(ids, x, y, w, h, ps, name="Puntos")


def caption(ids, x, y, w, text):
    return textbox(ids, x, y, w, 0.3, [para([run(text, 10, False, INK2)])], name="Fuente")


SLD_HEAD = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<p:sld xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" '
            'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" '
            'xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">'
            '<p:cSld><p:spTree><p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr>'
            '<p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/><a:chOff x="0" y="0"/>'
            '<a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr>')
SLD_TAIL = '</p:spTree></p:cSld><p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr></p:sld>'


# ---- slide content ---------------------------------------------------------------------------------------------
# The deck sells the idea: what the earthquake left in Coclé, who is most exposed in Penonomé, and where to help first.
# Every chart is produced by analisis-penonome.ipynb (documento/img/pulso-*.png).

U1, U2, U3 = "Unidad 1. Penonomé antes, Coclé después", "Unidad 2. Análisis de datos", "Unidad 3. La propuesta"


def takeaway(ids, x, y, w, lead, text, size=13):
    return textbox(ids, x, y, w, 0.9, [para([run(lead + " ", size, True, INK), run(text, size, False, INK)], line=108)])


def s_antes(ids, img):
    out = [band_title(ids, U1), slide_title(ids, "Dos distritos en uno")]
    out.append(picture(ids, img["pulso-01-poblacion-pobreza"], 0.49, 2.05, 7.0, 4.06, "Población y pobreza por corregimiento"))
    cards = [("104,326", "habitantes en 16 corregimientos"),
             ("61 %", "vive en el sur, con pobreza baja"),
             ("86 %", "de pobreza en Riecito, en el norte")]
    for k, (v, l) in enumerate(cards):
        out.append(stat_card(ids, 7.7, 2.05 + k * 1.45, 2.64, 1.35, v, l))
    return out


def s_carencias(ids, img):
    out = [band_title(ids, U1), slide_title(ids, "Antes del sismo: viviendas con más carencias que el país")]
    out.append(picture(ids, img["pulso-02-carencias"], 0.49, 2.05, 6.9, 3.59, "Carencias de las viviendas"))
    cards = [("41.9 %", "de las viviendas del distrito no tiene internet (país: 30.3 %)"),
             ("15.7 %", "cocina con leña (país: 6.0 %)"),
             ("9.3 %", "tiene piso de tierra (país: 5.4 %)")]
    for k, (v, l) in enumerate(cards):
        out.append(stat_card(ids, 7.6, 2.05 + k * 1.45, 2.74, 1.35, v, l))
    out.append(caption(ids, 0.49, 5.8, 6.9, "Fuente: INEC, Censo 2023, Cuadro 1. Porcentajes de viviendas particulares ocupadas."))
    return out


def s_sismo(ids, img):
    out = [band_title(ids, U1), slide_title(ids, "9 de octubre de 2026: el terremoto")]
    out.append(picture(ids, img["pulso-05-danos"], 0.49, 2.05, 5.6, 2.69, "Viviendas afectadas en Coclé por comunicado"))
    out.append(picture(ids, img["catedral-despues"], 6.3, 2.05, 1.55, 2.06, "Catedral de Penonomé con grietas"))
    out.append(picture(ids, img["hotel-dos-continentes"], 7.98, 2.05, 2.36, 2.06, "Hotel Dos Continentes colapsado"))
    cards = [("7.5", "magnitud según SINAPROC (7.7 según el USGS), con epicentro en Azuero"),
             ("2,531", "viviendas evaluadas en Coclé al cierre de la EDAN, el 15 de noviembre (SINAPROC)"),
             ("1,690", "réplicas al 20 de noviembre (IGC-UP)")]
    w = 3.13
    for k, (v, l) in enumerate(cards):
        out.append(stat_card(ids, 0.49 + k * (w + 0.23), 4.92, w, 1.45, v, l))
    return out


def s_hoy(ids, img):
    out = [band_title(ids, U1), slide_title(ids, "Cómo está Coclé hoy, a mes y medio del sismo")]
    datos = [("439", "viviendas contratadas para reconstruir en Coclé; 67 ya en obra", "Miviot, 9 de noviembre"),
             ("1,890", "familias de Coclé con ficha social de emergencia del MIDES", "MIDES, 6 de noviembre"),
             ("193,000", "estudiantes de cuatro provincias sin clases presenciales; escuelas de Tulú y Toabré en demolición",
              "Meduca, 17 de noviembre"),
             ("9,693", "bolsas de alimentos del IMA entregadas en 448 comunidades de Coclé", "COE Nacional, 25 de noviembre"),
             ("0", "albergues activos y personas albergadas en Coclé",
              "COE Nacional, 25 de noviembre"),
             ("113,409", "habitantes proyectados en el distrito de Penonomé para 2026", "INEC, proyecciones revisadas")]
    w, h, gx, gy = 3.13, 1.95, 0.23, 0.2
    for k, (v, d, f) in enumerate(datos):
        r, c = divmod(k, 3)
        out.append(shape(ids, 0.49 + c * (w + gx), 2.05 + r * (h + gy), w, h, CARD,
                         [para([run(v, 26, True, BLUE)], space_after=4), para([run(d, 13, False, INK)], space_after=4, line=104),
                          para([run(f, 10, False, INK2)])], anchor="t", inset=0.16, adj=8000, name="Hoy"))
    return out


def s_flujo(ids, img):
    out = [band_title(ids, U2), slide_title(ids, "Del dato oficial a la decisión: el flujo de análisis")]
    pasos = [("Fuentes", "INEC, PNUD y SINAPROC: cada cifra con su enlace y verificada."),
             ("Carga", "Censo, pobreza y daños unidos en una tabla de los 16 corregimientos."),
             ("Limpieza", "Sumas de control: los corregimientos dan 104,326 y los daños suman 2,531 viviendas."),
             ("Análisis", "Carencias, niveles de daño y personas vulnerables en viviendas dañadas."),
             ("Gráficas", "Siete gráficas, del Censo al ranking final."),
             ("Decisión", "Índice de prioridad que ordena los 16 corregimientos.")]
    w, h, gx, gy = 3.13, 1.95, 0.23, 0.25
    for k, (titulo, hecho) in enumerate(pasos):
        r, c = divmod(k, 3)
        out.append(shape(ids, 0.49 + c * (w + gx), 2.05 + r * (h + gy), w, h, CARD,
                         [para([run(f"{k + 1}. {titulo}", 18, True, BLUE)], space_after=8),
                          para([run(hecho, 15, False, INK)], line=108)],
                         anchor="t", inset=0.16, adj=8000, name="Paso"))
    return out


def s_danos(ids, img):
    out = [band_title(ids, U2), slide_title(ids, "Qué dejó el sismo en las viviendas de Coclé")]
    out.append(picture(ids, img["pulso-03-nivel-dano"], 0.49, 2.05, 6.9, 3.31, "Viviendas evaluadas por nivel de daño"))
    cards = [("561", "viviendas con daño total o moderado: 22.2 % de las evaluadas"),
             ("10,199", "personas viven en las viviendas evaluadas"),
             ("40 y 2", "escuelas y hospitales afectados en Coclé")]
    for k, (v, l) in enumerate(cards):
        out.append(stat_card(ids, 7.6, 2.05 + k * 1.45, 2.74, 1.35, v, l))
    out.append(takeaway(ids, 0.49, 5.5, 6.9, "Ojo:", "son las viviendas que SINAPROC evaluó, no todas las de la provincia, "
                        "y «daño total» no significa colapso.", size=12))
    return out


def s_vulnerables(ids, img):
    out = [band_title(ids, U2), slide_title(ids, "Quiénes viven en las casas más dañadas")]
    out.append(picture(ids, img["pulso-04-vulnerables"], 0.49, 2.05, 6.9, 3.31, "Personas con discapacidad según el daño de su vivienda"))
    cards = [("91", "personas con discapacidad en casas con daño total o moderado"),
             ("9", "mujeres embarazadas en casas con daño total o moderado"),
             ("17.0 %", "de las personas evaluadas son adultos mayores; 22.6 % son niños o recién nacidos")]
    for k, (v, l) in enumerate(cards):
        out.append(stat_card(ids, 7.6, 2.05 + k * 1.45, 2.74, 1.35, v, l))
    out.append(takeaway(ids, 0.49, 5.5, 6.9, "Salud pública:", "son las primeras personas que necesitan seguimiento médico "
                        "y un lugar seguro.", size=12))
    return out


def s_prioridad(ids, img):
    out = [band_title(ids, U2), slide_title(ids, "Dónde ayudar primero")]
    out.append(picture(ids, img["pulso-09-prioridad"], 0.49, 2.05, 6.9, 4.14, "Índice de prioridad por corregimiento"))
    out.append(stat_card(ids, 7.6, 2.05, 2.74, 1.35, "10", "corregimientos con prioridad alta"))
    out.append(stat_card(ids, 7.6, 3.52, 2.74, 1.35, "40,290", "personas viven en ellos"))
    out.append(textbox(ids, 7.6, 5.0, 2.74, 1.3, [para([run("Tulú, San Miguel, Riecito y Chiguirí Arriba encabezan con cualquier peso.", 13, False, INK)], space_after=8, line=105), para([run("La prensa mira la cabecera; la necesidad está en el norte.", 13, True, BLUE)], line=105)]))
    return out


def s_propuesta(ids, img):
    out = [band_title(ids, U3), slide_title(ids, "La propuesta: llevar la ayuda por fases, guiada por datos")]
    fases = [("Fase 1: urgente", "12,779 personas",
              "Tulú, San Miguel, Riecito y Chiguirí Arriba: encabezan el índice con cualquier peso."),
             ("Fase 2: alta", "27,511 personas",
              "Río Indio, Candelario Ovalle, Boca de Tucué, Toabré, Pajonal y Las Minas."),
             ("Fase 3: la cabecera", "64,036 personas",
              "Reabrir escuelas, mercado, hospital y servicios del centro, donde se concentró el daño a edificios públicos.")]
    w, gap = 3.13, 0.23
    for k, (titulo, gente, detalle) in enumerate(fases):
        out.append(shape(ids, 0.49 + k * (w + gap), 2.1, w, 3.9, CARD,
                         [para([run(titulo, 18, True, BLUE)], space_after=10),
                          para([run(gente.split()[0], 32, True, INK)], space_after=0),
                          para([run(" ".join(gente.split()[1:]), 15, False, INK2)], space_after=14),
                          para([run(detalle, 16, False, INK)], line=110)],
                         anchor="t", inset=0.18, adj=8000, name="Fase"))
    return out


def s_como(ids, img):
    out = [band_title(ids, U3), slide_title(ids, "Cómo hacerlo: una acción para cada problema")]
    cols = [(0.49, 2.55, "Problema"), (3.1, 4.35, "Qué hacer"), (7.51, 2.83, "Con quién")]
    filas = [("Viviendas precarias y dañadas", "Evaluar y reparar primero en la fase 1: piso, techo y estructura.",
              "Miviot, SINAPROC"),
             ("Personas vulnerables en casas dañadas", "Seguimiento médico y lugar seguro para las 91 personas con "
              "discapacidad y las 9 embarazadas en casas con daño grave.", "MINSA, SENADIS, MIDES"),
             ("Sin agua, luz ni internet", "Reconexión prioritaria y puntos de internet en escuelas y casas comunales.",
              "IDAAN, ASEP, municipio"),
             ("Sin datos de daños por corregimiento", "Pedir a SINAPROC la evaluación por corregimiento y actualizar "
              "el índice.", "SINAPROC, MIDES, municipio")]
    y0, rh = 2.05, 0.9
    for x, w, head in cols:
        out.append(shape(ids, x, y0, w, 0.45, BLUE, [para([run(head, 14, True, WHITE)])], prst="rect", inset=0.12,
                         name="Encabezado"))
    for k, fila in enumerate(filas):
        y = y0 + 0.5 + k * (rh + 0.06)
        for (x, w, _), val, bold in zip(cols, fila, (True, False, False)):
            out.append(shape(ids, x, y, w, rh, CARD, [para([run(val, 14, bold, BLUE if bold else INK)], line=104)],
                             prst="rect", inset=0.12, name="Celda"))
    return out


def s_proyeccion(ids, img):
    out = [band_title(ids, U3), slide_title(ids, "Cómo se da seguimiento")]
    etapas = [("0 a 3 meses", "Validar el índice en campo con el municipio y SINAPROC, y atender la fase 1.",
               "Viviendas reparadas y personas vulnerables con seguimiento"),
              ("3 a 12 meses", "Fase 2 y reapertura de servicios en la cabecera; tablero mensual con datos nuevos.",
               "Escuelas reabiertas y familias con ficha social atendidas"),
              ("Siguiente medición", "Repetir el análisis con la próxima medición de pobreza por corregimiento.",
               "Pobreza multidimensional y carencias de vivienda del norte")]
    w, gap = 3.13, 0.23
    for k, (cuando, que, mide) in enumerate(etapas):
        x = 0.49 + k * (w + gap)
        out.append(shape(ids, x, 2.1, w, 3.0, CARD,
                         [para([run(cuando, 18, True, BLUE)], space_after=8),
                          para([run(que, 14, False, INK)], space_after=10, line=106),
                          para([run("Se mide con: ", 13, True, INK2), run(mide, 13, False, INK2)], line=104)],
                         anchor="t", inset=0.18, adj=8000, name="Etapa"))
        if k < 2:
            out.append(shape(ids, x + w + 0.02, 3.45, 0.19, 0.26, BLUE, prst="rightArrow", inset=0, name="Flecha"))
    out.append(textbox(ids, 0.49, 5.35, 9.85, 0.45, [para([
        run("Después: ", 14, True, INK),
        run("aplicar el mismo método en Los Santos, Herrera y Veraguas, también afectados por el sismo.", 14, False, INK)])]))
    return out


def s_problema(ids, img):
    out = [band_title(ids, "Planteamiento"), slide_title(ids, "El problema y los objetivos")]
    probl = [("Penonomé, ", "capital de Coclé: 104,326 habitantes; el norte rural tiene pobreza de hasta 86 %."),
             ("El 9 de octubre de 2026 ", "un sismo de magnitud 7.5 dejó en Coclé 561 viviendas con daño total o "
                                         "moderado, 40 escuelas y 2 hospitales afectados."),
             ("Los datos están dispersos: ", "el daño se publica por provincia y la pobreza por corregimiento, en "
                                            "decenas de PDF y plataformas.")]
    ps = [para([run("El problema", 16, True, BLUE)], space_after=8)]
    ps += [para([run(a, 13, True, INK), run(b, 13, False, INK)], bullet=True, space_after=7, line=106) for a, b in probl]
    out.append(shape(ids, 0.49, 2.1, 4.81, 4.1, CARD, ps, anchor="t", inset=0.2, adj=6000, name="Problema"))
    objs = ["Reunir y verificar los datos oficiales del distrito y del sismo.",
            "Medir qué dejó el sismo en las viviendas de Coclé.",
            "Identificar a las personas que necesitan atención primero.",
            "Ordenar los corregimientos por prioridad de ayuda."]
    out.append(textbox(ids, 5.55, 2.1, 4.8, 0.45, [para([run("Objetivos", 16, True, BLUE)])]))
    for k, o in enumerate(objs):
        y = 2.7 + k * 0.85
        out.append(shape(ids, 5.55, y, 0.5, 0.5, BLUE, [para([run(str(k + 1), 16, True, WHITE)], align="ctr")],
                         prst="ellipse", inset=0, name="Numero"))
        out.append(textbox(ids, 6.25, y - 0.05, 4.1, 0.62, [para([run(o, 14, False, INK)], line=105)], anchor="ctr"))
    return out


def s_equipo(ids, img):
    out = [band_title(ids, "Equipo RacoonCity"), slide_title(ids, "Quiénes somos")]
    team = [("[Integrante 1]", "Líder del proyecto y coordinación del equipo"),
            ("[Integrante 2]", "Investigación y verificación de datos"),
            ("[Integrante 3]", "Desarrollo del código"),
            ("[Integrante 4]", "Análisis de datos"),
            ("[Integrante 5]", "Visualización y presentación")]
    w, h = 3.13, 1.75
    pos = [(0, 0), (1, 0), (2, 0), (0, 1), (1, 1)]
    for (name, role), (c, r) in zip(team, pos):
        dx = (w + 0.23) / 2 if r == 1 else 0
        out.append(shape(ids, 0.49 + dx + c * (w + 0.23), 2.15 + r * (h + 0.25), w, h, CARD,
                         [para([run(name, 15, True, BLUE)], space_after=6), para([run(role, 13, False, INK)], line=105)],
                         anchor="t", inset=0.18, adj=8000, name="Integrante"))
    return out


CONTENIDO = [s_problema, s_antes, s_carencias, s_sismo, s_hoy, s_flujo, s_danos, s_vulnerables, s_prioridad,
             s_propuesta, s_como, s_proyeccion, s_equipo]
AGENDA = [(U1, ["1.1. Dos distritos en uno", "1.2. Carencias de las viviendas", "1.3. El terremoto y cómo está hoy"]),
          (U2, ["2.1. El flujo de análisis", "2.2. Viviendas dañadas y personas vulnerables", "2.3. Dónde ayudar primero"]),
          (U3, ["3.1. Ayuda por fases", "3.2. Cómo hacerlo", "3.3. Cómo se da seguimiento"])]
NOTAS = [
    "El problema: el sismo golpeó a una provincia con zonas muy pobres y los datos estaban dispersos. Estos son nuestros objetivos.",
    "Penonomé son dos distritos: el sur concentra a la gente y el norte, la pobreza.",
    "Antes del sismo el distrito ya tenía más carencias de vivienda que el país, sobre todo internet y leña.",
    "El 9 de octubre el balance de viviendas afectadas se multiplicó por nueve en cuatro días; la evaluación cerró con 2,531 viviendas evaluadas.",
    "Hoy: la reconstrucción avanza lento; ya no hay albergues y la ayuda alimentaria llegó a 448 comunidades.",
    "Así trabajamos los datos: de la fuente oficial a la decisión, con lo aprendido en el módulo.",
    "De las viviendas evaluadas, 561 quedaron con daño total o moderado.",
    "En esas casas viven 91 personas con discapacidad y 9 embarazadas: son la prioridad de salud pública.",
    "El resultado: dónde ayudar primero. Diez corregimientos del norte.",
    "La propuesta: atender por fases, empezando por los cuatro corregimientos que encabezan siempre el índice.",
    "Cómo hacerlo: una acción y una institución responsable para cada problema que mostraron los datos.",
    "Cómo se da seguimiento: etapas, indicadores para medir si funciona y extensión a Azuero.",
    "El equipo RacoonCity y el rol de cada integrante.",
]


# ---- package edits ---------------------------------------------------------------------------------------------

def set_texts(xml, mapping):
    for old, new in mapping:
        assert old in xml, old
        xml = xml.replace(old, escape(new), 1)
    return xml


def main():
    if ADD_SLIDE is None:
        sys.exit("Usage: generar_presentacion.py <path to add_slide.py>")
    work = Path(tempfile.mkdtemp())
    with zipfile.ZipFile(PLANTILLA) as z:
        z.extractall(work)
    ppt = work / "ppt"

    # Structure first: content slides are copies of the template's content slide (slide4), placed before slide5.
    after = "slide4.xml"
    new_slides = []
    for _ in CONTENIDO[1:]:
        out = subprocess.run([sys.executable, str(ADD_SLIDE), str(work), "slide4.xml", "--after", after],
                             capture_output=True, text=True, check=True).stdout
        name = re.search(r"(slide\d+\.xml)", out.split("Created")[-1]).group(1)
        new_slides.append(name)
        after = name
    content_files = ["slide4.xml"] + new_slides

    # Footer project name on the content layouts (the template asks to edit it in the master).
    for lay in ("slideLayout3.xml", "slideLayout4.xml"):
        p = ppt / "slideLayouts" / lay
        p.write_text(p.read_text(encoding="utf-8").replace("Project Name", f"{PROYECTO} | RacoonCity"), encoding="utf-8")

    # Slide 2: project and team names.
    p = ppt / "slides" / "slide2.xml"
    p.write_text(set_texts(p.read_text(encoding="utf-8"), [("Nombre del proyecto", PROYECTO),
                                                           ("Nombre del equipo", EQUIPO)]), encoding="utf-8")

    # Slide 3: agenda.
    p = ppt / "slides" / "slide3.xml"
    x = p.read_text(encoding="utf-8")
    x = set_texts(x, [("Project Name", "Contenido")])
    for old_title, (title, subs) in zip(["UNIDAD 1. Título", "UNIT 2. Título", "UNIT 3. Título"], AGENDA):
        x = set_texts(x, [(old_title, title)])
    # Subtitles: each unit's text box holds runs "N.1. Subtítulo", "N.2. ", "Subtítulo", ...; rebuild those boxes.
    for n, (_, subs) in enumerate(AGENDA, start=1):
        pattern = re.compile(rf"(<p:txBody>(?:(?!</p:txBody>).)*?<a:t>{n}\.1\. Subt.*?</p:txBody>)", re.S)
        m = pattern.search(x)
        assert m, n
        body = m.group(1)
        first_p = re.search(r"<a:p>.*?</a:p>", body, re.S).group(0)
        rpr = re.search(r"<a:rPr[^>]*?(?:/>|>.*?</a:rPr>)", first_p, re.S).group(0)
        ppr = re.search(r"<a:pPr.*?</a:pPr>|<a:pPr[^>]*/>", first_p, re.S)
        ppr = ppr.group(0) if ppr else ""
        paras = "".join(f"<a:p>{ppr}<a:r>{rpr}<a:t>{escape(s)}</a:t></a:r></a:p>" for s in subs)
        head = body[:body.index("<a:p>")]
        x = x.replace(body, head + paras + "</p:txBody>", 1)
    p.write_text(x, encoding="utf-8")

    # Media for content slides.
    img_dir = PROJ / "documento/img"
    media = {f.stem: f for f in sorted(img_dir.glob("pulso-*.png"))}
    media["catedral-despues"] = img_dir / "catedral-despues.jpg"
    media["hotel-dos-continentes"] = img_dir / "hotel-dos-continentes.jpg"
    for key, src in media.items():
        shutil.copy(src, ppt / "media" / f"pulso-{key}{src.suffix}")
    ct = work / "[Content_Types].xml"
    c = ct.read_text(encoding="utf-8")
    for ext, mime in (("png", "image/png"), ("jpg", "image/jpeg")):
        if f'Extension="{ext}"' not in c:
            c = c.replace("<Types ", "<Types ", 1).replace(">", f'><Default Extension="{ext}" ContentType="{mime}"/>', 1)
    ct.write_text(c, encoding="utf-8")

    for fname, build, note in zip(content_files, CONTENIDO, NOTAS):
        rels_p = ppt / "slides" / "_rels" / f"{fname}.rels"
        rels = rels_p.read_text(encoding="utf-8")
        img = {}
        for k, (key, src) in enumerate(media.items(), start=50):
            rid = f"rId{k}"
            img[key] = rid
            rels = rels.replace("</Relationships>", f'<Relationship Id="{rid}" Type="http://schemas.openxmlformats.org/'
                                f'officeDocument/2006/relationships/image" Target="../media/pulso-{key}{src.suffix}"/>'
                                f"</Relationships>")
        rels_p.write_text(rels, encoding="utf-8")
        ids = Ids()
        (ppt / "slides" / fname).write_text(SLD_HEAD + "".join(build(ids, img)) + SLD_TAIL, encoding="utf-8")
        # speaker note: replace the copied note text with this slide's line
        nrel = re.search(r'Target="\.\./notesSlides/(notesSlide\d+\.xml)"', rels)
        if nrel:
            npth = ppt / "notesSlides" / nrel.group(1)
            nx = npth.read_text(encoding="utf-8")
            nx = re.sub(r"(<p:ph[^>]*type=\"body\"[^>]*/>.*?<p:txBody>.*?)(<a:p>.*?</p:txBody>)",
                        lambda m: m.group(1) + f'<a:p><a:r><a:rPr lang="es-PA"/><a:t>{escape(note)}</a:t></a:r></a:p>'
                                                 "</p:txBody>", nx, count=1, flags=re.S)
            npth.write_text(nx, encoding="utf-8")

    if DESTINO.exists():
        DESTINO.unlink()
    with zipfile.ZipFile(DESTINO, "w", zipfile.ZIP_DEFLATED) as z:
        ct_path = work / "[Content_Types].xml"
        z.write(ct_path, "[Content_Types].xml")
        for f in sorted(work.rglob("*")):
            if f.is_file() and f != ct_path:
                z.write(f, f.relative_to(work).as_posix())
    shutil.rmtree(work)
    print(f"Guardado: {DESTINO.name}")


if __name__ == "__main__":
    main()
