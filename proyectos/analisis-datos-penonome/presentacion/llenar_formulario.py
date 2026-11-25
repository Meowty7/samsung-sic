"""Fill the SIC project form (docx) with this project's answers.

Run from the project folder: uv run --with python-docx python presentacion/llenar_formulario.py
"""
import copy
from pathlib import Path

import docx
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn

HERE = Path(__file__).resolve().parent
ORIGEN = HERE / "plantillas" / "formulario-proyecto-sic.docx"
DESTINO = HERE / "entrega" / "RacoonCity - Formulario de desarrollo.docx"

EQUIPO = [
    ("[Integrante 1]", "Líder del proyecto y coordinación del equipo"),
    ("[Integrante 2]", "Investigación y verificación de datos"),
    ("[Integrante 3]", "Desarrollo del código"),
    ("[Integrante 4]", "Análisis de datos"),
    ("[Integrante 5]", "Visualización y presentación"),
]

NOMBRE = ("Pulso Penonomé: datos verificados sobre las afectaciones sociales del terremoto de 2026 en Coclé y "
          "dónde ayudar primero")

DESCRIPCION = [
    "Penonomé es la capital de Coclé: 104,326 habitantes en el Censo 2023 y 113,409 proyectados para 2026 (INEC). El "
    "9 de octubre de 2026 un sismo de magnitud 7.5 según SINAPROC (7.7 según el USGS), con epicentro en Azuero, dañó "
    "viviendas, escuelas y hospitales de la provincia. La evaluación de daños de SINAPROC cerró el 15 de noviembre con "
    "2,531 viviendas evaluadas en Coclé, donde viven 10,199 personas: 561 quedaron con daño total o moderado, y además "
    "hay 40 escuelas y 2 hospitales afectados.",
    "El problema es que la información está dispersa y en niveles distintos: el daño se publica por provincia, la "
    "pobreza y las carencias de vivienda por corregimiento, y todo está repartido en PDF del INEC y del PNUD, "
    "comunicados y la plataforma de SINAPROC, más notas de prensa. Así es difícil saber quién necesita ayuda primero.",
    "Pulso Penonomé analiza con datos oficiales cómo estaba el distrito antes del sismo, qué dejó el sismo en Coclé y "
    "dónde ayudar primero. El análisis muestra un distrito partido en dos: el sur concentra al 61 % de la población con "
    "pobreza baja, mientras el norte rural tiene pobreza de 45 % a 86 % y viviendas sin internet, con piso de tierra y "
    "cocina de leña. En Coclé, 91 personas con discapacidad y 9 mujeres embarazadas viven en casas con daño total o "
    "moderado. Con esos datos el proyecto construye un índice de prioridad por corregimiento (pobreza, carencias de la "
    "vivienda y daños reportados) que señala 10 corregimientos del norte, con 40,290 habitantes, donde la ayuda "
    "debería llegar primero, aunque la prensa hable sobre todo de la cabecera.",
    "El flujo completo de análisis está programado en Python con lo aprendido en el módulo: carga con csv y pandas, "
    "limpieza con sumas de control, análisis con funciones, tablas dinámicas y series temporales, ordenamiento de los "
    "corregimientos y siete gráficas con matplotlib. Todo se publica en un sitio web y se actualiza con un comando "
    "cuando sale un dato nuevo.",
]

