# Datos del proyecto

| Carpeta | Qué contiene | Fuentes |
|---|---|---|
| `penonome/` | Tablas oficiales de Penonomé y Coclé: Censo 2023, Encuesta de Mercado Laboral, CSS, PIB provincial y turismo, más la base larga y el libro Excel | INEC, CSS, ATP (verificadas cifra por cifra) |
| `comparacion-colombia/` | Desempleo de las ciudades colombianas, pobreza por corregimiento y escenarios de desempleo de Coclé | DANE, INEC, MEF, PNUD |
| `analisis/` | Tablas armadas para el análisis principal: desempleo 2019-2026, daños de SINAPROC, registros por corregimiento, réplicas y ocupación hotelera | INEC, SINAPROC, ATP y prensa con datos oficiales |

Cada carpeta tiene su `LEEME.md` con el detalle de cada archivo. Todas las URL están registradas en `../investigacion/fuentes.csv`. Los archivos están en UTF-8; en pandas: `pd.read_csv(ruta, encoding="utf-8-sig")`.
