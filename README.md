# samsung-sic

Cuaderno de estudio del programa **Samsung Innovation Campus 2026** (Python, Inteligencia Artificial e IA Generativa, 24 semanas).

## Empezar

Requisitos: [uv](https://docs.astral.sh/uv/) y Python 3.14. Para los ejemplos de `turtle` (semana 2, unidad 20)
hace falta `tkinter`: en macOS con Homebrew, `brew install python-tk@3.14`.

```bash
uv sync                # crea el ambiente (Python 3.14 + JupyterLab)
uv run jupyter lab     # abre el cuaderno
```

Abre `00-inicio.ipynb`: es la portada con el cronograma y los links a cada semana.

## Estructura

```
00-inicio.ipynb          portada y cronograma enlazado
glosario.ipynb           glosario acumulado del curso
01-python/               semanas 0–8 (la 0 es la preparatoria, capítulo 1)
02-ia/                   semanas 9–18
03-ia-generativa/        semanas 19–24
  semana-NN/
    semana-NN.ipynb      índice de la semana
    clase-*/uNN-*.ipynb  una unidad por notebook
    tutoria.ipynb
    quiz.ipynb           quiz de práctica
    repaso.ipynb
    quiz-calificado.ipynb, actividad-asincronica.ipynb   evaluaciones de la plataforma (si las hay)
proyectos/               cada proyecto con su propio ambiente
herramientas/            scripts para crear semanas y regenerar el índice y el toc del sitio
myst.yml                 configuración del sitio (Jupyter Book 2 / MyST)
recursos/                cronograma y material de apoyo
```

## Sitio web

El cuaderno se publica como sitio de lectura con [Jupyter Book 2](https://jupyterbook.org) (motor MyST),
usando las salidas ya guardadas en los notebooks (no se ejecuta nada al construir). Jupyter Book es una
dependencia de desarrollo (`uv sync` la instala) y trae su propio Node.js, así que no hace falta instalar Node.

```bash
uv run jupyter book start            # previsualización local con recarga en http://localhost:3000
uv run jupyter book build --html     # construye el sitio estático en _build/html
```

El índice del sitio (`toc` en `myst.yml`) se regenera solo con `herramientas/actualizar_inicio.py` y
`herramientas/construir_semana.py`; para forzarlo: `uv run python herramientas/actualizar_toc.py`.
Al hacer push a `main`, Cloudflare Workers Builds ejecuta `wrangler deploy`: `wrangler.jsonc` construye el sitio y
publica `_build/html`.

## Nueva semana

```bash
uv run python herramientas/nueva_semana.py 2
```

Los PDFs oficiales del curso no se publican en el repositorio (`*.pdf` está en `.gitignore`).
