"""Regenera 00-inicio.ipynb a partir del cronograma y el índice (toc) del sitio en myst.yml.

Las semanas cuya carpeta ya existe aparecen con link; las demás, como texto.

Uso (desde la raíz del curso):
    uv run python herramientas/actualizar_inicio.py
"""

import sys
from pathlib import Path

import nbformat
from nbformat.v4 import new_markdown_cell, new_notebook

sys.path.insert(0, str(Path(__file__).parent))
from actualizar_toc import actualizar_toc  # noqa: E402
from cronograma import MODULOS, SEMANAS, carpeta_de, modulo_de  # noqa: E402

RAIZ = Path(__file__).resolve().parent.parent

PRESENTACION = """# Samsung Innovation Campus 2026

Cuaderno de estudio del programa SIC 2026: Python, Inteligencia Artificial e IA Generativa (240 horas, 24 semanas).

## Cómo usar este cuaderno

1. Abre JupyterLab desde la raíz del curso: `uv run jupyter lab`
2. Entra a la semana que corresponda desde la tabla de abajo.
3. Cada semana tiene un índice con sus clases, la tutoría, el quiz y el repaso.
4. Cada unidad sigue el mismo orden: resumen del PDF con páginas de referencia, explicación con ejemplos, proyecto de la unidad, práctica con verificación automática, apuntes para estudiar y autoevaluación.

## Convenciones

- **Referencia:** página del PDF oficial donde está el contenido, para contrastar.
- **Ampliación (no está en el PDF):** explicación adicional que no forma parte del material oficial.
- **Nota sobre el PDF:** corrección de un error del material oficial.
- **Clave / Error común / Para el quiz:** apuntes de estudio.

Material complementario: [Glosario](glosario.ipynb) · [Cronograma original](recursos/cronograma-sic-2026.jpg) · [Proyectos](proyectos/README.md)
"""


def actualizar_inicio() -> None:
    celdas = [new_markdown_cell(PRESENTACION)]
    for modulo, nombre in MODULOS.items():
        filas = [
            f"## Módulo {nombre}\n",
            "| Semana | Fechas | Capítulos / actividad | Contenido |",
            "|---|---|---|---|",
        ]
        for semana, fechas, capitulos, contenido in SEMANAS:
            if modulo_de(semana) != modulo:
                continue
            indice = f"{carpeta_de(semana)}/semana-{semana:02d}.ipynb"
            etiqueta = f"Semana {semana}"
            if (RAIZ / indice).exists():
                etiqueta = f"[{etiqueta}]({indice})"
            filas.append(f"| {etiqueta} | {fechas} | {capitulos} | {contenido} |")
        celdas.append(new_markdown_cell("\n".join(filas)))

    nb = new_notebook()
    nb.cells = celdas
    nbformat.write(nb, RAIZ / "00-inicio.ipynb")
    print("Actualizado: 00-inicio.ipynb")
    actualizar_toc()


if __name__ == "__main__":
    actualizar_inicio()
