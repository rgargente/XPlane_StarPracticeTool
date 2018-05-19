import pytest

from starpracticetool_lib.fixparser import FixParser


@pytest.fixture()
def fixparser():
    return FixParser('earth_fix.dat')


def test_count_fixes(fixparser):
    assert 8 == len(fixparser.fixes)


def test_latlon_by_name(fixparser):
    assert (0.000000000, 6.583333333) == fixparser.get_latlon_by_name('72LV')
