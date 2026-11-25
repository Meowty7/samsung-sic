# samsung-sic — cuaderno de estudio SIC 2026

Material de estudio personal del programa Samsung Innovation Campus 2026 (24 semanas, 2 clases por semana
con PDF, una tutoría y clases asincrónicas con quiz). Repo: github.com/Meowty7/samsung-sic (público).

## Ambiente
- `uv`, Python 3.14 de Homebrew (fijado en `.python-version`); es el único Python de la máquina además del de macOS.
  JupyterLab vive en el ambiente del curso. TensorFlow aún no publica wheels para 3.14: si el módulo de IA lo exige,
  ese proyecto o semana usará un Python aparte gestionado por uv.
- Cada proyecto de `proyectos/` tiene su propio `pyproject.toml` y su propio ambiente. No mezclar dependencias.

## Estructura
- `00-inicio.ipynb` se genera con `herramientas/actualizar_inicio.py`; no editarlo a mano.
- Nueva semana: `uv run python herramientas/nueva_semana.py N` (datos en `herramientas/cronograma.py`).
- Una unidad del PDF = un notebook `clase-K-<tema>/uNN-<tema>.ipynb`.

## Sitio web (Jupyter Book 2 / MyST)
- Configuración en `myst.yml`. El bloque `toc` entre `# toc:inicio` y `# toc:fin` lo genera
  `herramientas/actualizar_toc.py` (lo llaman `actualizar_inicio.py` y `construir_semana.py`); no editarlo a mano.
  Solo aparecen las semanas que existen; los títulos salen de la primera línea `# ...` de cada notebook.
  Cada proyecto de `proyectos/` con `README.md` entra bajo Proyectos con sus notebooks de la raíz y de `notebooks/`, los `*_ejecutado.ipynb` de subcarpetas, `documento/*.md` e `investigacion/verificaciones/*.md`.
- Previsualizar: `uv run jupyter book start`. Construir: `uv run jupyter book build --html` (salida en `_build/`, ignorada por git).
- No se ejecutan notebooks al construir: se usan las salidas guardadas. `<details>` y ```mermaid funcionan tal cual en el sitio y en JupyterLab.
- Se publica en Cloudflare Workers: cada push a `main` dispara Workers Builds, que corre
  `wrangler deploy`; `wrangler.jsonc` construye el sitio (build.command) y publica `_build/html`.
  GitHub Pages está apagado.
- `site.options.folders: true`: las direcciones siguen las carpetas, sin el prefijo numérico del módulo
  (`01-python/semana-01/quiz-calificado.ipynb` -> `/python/semana-01/quiz-calificado/`). Por eso los notebooks
  de cada semana no llevan prefijo de semana; el nombre se arma con `cronograma.archivo_semana()`.
- Evaluaciones de la plataforma por semana: `quiz-calificado.ipynb` y `actividad-asincronica.ipynb`
  (consigna, guía, respuesta ejecutada y explicación). El índice de la semana y el toc los enlazan si existen.
- Los links entre notebooks deben ser relativos y apuntar a `.ipynb` para que funcionen en ambos entornos.
- Apariencia: `estilos/sitio.css` (site.options.style). Colores como variables en `:root` y `.dark`, etiquetas en
  pastilla, animaciones suaves que respetan "reducir movimiento". Sin sombras tipo tarjeta (el usuario las descartó).
  `logo_text` y `pie-menu.md` reemplazan el "Made with MyST". Probar cambios con `uv run jupyter book start`.
- Semanas terminadas: `"checklist_completo": True` en su entrada de `SEMANAS` marca unidades, tutoría y repaso.

## Cómo trabajamos (acordado con el usuario)
- El usuario pega en el chat, por cada clase, los **objetivos, el contexto y el vocabulario** del docente, y deja los
  PDFs en la raíz del repo. Más tarde pega la **actividad asincrónica** y el **quiz** de la plataforma.
- **Se entrega por link, no por consola:** se publica en el repo y el sitio, se verifica que la página responda y se
  contesta con el link (más cualquier aviso que exija acción, como erratas del enunciado). Nunca se pegan las
  respuestas en el chat.
- Al terminar cada tarea: commit (conventional, sin atribución de IA), push y verificación del despliegue.
- El nombre del archivo PDF puede no coincidir con la semana real: manda el contenido (unidades) y el cronograma.

## Flujo para una semana nueva
1. `uv run python herramientas/nueva_semana.py N` y mover los PDFs a `<modulo>/semana-NN/pdfs/semana-NN-parte-K.pdf`.
2. Mapear unidades por página (buscar "Objetivo de aprendizaje de la unidad (1/" y las portadas "Unidad NN.").
   Comprobar si la parte 2 repite unidades de la parte 1 (pasó en las semanas 1 y 2).
3. Construir cada notebook de unidad según `herramientas/especificacion-unidad.md`, un agente por unidad (o dos
   unidades cortas), en paralelo y con archivos disjuntos; sus aportes van a `herramientas/aportes/semana-NN/uXX.md`.
4. Añadir la semana a `SEMANAS` en `herramientas/construir_semana.py` (objetivos, contexto y vocabulario del docente)
   y correr `uv run python herramientas/construir_semana.py N` (índice, quiz de práctica, repaso, glosario y toc).
5. Ejecutar el quiz de práctica con nbconvert y `uv run python herramientas/validar.py`. El único link roto aceptable
   es "Semana siguiente" hacia una semana que aún no existe. El push a `main` publica el sitio.

## Evaluaciones de la plataforma (actividad asincrónica y quiz calificado)
- Especificación completa: `herramientas/especificacion-evaluaciones.md`.
- Un generador por evaluación en `herramientas/evaluaciones/` (`actividad_sNN.py`, `quiz_sNN.py`); se copia el de una
  semana anterior como plantilla. Cada uno ejecuta y comprueba todas las respuestas antes de escribir el notebook.
- Al recibir la nota: en el generador, `Estado` pasa a `**Entregado. Nota final: X/Y.**` (o "Entregada") y el
  checklist a `[x]`; luego `uv run python herramientas/evaluaciones/<archivo>.py` y
  `uv run python herramientas/construir_semana.py N` (el checklist de la semana lee la nota del notebook).

## Reglas de contenido
- Todo en español neutro y profesional.
- Sin emojis ni iconos decorativos, en ningún archivo. Etiquetas de texto: **Referencia:**, **Clave:**,
  **Error común:**, **Para el quiz:**, **Ampliación (no está en el PDF):**, **Nota sobre el PDF:**.
- Cada resumen cita la página del PDF. Lo que no está en el PDF se marca como ampliación.
- Orden de cada notebook de unidad: encabezado y navegación, `verificar()`, objetivos, contexto, conceptos con
  ejemplos, proyecto de la unidad, práctica con verificación y solución plegada, apuntes, autoevaluación, pie.
- Los notebooks se guardan ejecutados (`jupyter nbconvert --execute --inplace`) y deben correr sin errores.
- Los PDFs oficiales no se publican (`*.pdf` en `.gitignore`).

## Git
- Conventional commits, sin atribución de IA. Push al terminar cada tarea.
