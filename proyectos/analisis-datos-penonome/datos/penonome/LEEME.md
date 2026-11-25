# Paquete de datos oficiales: Penonomé (versión 25-nov-2026)

Este paquete reúne en CSV las tablas oficiales de Penonomé que usa el proyecto: el Censo 2023 del INEC por corregimiento y la pobreza multidimensional por corregimiento del PNUD. El enlace exacto de cada tabla está en `14_trazabilidad_fuentes.csv` y en la columna `url` de `99_base_larga_todo.csv`. Ninguna cifra viene de prensa ni es una estimación propia.

Los datos del sismo (evaluación de daños de SINAPROC, registros por corregimiento, réplicas) están en `../analisis/`.

Todos los archivos están en UTF-8 y se abren bien en Excel. En pandas: `pd.read_csv(ruta, encoding="utf-8-sig")`.

---

## 1. Cómo se relaciona todo

Todas las tablas están al nivel de corregimiento y se unen por `id_corregimiento`:

```
NIVEL CORREGIMIENTO (Penonomé, 16 corregimientos)      clave: id_corregimiento
  00_catalogo_corregimientos ──┬── 01_censo2023_poblacion_corregimientos
                               ├── 02_censo2023_viviendas_caracteristicas (filas nivel = corregimiento)
                               └── 03_pnud_ipm_corregimientos_2023

TODO JUNTO
  99_base_larga_todo  = las tablas 01 a 03 en formato largo (una fila por dato)
  14_trazabilidad_fuentes = fuente, enlace y verificación de cada tabla
```

**Reglas para unir:**
- **Corregimiento con corregimiento:** une `01`, `02` y `03` por `id_corregimiento`.
- **Totales:** en `02`, la fila `nivel = distrito` es el total de Penonomé y la fila `nivel = provincia` es el total de Coclé; no las sumes junto con los corregimientos.

---

## 2. Qué es cada archivo

| Archivo | Qué contiene | Fuente oficial | Unidad |
|---|---|---|---|
| `00_catalogo_corregimientos` | Lista de los 16 corregimientos con su clave y una nota si cambiaron de límites | INEC, Censo 2023 | — |
| `01_censo2023_poblacion_corregimientos` | Superficie y población 2000, 2010 y 2023 por corregimiento | INEC, Censo 2023, Cuadro 4 | personas, km² |
| `02_censo2023_viviendas_caracteristicas` | Viviendas sin agua, sin luz, con piso de tierra, sin internet; población, analfabetismo y discapacidad | INEC, Censo 2023, Cuadro 1 | viviendas / personas |
| `03_pnud_ipm_corregimientos_2023` | Pobreza multidimensional: incidencia (H), intensidad (A) e índice (M0) | PNUD, Gabinete Social y MEF, IPM por corregimiento 2023 | % / índice |
| `14_trazabilidad_fuentes` | Institución, cuadro, enlace y cómo se verificó cada tabla | — | — |
| `99_base_larga_todo` | Todo lo anterior en formato largo | — | ver columna `unidad` |
| `Penonome_Cocle_datos_oficiales_v2.xlsx` | Las mismas tablas en Excel, con fórmulas de porcentajes y una hoja de validaciones | — | — |

### Columnas de `99_base_larga_todo`

| Columna | Significado |
|---|---|
| `provincia`, `distrito`, `corregimiento` | Dónde aplica el dato. Vacío = nivel superior. |
| `indicador` | Qué mide (por ejemplo `censo_sin_internet` o `pnud_ipm_incidencia_h`). |
| `valor`, `unidad` | El número y su unidad. |
| `fecha` | Año del dato. |
| `fuente`, `url` | Institución y cuadro; enlace al documento original. |
| `tipo_fuente` | Siempre `oficial` en este paquete. |
| `quiebre_serie` | `si` cuando el dato no es comparable con otros años (ver advertencias). |
| `nota` | Cambio de límites u otra aclaración. |

---

## 3. Advertencias para la limpieza

1. **Corregimientos nuevos.** Boca de Tucué, Candelario Ovalle, General Victoriano Lorenzo, Las Minas, Riecito y San Miguel se crearon por la Ley 296 del 26 de abril de 2022 (nota 53 del Cuadro 4), a partir de Chiguirí Arriba (Candelario Ovalle), Pajonal (General Victoriano Lorenzo), Río Indio (Riecito), Toabré (Boca de Tucué y San Miguel) y Tulú (Las Minas). Por eso la población de esos cinco en 2000 y 2010 no se puede comparar con la de 2023. Para comparar en el tiempo, agrupa los once como un solo bloque.
2. **Columnas omitidas del Censo.** Del Cuadro 1 no se transcriben las columnas de condición de actividad (ocupados, desocupados y población no económicamente activa): el proyecto no analiza empleo.
3. **Población del IPM.** La población que usa el PNUD para el índice (`poblacion_ipm`) es la de las viviendas particulares, distinta del total censal de la tabla `01`.
4. **Valores "-" del INEC.** En la fuente, "-" significa cero. Aquí ya están como 0.

---

## 4. Verificación

Cada tabla se comprobó de dos formas. Primero, una segunda lectura independiente del documento original. Segundo, sumas de control: corregimientos = distrito y hombres + mujeres = total. Los resultados están en la hoja `Validaciones` del Excel. El Censo 2023 (Cuadro 1) además se cotejó visualmente con el PDF original del INEC.

### Correcciones

- **24-nov-2026, `00` y `99`, notas de corregimientos:** decían "dividido en 2023". Ahora citan la Ley 296 de 2022.
- **25-nov-2026, reenfoque del proyecto:** se retiraron del paquete las tablas de mercado laboral, seguridad social, PIB provincial y turismo, y las columnas laborales del Cuadro 1. Se añadió la tabla `03` del PNUD, que antes vivía en la carpeta de comparación con Colombia (también retirada); sus 16 valores de incidencia coinciden con los usados antes.

---

## 5. Relación con el análisis

El análisis principal (`analisis-penonome.ipynb`) usa `00`, `01`, `02` y `03` para la sección «¿Cómo estaba Penonomé antes del sismo?» y para el índice de prioridad por corregimiento. El estudio completo está en `documento/estudio-penonome.md`.
