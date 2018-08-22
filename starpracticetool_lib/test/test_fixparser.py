import pytest

from starpracticetool_lib.fixparser import FixParser


@pytest.fixture()
def fixparser():
    return FixParser('earth_fix.dat')


def test_count(fixparser):
    assert 8 == len(fixparser.fixes)


def test_get_coord(fixparser):
    assert (0.0, 6.583333333) == fixparser.get_coord('72LV')


def test_name_beginning_with_is_ignored(fixparser):
    "If I look for SAM, I shouldn't get SAM27"
    assert 'SAM27' in fixparser.fixes  # First make sure SAM27 is actually there
    assert fixparser.get_coord('SAM') is None
