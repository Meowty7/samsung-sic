"""Genera 01-python/semana-06/quiz-calificado.ipynb (Quiz 6 de la plataforma) y prueba cada respuesta."""

import contextlib
import io
import os
import tempfile
from pathlib import Path

import nbformat
from nbformat.v4 import new_code_cell, new_markdown_cell, new_notebook, new_output

RAIZ = Path(__file__).resolve().parents[2]
DESTINO = RAIZ / "01-python/semana-06/quiz-calificado.ipynb"
C1 = "clase-1-ordenacion-y-series-temporales"
C0 = "../semana-05/clase-2-modulos-y-pandas"
U = {
    34: f"{C0}/u34-modulos-de-python.ipynb",
    35: f"{C0}/u35-series-de-pandas.ipynb",
    36: f"{C0}/u36-dataframes-de-pandas.ipynb",
    37: f"{C1}/u37-ordenacion-de-datos.ipynb",
    38: f"{C1}/u38-series-temporales.ipynb",
}
ESTADO = "**Entregado. Nota final: 100/100.**"
MARCA = "x"

DATOS = "d = {'col1': [1, 2], 'col2': [3, 4], 'col3': [5, 6], 'col4': [7, 8]}"


def unidad(*nums):
    return ", ".join(f"[Unidad {n}]({U[n]})" for n in nums)


# (titulo, consigna, donde_se_ve, codigo, explicacion)
PREGUNTAS = [
    ("Q 34-01 (20 puntos)",
     "Convierta los siguientes datos del diccionario en un dataframe usando Pandas. (Denomina el dataframe `df`)\n\n"
     f"```python\nd = {{ 'col1':[1,2], 'col2':[3,4], 'col3':[5,6], 'col4':[7,8] }}\n```",
     f"{unidad(34)} (uso de módulos de Python, semana 5). En resumen: `import pandas as pd` trae el "
     "módulo y `pd.DataFrame(d)` convierte un diccionario de listas en tabla: cada clave es una columna.",
     "import pandas as pd\n\n" + DATOS + "\n\ndf = pd.DataFrame(d)\nprint(df)",
     "**Respuesta: `df = pd.DataFrame(d)`.** Cada clave del diccionario pasa a ser el nombre de una columna y cada "
     "lista sus valores; el índice se crea solo (0 y 1). La respuesta incluye `import pandas as pd` y la definición "
     "de `d` para que el código corra solo en la plataforma."),

    ("Q 35-01 (20 puntos)",
     "En el DataFrame creado en la pregunta Q 34-01, cree un nuevo dataframe que consista solo en los datos de la "
     "columna con el nombre de columna `col4`. (Denomina el dataframe `new_df`)",
     f"{unidad(35)} (Serie de Pandas, semana 5). En resumen: `df['col4']` devuelve una **Serie** (una "
     "columna) y `df[['col4']]` devuelve un **DataFrame** con esa columna.",
     "import pandas as pd\n\n" + DATOS + "\ndf = pd.DataFrame(d)\n\n"
     "new_df = df[['col4']]        # doble corchete: se mantiene un DataFrame\n"
     "print(new_df)\nprint(type(new_df))",
     "**Respuesta: `new_df = df[['col4']]`.** Los corchetes dobles reciben una lista de columnas y devuelven un "
     "DataFrame, que es lo que pide la pregunta. Con `df['col4']` (corchete simple) se obtendría una Serie, no un "
     "dataframe. Como cada respuesta debe poder ejecutarse sola, se vuelve a crear `df` con el código de la Q 34-01."),

    ("Q 36-01 (20 puntos)",
     "El índice del dataframe creado en la pregunta Q 34-01 es 0 y 1. Escriba un comando para cambiar el nombre de "
     "estos índices a `primero` y `segundo`.",
     f"{unidad(36)} (Pandas DataFrame, semana 5). En resumen: el atributo `df.index` se puede "
     "reasignar con una lista de la misma longitud, y `df.rename(index={...})` cambia etiquetas concretas.",
     "import pandas as pd\n\n" + DATOS + "\ndf = pd.DataFrame(d)\n\n"
     "df.index = ['primero', 'segundo']\nprint(df)\n\n"
     "# Otra forma equivalente (devuelve un dataframe nuevo):\n"
     "df2 = pd.DataFrame(d).rename(index={0: 'primero', 1: 'segundo'})\nprint(df2.equals(df))",
     "**Respuesta: `df.index = ['primero', 'segundo']`.** La lista debe tener tantos elementos como filas. También "
     "sirve `df.rename(index={0: 'primero', 1: 'segundo'})`, que devuelve un dataframe nuevo (hay que asignarlo o "
     "usar `inplace=True`). La última línea comprueba que ambas formas dan el mismo resultado.\n\n"
     "**Nota sobre las preguntas siguientes:** las respuestas de Q 37-01 y Q 38-01 trabajan con el `df` **original** "
     "de la Q 34-01 (índice 0 y 1); como el cambio de índice no altera los datos, el resultado sería el mismo con "
     "las filas llamadas `primero` y `segundo`, solo cambiarían las etiquetas de fila."),

    ("Q 37-01 (20 puntos)",
     "Escriba un comando para buscar datos faltantes en el dataframe `df` creado en la pregunta Q 34-01 e imprima "
     "el resultado. (Sin embargo, los datos que faltan deben devolverse como verdaderos).",
     f"{unidad(37)} (y la {unidad(36)} de la semana 5). En resumen: `isnull()` (o `isna()`) devuelve "
     "un dataframe del mismo tamaño con `True` donde falta el dato.",
     "import pandas as pd\n\n" + DATOS + "\ndf = pd.DataFrame(d)\n\n"
     "print(df.isnull())\n\n"
     "# Para contar los faltantes por columna:\nprint(df.isnull().sum())",
     "**Respuesta: `print(df.isnull())`.** Devuelve `True` donde falta el dato y `False` donde existe (lo que pide "
     "el paréntesis de la consigna; `notnull()` haría lo contrario). En este dataframe no falta nada, así que todo "
     "es `False`. `df.isnull().sum()` cuenta los faltantes por columna; `df.isna()` es un sinónimo."),

    ("Q 38-01 (20 puntos)",
     "Escriba un comando para verificar el resumen de las estadísticas descriptivas (desviación estándar, valor "
     "mínimo, moda, etc.) del dataframe `df` creado en la pregunta Q 34-01 e imprima el resultado.",
     f"{unidad(38)} (y la {unidad(36)} de la semana 5). En resumen: `describe()` resume cada "
     "columna numérica con cantidad, media, desviación estándar, mínimo, cuartiles y máximo.",
     "import pandas as pd\n\n" + DATOS + "\ndf = pd.DataFrame(d)\n\n"
     "print(df.describe())\n\n"
     "# describe() no incluye la moda; se obtiene aparte:\nprint(df.mode())",
     "**Respuesta: `print(df.describe())`.** Muestra `count`, `mean`, `std` (desviación estándar), `min`, `25%`, "
     "`50%`, `75%` y `max`.\n\n"
     "**Nota sobre el enunciado:** menciona la moda, pero `describe()` **no la incluye**. Se agrega `print(df.mode())` "
     "como complemento: aquí todos los valores de cada columna aparecen una sola vez, así que la moda devuelve "
     "ambos valores (dos filas). Si la plataforma solo espera `describe()`, esa línea basta."),
]


