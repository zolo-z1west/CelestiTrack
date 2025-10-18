from __future__ import annotations
from pathlib import Path
from typing import List, Dict, Any, Optional
import pandas as pd
import csv
import tempfile
import shutil
from datetime import datetime

def ensure_parent_dir(path: Path) -> None:
    parent = path.parent
    parent.mkdir(parents=True, exist_ok=True)

def append_rows_to_csv(rows: List[Dict[str, Any]], column_order: List[str], out_path: Path) -> None:
    df = pd.DataFrame(rows)
    cols_existing = [c for c in column_order if c in df.columns]
    other_cols = [c for c in df.columns if c not in cols_existing]
    final_cols = cols_existing + other_cols
    ensure_parent_dir(out_path)
    compression = "gzip" if str(out_path).endswith(".gz") else None
    write_header = not out_path.exists()
    if compression == "gzip":
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".csv.gz")
        try:
            df.to_csv(tmp.name, mode="w", header=write_header, index=False, columns=final_cols, compression="gzip")
            if out_path.exists():
                with tempfile.NamedTemporaryFile(delete=False) as combined:
                    with pd.read_csv(out_path, compression="gzip", iterator=True, chunksize=100000) as reader:
                        for chunk in reader:
                            chunk.to_csv(combined.name, mode="a", header=combined.tell()==0, index=False)
                    with pd.read_csv(tmp.name, compression="gzip", iterator=True, chunksize=100000) as reader2:
                        for chunk in reader2:
                            chunk.to_csv(combined.name, mode="a", header=False, index=False)
                    shutil.move(combined.name, out_path)
            else:
                shutil.move(tmp.name, out_path)
        finally:
            try:
                Path(tmp.name).unlink(missing_ok=True)
            except Exception:
                pass
    else:
        mode = "a" if out_path.exists() else "w"
        df.to_csv(out_path, mode=mode, header=write_header, index=False, columns=final_cols)

def update_manifest(manifest_path: Path, partition_path: str, tle_source: str, orbit_class: str, start_time: str, end_time: str, row_count: int, validation_report: str) -> None:
    ensure_parent_dir(manifest_path)
    exists = manifest_path.exists()
    with manifest_path.open("a", newline="") as fh:
        writer = csv.writer(fh)
        if not exists:
            writer.writerow(["partition_path", "tle_source", "orbit_class", "start_time", "end_time", "row_count", "validation_report", "extraction_time"])
        writer.writerow([partition_path, tle_source, orbit_class, start_time, end_time, str(row_count), validation_report, datetime.utcnow().isoformat()])

def write_validation_report(report: Dict[str, Any], out_path: Path) -> None:
    ensure_parent_dir(out_path)
    with out_path.open("w") as fh:
        import json
        json.dump(report, fh, indent=2, default=str)

def read_manifest(manifest_path: Path) -> Optional[List[Dict[str, Any]]]:
    if not manifest_path.exists():
        return None
    import pandas as pd
    df = pd.read_csv(manifest_path)
    return df.to_dict(orient="records")
