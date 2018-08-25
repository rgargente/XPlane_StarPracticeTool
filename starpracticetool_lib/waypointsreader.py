import mathlib
from starpracticetool_lib import paths
from starpracticetool_lib.fixparser import FixParser
from starpracticetool_lib.navparser import NavParser


class WaypointsReader:
    """A reader class for waypoints coming from both earth_fix.dat and earth_nav.dat files"""

    def __init__(self, xplane_path, fixparser=None, navparser=None):
        """
        Either xplane_path or (fixparser and navparser) should be passed.
        Just use xplane_path for normal use, the other option is for testing.
        """
        if xplane_path:
            self._fixparser = FixParser(paths.get_earth_fix_dat_file_path(xplane_path))
            self._navparser = NavParser(paths.get_earth_nav_dat_file_path(xplane_path))
        else:
            self._fixparser = fixparser
            self._navparser = navparser

    def get_latlon(self, waypoint_name, airport_lat, airport_lon):
        waypoints = self._navparser.get_latlon(waypoint_name) + \
                    self._fixparser.get_latlon(waypoint_name)
        if waypoints:
            return min(waypoints, key=lambda wp: mathlib.get_distance_between_latlon((airport_lat, airport_lon), wp))
        else:
            return None, None
