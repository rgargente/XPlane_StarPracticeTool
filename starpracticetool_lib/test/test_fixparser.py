def test_count(fixparser):
    assert 9 == len(fixparser.waypoints)


def test_get_coord(fixparser):
    assert [(0.0, 6.583333333)] == fixparser.get_latlon('72LV')


def test_name_beginning_with_is_ignored(fixparser):
    "If I look for SAM, I shouldn't get SAM27"
    assert len(fixparser.get_latlon('SAM27')) > 0  # First make sure SAM27 is actually there
    assert len(fixparser.get_latlon('SAM')) == 0


def test_duplicate_name(fixparser):
    waypoints = fixparser.get_latlon('ABATI')
    assert (34.829444444, 10.959444444) in waypoints
    assert (10.829444444, - 10.959444444) in waypoints
