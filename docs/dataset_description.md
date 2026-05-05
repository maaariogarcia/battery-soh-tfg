# Dataset description — eVTOL Battery Dataset

## Project context

This project focuses on predictive modelling of lithium-ion battery health in unmanned autonomous systems, using the eVTOL Battery Dataset published by Carnegie Mellon University.

The main objective is to build a rigorous data science pipeline for understanding, cleaning, transforming and modelling battery degradation data. The project will focus primarily on State of Health (SoH) prediction, although alternative target definitions may also be explored, such as present-cycle SoH, future-cycle SoH, or Remaining Useful Life (RUL).

## Dataset origin

The dataset contains experimental cycling data from lithium-ion cells tested under power profiles designed to emulate electric vertical takeoff and landing aircraft missions.

The dataset includes 22 Sony-Murata 18650 VTC-6 cylindrical cells. These cells have a nominal capacity of approximately 3000 mAh and a nominal voltage of 3.6 V.

The complete dataset contains more than twenty thousand charge/discharge cycles across different cells and operating conditions.

## Mission profile

Each cycle is designed to represent a simplified eVTOL mission profile. The canonical mission consists of:

1. Takeoff: high power discharge.
2. Cruise: lower power discharge for a longer duration.
3. Landing: high power discharge.
4. Rest after discharge.
5. CC-CV charging.
6. Rest after charging.

The baseline discharge profile is approximately:

- Takeoff: 75 s at 54 W.
- Cruise: 800 s at 16 W.
- Landing: 105 s at 54 W.

Different cells modify one experimental condition at a time, such as cruise duration, discharge power, charge current, charge voltage or thermal chamber temperature.

## Raw variables

Each mission CSV contains the following variables:

| Variable | Meaning |
|---|---|
| `time_s` | Time since beginning of experiment in seconds |
| `Ecell_V` | Cell terminal voltage |
| `I_mA` | Cell current in milliamperes |
| `EnergyCharge_W_h` | Energy supplied during charge |
| `QCharge_mA_h` | Charge supplied during charge |
| `EnergyDischarge_W_h` | Energy extracted during discharge |
| `QDischarge_mA_h` | Charge extracted during discharge |
| `Temperature__C` | Cell surface temperature |
| `cycleNumber` | Raw cycle number from tester |
| `Ns` | Cycle segment identifier |

Important note: `cycleNumber` should not be blindly trusted. The dataset README states that the recorded cycle number is not fully accurate because raw tester outputs were concatenated. Therefore, cycle reconstruction should be validated using `Ns`, time resets, segment transitions and charge/discharge structure.

## Cell conditions

| Cell | Condition |
|---|---|
| VAH01 | Baseline |
| VAH02 | Extended cruise, 1000 s |
| VAH05 | 10% power reduction during discharge |
| VAH06 | CC charge current reduced to C/2 |
| VAH07 | CV charge voltage reduced to 4.0 V |
| VAH09 | Thermal chamber temperature 20 °C |
| VAH10 | Thermal chamber temperature 30 °C |
| VAH11 | 20% power reduction during discharge |
| VAH12 | Short cruise length, 400 s |
| VAH13 | Short cruise length, 600 s |
| VAH15 | Extended cruise, 1000 s |
| VAH16 | CC charge current reduced to 1.5 C |
| VAH17 | Baseline |
| VAH20 | Charge current reduced to 1.5 C |
| VAH22 | Extended cruise, 1000 s |
| VAH23 | CV charge voltage reduced to 4.1 V |
| VAH24 | CC charge current reduced to C/2 |
| VAH25 | Thermal chamber temperature 20 °C |
| VAH26 | Short cruise length, 600 s |
| VAH27 | Baseline |
| VAH28 | 10% power reduction during discharge |
| VAH30 | Thermal chamber temperature 35 °C |

## Known dataset issues

The dataset README reports several anomalies. These must be explicitly considered during data cleaning and validation.

Examples:

- Missing or duplicated capacity tests.
- Tester malfunctions in specific cells/cycles.
- Discontinuities within some cycles.
- Voltage spikes.
- Cycles split across files.
- Long rest periods.
- Inaccurate raw cycle numbering.

This project should therefore not treat the raw data as directly ready for modelling. Every cleaning decision must be documented and validated numerically and graphically.

## Main modelling target: SoH

The usual capacity-based definition of SoH is:

SoH(t) = C(t) / C0

where:

- C(t) is the available capacity at cycle or time t.
- C0 is the initial reference capacity.

In this dataset, Reference Performance Tests (RPTs) are performed approximately every 50 mission cycles. These tests can be used to estimate the degradation trajectory of each cell.

Possible SoH construction strategies:

1. Use raw RPT capacity values only.
2. Fit a smooth curve through RPT capacity points and estimate SoH for all cycles.
3. Compare several fitting strategies: polynomial, spline, monotonic smoothing or local interpolation.
4. Avoid using RPT cycles as normal training samples to prevent leakage.

## Possible prediction tasks

This TFG can explore several supervised learning formulations:

### Task A — Present-cycle SoH estimation

Input: features from cycle t.  
Target: SoH at cycle t.

This is the simplest formulation. It evaluates whether cycle-level measurements contain enough information to estimate current battery health.

### Task B — Future SoH forecasting

Input: features up to cycle t.  
Target: SoH at cycle t + h.

Possible horizons:

- h = 1 cycle.
- h = 10 cycles.
- h = 50 cycles.
- h = 100 cycles.
- h = 200 cycles.

This is closer to prognostics and predictive maintenance.

### Task C — RUL prediction

Input: features up to cycle t.  
Target: number of cycles remaining until SoH crosses a defined end-of-life threshold.

Possible EOL thresholds:

- SoH = 0.80.
- SoH = 0.75.
- SoH = 0.70.

This task may be harder because not all cells necessarily reach the same threshold cleanly.

## Recommended feature families

### Basic cycle-level features

For each reconstructed cycle:

- Min, max, mean and standard deviation of voltage.
- Min, max, mean and standard deviation of current.
- Min, max, mean and standard deviation of temperature.
- Charge duration.
- Discharge duration.
- Rest duration.
- Total cycle duration.
- Charge throughput.
- Discharge throughput.
- Energy charged.
- Energy discharged.
- Coulombic efficiency.
- Energy efficiency.

### Phase-based features

Extract features separately for:

- Charge.
- Charge rest.
- Takeoff.
- Cruise.
- Landing.
- Discharge rest.

This is important because eVTOL degradation is phase-dependent: takeoff and landing have high power demand, while cruise is longer but lower power.

### Degradation indicators

Potential health indicators:

- Capacity fade.
- Internal resistance proxy.
- Voltage drop under load.
- Temperature increase.
- Discharge energy decrease.
- Charge/discharge efficiency.
- Rolling statistics over previous cycles.
- Slopes or trends over recent windows.

## Critical methodological warnings

1. Do not trust `cycleNumber` without validation.
2. Do not mix RPT/capacity-test cycles with normal mission cycles.
3. Do not use future information in feature engineering.
4. Use grouped validation by cell when evaluating generalization to unseen batteries.
5. Use chronological validation when evaluating future forecasting.
6. Always compare model performance against simple baselines.
7. Document every cleaning rule and every excluded cycle/cell.
8. Evaluate results numerically and graphically.