def probar(codigo):
    """Ejecuta una respuesta en una carpeta temporal y devuelve lo impreso."""
    previo = os.getcwd()
    salida = io.StringIO()
    with tempfile.TemporaryDirectory() as tmp:
        os.chdir(tmp)
        try:
            with contextlib.redirect_stdout(salida):
                exec(compile(codigo, "<respuesta>", "exec"), {"__name__": "__main__"})
        finally:
            os.chdir(previo)
    return salida.getvalue()


# Comprobaciones de las respuestas
import pandas as pd  # noqa: E402

_d = {'col1': [1, 2], 'col2': [3, 4], 'col3': [5, 6], 'col4': [7, 8]}
_df = pd.DataFrame(_d)
assert list(_df.columns) == ["col1", "col2", "col3", "col4"] and _df.shape == (2, 4)
_new = _df[['col4']]
assert isinstance(_new, pd.DataFrame) and _new["col4"].tolist() == [7, 8]
assert isinstance(_df["col4"], pd.Series)
_df.index = ['primero', 'segundo']
assert list(_df.index) == ['primero', 'segundo']
assert not pd.DataFrame(_d).isnull().values.any()
_desc = pd.DataFrame(_d).describe()
assert {"count", "mean", "std", "min", "max"} <= set(_desc.index) and "mode" not in _desc.index
assert pd.DataFrame(_d).mode().shape == (2, 4)

celdas = [new_markdown_cell(
    "# Quiz 6 — Semana 6 (plataforma)\n\n"
    "**Capítulo 7: datos, estadística y visualización** (unidades 34 a 38)\n\n"
    "[Índice de la semana](semana-06.ipynb)\n\n"
    f"## Estado\n\n{ESTADO}\n\n"
    "## Cómo se califica\n\n"
    "- 5 preguntas de 20 puntos cada una (100). No tiene preguntas adicionales. La nota máxima es 100.\n"
    "- Al entregar, la plataforma califica pregunta por pregunta y muestra cuánto sacaste en cada una.\n"
    "- Se puede corregir cualquier pregunta y volver a entregar hasta que el docente la revise: pulsar «Corregir "
    "mi entrega», cambiar lo necesario y entregar de nuevo; la nota que cuenta es la de la última entrega. Cuando "
    "el docente la revisa ya no se puede modificar, salvo que habilite otro intento.\n\n"
    "**Nota sobre el enunciado:** la plataforma encabeza el quiz con las unidades 34 a 37, pero la última pregunta "
    "es la Q 38-01 (unidad 38).\n\n"
    "## Cómo usar este notebook\n\n"
    "Cada pregunta trae la consigna, el lugar donde se explica, la **respuesta resuelta** (ya ejecutada, con su "
    "salida) y una explicación. La respuesta a escribir está en negrita en la explicación; el código la comprueba. "
    "Cada respuesta recrea `df` para poder ejecutarse sola en la plataforma. Las unidades 34 a 36 son de la semana "
    "5: cada pregunta las enlaza y las explica en breve.\n\n"
    "## Checklist de entrega\n\n" + "\n".join(f"- [{MARCA}] {p[0]}" for p in PREGUNTAS)
    + f"\n- [{MARCA}] Revisar todo y pulsar «Entregar»"
)]

numero = 0
for titulo, consigna, donde, codigo, explicacion in PREGUNTAS:
    salida = probar(codigo)
    print(f"--- {titulo}\n{salida.rstrip()}")
    numero += 1
    celdas += [
        new_markdown_cell(f"## {titulo}\n\n### Consigna\n\n{consigna}\n\n**Dónde se ve:** {donde}"),
        new_markdown_cell("### Respuesta"),
        new_code_cell(codigo, execution_count=numero,
                      outputs=[new_output("stream", name="stdout", text=salida)]),
    ]
    celdas.append(new_markdown_cell("**Explicación:** " + explicacion))

celdas.append(new_markdown_cell("[Índice de la semana](semana-06.ipynb)"))
nb = new_notebook()
nb.cells = celdas
nbformat.write(nb, DESTINO)
print("Escrito:", DESTINO)
