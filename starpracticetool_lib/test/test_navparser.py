def test_stations_count(navparser):
    assert 6 == len(navparser.waypoints)


def test_station_not_duplicated(navparser):
    """There should be only one SAL"""
    latlons = navparser.get_latlon('SAL')
    assert 1 == len(latlons)
    assert (43.611833333, 5.102805556) in latlons


def test_station_by_name_several_results(navparser):
    latlons = navparser.get_latlon('SAM')
    assert 2 == len(latlons)
    assert (50.955250000, -1.345055556) in latlons
    assert (37.686625000, 26.907077778) in latlons


def test_name_beginning_with_is_ignored(navparser):
    "If I look for FY, I shouldn't get FYM"
    # First make sure FYM is actually there
    assert [(29.397500000, 30.393055556)] == navparser.get_latlon('FYM')
    assert [(17.930833333, 19.134166667)] == navparser.get_latlon('FY')
