"""
X Plane STAR Practice Tool Python plugin
Copyright (C) 2018 Rafael Garcia Argente
https://github.com/rgargente/XPlaneStarPracticeTool

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
from starpracticetool_lib import paths
from starpracticetool_lib.waypointsreader import WaypointsReader

"""
A library to handle CIFP data in X-Plane
Direct dependencies on X-Plane libraries is avoided to make the code more easily testable.
"""

import math
import os


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
    APT_NOT_FOUND_EXC = "Airport not found"

    def __init__(self, xplm_wrapper, airport_icao, xplane_path=None, file_path=None, waypoints_reader=None):
        """
        Either (xplane_path and airport_icao) or (file_path and waypoints_reader) should be passed.
        The second option should be used just for testing.
        :param file_path: If None, xplane_path and airport_icao are used to find the right path. Otherwise they are ignored and the passed path is used.
        """
        self.raw_lines = []
        self.star_names = []
        self.stars = {}

        if waypoints_reader:
            self.waypoints_reader = waypoints_reader
        else:
            self.waypoints_reader = WaypointsReader(xplane_path)

        airport_lat, airport_lon = xplm_wrapper.get_airport_lat_lon(airport_icao, None, None)
        if airport_lat is None:
            raise Exception(Cifp.APT_NOT_FOUND_EXC)

        if not file_path:
            file_path = paths.get_airport_file_path(xplane_path, airport_icao)

        if not os.path.exists(file_path):
            raise Exception(Cifp.APT_NOT_FOUND_EXC)

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
                    star = Star(self.waypoints_reader, star_name, airport_lat, airport_lon)
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

    def __init__(self, waypoints_reader, name, airport_lat, airport_lon):
        self.name = name
        self.airport_lat = airport_lat
        self.airport_lon = airport_lon
        self.waypoints = []
        self.init_lat = None
        self.init_lon = None
        self._init_heading = None

        self._waypoints_reader = waypoints_reader

    def _parse_raw_line(self, line_items):
        if line_items[self.INDEX_COURSE_INTERCEPT] == 'CI':
            self._init_heading = float(line_items[self.INDEX_CI_HEADING]) / 10
            self.waypoints.append('INTC')
        else:
            waypoint_id = line_items[self.INDEX_WAYPOINT]
            self.waypoints.append(waypoint_id)
            if self.init_lat is None:
                self.init_lat, self.init_lon = self._waypoints_reader.get_latlon(waypoint_id, self.airport_lat,
                                                                                       self.airport_lon)

    @property
    def init_heading(self):
        if self._init_heading is None:
            lat2, lon2 = self._waypoints_reader.get_latlon(self.waypoints[1], self.airport_lat, self.airport_lon)

            self._init_heading = get_heading_between_two_lat_lon(self.init_lat, self.init_lon,
                                                                 lat2, lon2)
        return self._init_heading
