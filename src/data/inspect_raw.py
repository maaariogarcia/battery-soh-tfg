"""Auditoría inicial de archivos CSV crudos del eVTOL Battery Dataset."""

from __future__ import annotations

import csv
import re
import sys
from pathlib import Path
from dataclasses import dataclass
from typing import Dict, Iterable, List, Optional, Sequence, Set, Tuple

import pandas as pd

if __package__ is None or __package__ == "":
    sys.path.append(str(Path(__file__).resolve().parents[2]))

from src.utils.paths import DATA_RAW_DIR, ensure_reports_results_dir

MISSION_EXPECTED_COLUMNS = {
    "time_s",
    "I_mA",
    "Ecell_V",
    "Temperature__C",
    "cycleNumber",
    "Ns",
}

IMPEDANCE_EXPECTED_COLUMNS = {
    "cycleNumber",
    "freq_Hz",
    "Zreal_Ohm",
    "Zimag_Ohm",
}


@dataclass
class FileInfo:
    """Metadatos básicos de un CSV crudo."""

    path: Path
    file_name: str
    file_type: str
    cell_id: str
    file_size_mb: float
    n_rows: int
    n_columns: int
    columns: List[str]


def detect_file_type_and_cell_id(file_name: str) -> Tuple[str, str]:
    """Clasifica un archivo como misión o impedancia y extrae la celda."""
    lowered = file_name.lower()
    file_type = "impedance" if lowered.endswith("_impedance.csv") else "mission"
    match = re.match(r"^(VAH\d+)", file_name, flags=re.IGNORECASE)
    cell_id = match.group(1).upper() if match else "UNKNOWN"
    return file_type, cell_id


def read_columns(path: Path) -> List[str]:
    """Lee la cabecera de columnas sin cargar el archivo completo."""
    try:
        df_head = pd.read_csv(path, nrows=0)
        return [str(col) for col in df_head.columns]
    except Exception as exc:
        raise RuntimeError(f"No se pudo leer cabecera en {path.name}: {exc}") from exc


def count_rows_streaming(path: Path) -> int:
    """Cuenta filas de datos usando lectura en streaming."""
    try:
        with path.open("r", encoding="utf-8", errors="replace", newline="") as f:
            row_count = sum(1 for _ in f)
        return max(0, row_count - 1)
    except Exception as exc:
        raise RuntimeError(f"No se pudo contar filas en {path.name}: {exc}") from exc


def build_file_info(path: Path) -> FileInfo:
    """Construye metadatos básicos para un CSV crudo."""
    file_type, cell_id = detect_file_type_and_cell_id(path.name)
    columns = read_columns(path)
    n_rows = count_rows_streaming(path)
    file_size_mb = path.stat().st_size / (1024 * 1024)
    return FileInfo(
        path=path,
        file_name=path.name,
        file_type=file_type,
        cell_id=cell_id,
        file_size_mb=round(file_size_mb, 4),
        n_rows=n_rows,
        n_columns=len(columns),
        columns=columns,
    )


def _resolve_first_present_column(columns: Sequence[str], candidates: Sequence[str]) -> Optional[str]:
    """Devuelve la primera columna candidata presente."""
    available = set(columns)
    for name in candidates:
        if name in available:
            return name
    return None


def _compute_time_metrics(path: Path, time_col: str) -> Tuple[Optional[float], Optional[float], bool, int]:
    min_t: Optional[float] = None
    max_t: Optional[float] = None
    prev_t: Optional[float] = None
    n_decreases = 0

    for chunk in pd.read_csv(path, usecols=[time_col], chunksize=200_000):
        series = pd.to_numeric(chunk[time_col], errors="coerce").dropna()
        if series.empty:
            continue

        chunk_min = float(series.min())
        chunk_max = float(series.max())
        min_t = chunk_min if min_t is None else min(min_t, chunk_min)
        max_t = chunk_max if max_t is None else max(max_t, chunk_max)

        values = series.to_numpy()
        if prev_t is not None and values[0] < prev_t:
            n_decreases += 1
        for i in range(1, len(values)):
            if values[i] < values[i - 1]:
                n_decreases += 1
        prev_t = values[-1]

    return min_t, max_t, n_decreases > 0, n_decreases


