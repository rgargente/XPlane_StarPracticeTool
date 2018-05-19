import pytest

from starpracticetool_lib.navparser import NavParser


@pytest.fixture
def navparser():
    return NavParser('earth_nav.dat')


def test_stations_count(navparser):
    assert 4 == len(navparser.stations)


def test_station_not_duplicated(navparser):
    """There should be only one SAL"""
    latlons = navparser.get_station_latlon_by_name('SAL')
    assert 1 == len(latlons)
    assert (43.611833333, 5.102805556) in latlons


def test_station_by_name_several_results(navparser):
    latlons = navparser.get_station_latlon_by_name('SAM')
    assert 2 == len(latlons)
    assert (50.955250000, -1.345055556) in latlons
    assert (37.686625000, 26.907077778) in latlons
