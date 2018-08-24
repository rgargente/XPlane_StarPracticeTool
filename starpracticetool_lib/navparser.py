import re

from mathlib import is_number
from starpracticetool_lib.waypointparser import WaypointParser, Waypoint


class NavParser(WaypointParser):
    """A parser for earth_nav.dat files"""

    def __init__(self, dat_filepath):
        WaypointParser.__init__(self)

        with open(dat_filepath) as f:
            for l in f:
                l = re.sub(' +', ' ', l.strip())  # Remove multiple spaces
                parts = l.split(' ', 10)
                if len(parts) == 11 \
                        and is_number(parts[1]) and is_number(parts[2]):
                    self.waypoints.add(Waypoint(float(parts[1]), float(parts[2]), parts[7]))
