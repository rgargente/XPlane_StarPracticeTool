import pytest

from starpracticetool_lib.fixparser import FixParser
from starpracticetool_lib.navparser import NavParser
from starpracticetool_lib.waypointsreader import WaypointsReader



def test_unique_name_nav(waypoints_reader):
    assert (37.916666667, 23.914166667) == waypoints_reader.get_latlon('SAT', 1.0, 1.0)


def test_unique_name_fix(waypoints_reader):
    assert (-10.021666667, 25.415000000) == waypoints_reader.get_latlon('55LUB', 1.0, 1.0)
    assert (51.330925000, -0.969747222) == waypoints_reader.get_latlon('SAM27', 1.0, 1.0)


def test_repeated_name_only_nav(waypoints_reader):
    assert (50.955250000, -1.345055556) == waypoints_reader.get_latlon('SAM', 49.0, 1.0)
    assert (37.686625000, 26.907077778) == waypoints_reader.get_latlon('SAM', 33.0, 24.0)


def test_repeated_name_only_fix(waypoints_reader):
    assert (34.829444444, 10.959444444) == waypoints_reader.get_latlon('ABATI', 30.0, 1.0)
    assert (10.829444444, -10.959444444) == waypoints_reader.get_latlon('ABATI', 11.0, -1.0)


def test_repeated_name_nav_and_fix(waypoints_reader):
    assert (29.397500000, 30.393055556) == waypoints_reader.get_latlon('FYM', 30.0, 30.0)
    assert (0.325000000, 22.625000000) == waypoints_reader.get_latlon('FYM', 0.0, 25.0)
