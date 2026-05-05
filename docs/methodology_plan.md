# Methodology plan

## Scope and objective

This TFG aims to design a **reproducible and methodologically robust** workflow for predicting lithium-ion battery State of Health (SoH) under eVTOL-like mission profiles.

At this stage, the focus is on planning and data understanding. No training, benchmarking or final model selection is performed yet.

## Stage 1 — Repository and documentation readiness

Prepare and maintain a clean project structure with:

- `docs/` for dataset context, literature synthesis and methodological decisions.
- `configs/` for experiment/configuration files.
- `data/` and `reports/` with `.gitkeep` placeholders and ignored heavy artifacts.
- Future `notebooks/` and `src/` work kept aligned with documented decisions.

## Stage 2 — Raw data audit (planned)

Goals:

- Load all mission CSV files by cell.
- Validate schema consistency (column names and dtypes).
- Identify missing/duplicated columns or rows.
- Check time continuity and resets.
- Inspect sign convention and ranges for current/voltage/temperature.
- Quantify anomalies per file and per cell.

Planned outputs:

- Data inventory table.
- Per-cell quality summary.
- Traceable anomaly log.
- Initial diagnostic plots.

## Stage 3 — Cycle reconstruction (planned)

Because raw `cycleNumber` may be inconsistent, cycles will be reconstructed using available signals such as:

- `Ns` transitions,
- time discontinuities/resets,
- charge/discharge pattern logic,
- expected mission sequence.

Validation criteria:

- coherence of reconstructed cycle order,
- phase ordering consistency,
- detection of incomplete or split cycles,
- comparison against raw cycle indexing for diagnostics only.

## Stage 4 — Phase segmentation (planned)

Rows will be classified into mission phases:

- charge,
- charge rest,
- takeoff,
- cruise,
- landing,
- discharge rest,
- unknown/anomalous.

Segmentation will be rule-based and auditable, using current/power behavior, timing and segment metadata.

## Stage 5 — SoH target definition (planned)

SoH will follow a capacity-based definition:

\[
\mathrm{SoH}(t)=\frac{C(t)}{C_0}
\]

where `C(t)` is estimated from reference capacity tests and `C0` is the cell baseline capacity.

Planned decisions to document explicitly:

- how reference tests are detected,
- how intermediate-cycle SoH is assigned (interpolation/smoothing strategy),
- how potential leakage from reference cycles is prevented.

## Stage 6 — Feature design plan (planned, not implemented)

Feature families to be considered later:

1. Cycle-level statistical descriptors.
2. Phase-specific descriptors.
3. Efficiency and throughput indicators.
4. Temperature/stress indicators.
5. Trend/rolling indicators with strict anti-leakage constraints.
6. Data-quality flags.

No feature extraction is implemented in this preparation phase.

## Stage 7 — EDA plan (planned)

Planned EDA artifacts include:

- degradation trajectories by cell,
- phase-duration distributions,
- signal stability checks,
- feature-target relationship diagnostics (once targets exist).

## Stage 8 — Modelling tasks definition (future)

Potential tasks remain:

- Present-cycle SoH estimation,
- Future SoH forecasting at horizon `h`,
- RUL-style prediction.

These tasks are defined conceptually only and will be activated after data and target quality are validated.

## Stage 9 — Validation strategy design (future)

Evaluation will prioritize robust splits:

- grouped-by-cell validation for cross-cell generalization,
- chronological splits for forecasting realism,
- random split only as a weak sanity reference.

## Stage 10 — Baselines and interpretability (future)

Baseline families and interpretability analyses are reserved for later implementation after data curation and target construction are complete.

## Deliverables of the current phase

- Coherent methodological plan.
- Harmonized project documentation.
- Repository structure ready for reproducible work.
- Clear boundary: no model training and no data upload to Git.
