import pytest

from starpracticetool_lib.fixparser import FixParser

@pytest.fixture()
def fixparser():
    return FixParser('earth_fix.dat')

def test_count(fixparser):
    assert 7 == len(fixparser.fixes)


def test_get_coord(fixparser):
    assert (0.0, 6.583333333) == fixparser.get_coord('72LV')
