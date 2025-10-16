from datetime import datetime
from typing import List, Dict, Any, Union

#schema defintion 
SCHEMA = [
    # Core identifiers
    {"name": "satellite_id", "type": str, "unit": None, "source": "CelesTrak TLE", "required": True},
    {"name": "satellite_name", "type": str, "unit": None, "source": "CelesTrak TLE", "required": True},
    {"name": "group", "type": str, "unit": None, "source": "CelesTrak TLE", "required": True},
    {"name": "tle_epoch", "type": "datetime", "unit": "ISO8601", "source": "CelesTrak TLE", "required": True},
    {"name": "last_updated_tle", "type": "datetime", "unit": "ISO8601", "source": "CelesTrak TLE", "required": True},
    # Temporal fields
    {"name": "timestamp_utc", "type": "datetime", "unit": "ISO8601", "source": "Skyfield", "required": True},
    {"name": "tle_age_hours", "type": float, "unit": "hours", "source": "computed", "required": True},
    # Orbital/spatial fields
    {"name": "temex", "type": float, "unit": "km", "source": "Skyfield", "required": True},
    {"name": "temey", "type": float, "unit": "km", "source": "Skyfield", "required": True},
    {"name": "temez", "type": float, "unit": "km", "source": "Skyfield", "required": True},
    {"name": "alt_deg", "type": float, "unit": "degrees", "source": "Skyfield", "required": True},
    {"name": "az_deg", "type": float, "unit": "degrees", "source": "Skyfield", "required": True},
    {"name": "range_km", "type": float, "unit": "km", "source": "Skyfield", "required": True},
    {"name": "inclination_deg", "type": float, "unit": "degrees", "source": "Skyfield", "required": True},
    {"name": "eccentricity", "type": float, "unit": None, "source": "Skyfield", "required": True},
    {"name": "raan_deg", "type": float, "unit": "degrees", "source": "Skyfield", "required": True},
    {"name": "perigee_km", "type": float, "unit": "km", "source": "Skyfield", "required": True},
    {"name": "apogee_km", "type": float, "unit": "km", "source": "Skyfield", "required": True},
    {"name": "orbital_period_min", "type": float, "unit": "minutes", "source": "Skyfield", "required": True},
    {"name": "mean_anomaly_deg", "type": float, "unit": "degrees", "source": "Skyfield", "required": True},
    # Derived fields/ ML features
    {"name": "velocity_mag_kms", "type": float, "unit": "km/s", "source": "derived", "required": True},
    {"name": "subpoint_lat_deg", "type": float, "unit": "degrees", "source": "derived", "required": True},
    {"name": "subpoint_lon_deg", "type": float, "unit": "degrees", "source": "derived", "required": True},
    {"name": "phase_angle_deg", "type": float, "unit": "degrees", "source": "derived", "required": True},
    {"name": "angular_size_deg", "type": float, "unit": "degrees", "source": "derived", "required": False},
    {"name": "cyclical_time_sin", "type": float, "unit": None, "source": "computed", "required": True},
    {"name": "cyclical_time_cos", "type": float, "unit": None, "source": "computed", "required": True},
    {"name": "orbit_class", "type": str, "unit": None, "source": "derived", "required": True},
    # Verification fields
    {"name": "verified_stellarium", "type": bool, "unit": None, "source": "manual", "required": False},
    {"name": "estimated_error_km", "type": float, "unit": "km", "source": "optional", "required": False},
    {"name": "notes", "type": str, "unit": None, "source": "optional", "required": False},
]


#define helper functions
def get_column_names() -> List[str]:
    """Return ordered list of canonical column names."""
    return [col["name"] for col in SCHEMA]

def validate_row(row: Dict[str, Any]) -> List[str]:
    """
    Validate a single row against the CelestiTrack schema.
    Returns a list of errors; empty if valid.
    """
    errors = []
    for col in SCHEMA:
        name = col["name"]
        required = col.get("required", True)
        expected_type = col["type"]
        value = row.get(name)

        # error def for missing required fields
        if required and value is None:
            errors.append(f"Missing value for required column: {name}")
            continue

        # note to dev - skip none values for optional columns
        if value is None:
            continue

        # check for type mismatches
        if expected_type == "datetime":
            if not isinstance(value, datetime):
                errors.append(f"{name} expected datetime, got {type(value).__name__}")
        elif expected_type == float:
            try:
                float(value)
            except Exception:
                errors.append(f"{name} expected float, got {value}")
        elif expected_type == str:
            if not isinstance(value, str):
                errors.append(f"{name} expected str, got {type(value).__name__}")
        elif expected_type == bool:
            if not isinstance(value, bool):
                errors.append(f"{name} expected bool, got {type(value).__name__}")
        else:
            errors.append(f"{name} has unknown type: {expected_type}")
    return errors

def get_schema() -> List[Dict[str, Any]]:
    return SCHEMA