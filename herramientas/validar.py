"""Valida todos los notebooks: formato, errores de ejecución, emojis y links rotos.

Uso (desde la raíz del curso): uv run python herramientas/validar.py
"""
import re, sys, unicodedata
from pathlib import Path
import nbformat
raiz = Path(__file__).resolve().parent.parent; problemas = 0
emoji = re.compile("[\U0001F300-\U0001FAFF☀-➿⭐⭕✅❌️]")
for nb_path in sorted(raiz.rglob("*.ipynb")):
    if {".venv", ".ipynb_checkpoints", "_build"} & set(nb_path.parts): continue
    nb = nbformat.read(nb_path, 4); nbformat.validate(nb)
    for c in nb.cells:
        for o in c.get("outputs", []):
            if o.get("output_type") == "error":
                print("ERROR de ejecución:", nb_path, o.get("ename")); problemas += 1
        if emoji.search(c.source):
            print("EMOJI:", nb_path, emoji.findall(c.source)[:3]); problemas += 1
        if c.cell_type == "markdown":
            for link in re.findall(r"\]\(([^)\s]+)\)", re.sub(r"`[^`]*`", "", c.source)):
                if link.startswith(("http", "#", "mailto")): continue
                if not (nb_path.parent / link.split("#")[0]).exists():
                    print("LINK roto:", nb_path.relative_to(raiz), "->", link); problemas += 1
print("problemas:", problemas)
