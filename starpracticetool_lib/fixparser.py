import re

from starpracticetool_lib.mathlib import is_number
from starpracticetool_lib.waypointparser import WaypointParser, Waypoint


class FixParser(WaypointParser):
    """A parser for earth_fix.dat files"""

    def __init__(self, fix_filepath):
        WaypointParser.__init__(self)

        with open(fix_filepath) as f:
            for l in f:
                l = re.sub(' +', ' ', l.strip())  # Remove multiple spaces
                parts = l.split(' ')
                if len(parts) == 5 or len(parts) == 6 \
                        and is_number(parts[0]) and is_number(parts[1]):
                    self.waypoints.add(Waypoint(float(parts[0]), float(parts[1]), parts[2]))
