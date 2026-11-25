# Proyectos

Cada proyecto vive en su propia carpeta con su propio ambiente `uv`, aislado del cuaderno de estudio.

| Proyecto | Semanas | Carpeta |
|---|---|---|
| Análisis de datos de Penonomé (investigación con datos oficiales) | 1–6 | [analisis-datos-penonome](analisis-datos-penonome/README.md) |
| Proyecto Python | 7–8 | (pendiente) |
| Proyecto IA | 16–18 | (pendiente) |
| Mini Hands Project | 22 | (pendiente) |
| Hackathon | 23–24 | (pendiente) |

## Estructura de cada proyecto

```
proyectos/<nombre>/
├── pyproject.toml     dependencias propias
├── README.md          qué hace, cómo levantarlo, estructura
├── proyecto.ipynb     bitácora: exploración, pruebas y decisiones justificadas
├── docs/              entregable formal (informe, presentación, diagramas)
├── src/               código
└── datos/
```

## Cómo levantar un proyecto

```bash
cd proyectos/<nombre>
uv sync
uv run python -m src.main
```

[Inicio del curso](../00-inicio.ipynb)
