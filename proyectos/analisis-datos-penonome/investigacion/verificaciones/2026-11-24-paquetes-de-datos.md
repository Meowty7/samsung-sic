# Verificación de los paquetes de datos (24-nov-2026)

**Nota del 25-nov-2026:** con el reenfoque del proyecto en las afectaciones sociales del sismo se retiraron las tablas y secciones de empleo, seguridad social, PIB, turismo y la comparación con Colombia. Este informe conserva solo lo que sigue en el proyecto; el detalle está en `2026-11-25-reenfoque-social.md`.

**Alcance:** `paquete_penonome/` (tablas 00 a 14 y 99, más el Excel).
**Método:** cada cifra contra el PDF o el dataset original con el MCP `web-research`. Los PDF se descargaron con
`curl` y se leyeron con `pdftotext`; las copias están en `descargas/`. Las sumas de control se calcularon con pandas.
Tres verificadores trabajaron en paralelo, cada uno con un grupo de fuentes distinto.

## Resultado por archivo

| Archivo | Veredicto | Nota |
|---|---|---|
| 00 catálogo | Corregido | La nota decía "dividido en 2023". Los seis corregimientos nuevos los creó la Ley 296 del 26-abr-2022. |
| 01 población Censo 2023 | Confirmado | Las 16 filas coinciden con el Cuadro 4. |
| 02 viviendas Censo 2023 | Confirmado | Las 18 filas y las 24 columnas coinciden con el Cuadro 1; el orden de columnas corregido el 21-nov es el correcto. |
| 14 trazabilidad | Corregido | Una cita de una tabla que después se retiró mezclaba dos fechas. |
| 99 base larga | Corregido | Arrastraba errores de tablas que después se retiraron del proyecto. |

## Afirmaciones de los LEEME

- **El sismo de Panamá (9-oct-2026, epicentro en Azuero):** confirmado con fuentes independientes (USGS y SINAPROC).

## Pendiente

- El Excel guarda las fórmulas sin valores calculados; Excel los recalcula al abrirlo.
