# Datos del análisis principal

Tablas propias del análisis principal (`analisis-penonome.ipynb`), además de `datos/penonome/` y `datos/comparacion-colombia/`. Cada fila trae su fuente, y todas están registradas en `investigacion/fuentes.csv`.

| Archivo | Qué contiene | Tipo de fuente |
|---|---|---|
| `desempleo_cocle_2019_2026.csv` | Siete cortes de la EML: PEA, ocupados, desocupados y tasas de Coclé y del país | Oficial (INEC), cotejada el 24-nov-2026 |
| `danos_sinaproc_cocle.csv` | Viviendas afectadas en Coclé en tres comunicados de SINAPROC | Oficial |
| `registros_danos_corregimiento.csv` | Registros de daños por corregimiento según la compilación de prensa de mapadelterremoto.com | Prensa (compilación); son registros, no unidades dañadas |
| `replicas_acumuladas.csv` | Réplicas localizadas por el IGC-UP, según la prensa | Prensa con datos del IGC-UP |
| `ocupacion_hotelera_2025_2026.csv` | Ocupación hotelera nacional, 2025 y meses de 2026 | Oficial (ATP); solo nacional |
| `eml_cocle_agosto_2026.csv` | Encuesta de Mercado Laboral de agosto de 2026 para Coclé: desempleo por sexo y área, participación, subempleo, ocupados por categoría y rama, informalidad | Oficial (INEC); nuevo marco muestral, por eso `quiebre_serie = si` |
| `poblacion_proyeccion_2023_2026.csv` | Población del distrito de Penonomé (Censo 2023 y proyecciones 2024-2026) y de Coclé (2025-2026) | Oficial (INEC, proyecciones revisadas con el Censo 2023) |
| `situacion_actual_2026.csv` | Cómo está hoy: balances del sismo, viviendas en reconstrucción, ayuda social, escuelas, turismo, crédito, agro, empleo de la mina y canasta básica | Oficial, prensa con datos oficiales o empresa (columna `tipo_fuente`) |

