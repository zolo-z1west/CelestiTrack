
from skyfield.api import EarthSatellite, load
from pathlib import Path
from typing import List, Tuple
import logging

logging.basicConfig(level=logging.INFO, format = '%(levelname)s: %(message)s')

def read_tle_file(file_path:str) ->List[Tuple[str, str, str]] : #reads a TLE file and returns a list of tuples (name, line1, line2) for each satellite
    tle_entries = []
    file_path = Path(file_path)

    if not file_path.exists():
        logging.error(f"TLE file not found: {file_path}")
        return tle_entries
    with file_path.open('r') as f:
        lines = [line.strip() for line in f if line.strip()]
    for i in range(0, len(lines), 3):
        try: 
            name = lines[i]
            line1 = lines[i+1]
            line2 = lines[i+2]
            tle_entries.append((name, line1, line2))
        except IndexError:
            logging.warning(f"Incomplete TLE entry at lines {i+1}-{i+3} in file {file_path}") #error definition for incomplete TLE entry (if found)
    logging.info(f"Read {len(tle_entries)} TLEs from {file_path}")
    return tle_entries

def parse_tles(tle_list: List[Tuple[str, str, str]]) -> List[EarthSatellite]: #parses list of TLE by argparse, return list of satellite objects
    satellites = []
    for name, line1, line2 in tle_list:
        try:
            sat = EarthSatellite(line1, line2, name)
            satellites.append(sat)
        except Exception as e:
            logging.warning(f"Failed to parse TLE for {name}: {e}")
    logging.info(f"Parsed {len(satellites)} satellites")
    return satellites

def load_group(file_path: str) -> List[EarthSatellite]: #function to read and parse tles from file to object - EarthSatellite
    tle_list = read_tle_file(file_path)
    satellites = parse_tles(tle_list)
    return satellites

#test function to test 
def get_positions(satellites: List[EarthSatellite], ts=None) :
    if ts is None:
        ts = load.timescale()
    t = ts.now()
    positions = {}
    for sat in satellites:
        geo = sat.at(t) #geocentric location at that particular time
        x,y,z = geo.position.km
        positions[sat.name] = (round(x,2), round(y,2), round(z,2))
    
    return positions