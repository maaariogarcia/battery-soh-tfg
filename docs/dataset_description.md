# Dataset description — eVTOL Battery Dataset

## Project context

This project studies predictive modelling of lithium-ion battery health in unmanned autonomous systems using the eVTOL Battery Dataset.

At this stage, the goal is to document the dataset and methodological implications clearly. No modelling results are reported here.

## Dataset origin

The dataset contains experimental cycling data from lithium-ion cells tested under mission profiles inspired by eVTOL operation.

Reported characteristics (to verify against the official dataset README during ingestion):

- 22 Sony-Murata 18650 VTC-6 cells,
- nominal capacity around 3000 mAh,
- nominal voltage around 3.6 V,
- mission-style cycling with varying operational conditions.

## Mission profile summary

A canonical mission cycle includes:

1. Takeoff (high power discharge),
2. Cruise (lower power, longer discharge),
3. Landing (high power discharge),
4. Rest,
5. CC-CV charge,
6. Rest.

Typical baseline values often cited in public descriptions are approximately:

- takeoff: 75 s at 54 W,
- cruise: 800 s at 16 W,
- landing: 105 s at 54 W.

These values should be treated as nominal references and checked against raw files per cell.

## Raw variables (mission files)

| Variable | Meaning |
|---|---|
| `time_s` | Time since beginning of experiment (s) |
| `Ecell_V` | Cell terminal voltage (V) |
| `I_mA` | Cell current (mA) |
| `EnergyCharge_W_h` | Charged energy (Wh) |
| `QCharge_mA_h` | Charged capacity (mAh) |
| `EnergyDischarge_W_h` | Discharged energy (Wh) |
| `QDischarge_mA_h` | Discharged capacity (mAh) |
| `Temperature__C` | Cell surface temperature (°C) |
| `cycleNumber` | Raw cycle index from tester |
| `Ns` | Segment identifier |

## Important data integrity note

`cycleNumber` should be treated as a diagnostic field, not as a guaranteed cycle index.

Cycle reconstruction and validation should use multiple signals (`Ns`, timing continuity, segment order, charge/discharge transitions).

## Experimental-condition mapping

Cell-condition metadata must be confirmed against the official dataset documentation before final analysis.

Until that verification step is completed, any per-cell condition table should be considered provisional.

## Known dataset risks to address during preprocessing

Potential issues reported in documentation and prior work include:

- missing or duplicated reference tests,
- tester anomalies in specific files/cycles,
- discontinuities within cycles,
- signal spikes,
- cycles split across files,
- long non-standard rest periods,
- inconsistencies in raw cycle indexing.

## Main target concept: State of Health (SoH)

Capacity-based SoH definition:

\[
\mathrm{SoH}(t)=\frac{C(t)}{C_0}
\]

where:

- `C(t)` is available capacity at cycle/time `t`,
- `C0` is reference initial capacity.

Reference tests (RPT/capacity checks) are expected to be key for estimating degradation trajectories.

## Candidate prediction tasks (future phases)

- **Task A**: present-cycle SoH estimation,
- **Task B**: future SoH forecasting at horizon `h`,
- **Task C**: RUL-style prediction to an EOL threshold.

Task activation depends on successful cycle reconstruction and target-quality validation.

## Methodological guardrails

1. Validate cycle indexing before feature/target construction.
2. Prevent leakage from future cycles and reference-test information.
3. Use split strategies aligned with the research question (grouped and chronological).
4. Document every exclusion/cleaning rule with traceability.
