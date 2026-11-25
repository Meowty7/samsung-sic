# Semana 04 — cuaderno de estudio

**Objetivo:** semana 4 completa (ordenamiento, greedy, divide y vencerás) con la estructura habitual, más la
actividad asincrónica y el quiz calificado resueltos.
**Restricciones:** español neutro, sin emojis, fidelidad al PDF con páginas citadas, PDFs fuera del repo público.
**Checks:** notebooks ejecutan sin errores; `herramientas/validar.py`; build del sitio.

## Hallazgo
Los PDFs venían rotulados "semana 3" pero son de la semana 4 (U27–U31; cronograma 2/11–7/11, capítulos 5 y 6).
Parte 1 (155 págs.): U27 desde pág. 4, U28 desde 68, U29 desde 113. Parte 2 (94 págs.): U30 desde 4, U31 desde 53.

## Tareas
- [x] T1 Esqueleto, PDFs movidos y renombrados, mapa de unidades, configuración en `construir_semana.py` — inline
- [x] T2 Notebooks U27–U31 — delegado (5 agentes, archivos disjuntos; disparador: lectura de 249 págs.).
  Rangos reales: U27 4–67, U28 68–112, U29 113–153 (parte 1); U30 4–52, U31 53–94 (parte 2).
- [x] T3 Índice, quiz de práctica, repaso, glosario y toc — inline
- [x] T4 Actividad asincrónica y quiz calificado (dependen de `partition1` y quicksort de la U29) — inline
- [x] T5 Validación, commit, push y verificación del sitio

## Progreso
- 2026-10-19: T1–T5 terminadas. `partition1` del PDF usa `left < right` y falla con listas como [1, 2, 3]; las
  respuestas usan la versión corregida. Quiz Q27-02: el enunciado repite el Output de la Q27-01.
