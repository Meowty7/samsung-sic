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

NOMBRE = ("Pulso Penonomé: datos verificados para medir el empleo y la recuperación de Coclé después del "
          "terremoto de 2026")

DESCRIPCION = [
    "Penonomé es la capital de Coclé: 104,326 habitantes en el Censo 2023 y 113,409 proyectados para 2026 (INEC). El "
    "desempleo de Coclé pasó de 4.0 % en 2023 a 7.1 % en septiembre de 2025, después del cierre de la mina, y bajó a "
    "5.5 % en agosto de 2026, pero con 59.5 % de informalidad y un desempleo de las mujeres (8.2 %) que duplica al de "
    "los hombres. El 9 de octubre de 2026 un sismo de magnitud 7.7 con epicentro en Azuero dejó en Coclé 1,324 viviendas "
    "y 4,703 personas afectadas (SINAPROC, comunicado 12).",
    "El problema es que nadie puede medir todavía el impacto del sismo en el empleo: la próxima encuesta laboral con "
    "datos posteriores llega en 2027, el último balance oficial de daños con desglose de Coclé es del 14 de octubre, y "
    "la información está repartida en decenas de PDF del INEC, la CSS, la ATP, el MEF, el MIDES, el Miviot y la DGI, "
    "más notas de prensa.",
    "Pulso Penonomé analiza con datos oficiales cómo estaba el distrito antes del sismo, qué le pasó, cómo está hoy y "
    "dónde ayudar primero. El análisis muestra un distrito partido en dos: el sur concentra al 61 % de la población con "
    "pobreza baja, mientras el norte rural tiene pobreza de 45 % a 86 % y viviendas sin internet, con piso de tierra y "
    "cocina de leña. Con esos datos el proyecto construye un índice de prioridad por corregimiento (pobreza, carencias de "
    "la vivienda y daños reportados) que señala 10 corregimientos del norte, con 40,290 habitantes, donde la ayuda "
    "debería llegar primero, aunque la prensa hable sobre todo de la cabecera. A mes y medio del sismo, la "
    "reconstrucción avanza lento: 439 viviendas contratadas en Coclé y 67 en obra, 1,890 familias con ficha social del "
    "MIDES y escuelas dañadas recién en demolición.",
    "El flujo completo de análisis está programado en Python con lo aprendido en el módulo: carga con csv y pandas, "
    "limpieza con sumas de control, análisis con funciones y series temporales, ordenamiento de los corregimientos y "
    "diez gráficas con matplotlib. Además compara con el sismo de Colombia de agosto de 2026 y proyecta escenarios de "
    "desempleo para Coclé. Todo se publica en un sitio web y se actualiza con un comando cuando sale un dato nuevo.",
]

RESPUESTAS = {
    "(1)": [
        "Valor social: muestra dónde están las carencias para priorizar la ayuda. En el distrito de Penonomé, 41.9 % de "
        "las viviendas no tiene internet y 15.7 % cocina con leña, frente a 30.3 % y 6.0 % en el país (Censo 2023).",
        "Valor público: deja una base de datos abierta, verificada y reproducible que el municipio, las ONG o la "
        "prensa pueden reutilizar y actualizar cuando salga un dato nuevo.",
        "Valor financiero: ayuda a seguir el crédito para mipymes afectadas (B/.310 millones de Banconal y B/.4 millones "
        "de FIDEMICRO de la AMPYME) y la reconstrucción de viviendas (B/.12.7 millones contratados en Coclé), con "
        "indicadores como los cotizantes de la CSS.",
    ],
    "(2)": [
        "Separamos siempre los datos oficiales de los de prensa y marcamos cada cifra con su veredicto, para no "
        "presentar como hecho lo que es una estimación.",
        "Los escenarios a 2030 son supuestos, no pronósticos; hay que explicarlo para que nadie los use como cifra "
        "oficial.",
        "Señalar corregimientos con más pobreza puede estigmatizarlos; por eso se presentan como prioridad de ayuda y "
        "no como ranking negativo. Los datos son agregados, sin información personal.",
        "Las instituciones tendrán que acostumbrarse a publicar datos por provincia con más frecuencia para que el "
        "seguimiento sea útil.",
    ],
    "(3)": [
        "Positivo: más transparencia sobre el impacto del sismo, prioridades de ayuda basadas en datos y un "
        "seguimiento mensual que antes no existía.",
        "Si no se actúa: nuestro modelo estima unos 4,300 desocupados más en Coclé en 2026 y que el desempleo no "
        "vuelva a 5.5 % antes de 2031; frente a una recuperación rápida son unos 11,600 años-persona de desempleo de más.",
        "Riesgo negativo: que se usen las proyecciones fuera de contexto o se comparen cifras que se miden distinto. "
        "Lo mitigamos con las limitaciones explícitas en el estudio y el veredicto de cada fuente.",
    ],
    "(4)": [
        "Supuestos: que la reacción del empleo en las ciudades colombianas afectadas sirve como referencia para "
        "Coclé, aunque los dos países miden distinto (por eso comparamos con un índice relativo y no con los números "
        "directos); que los rangos de los escenarios son razonables; y que los registros de prensa por corregimiento "
        "ubican bien los daños.",
        "Preguntas ya resueltas: la encuesta de agosto de 2026 sí tiene datos completos de Coclé y la usamos como línea "
        "base; y los cotizantes de la CSS ya llegan a 2025 con la serie revisada del INEC (58,113 en Coclé).",
    ],
    "(5)": [
        "¿Cuántos empleos perdió Coclé después del sismo? Se sabrá con la encuesta de 2027 o con el plan del INEC de "
        "medir el empleo cada trimestre.",
        "¿Cuál es el balance de daños de Coclé posterior al 14 de octubre? SINAPROC solo publica cifras nacionales "
        "(77,778 personas afectadas al 20 de noviembre); hay que pedir el desglose provincial y por corregimiento.",
        "¿Cuántas viviendas de Coclé estarán reconstruidas a fin de año? Hoy hay 439 contratadas y 67 en obra.",
        "¿Cuántos cotizantes tiene Coclé mes a mes en 2026? La CSS no lo publica por provincia y habría que "
        "solicitarlo por la Ley 6 de 2002.",
    ],
    "(6)": [
        "Métrica principal: la tasa de desempleo de Coclé frente a la línea base de 5.5 % de agosto de 2026, con "
        "atención especial al desempleo de las mujeres (8.2 %), acompañada de los cotizantes activos de la CSS en Coclé "
        "(58,113 en 2025) como señal del empleo formal.",
        "Métricas de la recuperación: viviendas reconstruidas frente a las 439 contratadas en Coclé y familias "
        "atendidas frente a las 1,890 fichas sociales del MIDES.",
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
