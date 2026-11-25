# Sitio web de estudio (Jupyter Book)

**Objetivo:** publicar el cuaderno como sitio de lectura (menú lateral, buscador, modo oscuro) en GitHub Pages,
regenerado automáticamente en cada push a `main`.
**Problema:** JupyterLab es cómodo para ejecutar, no para leer y repasar (ni desde el celular).
**Alcance:** configuración de Jupyter Book 2 (MyST), índice generado desde el cronograma, workflow de GitHub Actions,
activación de Pages, ajustes de contenido que no rendericen bien (plegables, links, diagramas).
**Restricciones:** el sitio no ejecuta código (usa las salidas guardadas); los PDFs no se publican; sin emojis.
**Checks:** build local sin errores ni links rotos internos; workflow verde; sitio accesible.

## Tareas
- [x] T1 Configuración MyST + índice generado + build local limpio — delegado (escritor único; varios archivos y documentación externa).
  Jupyter Book 2.1.7 (trae su propio Node). 36 páginas, sin advertencias.
- [x] T2 Workflow de GitHub Actions + activación de Pages + verificación del sitio publicado — inline.
  Run 39321938659: build y deploy en verde. Portada, unidades y buscador responden 200.
- [x] T3 Documentación (README, CLAUDE.md) — con T1

## Progreso
- 2026-10-19: publicado en GitHub Pages (desactivado después).
- Limitaciones conocidas: la interfaz del tema queda en inglés (Jupyter Book 2 no tiene opción de idioma);
  las URLs usan el nombre del archivo y los repetidos se numeran (`quiz`, `quiz-1`, `quiz-2`).