RESPUESTAS = {
    "(1)": [
        "Valor social: muestra quiénes necesitan atención primero. En Coclé, 91 personas con discapacidad y 9 "
        "embarazadas viven en casas con daño grave, y en el distrito de Penonomé 41.9 % de las viviendas no tiene "
        "internet y 15.7 % cocina con leña, frente a 30.3 % y 6.0 % en el país (Censo 2023).",
        "Valor público: deja una base de datos abierta, verificada y reproducible que el municipio, las ONG o la "
        "prensa pueden reutilizar y actualizar cuando salga un dato nuevo.",
        "Valor financiero: ayuda a orientar el gasto de la reconstrucción (B/.12.7 millones contratados en Coclé para "
        "439 viviendas) hacia los corregimientos con más necesidad.",
    ],
    "(2)": [
        "Separamos siempre los datos oficiales de los de prensa y marcamos cada cifra con su fuente, para no presentar "
        "como hecho lo que es una estimación.",
        "Los registros de daños por corregimiento salen de la prensa: son registros, no casas contadas, y la prensa "
        "cubre más la cabecera. Por eso el índice solo los usa como sí o no.",
        "Señalar corregimientos con más pobreza puede estigmatizarlos; por eso se presentan como prioridad de ayuda y "
        "no como ranking negativo. Los datos son agregados, sin información personal de las familias.",
    ],
    "(3)": [
        "Positivo: más transparencia sobre el impacto del sismo y prioridades de ayuda basadas en datos, con atención "
        "especial a las personas con discapacidad, las embarazadas, la niñez y los adultos mayores.",
        "Si no se actúa: las familias pobres del norte, con menos recursos para reparar, pueden quedar más tiempo en "
        "viviendas dañadas, y la ayuda puede seguir concentrándose donde hay más cobertura de prensa.",
        "Riesgo negativo: que se comparen cifras que se miden distinto (viviendas afectadas de un comunicado frente a "
        "viviendas evaluadas de la EDAN). Lo mitigamos con las limitaciones explícitas en el estudio.",
    ],
    "(4)": [
        "Supuestos: que los pesos del índice (pobreza 50 %, carencias 30 %, daños 20 %) son razonables, por eso se "
        "probó con pesos iguales y el grupo de prioridad alta se mantiene; y que los registros de prensa ubican bien en "
        "qué corregimientos hubo daños.",
        "Preguntas ya resueltas: la evaluación de daños de SINAPROC ya tiene cifras finales para Coclé (al 15 de "
        "noviembre de 2026), con viviendas por nivel de daño y las personas que viven en ellas.",
    ],
    "(5)": [
        "¿Cuántas viviendas se dañaron en cada corregimiento de Penonomé? SINAPROC publica la evaluación por provincia; "
        "hay que pedir el desglose por corregimiento.",
        "¿Cuántas viviendas de Coclé estarán reconstruidas a fin de año? Hoy hay 439 contratadas y 67 en obra.",
        "¿Cuándo vuelven a clases presenciales las escuelas de Coclé que deben demolerse?",
    ],
    "(6)": [
        "Métrica principal: personas con discapacidad y embarazadas en viviendas con daño grave que reciben "
        "seguimiento médico y un lugar seguro, frente a las 91 y 9 identificadas.",
        "Métricas de la recuperación: viviendas reconstruidas frente a las 439 contratadas en Coclé, familias atendidas "
        "frente a las 1,890 fichas sociales del MIDES y escuelas reabiertas frente a las 40 afectadas.",
        "Métricas del propio proyecto: porcentaje de cifras verificadas contra su fuente y tiempo para actualizar el "
        "estudio cuando sale un dato nuevo (las referencias y los gráficos se regeneran con un comando).",
    ],
}


def answer_paragraph(template_par, text):
    """New paragraph after a question, copying its paragraph format and run format without bold."""
    new = copy.deepcopy(template_par._p)
    for r in new.findall(qn("w:r"))[1:]:
        new.remove(r)
    runs = new.findall(qn("w:r"))
    if not runs:
        return new
    r = runs[0]
    for child in list(r):
        if child.tag != qn("w:rPr"):
            r.remove(child)
    rpr = r.find(qn("w:rPr"))
    if rpr is not None:
        for tag in ("w:b", "w:bCs", "w:i", "w:iCs"):
            el = rpr.find(qn(tag))
            if el is not None:
                rpr.remove(el)
    t = r.makeelement(qn("w:t"), {})
    t.text = text
    t.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
    r.append(t)
    num = new.find(f"{qn('w:pPr')}/{qn('w:numPr')}")
    if num is not None:
        num.getparent().remove(num)
    return new


def insert_after(par, template, texts):
    anchor = par._p
    for text in texts:
        new = answer_paragraph(template, text)
        anchor.addnext(new)
        anchor = new


def main():
    d = docx.Document(ORIGEN)
    table = d.tables[0]
    for i, (nombre, rol) in enumerate(EQUIPO, start=1):
        for cell, value in zip(table.rows[i].cells, (nombre, rol)):
            p = cell.paragraphs[0]
            if p.runs:
                p.runs[0].text = value
                for extra in p.runs[1:]:
                    extra.text = ""
            else:
                p.add_run(value)
        table.rows[i].cells[1].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.LEFT

    ps = d.paragraphs
    find = lambda start: next(p for p in ps if p.text.strip().startswith(start))
    insert_after(find("Escriba el nombre del prototipo") if any("Escriba el nombre" in p.text for p in ps) else
                 next(p for p in ps if "Escriba el nombre del prototipo" in p.text),
                 next(p for p in ps if "Describa de qué tratará" in p.text), [NOMBRE])
    descr = next(p for p in ps if "Describa de qué tratará" in p.text)
    insert_after(descr, descr, DESCRIPCION)
    for key, texts in RESPUESTAS.items():
        q = find(key)
        insert_after(q, descr, texts)
    d.save(DESTINO)
    print(f"Guardado: {DESTINO.name}")


if __name__ == "__main__":
    main()
