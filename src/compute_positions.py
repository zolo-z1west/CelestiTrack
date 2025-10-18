from __future__ import annotations
from typing import List, Dict, Any
from pathlib import Path
from datetime import datetime, timezone
from skyfield.api import load
from src.io_utils import append_rows_to_csv

def compute_positions(tle_paths: List[Path], out_csv: Path, column_order: List[str]) -> None:
    ts = load.timescale()
    now = datetime.now(timezone.utc)
    rows: List[Dict[str, Any]] = []
    for tle_path in tle_paths:
        with open(tle_path) as fh:
            lines = [line.strip() for line in fh.readlines() if line.strip()]
        for i in range(0, len(lines), 3):
            if i + 2 >= len(lines):
                continue
            name, l1, l2 = lines[i : i + 3]
            try:
                sat = load.tle(lines[i + 1], lines[i + 2], name=name)
                geo = sat.at(ts.utc(now))
                pos = geo.position.km
                vel = geo.velocity.km_per_s
                sub = geo.subpoint()
                rows.append(
                    {
                        "satellite_name": name,
                        "timestamp_utc": now.isoformat(),
                        "temex": pos[0],
                        "temey": pos[1],
                        "temez": pos[2],
                        "temevx": vel[0],
                        "temevy": vel[1],
                        "temevz": vel[2],
                        "subpoint_lat_deg": sub.latitude.degrees,
                        "subpoint_lon_deg": sub.longitude.degrees,
                        "subpoint_elevation_m": sub.elevation.m,
                        "tle_source": tle_path.name,
                    }
                )
            except Exception:
                continue
    if rows:
        append_rows_to_csv(rows, column_order, out_csv)
