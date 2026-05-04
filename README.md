# Battery SoH TFG

Proyecto de Trabajo de Fin de Grado orientado al modelado predictivo del estado de salud (SoH) de baterías en sistemas autónomos no tripulados.

## Objetivo

Construir un pipeline reproducible de ciencia de datos para:

- analizar el eVTOL Battery Dataset;
- reconstruir ciclos de batería;
- limpiar y validar los datos;
- generar variables explicativas;
- entrenar y comparar modelos predictivos de SoH.

## Estructura

```text
data/
  raw/          # datos originales, no se suben a GitHub
  interim/      # datos intermedios
  processed/    # datos finales limpios

notebooks/      # análisis exploratorios

src/            # código fuente modular
  data/
  features/
  models/
  utils/

reports/
  figures/      # gráficos generados
  results/      # tablas y métricas

configs/        # configuración del proyecto