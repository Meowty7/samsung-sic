# Reenfoque en las afectaciones sociales del sismo (25-nov-2026)

**Alcance:** todo el proyecto. Se retiraron el mercado laboral, la seguridad social, el PIB provincial, el turismo, la mina y la comparación con Colombia, y el análisis se centró en las afectaciones sociales del sismo del 9-oct-2026: Coclé como provincia para el daño y Penonomé por corregimiento para la vulnerabilidad.

## Datos nuevos incorporados

| Tema | Dato | Fuente | Veredicto |
|---|---|---|---|
| Evaluación de daños (EDAN) de Coclé | 2,531 viviendas evaluadas y 10,199 personas; daño total 414, moderado 147, parcial 1,750, leve 145, menor 75 | SINAPROC, plataforma de afectaciones (ficha de Coclé), cifras finales al 15-nov-2026 | Confirmado en la plataforma; los cinco niveles suman 2,531 |
| Personas con atención especial | 431 personas con discapacidad y 21 embarazadas, con su desglose por nivel de daño | Misma plataforma | Confirmado; los desgloses suman 431 y 21 |
| Edad y sexo | Personas en las viviendas evaluadas por grupo de edad y sexo | Misma plataforma | Confirmado; suman 10,199 |
| Otras afectaciones (COE) | 17 lesionados, 2 hospitales, 40 escuelas, 14 iglesias, 17 edificios, 7 hoteles, 6 puentes, 0 albergues y 9,693 bolsas del IMA en 448 comunidades | Misma plataforma, corte del 25-nov-2026 | Confirmado al consultar la plataforma |
| Provincias | Viviendas evaluadas y personas en las 11 provincias y comarcas con evaluaciones | Misma plataforma, cifras finales al 15-nov-2026 | Confirmado |
| Pobreza multidimensional | Incidencia, intensidad e índice de los 16 corregimientos | PNUD, Gabinete Social y MEF, IPM por corregimiento 2023 | Sin cambios: los 16 valores de incidencia coinciden con los usados antes |

## Retirado del proyecto

- **Datos:** tablas de la EML, de la CSS, del PIB provincial, de la ATP y de ocupación hotelera; desempleo de Coclé 2019-2026; la carpeta `comparacion-colombia/`; las columnas laborales del Cuadro 1 del Censo; seis filas de `situacion_actual_2026.csv` (visitantes, FIDEMICRO, arroz, contratos suspendidos, Cobre Panamá y canasta básica).
- **Gráficas:** `pulso-03-desempleo`, `pulso-04-economia`, `pulso-07-colombia`, `pulso-08-escenarios`, `pulso-10-empleo-2026` y `pulso-11-sin-intervencion`. Se añadieron `pulso-03-nivel-dano` y `pulso-04-vulnerables`.
- **Fuentes:** `fuentes.csv` pasó de 208 a 113 filas: quedan las que cita algún archivo del proyecto, más dos nuevas de SINAPROC (la ficha de Coclé y la entrada en Panamá Conecta).
- **Afirmaciones:** se retiraron las de empleo, seguridad social y turismo, y se añadieron seis de la EDAN con su fuente.

## Advertencias

- «Afectadas» (comunicados #5, #7 y #12) y «evaluadas» (EDAN) no son la misma unidad; el análisis no las suma ni las resta.
- El nivel «Total» de la EDAN es daño total, no el total general: lo confirma la suma de los cinco niveles.
- SINAPROC publica la EDAN por provincia. El índice de prioridad por corregimiento sigue usando los registros de prensa solo como sí o no.

## Resultado

Los siete cuadernos se ejecutaron completos el 25-nov-2026 y todas las llamadas a `verificar` imprimen «Correcto».
