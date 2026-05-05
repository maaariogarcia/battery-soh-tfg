# Literature notes — Battery SoH prediction for eVTOL applications

## Purpose of this document

Summarize the most relevant references for framing the TFG methodology.

This note captures methodological takeaways only. It does **not** report original experimental results from this repository.

## 1) eVTOL dataset publication (Bills et al.)

Why it matters:

- provides public aging data under mission-like profiles,
- better aligned with eVTOL use cases than purely constant-current datasets,
- includes operational variability useful for data-driven degradation studies.

Main implication for this TFG:

- modelling choices must respect mission-phase dynamics (takeoff/cruise/landing) instead of assuming homogeneous discharge behavior.

## 2) SoH forecasting work on this dataset (Granado et al.)

Most relevant methodological ideas to reuse carefully:

- reconstruct cycles rather than trusting raw cycle index directly,
- derive SoH from reference capacity tests,
- avoid leakage by separating reference-test logic from mission-sample training,
- evaluate multi-horizon forecasting.

How to use it in this TFG:

- as a baseline methodological reference,
- not as a replication target,
- with stronger emphasis on traceability, validation rigor and leakage diagnostics.

## 3) Phase-segmented feature approaches (e.g., Yang et al.)

Key takeaway:

- features extracted per operating phase can capture degradation signals that unified cycle-level summaries may dilute.

Practical stance for this TFG:

- prioritize robust, interpretable phase-aware features before complex optimization procedures.

## 4) SoH estimation review literature (e.g., Fu et al.)

High-level guidance:

- SoH is latent and must be inferred from observable proxies,
- health indicators must balance informativeness, robustness and deployability,
- validation and generalization are central when moving from lab data to practice.

Use in this TFG:

- support the theoretical rationale for feature engineering,
- motivate strict validation design and transparent limitations.

## 5) LLM-assisted ML workflow literature (e.g., Tuncel et al.)

Relevant for process design:

- LLMs can accelerate coding and iteration,
- expert review remains mandatory,
- reproducibility and methodological control should not be delegated.

Operational implication:

- Codex is used as an assistant for drafting/refining artifacts,
- final scientific responsibility remains human.

## Cross-cutting methodological warnings

1. Distinguish clearly between *documented literature findings* and *results produced in this TFG*.
2. Avoid benchmarking claims until data curation and split strategy are finalized.
3. Treat leakage prevention as a first-class design constraint.
4. Prefer explainable baselines before deep/complex models.
5. Keep all assumptions explicit in `docs/` before implementation.
