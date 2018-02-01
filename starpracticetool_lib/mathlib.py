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

import math


def heading_and_speed_to_xyz_vector(heading, speed_ms):
    """
    Converts a heading and speed to a velocity vector in XPlane's Open GL coordinates.
    Coordinate system is right handed, Y up. X is East
    :param heading: in degrees 
    :param speed_ms: in m/s
    :return: [x, y, z]
    """
    alpha = math.radians(heading - 90)
    x = math.cos(alpha) * speed_ms
    z = math.sin(alpha) * speed_ms
    return [x, 0, z]


def hpr_to_quaternion(heading, pitch, roll):
    """
    Converts a heading, pitch and roll to a quaternion as explained here:
    http://www.xsquawkbox.net/xpsdk/mediawiki/MovingThePlane#Orienting_the_Aircraft_in_Space
    """
    q = [None] * 4
    heading = math.pi / 360 * heading
    pitch = math.pi / 360 * pitch
    roll = math.pi / 360 * roll
    q[0] = math.cos(heading) * math.cos(pitch) * math.cos(roll) + math.sin(heading) * math.sin(pitch) * math.sin(roll)
    q[1] = math.cos(heading) * math.cos(pitch) * math.sin(roll) - math.sin(heading) * math.sin(pitch) * math.cos(roll)
    q[2] = math.cos(heading) * math.sin(pitch) * math.cos(roll) + math.sin(heading) * math.cos(pitch) * math.sin(roll)
    q[3] = -math.cos(heading) * math.sin(pitch) * math.sin(roll) + math.sin(heading) * math.cos(pitch) * math.cos(roll)
    return q


def knots_to_m_sec(kts):
    """Knots (kt) to meters/second (m/s)"""
    return kts * 0.514444


def feet_to_meters(feet):
    return feet * 0.3048
