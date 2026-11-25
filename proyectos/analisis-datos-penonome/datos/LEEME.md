# Datos del proyecto

| Carpeta | Qué contiene | Fuentes |
|---|---|---|
| `penonome/` | Tablas oficiales de Penonomé: Censo 2023 por corregimiento (población, viviendas y carencias) y pobreza multidimensional por corregimiento, más la base larga y el libro Excel | INEC y PNUD (verificadas cifra por cifra) |
| `analisis/` | Tablas del sismo para el análisis principal: evaluación de daños de SINAPROC en Coclé y por provincia, comunicados de SINAPROC, registros de daños por corregimiento, réplicas, proyecciones de población y situación actual | SINAPROC, INEC, MIDES, Miviot, Meduca y prensa con datos oficiales |

Cada carpeta tiene su `LEEME.md` con el detalle de cada archivo. Todas las URL están registradas en `../investigacion/fuentes.csv`. Los archivos están en UTF-8; en pandas: `pd.read_csv(ruta, encoding="utf-8-sig")`.
