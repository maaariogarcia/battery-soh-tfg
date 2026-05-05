# Literature notes — Battery SoH prediction for eVTOL applications

## 1. Dataset source: Bills et al.

The eVTOL Battery Dataset was created to provide public battery aging data under mission profiles representative of electric vertical takeoff and landing aircraft.

The dataset is especially relevant because many public battery datasets use generic constant-current cycling protocols, whereas this dataset includes dynamic mission profiles with takeoff, cruise and landing phases.

Key ideas for this TFG:

- The dataset is application-specific.
- The mission profile is not equivalent to standard CC discharge.
- The landing phase is critical because high power is demanded when the cell is already partially depleted.
- Degradation depends on duty cycle, temperature, current and depth of discharge.
- The dataset is suitable for data-driven degradation modelling, empirical modelling and machine learning.

## 2. Granado et al. — Machine learning predictions of SoH for eVTOL applications

This paper is the most directly relevant ML baseline for the TFG.

Main methodological ideas:

- Reconstruct cycle numbers because the raw `cycleNumber` is not fully reliable.
- Compute SoH from reference capacity tests.
- Fit a smooth degradation trajectory to estimate SoH across cycles.
- Remove capacity measurement cycles from model training to avoid leakage.
- Aggregate raw time-series into cycle-level features.
- Use rolling windows to include recent historical information.
- Compare several classical ML models:
  - Linear Regression.
  - Support Vector Machines.
  - k-Nearest Neighbors.
  - Random Forest.
  - Gradient Boosting / LightGBM.

Important result:

- kNN achieved very strong results for SoH forecasting up to approximately 200 cycles ahead.
- Classical ML models may outperform more complex deep learning models when the dataset is small and features are well engineered.

Critical interpretation:

- This paper is a strong baseline, but the TFG should not simply reproduce it.
- The project should improve methodological robustness:
  - more transparent cleaning,
  - stronger validation,
  - explicit leakage checks,
  - richer visual EDA,
  - comparison of different target definitions,
  - phase-based feature extraction.

## 3. Yang et al. — Phase-segmented feature extraction

This paper proposes extracting features separately from different operating phases instead of using only unified cycle-level features.

Useful ideas:

- eVTOL batteries operate under dynamic discharge profiles.
- Takeoff, cruise and landing may contain different degradation information.
- Phase-specific features can improve model performance.
- Random Forest importance and Mutual Information can be used for feature selection.
- Internal resistance proxies can be estimated from voltage/current changes.

Critical interpretation:

- The phase-based idea is highly relevant.
- However, complex optimization algorithms such as genetic algorithms should not be the first priority.
- The TFG should first build a reliable, interpretable and validated feature pipeline.
- Advanced optimization should only be considered after strong baselines exist.

## 4. Fu et al. review — SOH estimation from laboratory to practical application

This review is useful for the theoretical framework.

Key ideas:

- SOH is not directly measurable during normal operation.
- Health Indicators are needed to estimate SOH from observable signals.
- Health indicators can be geometric, statistical, parametric or learned directly by models.
- There is a gap between laboratory datasets and practical BMS deployment.
- Statistical health indicators are promising because they can be extracted from operational data.
- Practical battery SOH models should consider generalization, computational cost and interpretability.

Use in the TFG:

- Justify why feature engineering is central.
- Justify why voltage, current, temperature, energy, capacity and resistance-related indicators are relevant.
- Discuss the limitations of laboratory data.
- Discuss why robust validation matters.

## 5. Tuncel et al. — LLM-assisted ML workflow

This paper is useful as context for using ChatGPT/Codex as an assistant in the machine learning workflow.

Relevant ideas:

- LLMs can help automate preprocessing, feature importance, model implementation, hyperparameter tuning and evaluation.
- The workflow is iterative: prompt, run, evaluate, correct, refine.
- LLMs are not substitutes for expert validation.
- The scientist must still define the target, avoid leakage, check assumptions and interpret results.

Use in this TFG:

- Codex can be used as a coding assistant.
- ChatGPT can be used as a methodological reviewer.
- All generated code must be inspected, tested and justified.