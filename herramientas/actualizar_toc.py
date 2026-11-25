"""Regenera la sección `toc` de myst.yml (índice del sitio) a partir del cronograma y los archivos.

Solo aparecen las semanas cuya carpeta existe. Jerarquía: Módulo > Semana N > índice de la
semana, clases con sus unidades, Tutoría, Quiz y Repaso. La portada es 00-inicio.ipynb; el
Glosario y los Proyectos van al final.

Uso (desde la raíz del curso):
    uv run python herramientas/actualizar_toc.py

`actualizar_inicio.py` lo llama, así que el flujo semanal no necesita pasos extra.
"""

import re
import sys
from pathlib import Path

import nbformat

sys.path.insert(0, str(Path(__file__).parent))
from cronograma import MODULOS, SEMANAS, archivo_semana, carpeta_de, modulo_de  # noqa: E402

RAIZ = Path(__file__).resolve().parent.parent
MYST = RAIZ / "myst.yml"
INICIO, FIN = "# toc:inicio", "# toc:fin"
SANGRIA = "  "  # el toc vive bajo `project:`


def titulo_de(ruta: Path, por_defecto: str) -> str:
    """Primer encabezado `# ...` del notebook; si no hay, `por_defecto`."""
    nb = nbformat.read(ruta, 4)
    for celda in nb.cells:
        if celda.cell_type != "markdown":
            continue
        for linea in celda.source.splitlines():
            if re.match(r"^# \S", linea):
                return linea[2:].strip()
        break
    return por_defecto


def texto(valor: str) -> str:
    """Escalar YAML entre comillas dobles."""
    return '"' + valor.replace("\\", "\\\\").replace('"', '\\"') + '"'


def titulo_clase(carpeta: Path) -> str:
    """`clase-1-listas-tuplas` -> `Clase 1: listas tuplas`."""
    _, numero, *resto = carpeta.name.split("-")
    return f"Clase {numero}: {' '.join(resto)}"


def entradas_semana(semana: int) -> list[str]:
    """Líneas del toc de una semana (sin sangría base) o [] si la semana no existe."""
    carpeta = RAIZ / carpeta_de(semana)
    indice = carpeta / f"semana-{semana:02d}.ipynb"
    if not indice.exists():
        return []
    rel = carpeta.relative_to(RAIZ).as_posix()
    lineas = [
        f"- title: {texto(titulo_de(indice, f'Semana {semana}'))}",
        "  children:",
        f"    - file: {rel}/{indice.name}",
        '      title: "Índice de la semana"',
    ]
    for clase in sorted(carpeta.glob("clase-*")):
        unidades = sorted(clase.glob("u[0-9][0-9]-*.ipynb"))
        if not unidades:
            continue
        lineas += [f"    - title: {texto(titulo_clase(clase))}", "      children:"]
        for u in unidades:
            titulo = titulo_de(u, u.stem)
            lineas += [f"        - file: {rel}/{clase.name}/{u.name}", f"          title: {texto(titulo)}"]
    for nombre, titulo in (("tutoria", "Tutoría"), ("quiz", "Quiz de práctica"),
                           ("quiz-calificado", "Quiz calificado"),
                           ("actividad-asincronica", "Actividad asincrónica"), ("repaso", "Repaso")):
        archivo = archivo_semana(semana, nombre)
        if (carpeta / archivo).exists():
            lineas += [f"    - file: {rel}/{archivo}", f"      title: {texto(titulo)}"]
    return lineas


def construir_toc() -> list[str]:
    """Elementos del toc, sangrados para quedar bajo `toc:` dentro de `project:`."""
    lineas = ["- file: 00-inicio.ipynb", '  title: "Portada"']
    for carpeta_modulo, nombre in MODULOS.items():
        hijos: list[str] = []
        for semana, *_ in SEMANAS:
            if modulo_de(semana) == carpeta_modulo:
                hijos += entradas_semana(semana)
        if hijos:
            lineas += [f"- title: {texto('Módulo ' + nombre)}", "  children:"]
            lineas += ["    " + l for l in hijos]
    if (RAIZ / "glosario.ipynb").exists():
        lineas += ["- file: glosario.ipynb", f"  title: {texto('Glosario')}"]
    if (RAIZ / "proyectos/README.md").exists():
        lineas += ["- file: proyectos/README.md", f"  title: {texto('Proyectos')}"]
        hijos = entradas_proyectos()
        if hijos:
            lineas += ["  children:"] + ["    " + l for l in hijos]
    return [SANGRIA * 2 + l for l in lineas]


def titulo_md(ruta: Path, por_defecto: str) -> str:
    """Primer encabezado `# ...` de un archivo Markdown; si no hay, `por_defecto`."""
    for linea in ruta.read_text(encoding="utf-8").splitlines():
        if re.match(r"^# \S", linea):
            return linea[2:].strip()
    return por_defecto


def entradas_proyectos() -> list[str]:
    """Cada proyecto con README.md: su README y, debajo, sus notebooks de la raíz y de `notebooks/`, los notebooks ejecutados de
    subcarpetas (`*_ejecutado.ipynb`), el documento (`documento/*.md`) y el historial (`verificaciones/*.md`)."""
    lineas: list[str] = []
    for proyecto in sorted(p for p in (RAIZ / "proyectos").iterdir() if (p / "README.md").exists()):
        rel = proyecto.relative_to(RAIZ).as_posix()
        paginas = [(n, titulo_de(n, n.stem)) for n in sorted(proyecto.glob("*.ipynb"))]
        paginas += [(n, titulo_de(n, n.stem)) for n in sorted(proyecto.glob("notebooks/**/*.ipynb"))]
        paginas += [(n, titulo_de(n, n.stem)) for n in sorted(proyecto.glob("*/*_ejecutado.ipynb"))]
        paginas += [(m, titulo_md(m, m.stem)) for m in sorted(proyecto.glob("documento/*.md"))]
        paginas += [(m, titulo_md(m, m.stem)) for m in sorted(proyecto.glob("investigacion/verificaciones/*.md"))]
        lineas += [f"- file: {rel}/README.md", f"  title: {texto(titulo_md(proyecto / 'README.md', proyecto.name))}"]
        if paginas:
            lineas.append("  children:")
            for ruta, titulo in paginas:
                lineas += [f"    - file: {ruta.relative_to(RAIZ).as_posix()}", f"      title: {texto(titulo)}"]
    return lineas


def actualizar_toc() -> None:
    contenido = MYST.read_text(encoding="utf-8")
    patron = re.compile(rf"{re.escape(SANGRIA)}{re.escape(INICIO)}\n.*?{re.escape(SANGRIA)}{re.escape(FIN)}", re.S)
    if not patron.search(contenido):
        raise SystemExit(f"myst.yml no tiene los marcadores {INICIO} / {FIN}")
    bloque = "\n".join([SANGRIA + INICIO, SANGRIA + "toc:", *construir_toc(), SANGRIA + FIN])
    MYST.write_text(patron.sub(lambda _: bloque, contenido), encoding="utf-8")
    print("Actualizado: toc de myst.yml")


if __name__ == "__main__":
    actualizar_toc()
