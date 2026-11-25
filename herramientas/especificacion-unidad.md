# Especificación de notebooks de unidad — Samsung Innovation Campus 2026, Semana N

Repo: raíz de este curso (proyecto uv, Python 3.12, JupyterLab instalado; usar `uv run ...` desde la raíz).
Material de estudio para un alumno. Idioma de TODO el contenido: español neutro y profesional (sin voseo, sin modismos).

## Reglas duras
- PROHIBIDO usar emojis o iconos decorativos (nada de 📄 📌 ⚠️ 🎯 ✅ ❌ etc.) en ningún lugar: markdown, código, salidas.
  En su lugar, etiquetas de texto en negrita: **Referencia:**, **Clave:**, **Error común:**, **Para el quiz:**, **Ampliación (no está en el PDF):**, **Nota sobre el PDF:**.
- Fidelidad al PDF: cada sección del resumen termina con `**Referencia:** PDF parte N, pág. X` (o `págs. X–Y`). Los números de página son los del PDF real (los marcadores `===== PAGINA N =====` del texto extraído).
- Todo lo que agregues que NO esté en el PDF va marcado como **Ampliación (no está en el PDF):**. Así el alumno distingue lo oficial de lo extra.
- Si el PDF tiene un error (traducción rota, código que no corre, salida incorrecta), muéstralo corregido y explícalo con **Nota sobre el PDF:**.
- Verificación visual: muchas diapositivas son imágenes y el texto extraído es incompleto. Para cada página con poco texto o con código/diagramas relevantes, renderízala y mírala:
  `pdftoppm -f X -l X -r 60 -png "<pdf>" <scratchpad>/img/pX` y luego léela con la herramienta Read. No inventes contenido de páginas que no viste.
- Identificadores del código como en el PDF (por ejemplo `persona1`, `cafe_menu`), comentarios en español.
- No toques archivos fuera de los que te asignaron. No hagas commits de git.

## Estructura de cada notebook de unidad (en este orden)
1. **Encabezado** (markdown): `# Unidad NN — Título`, línea con `Semana N · Clase K · Fuente: PDF parte N, págs. X–Y`, y navegación:
   `[Índice de la semana](../semana-01.ipynb) | [Anterior](ruta) | [Siguiente](ruta)` (rutas relativas, te las doy en el encargo).
2. **Celda de código de apoyo** con la función de verificación (cópiala tal cual):
   ```python
   def verificar(descripcion, obtenido, esperado):
       """Compara el resultado de un ejercicio con el esperado e informa sin detener el notebook."""
       if obtenido == esperado:
           print(f"Correcto: {descripcion}")
       else:
           print(f"Incorrecto: {descripcion}. Se esperaba {esperado!r} y se obtuvo {obtenido!r}")
   ```
3. `## Objetivos de la unidad` — los del PDF.
4. `## Contexto` — la motivación/problema que plantea el PDF (big data, cafetería, etc.), breve.
5. Secciones de concepto, siguiendo el orden del PDF. Cada una: explicación en markdown (qué es, por qué existe, cómo se usa), una o más celdas de código ejecutables con ejemplos (que muestren salida), y al cierre las notas **Clave:** / **Error común:** / **Para el quiz:** cuando apliquen, más la **Referencia:**.
   Incluye los ejemplos de código del PDF y añade otros propios (marcados como ampliación si el concepto no está en el PDF).
6. `## Proyecto de la unidad` — el caso práctico del PDF: problema, plan de programación (los pasos del PDF), código final comentado y ejecutado, resultado esperado. Si usa `input()`, encapsúlalo en una función y deja una versión no interactiva que se ejecute (por ejemplo, procesando una lista de comandos de prueba); la llamada interactiva queda comentada con la instrucción `# Para usarlo de forma interactiva, quita el comentario de la siguiente línea`.
   Si el PDF tiene secciones de "Programación en pareja" o ejercicios propios, inclúyelos aquí o en Práctica con su referencia.
7. `## Práctica` — entre 6 y 8 ejercicios de dificultad creciente sobre lo visto. Cada ejercicio:
   - markdown con el enunciado (`### Ejercicio N — título`),
   - celda de código con la función a completar (`def nombre(...):\n    # Escribe tu solución aquí\n    pass`),
   - celda de código que llama a `verificar(...)` con 2–3 casos,
   - markdown con la solución plegada:
     `<details><summary>Ver solución</summary>\n\n```python\n...\n```\n\nExplicación breve.\n</details>`
8. `## Apuntes para estudiar` — consolidado de la unidad en tres listas: **Clave**, **Errores comunes**, **Para el quiz**.
9. `## Autoevaluación` — 5 preguntas conceptuales, cada respuesta plegada con `<details><summary>Ver respuesta</summary>...</details>`.
10. **Pie** con la misma navegación del encabezado.

## Construcción y validación
- Genera el `.ipynb` con un script Python que use `nbformat` (v4), guardado en tu carpeta del scratchpad (no en el repo). Ejecútalo con `uv run python <script>` desde la raíz del repo.
- Después ejecuta el notebook para guardar las salidas y comprobar que todo corre:
  `uv run jupyter nbconvert --to notebook --execute --inplace "<ruta del notebook>"`
  Debe terminar sin errores. Las prácticas sin resolver imprimen "Incorrecto: ..." y eso está bien; ninguna celda debe lanzar excepción (salvo que sea un ejemplo didáctico de error: en ese caso captúralo con try/except y muestra el mensaje).
- Verifica el JSON: `uv run python -c "import nbformat; nbformat.validate(nbformat.read('<ruta>', 4))"`.

## Aportes para los archivos de la semana
Además del notebook, escribe `herramientas/aportes/semana-NN/uXX.md` por cada unidad con:
- `## Glosario` — 4–8 términos `**término**: definición`.
- `## Quiz` — 6 preguntas de opción múltiple (4 opciones, una correcta, indicar cuál y una explicación de una línea), en este formato exacto:
  ```
  P: enunciado
  A) ...
  B) ...
  C) ...
  D) ...
  Correcta: B
  Por qué: ...
  Referencia: PDF parte N, pág. X
  ```
- `## Cheatsheet` — 8–15 líneas `código  # qué hace`.
- `## Errores comunes` — 3–6 viñetas.

## Informe final (tu respuesta)
Breve: archivos creados, títulos reales de las unidades, páginas que verificaste visualmente, errores del PDF encontrados, y cualquier contenido que no pudiste verificar.

## Lecciones de la semana 1 (aplícalas)
- La portada de la unidad siguiente no pertenece a la unidad actual: ajusta el rango real de páginas en el encabezado e indícalo en el informe.
- Los PDFs son traducciones automáticas: nombres de funciones y métodos traducidos (por ejemplo "filtro" por `filter`, "mapa" por `map`), comillas rotas, variables con nombres distintos entre diapositivas y salidas que no coinciden con el código. Ejecuta todo el código del PDF y corrige con **Nota sobre el PDF:**.
- Si la unidad trae temas que no estaban en el encargo, inclúyelos igual, con su referencia.
- Si un ejemplo escribe archivos, hazlo en una carpeta temporal para no ensuciar el repo.
- Antes de guardar, comprueba cada solución plegada contra sus casos de `verificar`.
