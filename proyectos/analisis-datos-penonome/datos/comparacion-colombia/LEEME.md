# Comparación: Coclé (Panamá) vs. Colombia, sismo del 10 de agosto de 2026

Datos para comparar el sismo de Colombia (10 de agosto de 2026) con el de Coclé (9 de octubre de 2026). Los usa `analisis-penonome.ipynb` (sección 7) y el anexo de las semanas 5 y 6.

| Archivo | Qué es | Tipo |
|---|---|---|
| `20_colombia_geih_td_ciudades.csv` | Desempleo de las 23 ciudades, 4 trimestres móviles (abr-jun a jul-sep), 2025 y 2026; grupo de cada ciudad (afectada, control, intermedia, total) | Oficial (DANE, GEIH), con doble lectura del PDF |
| `23_socioeconomico_colombia_vs_cocle.csv` | Pobreza, desempleo e informalidad de los departamentos afectados y de Coclé, y la pobreza multidimensional de los 16 corregimientos de Penonomé | Oficial (DANE, INEC, MEF, PNUD); desempleo departamental de ANIF |
| `30_proyeccion_cocle_escenarios.csv` | Desempleo proyectado de Coclé 2026–2030 en 3 escenarios, desde el 5.5 % de agosto de 2026. El modelo está en `src/penonome/analisis.py` (`proyectar_desempleo`) | **Modelo, no dato oficial** |
| `31_colombia_diferencias_en_diferencias.csv` | Cambio promedio en ciudades afectadas frente a las de control | Cálculo sobre datos DANE |

**Grupos de ciudades**
- **Afectadas:** Quibdó (Chocó), Cali (Valle), Pereira (Risaralda), Armenia (Quindío) y Manizales (Caldas).
- **Control:** ciudades del Caribe y del oriente, lejos del epicentro.
- **Intermedias:** Bogotá, Medellín, Ibagué, Popayán, Pasto, Neiva y Tunja. Se excluyen del cálculo.

**Cómo se resolvieron las advertencias**
- **Pobreza multidimensional y pobreza monetaria:** cada país las mide con su propio método, así que no se comparan los números sino el **índice relativo** (archivo 24): zona ÷ total de su país. Panamá usa el IPM por encuesta del MEF 2025 (país 12.4%, Coclé 9.9%), del mismo tipo que el del DANE. El IPM por corregimiento (censal) solo se usa para la brecha interna de Penonomé, comparándolo consigo mismo.
- **Informalidad:** Coclé es informalidad no agrícola; por eso se divide entre la república no agrícola de la misma fecha (45.8%, agosto 2026), y cada capital colombiana entre el promedio de las 23 ciudades (41.5%). Manizales y el total nacional están en el texto del boletín del DANE; las demás ciudades se leyeron dos veces de su gráfico 5 con el mismo resultado.
- **Daños de Chocó y Caldas:** son cortes tempranos (Blu Radio, 15 de agosto) y probablemente están incompletos.
- **Desempleo departamental de Colombia** (Chocó 11.5%, Valle 9.7%, Risaralda 7.3%, Caldas 7.7%, nacional 8.9%): viene de ANIF citado por Valora Analitik, una fuente secundaria que no indica el periodo. Por eso, en el índice relativo, los periodos de Colombia y Coclé no coinciden. Úsalo solo como referencia.
- **`cambio_pp` del archivo 20:** se calcula restando las tasas redondeadas. En cuatro filas difiere 0.1 de la diferencia que imprime el DANE (Quibdó, Cali y Armenia en may-jul; Riohacha en jun-ago). No cambia las diferencias en diferencias.
- **Cifras del sismo con fechas distintas:** cada fila tiene su `fecha_dato` porque los balances cambian. Por ejemplo, los fallecidos son 304 al 18 de agosto (OPS), 319 al 20 y 331 al 31 (UNGRD).

**Verificación del 24-nov-2026:** se cotejaron todas las cifras con sus fuentes y coinciden. Se corrigió lo siguiente:
- La línea base de Coclé en el archivo 22 decía 7.1% (septiembre 2025); ahora dice 5.5% (agosto 2026).
- La informalidad de Coclé citaba el Cuadro 11; está en el Cuadro 7.
- Las fuentes de la pobreza monetaria nacional, de la fecha del sismo de Panamá y del desempleo de 13 ciudades de junio, julio y septiembre ahora apuntan a la fuente primaria.
- La referencia de informalidad de este LEEME decía 47.1%; ahora dice 45.8%.

**Línea base:** el modelo y el índice relativo usan agosto de 2026 (INEC: Coclé 5.5% de desempleo y 59.5% de informalidad no agrícola; país 8.5% y 45.8%), el último dato antes del sismo del 9 de octubre. Así coinciden con las secciones 9, 14 y 18 del documento.
