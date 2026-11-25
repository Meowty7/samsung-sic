# Paquete de datos oficiales: Penonomé y Coclé (versión 21-nov-2026)

Este paquete reúne en CSV todas las tablas oficiales usadas en el estudio *"Desempleo y economía de Penonomé (Coclé): línea de tiempo, impacto del terremoto y proyección"*. Cada cifra viene de un cuadro del INEC, la CSS o la ATP. El enlace exacto está en `14_trazabilidad_fuentes.csv` y en la columna `url` de `99_base_larga_todo.csv`. Ninguna cifra viene de prensa ni la estimé yo.

Todos los archivos están en UTF-8 y se abren bien en Excel. En pandas: `pd.read_csv(ruta, encoding="utf-8-sig")`.

---

## 1. Cómo se relaciona todo

Los datos están en tres niveles geográficos. Cada nivel se une con los demás por una clave distinta.

```
NIVEL CORREGIMIENTO (Penonomé, 16 corregimientos)      clave: id_corregimiento
  00_catalogo_corregimientos ──┬── 01_censo2023_poblacion_corregimientos
                               └── 02_censo2023_viviendas_caracteristicas (filas nivel = corregimiento)

NIVEL PROVINCIA (Coclé) y NACIONAL (República)         clave: area / provincia + periodo
  03_eml_condicion_actividad      (República, Coclé, Coclé urbana, Coclé rural)  ─┐
  04_eml_categoria_ocupacion_cocle                                                │ mismo periodo:
  05_eml_rama_actividad_cocle                                                     │ oct-2024 y sep-2025
  06_eml_informalidad             (República y Coclé)                            ─┘
  07_css_poblacion_protegida_cocle (2016, 2020, 2024, 2025)       ─┐
  10_pib_cocle_actividad_2018_2024                           │ clave: año
  13_atp_oferta_alojamiento_cocle_2025                      ─┘
  08_css_nuevas_inscripciones_provincia_2022 (Coclé y total del país)

SOLO NACIONAL (contexto, no hay dato por provincia)
  09_css_cotizantes_por_sector_nacional (2021-2025, revisada)
  11_atp_visitantes_divisas_mensual (2024-2025, mensual)
  12_atp_ocupacion_hotelera

TODO JUNTO
  99_base_larga_todo  = las tablas 01 a 13 en formato largo (una fila por dato)
  14_trazabilidad_fuentes = fuente, enlace y verificación de cada tabla
```

**Reglas para unir:**
- **Censo, corregimiento con corregimiento:** une `01` y `02` por `id_corregimiento`. En `02`, la fila `nivel = distrito` es el total de Penonomé y la fila `nivel = provincia` es el total de Coclé; no las sumes junto con los corregimientos.
- **Corregimiento con provincia:** el Censo 2023 es la base que conecta los dos niveles. Por ejemplo, la tasa de desocupación censal de cada corregimiento (`desocupados / (ocupados + desocupados)` en `02`) se puede comparar con la tasa provincial de la EML (`03`). Ojo: la tasa del Censo y la de la EML se miden distinto, así que compara el orden de magnitud, no el número exacto.
- **Provincia con tiempo:** la EML (`03` a `06`) tiene dos fechas, `oct2024` y `sep2025`. El PIB (`10`) es anual de 2018 a 2024. La CSS (`07`) tiene 2016, 2020, 2024 y 2025. Para una serie de tiempo, usa `fecha` en `99_base_larga_todo`.

---

## 2. Qué es cada archivo

