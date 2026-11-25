# Cotejo de la cronología completa (24-nov-2026)

**Alcance:** las 41 filas de la sección 12 del estudio que la revisión anterior había dejado sin cotejar (las otras 27 se cotejaron en `2026-11-24-documento.md`). Con esto quedan verificadas las 67 filas.
**Método:** dos verificadores en paralelo con el MCP `web-research`; cada fila se comparó con su fuente enlazada y, cuando hizo falta, con una fuente primaria (Órgano Judicial, ASEP, MICI, OPS) o un medio independiente.

## Resultado

| Tanda | Filas | Confirmadas | Con discrepancia | Sin verificar |
|---|---|---|---|---|
| 9-oct a 16-oct | 21 | 14 | 7 | 0 |
| 19-oct a 21-nov | 20 | 13 | 7 | 0 |

## Correcciones aplicadas

- **Atribución:** el alcalde que reubicó las oficinas municipales fue el de Antón, Eric Domínguez, no el de Penonomé. La fila se queda porque Antón es de Coclé, y ahora enlaza a la página de Antón.
- **Fechas:**
  - la evaluación preliminar de la Gobernación pasa del 14-oct (aprox.) al 13-oct;
  - la construcción de casas en Chigoré pasa del 20-oct (aprox.) al 19-oct;
  - el Tribunal Electoral en el CIDETE pasa del 27-oct (aprox.) al 26-oct;
  - la demolición del CEBG San Isidro pasa del 20-nov al 19-nov;
  - la medida de la ASEP pasa del 21-nov al 20-nov.

  Las filas se reordenaron por fecha.
- **Alcance provincial:**
  - el formulario del MICI abarca Coclé, Veraguas, Los Santos y Herrera;
  - la prohibición de cortes de la ASEP vale para las mismas cuatro provincias, es solo por falta de pago y la resolución fue recurrida;
  - la falta de agua se reporta en Los Santos, Herrera, Veraguas y Coclé, y el IDAAN dice que las potabilizadoras de Coclé operan con normalidad.
- **Redacción ajustada a la fuente:**
  - MiCultura "identifica", no "declara", las estructuras inseguras;
  - el MINSA "mantiene", no "abre", la atención psicológica;
  - el mercado público retoma sus operaciones desde el 6-nov;
  - los 89 arrendatarios del mercado venden reubicados, no "sigue cerrado".
- **Fuentes mejoradas:**
  - TVN reemplaza al agregador mapadelterremoto en la fila de los albergues de Bajito de San Miguel;
  - Eco TV reemplaza a Destino Panamá en la declaración de Mulino;
  - se suma la nota oficial de la ASEP;
  - se suma La Prensa para la torre izquierda de la Catedral.

## Notas

- La página del Mitradel (oficina especial de La Mina) devolvió 403; la fila se apoya en Telemetro.
- El enlace de El Universo (EFE, 10-oct) redirige a veces a otro artículo; el texto original seguía disponible al cotejarlo.

## Registro de fuentes

En la misma jornada se registraron en `fuentes.csv` los enlaces de los datos que faltaban del paquete de Penonomé, ya cotejados en `2026-11-24-paquetes-de-datos.md`. `investigacion.py validar` ahora revisa también los enlaces de cada CSV de datos.
