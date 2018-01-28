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


class MockXplmWrapper:
    def get_airport_lat_lon(self, id, airport_lat, airport_lon):
        if id == 'LEBB':
            return 43.304305556, -2.922277778
        else:
            return None, None

    def get_waypoint_lat_lon(self, id, airport_lat, airport_lon):
        if id == 'DGO':
            return 42.453305556, -2.880694444
        elif id == 'VRA':
            return 42.731888889, -2.865583333
        elif id == 'MAPAX':
            return 43.683750000, -3.044083333
        else:
            return None, None
