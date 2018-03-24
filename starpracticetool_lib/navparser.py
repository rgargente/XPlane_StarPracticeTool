import re
from mathlib import is_number


class NavParser:
    def __init__(self, dat_filepath):
        self.stations = set()

        with open(dat_filepath) as f:
            for l in f:
                l = re.sub(' +', ' ', l.strip())  # Remove multiple spaces
                parts = l.split(' ', 10)
                if len(parts) == 11 \
                        and is_number(parts[1]) and is_number(parts[2]):
                    self.stations.add(Station(float(parts[1]), float(parts[2]), parts[7]))

    def get_station_latlon_by_name(self, name):
        from mathlib import get_distance_between_latlon
        return [s.latlon for s in self.stations if s.name == name]


class Station:
    """Dumb class for holding station data"""

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
