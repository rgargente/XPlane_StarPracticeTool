"""
A library to handle CIFP data in X-Plane
Direct dependencies on X-Plane libraries is avoided to make the code more easily testable.
"""

import os
import math


def _get_file_path(xplane_path, airport_icao):
    file_name = "{}.dat".format(airport_icao)
    file_path = os.path.join(xplane_path, "Custom Data", "CIFP", file_name)
    if not os.path.exists(file_path):
        file_path = os.path.join(xplane_path, "Resources", "default data", "CIFP", file_name)
    return file_path


def get_heading_between_two_lat_lon(lat1, lon1, lat2, lon2):
    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)
    d_lon = lon2 - lon1
    h = math.atan2(math.sin(d_lon) * math.cos(lat2),
                   math.cos(lat1) * math.sin(lat2) - math.sin(lat1) * math.cos(lat2) * math.cos(d_lon))
    return math.degrees(h)


class Cifp:

    def __init__(self, xplm_wrapper, airport_icao, xplane_path=None, file_path=None):
        """
        Either (xplane_path and airport_icao) or file_path should be passed.
        :param file_path: If None xplane_path and airport_icao are used to find the right path. Otherwise they are ignored and the passed path is used.
        """
        self.raw_lines = []
        self.star_names = []
        self.stars = {}

        airport_lat, airport_lon = xplm_wrapper.get_airport_lat_lon(airport_icao, None, None)
        if airport_lat is None:
            raise Exception("Airport not found")

        if not file_path:
            file_path = _get_file_path(xplane_path, airport_icao)

        f = open(file_path)
        for l in f:
            self.raw_lines.append(l)
            # STAR:010, 2, MAPA1K, RW30, MAPAX, LE, E, A, E,, , IF,, , , , , , , , , , , , , , , , , , , , , , , , , ;
            # STAR:020, 2, MAPA1K, RW30,, , , , , , , CI,, , , , , , , , 1690,, , , , , , , , , , , , , , , , ;
            if l.split(':')[0] == 'STAR':
                line_items = l.split(',')
                star_name = line_items[2]
                if star_name not in self.star_names:  # new STAR
                    self.star_names.append(star_name)
                    star = Star(xplm_wrapper, star_name, airport_lat, airport_lon)
                    self.stars[star_name] = star
                else:  # update star
                    star = self.stars[star_name]
                star._parse_raw_line(line_items)

    def get_prev_star(self, star_name):
        i = self.star_names.index(star_name)
        if i == 0:
            i = len(self.star_names)
        return self.star_names[i - 1]

    def get_next_star(self, star_name):
        i = self.star_names.index(star_name)
        if i == len(self.star_names) - 1:
            return self.star_names[0]
        else:
            return self.star_names[i + 1]


class Star:
    INDEX_WAYPOINT = 4
    INDEX_COURSE_INTERCEPT = 11
    INDEX_CI_HEADING = 20

    def __init__(self, xplm_wrapper, name, airport_lat, airport_lon):
        self.name = name
        self.airport_lat = airport_lat
        self.airport_lon = airport_lon
        self.waypoints = []
        self.init_lat = None
        self.init_lon = None
        self._init_heading = None

        self._xplm_wrapper = xplm_wrapper

    def _parse_raw_line(self, line_items):
        if line_items[self.INDEX_COURSE_INTERCEPT] == 'CI':
            self._init_heading = float(line_items[self.INDEX_CI_HEADING]) / 10
            self.waypoints.append('INTC')
        else:
            waypoint_id = line_items[self.INDEX_WAYPOINT]
            self.waypoints.append(waypoint_id)
            if self.init_lat is None:
                self.init_lat, self.init_lon = self._xplm_wrapper.get_waypoint_lat_lon(waypoint_id, self.airport_lat,
                                                                                       self.airport_lon)

    @property
    def init_heading(self):
        if self._init_heading is None:
            lat2, lon2 = self._xplm_wrapper.get_waypoint_lat_lon(self.waypoints[1], self.airport_lat, self.airport_lon)
            self._init_heading = get_heading_between_two_lat_lon(self.init_lat, self.init_lon,
                                                                 lat2, lon2)
        return self._init_heading
