# Datos del análisis principal

Tablas del sismo que usa el análisis principal (`analisis-penonome.ipynb`), además de `datos/penonome/`. Cada fila trae su fuente, y todas están registradas en `investigacion/fuentes.csv`.

| Archivo | Qué contiene | Tipo de fuente |
|---|---|---|
| `afectaciones_sinaproc_cocle.csv` | Evaluación de daños y análisis de necesidades (EDAN) de Coclé en formato largo: viviendas evaluadas y personas que viven en ellas, viviendas por nivel de daño, personas por edad y sexo, personas con discapacidad y mujeres embarazadas (en total y según el daño de su vivienda), y otras afectaciones del COE (lesionados, escuelas, hospitales, albergues, ayuda alimentaria) | Oficial (plataforma de afectaciones de SINAPROC, enlazada en Panamá Conecta). EDAN: cifras finales del 9-oct al 15-nov-2026. Otras afectaciones: corte del COE al consultar la plataforma el 25-nov-2026 |
| `afectaciones_sinaproc_provincias.csv` | Viviendas evaluadas y personas que viven en ellas en las 11 provincias y comarcas con evaluaciones | Oficial (misma plataforma, cifras finales al 15-nov-2026) |
| `edan_sinaproc_distritos_cocle.csv` | Viviendas evaluadas de Coclé por distrito: nivel de daño, personas, adultos mayores, personas con discapacidad y embarazadas | Cálculo propio con la capa pública de la EDAN de SINAPROC (un punto por vivienda evaluada) y los límites del Censo 2023 de Esri Panamá. Generado por `investigacion/edan_por_zona.py` |
| `edan_sinaproc_corregimientos_penonome.csv` | Lo mismo para los 16 corregimientos de Penonomé, con la clave `id_corregimiento` del catálogo | Mismo cálculo; aproximado por la calidad de las coordenadas (ver abajo) |
| `danos_sinaproc_cocle.csv` | Viviendas afectadas en Coclé en los comunicados #5, #7 y #12 de SINAPROC (10 al 14 de octubre) | Oficial; balances preliminares. «Afectadas» del comunicado y «evaluadas» de la EDAN no son la misma unidad |
| `registros_danos_corregimiento.csv` | Registros de daños por corregimiento según la compilación de prensa de mapadelterremoto.com | Prensa (compilación); son registros, no unidades dañadas |
| `replicas_acumuladas.csv` | Réplicas localizadas por el IGC-UP, según la prensa | Prensa con datos del IGC-UP |
| `poblacion_proyeccion_2023_2026.csv` | Población del distrito de Penonomé (Censo 2023 y proyecciones 2024-2026) y de Coclé (2025-2026) | Oficial (INEC, proyecciones revisadas con el Censo 2023) |
| `situacion_actual_2026.csv` | Cómo está hoy: balances nacionales del sismo, viviendas en reconstrucción, fichas sociales de emergencia, estudiantes sin clases presenciales y suspensión de cortes de luz | Oficial o prensa con datos oficiales (columna `tipo_fuente`) |

## Viviendas evaluadas por distrito y corregimiento

SINAPROC publica un punto por vivienda evaluada en la capa [`Sismo9oct_EDAN_Conteos`](https://sig.sinaproc.gob.pa/server/rest/services/Hosted/Sismo9oct_EDAN_Conteos/FeatureServer/0), sin nombres ni cédulas. `investigacion/edan_por_zona.py` descarga los 2,531 puntos de Coclé, asigna cada uno al corregimiento que contiene su coordenada (límites del [Censo 2023 de Esri Panamá](https://ags.esri.co/arcgis/rest/services/PanamaLivingAtlas/Censo_Poblacion_Corregimiento_Panama_2023/MapServer/0)) y guarda solo totales.

- **Control:** el script comprueba que los puntos de Coclé suman 2,531 viviendas, 10,199 personas, 431 personas con discapacidad y 21 embarazadas, igual que la ficha de la plataforma. Los distritos suman esos mismos totales.
- **Límites:** el área de cada polígono coincide con la superficie del Cuadro 4 del INEC. La columna de población de la capa de Esri tiene 7 corregimientos cruzados y no se usa.
- **Coordenadas:** muchas viviendas comparten coordenada (en la cabecera de Penonomé, 165 en un mismo punto), probablemente el lugar donde se llenó la ficha. Por eso el reparto por corregimiento es aproximado; la columna `viviendas_con_coordenada_compartida` indica cuántas están en ese caso. 18 viviendas tienen coordenadas fuera de Coclé.
- **Ceros:** Riecito y Río Indio no tienen viviendas evaluadas y Tulú tiene una. Eso no prueba que no hubo daño: puede que la evaluación no llegara a esas zonas.
- **Privacidad:** en la tabla por corregimiento, los conteos de 1 a 4 personas con discapacidad o embarazadas quedan en blanco.

Sumas de control de `afectaciones_sinaproc_cocle.csv`: los cinco niveles de daño suman las 2,531 viviendas evaluadas; los grupos de edad y sexo suman las 10,199 personas; el desglose por nivel de daño suma las 431 personas con discapacidad y las 21 embarazadas.
