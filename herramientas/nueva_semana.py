"""Crea el esqueleto de una semana y actualiza el índice del curso.

Uso (desde la raíz del curso):
    uv run python herramientas/nueva_semana.py 2

Crea, sin sobrescribir nada que ya exista:
    <modulo>/semana-NN/
        semana-NN.ipynb   índice de la semana
        sNN-tutoria.ipynb notas de la clase de tutoría
        sNN-quiz.ipynb    quiz de práctica
        sNN-repaso.ipynb  resumen para repasar
        pdfs/             PDFs de la semana (no se publican en git)
"""

import sys
from pathlib import Path

import nbformat
from nbformat.v4 import new_markdown_cell, new_notebook

sys.path.insert(0, str(Path(__file__).parent))
from cronograma import archivo_semana, carpeta_de, datos_de  # noqa: E402
from actualizar_inicio import actualizar_inicio  # noqa: E402

RAIZ = Path(__file__).resolve().parent.parent


def navegacion(semana: int) -> str:
    """Línea de navegación entre semanas, relativa a la carpeta de la semana."""
    partes = ["[Inicio del curso](../../00-inicio.ipynb)"]
    if semana > 0:
        anterior = f"../../{carpeta_de(semana - 1)}/semana-{semana - 1:02d}.ipynb"
        partes.append(f"[Semana anterior]({anterior})")
    if semana < 24:
        siguiente = f"../../{carpeta_de(semana + 1)}/semana-{semana + 1:02d}.ipynb"
        partes.append(f"[Semana siguiente]({siguiente})")
    return " | ".join(partes)


def indice_semana(semana: int) -> nbformat.NotebookNode:
    _, fechas, capitulos, contenido = datos_de(semana)
    nb = new_notebook()
    nb.cells = [
        new_markdown_cell(
            f"# Semana {semana}\n\n"
            f"**Fechas:** {fechas}  \n"
            f"**Capítulos:** {capitulos}  \n"
            f"**Contenido:** {contenido}\n\n"
            f"{navegacion(semana)}"
        ),
        new_markdown_cell(
            "## Clases\n\n"
            "| Clase | Unidad | Notebook |\n"
            "|---|---|---|\n"
            "| | | |"
        ),
        new_markdown_cell(
            "## Actividades\n\n"
            f"- [Tutoría]({archivo_semana(semana, 'tutoria')})\n"
            f"- [Quiz]({archivo_semana(semana, 'quiz')})\n"
            f"- [Repaso]({archivo_semana(semana, 'repaso')})"
        ),
        new_markdown_cell(
            "## Checklist de la semana\n\n"
            "- [ ] Leer los notebooks de cada clase\n"
            "- [ ] Resolver las prácticas\n"
            "- [ ] Asistir a la tutoría y anotar dudas\n"
            "- [ ] Hacer el quiz asincrónico\n"
            "- [ ] Repasar"
        ),
        new_markdown_cell(navegacion(semana)),
    ]
    return nb


def plantilla(titulo: str, cuerpo: str, semana: int) -> nbformat.NotebookNode:
    nb = new_notebook()
    volver = f"[Índice de la semana](semana-{semana:02d}.ipynb)"
    nb.cells = [
        new_markdown_cell(f"# {titulo} — Semana {semana}\n\n{volver}"),
        new_markdown_cell(cuerpo),
        new_markdown_cell(volver),
    ]
    return nb


def escribir_si_no_existe(ruta: Path, nb: nbformat.NotebookNode) -> None:
    if ruta.exists():
        print(f"Ya existe, no se toca: {ruta.relative_to(RAIZ)}")
        return
    nbformat.write(nb, ruta)
    print(f"Creado: {ruta.relative_to(RAIZ)}")


def crear_semana(semana: int) -> None:
    carpeta = RAIZ / carpeta_de(semana)
    (carpeta / "pdfs").mkdir(parents=True, exist_ok=True)

    escribir_si_no_existe(carpeta / f"semana-{semana:02d}.ipynb", indice_semana(semana))
    escribir_si_no_existe(
        carpeta / archivo_semana(semana, "tutoria"),
        plantilla("Tutoría", "## Fecha\n\n## Temas vistos\n\n## Dudas y respuestas\n\n## Código de la tutoría", semana),
    )
    escribir_si_no_existe(
        carpeta / archivo_semana(semana, "quiz"),
        plantilla("Quiz", "## Preguntas\n\nFormato: pregunta, mi respuesta, respuesta correcta y por qué.", semana),
    )
    escribir_si_no_existe(
        carpeta / archivo_semana(semana, "repaso"),
        plantilla("Repaso", "## Cheatsheet\n\n## Errores comunes\n\n## Conceptos clave", semana),
    )
    actualizar_inicio()


if __name__ == "__main__":
    if len(sys.argv) != 2 or not sys.argv[1].isdigit():
        sys.exit("Uso: uv run python herramientas/nueva_semana.py <número de semana>")
    crear_semana(int(sys.argv[1]))
