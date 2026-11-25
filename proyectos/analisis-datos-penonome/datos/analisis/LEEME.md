# Datos del análisis principal

Tablas del sismo que usa el análisis principal (`analisis-penonome.ipynb`), además de `datos/penonome/`. Cada fila trae su fuente, y todas están registradas en `investigacion/fuentes.csv`.

| Archivo | Qué contiene | Tipo de fuente |
|---|---|---|
| `afectaciones_sinaproc_cocle.csv` | Evaluación de daños y análisis de necesidades (EDAN) de Coclé en formato largo: viviendas evaluadas y personas que viven en ellas, viviendas por nivel de daño, personas por edad y sexo, personas con discapacidad y mujeres embarazadas (en total y según el daño de su vivienda), y otras afectaciones del COE (lesionados, escuelas, hospitales, albergues, ayuda alimentaria) | Oficial (plataforma de afectaciones de SINAPROC, enlazada en Panamá Conecta). EDAN: cifras finales del 9-oct al 15-nov-2026. Otras afectaciones: corte del COE al consultar la plataforma el 25-nov-2026 |
| `afectaciones_sinaproc_provincias.csv` | Viviendas evaluadas y personas que viven en ellas en las 11 provincias y comarcas con evaluaciones | Oficial (misma plataforma, cifras finales al 15-nov-2026) |
| `danos_sinaproc_cocle.csv` | Viviendas afectadas en Coclé en los comunicados #5, #7 y #12 de SINAPROC (10 al 14 de octubre) | Oficial; balances preliminares. «Afectadas» del comunicado y «evaluadas» de la EDAN no son la misma unidad |
| `registros_danos_corregimiento.csv` | Registros de daños por corregimiento según la compilación de prensa de mapadelterremoto.com | Prensa (compilación); son registros, no unidades dañadas |
| `replicas_acumuladas.csv` | Réplicas localizadas por el IGC-UP, según la prensa | Prensa con datos del IGC-UP |
| `poblacion_proyeccion_2023_2026.csv` | Población del distrito de Penonomé (Censo 2023 y proyecciones 2024-2026) y de Coclé (2025-2026) | Oficial (INEC, proyecciones revisadas con el Censo 2023) |
| `situacion_actual_2026.csv` | Cómo está hoy: balances nacionales del sismo, viviendas en reconstrucción, fichas sociales de emergencia, estudiantes sin clases presenciales y suspensión de cortes de luz | Oficial o prensa con datos oficiales (columna `tipo_fuente`) |

Sumas de control de `afectaciones_sinaproc_cocle.csv`: los cinco niveles de daño suman las 2,531 viviendas evaluadas; los grupos de edad y sexo suman las 10,199 personas; el desglose por nivel de daño suma las 431 personas con discapacidad y las 21 embarazadas.
