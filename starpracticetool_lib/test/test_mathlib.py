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

import pytest

from starpracticetool_lib.mathlib import heading_and_speed_to_xyz_vector


def test_heading_and_speed_to_xyz_vector_north():
    assert heading_and_speed_to_xyz_vector(0, 100) == [pytest.approx(0), 0, -100]


def test_heading_and_speed_to_xyz_vector_east():
    assert heading_and_speed_to_xyz_vector(90, 100) == [100, 0, pytest.approx(0)]


def test_heading_and_speed_to_xyz_vector_south():
    assert heading_and_speed_to_xyz_vector(180, 100) == [pytest.approx(0), 0, 100]


def test_heading_and_speed_to_xyz_vector_west():
    assert heading_and_speed_to_xyz_vector(270, 100) == [-100, 0, pytest.approx(0)]


def test_heading_and_speed_to_xyz_vector_nne():
    assert heading_and_speed_to_xyz_vector(60, 100) == [pytest.approx(86.6, 1), 0, pytest.approx(-50)]
