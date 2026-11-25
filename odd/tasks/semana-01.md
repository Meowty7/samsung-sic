# Semana 01 — cuaderno de estudio

**Objetivo:** dejar el curso SIC 2026 organizado como notebooks enlazados y la semana 1 completa para estudiar y repasar.
**Problema:** PDFs extensos (467 + 189 páginas) sin resumen, práctica ni navegación.
**Alcance:** ambiente uv, estructura del curso, herramientas de generación, 7 notebooks de unidad (U10–U16),
índice de semana, quiz, repaso, tutoría, glosario. Publicación en GitHub.
**Restricciones:** español neutro, sin emojis, fidelidad al PDF con páginas citadas, PDFs fuera del repo público.
**TDD:** no aplica (material de estudio). Check funcional: todos los notebooks ejecutan sin errores con nbconvert.

## Hallazgo
`semana-01-parte-2.pdf` es una copia de las unidades 14–16 de la parte 1 (págs. 283–467).
Clase 1 = U10–U13 (parte 1, págs. 5–282). Clase 2 = U14–U16 (parte 2, págs. 5–189).

## Tareas
- [x] T1 Ambiente uv (Python 3.12, JupyterLab), estructura, `.gitignore`, PDFs movidos — inline
- [x] T2 Herramientas: `cronograma.py`, `nueva_semana.py`, `actualizar_inicio.py`, `00-inicio.ipynb` — inline
- [x] T3 Notebooks U10–U16 — delegado (4 agentes, archivos disjuntos; disparador: lectura de 650 págs.).
  Todas las páginas con contenido verificadas visualmente; errores del PDF marcados con "Nota sobre el PDF".
- [x] T4 Índice de semana, quiz (42 preguntas), repaso, glosario a partir de los aportes — inline
- [x] T5 Validación: 11 notebooks válidos, sin errores de ejecución ni emojis. Único link pendiente:
  semana-01 -> semana-02 (se resuelve al crear la semana 2).
- [x] T6 Commit y push a `Meowty7/samsung-sic`

## Progreso
- 2026-10-19: T1 y T2 terminadas.
- 2026-10-19: T3–T6 terminadas. Rangos reales: U10 5–88, U11 89–148, U12 149–208, U13 209–281 (parte 1);
  U14 5–64, U15 65–125, U16 127–189 (parte 2).

## Siguiente paso
Semana 2: `uv run python herramientas/nueva_semana.py 2` cuando lleguen los PDFs.
