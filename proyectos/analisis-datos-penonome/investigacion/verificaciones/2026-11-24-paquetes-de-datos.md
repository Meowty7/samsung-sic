# Verificación de los paquetes de datos (24-nov-2026)

**Alcance:** `paquete_penonome/` (tablas 00 a 14 y 99, más el Excel) y `comparacion/` (archivos 20 a 31 y el mapa).
**Método:** cada cifra contra el PDF o el dataset original con el MCP `web-research`. Los PDF se descargaron con
`curl` y se leyeron con `pdftotext`; las copias están en `descargas/`. Las sumas de control se calcularon con pandas.
Tres verificadores trabajaron en paralelo, cada uno con un grupo de fuentes distinto.

## Resultado por archivo

| Archivo | Veredicto | Nota |
|---|---|---|
| 00 catálogo | Corregido | La nota decía "dividido en 2023". Los seis corregimientos nuevos los creó la Ley 296 del 26-abr-2022. |
| 01 población Censo 2023 | Confirmado | Las 16 filas coinciden con el Cuadro 4. |
| 02 viviendas Censo 2023 | Confirmado | Las 18 filas y las 24 columnas coinciden con el Cuadro 1; el orden de columnas corregido el 21-nov es el correcto. |
| 03 EML condición | Confirmado | Cuadro 2; oct-2024 figura como revisado (R). |
| 04 EML categoría | Confirmado | Cuadro 8. |
| 05 EML rama | Corregido | "Extraterritoriales y no declaradas" oct-2024 tenía 115 ocupados, que eran del bloque de Colón; en Coclé es 0. |
| 06 EML informalidad | Confirmado | Cuadro 7. |
| 07 CSS Coclé | Confirmado, enlace reemplazado | El boletín CSS 2020 ya no existe; las cifras están en la copia del INEC. |
| 08 y 09 CSS Datos Abiertos | Confirmado | La API CKAN del portal coincide. Faltaban en la base larga 99; ya están. |
| 10 PIB Coclé | Confirmado | Los 140 valores coinciden. Las diferencias de suma (4.3 millones en 2024, 11.9 en 2021) son la discrepancia estadística que explica el INEC. |
| 11 a 13 ATP | Confirmado | Julio y agosto de 2026 ahora apuntan a su PDF, no a la portada. |
| 14 trazabilidad | Corregido | La cita de informalidad mezclaba oct-2024 y sep-2025. |
| 99 base larga | Corregido | Arrastraba el error de 05; le faltaban la tabla 09 y nueve provincias de la 08. |
| 20 GEIH ciudades | Confirmado | 104 filas. `cambio_pp` difiere 0.1 del DANE en cuatro filas por redondeo; queda documentado. |
| 21 GEIH mensual | Confirmado, fuentes precisadas | Las 13 ciudades de jun, jul y sep están en los boletines técnicos, no en las presentaciones. |
| 22 impacto del sismo | Corregido | La línea base de Coclé decía 7.1% (sep-2025); ahora dice 5.5% (ago-2026). Los daños de Chocó y Caldas son del 15-ago, no del 12. La fecha del sismo de Panamá ahora cita a SINAPROC. |
| 23 socioeconómico | Corregido | La informalidad de Coclé está en el Cuadro 7 (decía 11). El desempleo departamental de ANIF es secundario y no tiene periodo. |
| 24 índice relativo | Confirmado, notas corregidas | Todos los cocientes se recalcularon. El IPM 2025 de Colombia es 9.9%, igual que el de Coclé por coincidencia. |
| 30 escenarios | Consistente | Parte de 5.5%. Es un modelo, no un dato. |
| 31 diferencias en diferencias | Confirmado | Recalculado: -1.87, -0.80, -0.42 y +0.18. |

## Afirmaciones de los LEEME

- **"Agosto 2026 no tiene cuadros por provincia": falso.** El INEC publicó el informe de agosto de 2026 el 29-sep-2026 con cuadros provinciales: Coclé 5.5% de desempleo y 59.5% de informalidad no agrícola; el país, 8.5% y 45.8%.
- **El sismo de Colombia (10-ago-2026, Mw 7.4, San José del Palmar) y el de Panamá (9-oct-2026, epicentro en Azuero):** los dos están confirmados con fuentes independientes (USGS, OPS, UNGRD vía prensa y SINAPROC).

## Pendiente

- La EML de agosto de 2026 no está transcrita como tabla en `paquete_penonome/`.
- El Excel guarda las fórmulas sin valores calculados; Excel los recalcula al abrirlo.