| Archivo | Qué contiene | Fuente oficial | Unidad |
|---|---|---|---|
| `00_catalogo_corregimientos` | Lista de los 16 corregimientos con su clave y una nota si cambiaron de límites | INEC, Censo 2023 | — |
| `01_censo2023_poblacion_corregimientos` | Superficie y población 2000, 2010 y 2023 por corregimiento | INEC, Censo 2023, Cuadro 4 | personas, km² |
| `02_censo2023_viviendas_caracteristicas` | Viviendas sin agua, sin luz, con piso de tierra, sin internet; población, ocupados, desocupados, analfabetas y discapacidad | INEC, Censo 2023, Cuadro 1 | viviendas / personas |
| `03_eml_condicion_actividad` | Población activa, ocupada, desocupada y tasas de desempleo y participación | INEC, Encuesta de Mercado Laboral, Cuadro 2 | personas / % |
| `04_eml_categoria_ocupacion_cocle` | Ocupados y desocupados por categoría: gobierno, empresa privada, cuenta propia, etc. | INEC, EML, Cuadro 8 | personas |
| `05_eml_rama_actividad_cocle` | Ocupados por rama de actividad (agro, construcción, comercio…) | INEC, EML, Cuadro 13 | personas / % |
| `06_eml_informalidad` | Empleo informal no agrícola | INEC, Cuadro 7 | personas / % |
| `07_css_poblacion_protegida_cocle` | Asegurados activos, pensionados y dependientes en Coclé | INEC / CSS | personas |
| `08_css_nuevas_inscripciones_provincia_2022` | Nuevos asegurados de Coclé y del país en 2022 (preliminar) | CSS, Datos Abiertos | personas |
| `09_css_cotizantes_por_sector_nacional` | Cotizantes activos del sector privado y público, 2021-2025 (serie revisada) | INEC, Seguridad Social 2025, Cuadro 4 | personas |
| `10_pib_cocle_actividad_2018_2024` | PIB de Coclé por actividad (2023 preliminar, 2024 estimado) | INEC, PIB Provincial | millones de B/., volumen encadenado (ref. 2018) |
| `11_atp_visitantes_divisas_mensual` | Visitantes internacionales y divisas por mes | ATP | personas / millones US$ |
| `12_atp_ocupacion_hotelera` | Ocupación hotelera nacional | ATP | % |
| `13_atp_oferta_alojamiento_cocle_2025` | Establecimientos y habitaciones de Coclé por tipo | ATP | unidades |
| `14_trazabilidad_fuentes` | Institución, cuadro, enlace y cómo se verificó cada tabla | — | — |
| `99_base_larga_todo` | Todo lo anterior en formato largo | — | ver columna `unidad` |
| `Penonome_Cocle_datos_oficiales_v2.xlsx` | Las mismas tablas en Excel, con fórmulas de porcentajes y una hoja de validaciones | — | — |

### Columnas de `99_base_larga_todo`

| Columna | Significado |
|---|---|
| `provincia`, `distrito`, `corregimiento` | Dónde aplica el dato. Vacío = nivel superior. |
| `indicador` | Qué mide. Las partes separadas por ` | ` indican desagregación (ej. `eml_Tasa de desempleo (%) | Coclé urbana | mujeres`). |
| `valor`, `unidad` | El número y su unidad. |
| `fecha` | Año (`2023`) o año-mes (`2025-09`). |
| `fuente`, `url` | Institución y cuadro; enlace al documento original. |
| `tipo_fuente` | Siempre `oficial` en este paquete. |
| `quiebre_serie` | `si` cuando el dato no es comparable con otros años (ver advertencias). |
| `nota` | Preliminar, estimado, revisado, cambio de límites. |

---

## 3. Advertencias para la limpieza

