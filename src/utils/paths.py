"""Utilidades de rutas para el proyecto."""

from __future__ import annotations

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_RAW_DIR = PROJECT_ROOT / "data" / "raw"
REPORTS_RESULTS_DIR = PROJECT_ROOT / "reports" / "results"


def ensure_reports_results_dir() -> Path:
    """Crea `reports/results` si no existe y devuelve su ruta."""
    REPORTS_RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    return REPORTS_RESULTS_DIR
