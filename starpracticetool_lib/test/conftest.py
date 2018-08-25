import pytest

from starpracticetool_lib.fixparser import FixParser
from starpracticetool_lib.navparser import NavParser
from starpracticetool_lib.waypointsreader import WaypointsReader


@pytest.fixture()
def fixparser():
    return FixParser('testdata/general/earth_fix.dat')


@pytest.fixture()
def navparser():
    return NavParser('testdata/general/earth_nav.dat')


@pytest.fixture()
def waypoints_reader(fixparser, navparser):
    return WaypointsReader(None, fixparser, navparser)
