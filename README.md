# Battery SoH TFG

Proyecto de Trabajo de Fin de Grado orientado al modelado predictivo del estado de salud (SoH) de baterías en sistemas autónomos no tripulados.

## Objetivo

Construir un flujo de trabajo reproducible de ciencia de datos para:

- comprender el eVTOL Battery Dataset;
- auditar y documentar la calidad de los datos;
- preparar una base metodológica sólida para el pipeline;
- definir tareas de predicción de SoH sin iniciar todavía el entrenamiento.

## Estado actual del repositorio

Este repositorio está en **fase de preparación metodológica**.

- ✅ Documentación inicial revisada y consolidada en `docs/`.
- ✅ Estructura de carpetas preparada para trabajo reproducible.
- ⏳ Próximo hito: auditoría de datos crudos y reconstrucción de ciclos.
- 🚫 Aún no se han implementado limpieza, ingeniería de variables ni modelado.

## Estructura

```text
docs/
  dataset_description.md
  literature_notes.md
  methodology_plan.md
  codex_workflow.md

data/
  raw/          # datos originales (no versionados)
  interim/      # artefactos intermedios (no versionados)
  processed/    # datos procesados (no versionados)

notebooks/      # cuadernos exploratorios (futuro)

src/            # código fuente modular (futuro)
  data/
  features/
  models/
  utils/

reports/
  figures/      # gráficas generadas
  results/      # tablas y métricas

configs/        # configuración del proyecto
```

## Próximos pasos (sin modelado todavía)

1. Ejecutar auditoría sistemática de CSV crudos por celda.
2. Validar convención de señales (`I_mA`, `Ecell_V`, temperatura, tiempos).
3. Definir reglas reproducibles para reconstrucción de ciclos.
4. Documentar criterios de exclusión y control de anomalías.

## Reglas de trabajo

- No subir datos reales al repositorio.
- Mantener `data/` y `reports/` con estructura vía `.gitkeep`.
- Registrar en `docs/` cualquier decisión metodológica antes de codificar.
