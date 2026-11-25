# Revisión del documento del estudio (24-nov-2026)

**Documento:** `documento/estudio-penonome.md`, copia de la actualización exportada a Descargas el 24-nov-2026.
**Método:** MCP `web-research` y descargas con `curl` y `pdftotext`. Las afirmaciones revisadas están en
`afirmaciones.csv`, y el estado de cada fuente en `fuentes.csv`.

## Figuras

- **Fotos:** las seis volvieron al documento, bajadas de Wikimedia Commons a `documento/img/`, con la licencia en el pie.
- **Gráficos rehechos con `documento/figuras.py`:**
  - servicios básicos del Censo 2023 (República, Coclé y distrito de Penonomé);
  - réplicas acumuladas.
- **No recuperados:** el mapa por corregimiento y la figura de lugares dañados. El original (`claude.ai/artifact/MPKruLqyPsH3GRhFdCyUU3`) no está compartido con esta cuenta. El mapa queda como tabla.

## Sección 15: verificada completa

| Fila | Veredicto | Cambio |
|---|---|---|
| CSS Coclé | Confirmado | Ninguno. |
| Variación nacional de asegurados | Discrepancia | El −12,853 es correcto. El reparto "más de la mitad en agricultura, comercio y hoteles" era de los 36,357 empleos que perdió Chiriquí; se quitó. |
| Ocupación hotelera | Confirmado y desactualizado | Se agregó septiembre de 2026 (55.9 %). Julio y agosto ahora apuntan a sus PDF. |
| Hoteles tras el sismo | Discrepancia | La ATP nombró hoteles dañados en Coclé (El Sitio, Dos Continentes), no "sobre todo en Azuero". |
| Banconal, mipymes y fondos | Confirmado | Ninguno. |
| Empresas afectadas | Confirmado | Ninguno. |
| Recaudación DGI | Confirmado y desactualizado | Pasa de mayo (B/.446.2 millones) a agosto de 2026 (B/.467.7 millones), el último IFP publicado. Septiembre y octubre todavía no existen. |
| Finanzas municipales | Confirmado | El enlace de la Gaceta Oficial devuelve HTML y no se pudo leer. |

## Sección 12: cronología

- **Cotejadas:** 27 de 67 filas, las que tienen cifras.
- **Corregidas:**
  - dos fechas «aprox.» se fijaron con la fecha real de la nota: 25-oct y 27-oct;
  - la frase «de 102 a 22 réplicas por día» no está en la fuente y se reemplazó por lo que la nota sí dice.
- **Sin cotejar:** las otras 40 filas siguen como estaban en el estudio original, y así lo dicen las limitaciones.

## Referencias

- **Antes:** 61 enlaces del texto faltaban en la lista y 3 entradas no se usaban.
- **Ahora:** la lista se genera desde `fuentes.csv` con `investigacion.py referencias`. Tiene 115 entradas y coincide exactamente con lo que el texto cita.
- **Títulos nuevos:** los de las fuentes que se agregaron se leyeron de la página de cada una.

## Pendiente

- Cotejar las 40 filas restantes de la cronología.
- Pedir a SINAPROC o al Miviot el desglose provincial de daños posterior al 14-oct.
- Rehacer el mapa por corregimiento con la capa de ANATI.
