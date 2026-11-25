# Semana 06 — cuaderno de estudio

**Objetivo:** semana 6 completa (ordenación de datos, series temporales, mini proyectos financiero y de la
pandemia) con la estructura habitual, más la actividad asincrónica y el quiz calificado resueltos.
**Restricciones:** español neutro, sin emojis, fidelidad al PDF con páginas citadas, PDFs fuera del repo público.
**Checks:** notebooks ejecutan sin errores; `herramientas/validar.py`; build del sitio.

## Hallazgo
Parte 1 (164 págs., capítulo 7): U37 4–72, U38 73–162 (la portada del capítulo lista U34–U38, pero U34–U36 no
están en este PDF: corresponden a la semana 5, que todavía no está en el repo).
Parte 2 (90 págs., capítulo 8): U39 4–56, U40 57–90.
La actividad asincrónica y el quiz cubren U34–U38 (pandas básico) aunque esas unidades no tienen notebook aún.
Dependencias nuevas: pandas 3.1, matplotlib, seaborn, folium, yfinance.

## Tareas
- [x] T1 Esqueleto, PDFs movidos, mapa de unidades, dependencias — inline
- [x] T2 Notebooks U37–U40 — delegado (4 agentes, archivos disjuntos; disparador: lectura de 254 págs.)
- [x] T3 Actividad asincrónica y quiz calificado — delegado (1 agente; disparador: 2 archivos no triviales)
- [x] T4 Configuración en `construir_semana.py`; índice, quiz de práctica, repaso, glosario y toc — inline
- [x] T5 Validación, commit, push y verificación del sitio

## Progreso
- 2026-10-22: T1 terminada.
- 2026-10-22: T2–T5 terminadas. Rangos reales: U37 4–72, U38 74–162, U39 4–56, U40 57–88. Datos reales guardados
  en `semana-06/datos/` (yfinance, FRED, OWID, UCI) para ejecutar sin red. `ted.csv` (7,6 MB, copia pública de
  justmarkham) junto al notebook de la actividad. Links rotos solo hacia semana 5 (no construida) y semana 7.