1. **Corregimientos nuevos.** Boca de Tucué, Candelario Ovalle, General Victoriano Lorenzo, Las Minas, Riecito y San Miguel se crearon por la Ley 296 del 26 de abril de 2022 (nota 53 del Cuadro 4), a partir de Chiguirí Arriba (Candelario Ovalle), Pajonal (General Victoriano Lorenzo), Río Indio (Riecito), Toabré (Boca de Tucué y San Miguel) y Tulú (Las Minas). Por eso la población de esos cinco en 2000 y 2010 no se puede comparar con la de 2023. Para comparar en el tiempo, agrupa los once como un solo bloque.
2. **Fechas de la EML.** Las tablas `03` a `06` usan octubre 2024, que aparece como revisado (R), y septiembre 2025. El INEC ya publicó la EML de **agosto 2026 (P)** con cuadros por provincia: [Situación de la Población Ocupada, agosto 2026](https://www.inec.gob.pa/archivos/P0705547520260929120433Informe%20de%20la%20Situaci%C3%B3n%20de%20Poblaci%C3%B3n%20Ocupada%20-%20Agosto%202026.pdf) (29-sep-2026). Coclé tiene 5.5 % de desempleo (Cuadro 2) y 59.5 % de informalidad no agrícola (Cuadro 7); el país, 8.5 % y 45.8 %. Esa edición todavía no está transcrita en este paquete. Ojo: la población de 15 años y más de Coclé pasa de 207,110 (sep-2025) a 222,190 (ago-2026), lo que sugiere una nueva base de población, así que compara las tasas, no los niveles.
3. **PIB.** Está en volumen encadenado, así que la suma de las actividades no da exacto el total. La diferencia es de 4.3 millones en 2024 y aparece también en los otros años (la mayor, 11.9 millones en 2021). El INEC la explica en la nota del Cuadro 3 como diferencia estadística del encadenamiento. No fuerces la suma.
4. **Valores "-" del INEC.** En la fuente, "-" significa cero. Aquí ya están como 0.
5. **Datos solo nacionales.** La ocupación hotelera, los visitantes y los cotizantes por sector no existen por provincia en público. Úsalos solo como contexto o como indicador del entorno.
6. **Sin datos posteriores al sismo.** Ninguna tabla oficial de este paquete es posterior al terremoto del 9-oct-2026. Los datos del sismo (daños, réplicas, cronología) son de prensa y de informes de SINAPROC; están en el documento del estudio, con su enlace.

---

## 4. Verificación

Cada tabla se comprobó de dos formas. Primero, una segunda lectura independiente del documento original. Segundo, sumas de control: corregimientos = distrito, ocupados + desocupados = población activa, meses = total anual, hombres + mujeres = total. Los resultados están en la hoja `Validaciones` del Excel. El Censo 2023 (Cuadro 1) además se cotejó visualmente con el PDF original del INEC.

### Correcciones del 24-nov-2026

Una verificación completa contra las fuentes originales confirmó todas las cifras salvo una, y encontró algunos enlaces y notas que había que corregir:

- **`05` y `99`, fila "Extraterritoriales y no declaradas":** decía 115 ocupados en oct-2024. Ese valor era de Colón, la provincia siguiente en el PDF; en Coclé el cuadro trae "-" (cero). Ahora las ramas terciarias suman exacto el sector terciario (69,193 y 72,088). El Excel tiene un control nuevo para esto en `Validaciones`.
- **`99` completo:** se agregó la tabla `09`, que no estaba en la base larga.
- **CSS actualizada a 2025:** la tabla `09` pasa a la serie revisada 2021-2025 del compendio de seguridad social 2025 del INEC (23-nov-2026), que corrige a la baja las cifras de 2021 a 2023 publicadas antes; la `07` suma Coclé 2025 (58,113 cotizantes activos).
- **Solo Coclé y el país:** la tabla `08` traía las diez provincias; ahora tiene Coclé y el total nacional (la suma de las diez, verificada), igual que la base larga y el Excel.
- **`00` y `99`, notas de corregimientos:** decían "dividido en 2023". Ahora citan la Ley 296 de 2022.
- **`07` y `99`, CSS 2020:** el enlace al boletín de la CSS ya no existe. Se reemplazó por la copia del INEC (Cuadro 2, año 2020), que trae las mismas cifras.
- **`12` y `99`, ocupación hotelera de julio y agosto de 2026:** apuntaban a la portada de la ATP, que solo muestra el último mes. Ahora apuntan al PDF de cada mes.
- **`14`, EML_Informalidad:** la cita mezclaba oct-2024 y sep-2025. Ahora separa las dos fechas.

---

## 5. Relación con el documento del estudio

Documento: https://claude.ai/artifact/MPKruLqyPsH3GRhFdCyUU3 (sección 17, "Archivos de datos de este estudio").

| Sección del documento | Archivos de este paquete que la respaldan |
|---|---|
| 3. Población actual de Penonomé | `01`, `02` |
| 4. Los 16 corregimientos | `00`, `01`, `02` |
| 5. Estructura económica | `10`, `05` |
| 6. Línea de tiempo 2018–2026 | `10`, `03`, `07` |
| 7. El desempleo en cifras | `03`, `04`, `06` |
| 8 a 12. Terremoto, entidades, réplicas, cronología | No están en este paquete: son datos de prensa y SINAPROC, con su enlace en el documento |
| 9. Análisis socioeconómico antes y después | `02` (servicios básicos antes del sismo), `03`, `06` |
| 15. Indicadores mensuales | `07`, `08`, `09`, `11`, `12`, `13` |
| 17. Plan de datos | `99_base_larga_todo` sigue el formato largo descrito ahí |
