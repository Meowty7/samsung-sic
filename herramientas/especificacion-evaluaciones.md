# Especificación de evaluaciones de la plataforma

Cada semana la plataforma del curso publica una **actividad asincrónica** y un **quiz** calificados. Se resuelven
en `<modulo>/semana-NN/actividad-asincronica.ipynb` y `<modulo>/semana-NN/quiz-calificado.ipynb`, generados por
`herramientas/evaluaciones/actividad_sNN.py` y `herramientas/evaluaciones/quiz_sNN.py`.

## Estructura del notebook
1. Encabezado: título ("Actividad asincrónica — Semana N" / "Quiz N — Semana N (plataforma)"), capítulo y unidades,
   link al índice de la semana.
2. `## Estado`: `**Pendiente de entrega.**` o `**Entregado. Nota final: X/Y.**` ("Entregada" para la actividad).
   El índice de la semana lee la nota con la expresión `Nota final: X/Y`.
3. `## Cómo se califica`: los puntos y reglas tal como los da la plataforma.
4. `## Cómo usar este notebook` y `## Checklist de entrega` (una casilla por pregunta + "Revisar todo y pulsar
   «Entregar»"; todas `[x]` cuando se entrega).
5. Por cada pregunta: `## Título`, `### Consigna` (texto de la plataforma), `### Guía` o **Dónde se ve:** con link a
   la unidad, `### Respuesta` (celda de código **ya ejecutada, con su salida**) y **Explicación:**.
6. Pie con el link al índice.

## Reglas
- Las respuestas se ejecutan y se comprueban en el generador (`exec` con entradas simuladas en una carpeta temporal)
  antes de escribir el notebook; la salida guardada es la real.
- Usar las clases y funciones **exactas del curso** (copiarlas del notebook de la unidad), no versiones propias.
- Datos del enunciado (textos, títulos, listas, números de entrada): se copian **literalmente**, con sus erratas,
  aunque el PDF los escriba distinto o el enunciado anuncie otro resultado. El docente descuenta si se cambian
  (semana 3: Q 26-01 3/10 y Q 26-02 8/10 por usar los títulos del PDF).
- Si el enunciado anuncia un resultado que sus propios datos no producen, se muestran **las dos cosas**: el
  cálculo con los datos literales y el resultado con el valor anunciado (semana 3, Q 26-01: con solo el texto
  literal y `1795 3` dio 5/10, porque se esperaba también `1763 3`).
- Errores de código que impiden ejecutar (`def` sin `:`, métodos inexistentes como `.key()`, operadores faltantes):
  se corrige lo mínimo para que corra. Cada cambio y cada discrepancia con el PDF se explican con
  **Nota sobre el enunciado:**.
- Preguntas "¿cuál es el resultado?": la respuesta a escribir va en negrita en la explicación; el código la comprueba.
- Toda respuesta de código incluye la salida concreta escrita en la explicación, no solo en la celda ejecutada.
- Lo que la consigna pide (analizar, comparar, justificar) va **dentro del bloque `Respuesta`**, que es lo que se
  entrega: en comentarios, con la complejidad de cada función nombrada. Un complemento "no es necesario entregarlo"
  solo agrega comprobaciones (semana 5, Q 32-01 y Q 32-02: la comparación con fib1-fib3 y bin1-bin2 estaba solo
  en la explicación y en el complemento, y el docente marcó que faltaba).
- Preguntas "con sus propias palabras": respuesta modelo visible y aviso de redactarla a su manera.
- "Presentación N" en una consigna es el número de página contando los PDFs del capítulo uno tras otro
  (por ejemplo, 192 = parte 2, pág. 15 si la parte 1 tiene 177 páginas).

## Particularidades de la plataforma
- Mientras el docente no la revise, una evaluación se puede corregir y volver a entregar sin límite; la nota
  nueva reemplaza a la anterior (semana 3). Conviene revisar la devolución y reentregar.
- Ejecuta Python en el navegador: `input()` abre una ventana emergente y lo impreso con `print()` se ve recién al
  terminar. Los programas con menú muestran el menú y el último resultado dentro del texto de `input()`, y terminan
  si el usuario cancela o deja vacío (ver `actividad_s01_act5.py`).
- Si una respuesta necesita un dato por `input()`, prever un valor por defecto cuando se cancela.
- Datos aleatorios: semilla fija en el generador para que la salida de ejemplo sea reproducible, y aviso de que en la
  plataforma cambia.