def _compute_numeric_min_max(path: Path, col_name: str) -> Tuple[Optional[float], Optional[float]]:
    min_v: Optional[float] = None
    max_v: Optional[float] = None
    for chunk in pd.read_csv(path, usecols=[col_name], chunksize=200_000):
        series = pd.to_numeric(chunk[col_name], errors="coerce").dropna()
        if series.empty:
            continue
        cmin = float(series.min())
        cmax = float(series.max())
        min_v = cmin if min_v is None else min(min_v, cmin)
        max_v = cmax if max_v is None else max(max_v, cmax)
    return min_v, max_v


def _compute_unique_count(path: Path, col_name: str) -> int:
    unique_values: Set[str] = set()
    for chunk in pd.read_csv(path, usecols=[col_name], chunksize=200_000):
        series = chunk[col_name].dropna()
        unique_values.update(series.astype(str).unique().tolist())
    return len(unique_values)


def save_csv(path: Path, rows: Iterable[Dict[str, object]], fieldnames: List[str]) -> None:
    """Guarda un CSV con columnas explícitas."""
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def inspect_raw_data() -> int:
    """Ejecuta auditoría inicial y exporta reportes CSV."""
    print("[INFO] Iniciando auditoría de data/raw...")
    raw_dir = DATA_RAW_DIR
    results_dir = ensure_reports_results_dir()

    if not raw_dir.exists():
        print(f"[ERROR] No existe el directorio esperado: {raw_dir}")
        return 1

    csv_files = sorted(raw_dir.glob("*.csv"))
    if not csv_files:
        print(f"[WARN] No se encontraron archivos .csv en {raw_dir}")
        return 0

    file_infos: List[FileInfo] = []
    failed_files: List[str] = []

    for idx, csv_path in enumerate(csv_files, start=1):
        print(f"[INFO] ({idx}/{len(csv_files)}) Procesando {csv_path.name}...")
        try:
            file_infos.append(build_file_info(csv_path))
        except Exception as exc:
            print(f"[ERROR] {exc}")
            failed_files.append(csv_path.name)

    if not file_infos:
        print("[ERROR] No se pudo procesar ningún archivo CSV.")
        return 1

    inventory_rows: List[Dict[str, object]] = []
    column_presence: Dict[str, Dict[str, object]] = {}

    for info in file_infos:
        expected = MISSION_EXPECTED_COLUMNS if info.file_type == "mission" else IMPEDANCE_EXPECTED_COLUMNS
        cols_set = set(info.columns)
        missing_cols = sorted(expected - cols_set)
        extra_cols = sorted(cols_set - expected)

        inventory_rows.append(
            {
                "file_name": info.file_name,
                "file_type": info.file_type,
                "cell_id": info.cell_id,
                "file_size_mb": info.file_size_mb,
                "n_rows": info.n_rows,
                "n_columns": info.n_columns,
                "column_names": "|".join(info.columns),
                "missing_columns_against_expected_schema": "|".join(missing_cols),
                "extra_columns_against_expected_schema": "|".join(extra_cols),
            }
        )

        for col in info.columns:
            stats = column_presence.setdefault(
                col,
                {
                    "column_name": col,
                    "count": 0,
                    "types": set(),
                    "examples": [],
                },
            )
            stats["count"] += 1
            stats["types"].add(info.file_type)
            if len(stats["examples"]) < 3:
                stats["examples"].append(info.file_name)

    save_csv(
        results_dir / "raw_file_inventory.csv",
        inventory_rows,
        [
            "file_name",
            "file_type",
            "cell_id",
            "file_size_mb",
            "n_rows",
            "n_columns",
            "column_names",
            "missing_columns_against_expected_schema",
            "extra_columns_against_expected_schema",
        ],
    )

    columns_rows = [
        {
            "column_name": data["column_name"],
            "number_of_files_where_present": data["count"],
            "file_types_where_present": "|".join(sorted(data["types"])),
            "example_files": "|".join(data["examples"]),
        }
        for _, data in sorted(column_presence.items(), key=lambda x: x[0].lower())
    ]
    save_csv(
        results_dir / "raw_columns_summary.csv",
        columns_rows,
        [
            "column_name",
            "number_of_files_where_present",
            "file_types_where_present",
            "example_files",
        ],
    )

    mission_rows: List[Dict[str, object]] = []
    imp_rows: List[Dict[str, object]] = []

    for info in file_infos:
        if info.file_type == "mission":
            cols = info.columns
            time_col = _resolve_first_present_column(cols, ["time_s", "t_s", "time"])
            voltage_col = _resolve_first_present_column(cols, ["Ecell_V", "voltage_V", "V"])
            current_col = _resolve_first_present_column(cols, ["I_mA", "current_mA", "I"])
            temp_col = _resolve_first_present_column(cols, ["Temperature__C", "temperature_C", "temp_C"])
            cycle_col = _resolve_first_present_column(cols, ["cycleNumber", "cycle_number"])
            ns_col = _resolve_first_present_column(cols, ["Ns", "ns"])

            try:
                min_t, max_t, has_resets, n_dec = (None, None, False, 0)
                if time_col:
                    min_t, max_t, has_resets, n_dec = _compute_time_metrics(info.path, time_col)

                min_v, max_v = (None, None)
                if voltage_col:
                    min_v, max_v = _compute_numeric_min_max(info.path, voltage_col)

                min_i, max_i = (None, None)
                if current_col:
                    min_i, max_i = _compute_numeric_min_max(info.path, current_col)

                min_temp, max_temp = (None, None)
                if temp_col:
                    min_temp, max_temp = _compute_numeric_min_max(info.path, temp_col)

                min_cycle, max_cycle = (None, None)
                n_unique_cycle = 0
                if cycle_col:
                    min_cycle, max_cycle = _compute_numeric_min_max(info.path, cycle_col)
                    n_unique_cycle = _compute_unique_count(info.path, cycle_col)

                n_unique_ns = _compute_unique_count(info.path, ns_col) if ns_col else 0

                mission_rows.append(
                    {
                        "cell_id": info.cell_id,
                        "n_rows": info.n_rows,
                        "min_time_s": min_t,
                        "max_time_s": max_t,
                        "has_time_resets": has_resets,
                        "n_time_decreases": n_dec,
                        "min_voltage": min_v,
                        "max_voltage": max_v,
                        "min_current": min_i,
                        "max_current": max_i,
                        "min_temperature": min_temp,
                        "max_temperature": max_temp,
                        "min_cycleNumber": min_cycle,
                        "max_cycleNumber": max_cycle,
                        "n_unique_cycleNumber": n_unique_cycle,
                        "n_unique_Ns": n_unique_ns,
                    }
                )
            except Exception as exc:
                print(f"[ERROR] Error en métricas de misión para {info.file_name}: {exc}")
        else:
            cycle_col = _resolve_first_present_column(info.columns, ["cycleNumber", "cycle_number"])
            min_cycle, max_cycle = (None, None)
            if cycle_col:
                try:
                    min_cycle, max_cycle = _compute_numeric_min_max(info.path, cycle_col)
                except Exception as exc:
                    print(f"[ERROR] Error leyendo ciclos en {info.file_name}: {exc}")

            imp_rows.append(
                {
                    "cell_id": info.cell_id,
                    "n_rows": info.n_rows,
                    "n_columns": info.n_columns,
                    "column_names": "|".join(info.columns),
                    "min_cycle_number_if_available": min_cycle,
                    "max_cycle_number_if_available": max_cycle,
                }
            )

    save_csv(
        results_dir / "raw_basic_quality_report.csv",
        mission_rows,
        [
            "cell_id",
            "n_rows",
            "min_time_s",
            "max_time_s",
            "has_time_resets",
            "n_time_decreases",
            "min_voltage",
            "max_voltage",
            "min_current",
            "max_current",
            "min_temperature",
            "max_temperature",
            "min_cycleNumber",
            "max_cycleNumber",
            "n_unique_cycleNumber",
            "n_unique_Ns",
        ],
    )

    save_csv(
        results_dir / "raw_impedance_inventory.csv",
        imp_rows,
        [
            "cell_id",
            "n_rows",
            "n_columns",
            "column_names",
            "min_cycle_number_if_available",
            "max_cycle_number_if_available",
        ],
    )

    print(f"[INFO] Reportes guardados en: {results_dir}")
    print(f"[INFO] Archivos procesados correctamente: {len(file_infos)}")
    if failed_files:
        print(f"[WARN] Archivos con error: {len(failed_files)} -> {', '.join(failed_files)}")
    return 0


if __name__ == "__main__":
    sys.exit(inspect_raw_data())
