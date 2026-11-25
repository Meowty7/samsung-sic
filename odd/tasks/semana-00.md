# Semana 00 — cuaderno de estudio (preparatoria)

**Objetivo:** cubrir el capítulo 1 (fundamentos) que faltaba, con la misma estructura de las semanas 1 y 2.
**Alcance:** semana 0 en el cronograma y las herramientas, 9 notebooks de unidad (U1–U9), índice, quiz, repaso,
glosario acumulado. Publicación en GitHub.
**Restricciones:** español neutro, sin emojis, fidelidad al PDF con páginas citadas, PDFs fuera del repo público.
**TDD:** no aplica (material de estudio). Check funcional: notebooks ejecutan sin errores; `herramientas/validar.py`.

## Hallazgo
Un único PDF (`semana-00.pdf`, 543 págs.). Unidades: U1 14–81, U2 82–126, U3 127–188, U4 189–250, U5 251–299,
U6 300–358, U7 359–422, U8 423–488, U9 489–543 (aprox.). Dividido en clase 1 = fundamentos (U1–U4) y
clase 2 = control de flujo (U5–U9). El PDF enseña Anaconda; el cuaderno usa uv: se explica como ampliación.

## Tareas
- [x] T1 Semana 0 en `cronograma.py`, navegación desde la semana 0 en las herramientas, esqueleto, PDF movido — inline
- [x] T2 Notebooks U1–U9 — delegado (5 agentes, archivos disjuntos; disparador: lectura de 543 págs.).
  Rangos reales: U1 14–80, U2 81–125, U3 126–187, U4 189–249, U5 250–298, U6 299–357, U7 358–421,
  U8 423–487, U9 489–541.
- [x] T3 Configuración en `construir_semana.py`, índice, quiz (54 preguntas), repaso, glosario — inline.
  `leer_aporte` acepta `u01.md` y `u1.md`.
- [x] T4 Validación y re-generación de las semanas 1 y 2: sin errores; único link pendiente semana-02 -> semana-03.
- [x] T5 Commit y push

## Progreso
- 2026-10-19: T1–T5 terminadas.
