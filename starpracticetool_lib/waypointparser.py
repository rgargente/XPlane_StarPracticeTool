from abc import ABCMeta


class WaypointParser:
    __metaclass__ = ABCMeta

    def __init__(self):
        self.waypoints = set()

    def get_latlon(self, name):
        return [s.latlon for s in self.waypoints if s.name == name]


class Waypoint:
    """Dumb class for holding waypoint data"""

    def __init__(self, lat, lon, name):
        self.latlon = lat, lon
        self.name = name

    def __eq__(self, other):
        return self.latlon == other.latlon and \
               self.name == other.name

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash((self.latlon, self.name))
