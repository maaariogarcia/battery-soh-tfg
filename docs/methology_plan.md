# Methodology plan

## Objective

Build a rigorous machine learning pipeline for predicting the State of Health of lithium-ion batteries under eVTOL mission profiles.

The work will prioritize data understanding, robust preprocessing, feature engineering, leakage prevention, validation strategy and interpretability.

## Stage 1 — Repository and project structure

Create a clean repository with:

- `docs/` for dataset description, literature notes and methodological decisions.
- `notebooks/` for exploratory work.
- `src/` for reusable Python code.
- `configs/` for experiment settings.
- `reports/` for generated figures and results.
- `data/` for local data only, excluded from GitHub.

## Stage 2 — Raw data audit

Goals:

- Load all VAH mission CSV files.
- Validate column names and types.
- Detect missing columns.
- Count rows by cell.
- Check time monotonicity.
- Check current sign convention.
- Check voltage and temperature ranges.
- Identify duplicated or missing cycles.
- Compare raw `cycleNumber` with reconstructed cycles.

Outputs:

- Data inventory table.
- Per-cell summary report.
- List of anomalies.
- First set of diagnostic plots.

## Stage 3 — Cycle reconstruction

Because `cycleNumber` is not fully reliable, cycles should be reconstructed.

Possible signals:

- `Ns` reset.
- time reset or discontinuity.
- transition from rest/discharge to charge.
- current sign and magnitude.
- segment structure.

Validation:

- Compare reconstructed cycle count with raw `cycleNumber`.
- Plot random reconstructed cycles.
- Verify phase order.
- Detect incomplete cycles.

## Stage 4 — Phase segmentation

Classify rows into phases:

- charge,
- charge rest,
- takeoff,
- cruise,
- landing,
- discharge rest,
- unknown/anomalous.

Possible classification rules:

- Use `I_mA` sign and magnitude.
- Use `Ns`.
- Use time inside reconstructed cycle.
- Use expected mission durations.
- Use power/voltage/current behaviour.

Validation:

- Plot voltage/current/temperature by phase for selected cycles.
- Check phase durations.
- Detect impossible transitions.

## Stage 5 — SoH target construction

Construct capacity-based SoH using RPT/capacity tests.

Possible approaches:

1. Detect RPT cycles from discharge capacity peaks.
2. Extract capacity at RPT cycles.
3. Fit a smooth degradation curve per cell.
4. Define SoH as fitted capacity divided by initial capacity.
5. Remove RPT cycles from normal training features.

Compare several target construction options:

- raw RPT interpolation,
- polynomial fit,
- spline fit,
- monotonic smoothing.

Document the final choice.

## Stage 6 — Feature engineering

Create one row per cell-cycle.

Feature groups:

1. General cycle statistics.
2. Charge features.
3. Discharge features.
4. Takeoff features.
5. Cruise features.
6. Landing features.
7. Rest features.
8. Efficiency features.
9. Temperature stress features.
10. Rolling window features.
11. Internal resistance proxy.
12. Data quality flags.

Every feature should have:

- name,
- definition,
- physical interpretation,
- leakage risk,
- missing value handling.

## Stage 7 — Exploratory data analysis

Minimum plots:

- SoH vs cycle by cell.
- Capacity vs cycle by cell.
- Internal resistance proxy vs cycle.
- Temperature evolution by cell.
- Distribution of cycle durations.
- Distribution of charge/discharge capacities.
- Correlation heatmap.
- Feature-target relationships.
- Comparison by experimental condition.
- Outlier diagnostics.

## Stage 8 — Modelling tasks

### Task A — Present SoH estimation

Predict SoH at the same cycle.

### Task B — Future SoH prediction

Predict SoH at t+h using information up to t.

Candidate horizons:

- 10 cycles,
- 50 cycles,
- 100 cycles,
- 200 cycles.

### Task C — RUL prediction

Predict remaining cycles until SoH reaches an EOL threshold.

Only attempt this after SoH modelling is stable.

## Stage 9 — Validation strategy

Use multiple validation schemes:

1. Random split only as a weak initial sanity check.
2. Group split by cell to evaluate generalization to unseen batteries.
3. Chronological split to evaluate forecasting.
4. Leave-one-cell-out validation if computationally feasible.

Avoid reporting only random split results because they may overestimate performance.

## Stage 10 — Baseline models

Start with simple baselines:

- Mean predictor.
- Last observed SoH.
- Linear Regression / Ridge.
- kNN.
- Random Forest.
- Gradient Boosting.
- XGBoost / LightGBM / CatBoost if installed.

Only after these are stable consider:

- MLP.
- LSTM/GRU.
- Temporal models.

## Stage 11 — Evaluation metrics

Use:

- MAE.
- RMSE.
- R2.
- MAPE if numerically stable.
- Error by cell.
- Error by cycle range.
- Error by experimental condition.
- Prediction plots.
- Residual plots.

## Stage 12 — Interpretability

Use:

- permutation importance,
- SHAP if feasible,
- feature correlation analysis,
- ablation by feature groups,
- phase-based vs unified features comparison.

## Stage 13 — Final deliverables

Final outputs:

- clean reusable pipeline,
- processed cycle-level dataset,
- documented target construction,
- feature dictionary,
- EDA report,
- model comparison table,
- validation results,
- final selected model,
- limitations and future work.