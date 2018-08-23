import os

import pytest

from starpracticetool_lib import paths


def mock_file_exists(monkeypatch, default_file_path, custom_file_path, custom_exists):
    def mock_exists(path):
        if path == default_file_path:
            return True
        elif path == custom_file_path:
            return custom_exists
        return False

    monkeypatch.setattr(os.path, 'exists', mock_exists)


XPLANE_PATH = 'xplanepath/'
AIRPORT_ICAO = 'LEBB'

CUSTOM_PATH = os.path.join(XPLANE_PATH, "Custom Data")
DEFAULT_PATH = os.path.join(XPLANE_PATH, "Resources", "default data")

CUSTOM_APT_PATH = os.path.join(CUSTOM_PATH, "CIFP", "LEBB.dat")
DEFAULT_APT_PATH = os.path.join(DEFAULT_PATH, "CIFP", "LEBB.dat")

DEFAULT_EARTH_FIX = os.path.join(DEFAULT_PATH, "earth_fix.dat")
CUSTOM_EARTH_FIX = os.path.join(CUSTOM_PATH, "earth_fix.dat")
DEFAULT_EARTH_NAV = os.path.join(DEFAULT_PATH, "earth_nav.dat")
CUSTOM_EARTH_NAV = os.path.join(CUSTOM_PATH, "earth_nav.dat")


def test_custom_airport_file_is_prioritised(monkeypatch):
    mock_file_exists(monkeypatch, DEFAULT_APT_PATH, CUSTOM_APT_PATH, custom_exists=True)
    assert paths.get_airport_file_path(XPLANE_PATH, AIRPORT_ICAO) == CUSTOM_APT_PATH


def test_default_airport_file_is_used(monkeypatch):
    mock_file_exists(monkeypatch, DEFAULT_APT_PATH, CUSTOM_APT_PATH, custom_exists=False)
    assert paths.get_airport_file_path(XPLANE_PATH, AIRPORT_ICAO) == DEFAULT_APT_PATH


def test_custom_earth_fix_dat_file_is_prioritised(monkeypatch):
    mock_file_exists(monkeypatch, DEFAULT_EARTH_FIX, CUSTOM_EARTH_FIX, custom_exists=True)
    assert paths.get_earth_fix_dat_file_path(XPLANE_PATH) == CUSTOM_EARTH_FIX


def test_default_earth_fix_dat_file_is_used(monkeypatch):
    mock_file_exists(monkeypatch, DEFAULT_EARTH_FIX, CUSTOM_EARTH_FIX, custom_exists=False)
    assert paths.get_earth_fix_dat_file_path(XPLANE_PATH) == DEFAULT_EARTH_FIX


def test_custom_earth_nav_dat_file_is_prioritised(monkeypatch):
    mock_file_exists(monkeypatch, DEFAULT_EARTH_NAV, CUSTOM_EARTH_NAV, custom_exists=True)
    assert paths.get_earth_nav_dat_file_path(XPLANE_PATH) == CUSTOM_EARTH_NAV


def test_default_earth_nav_dat_file_is_used(monkeypatch):
    mock_file_exists(monkeypatch, DEFAULT_EARTH_NAV, CUSTOM_EARTH_NAV, custom_exists=False)
    assert paths.get_earth_nav_dat_file_path(XPLANE_PATH) == DEFAULT_EARTH_NAV
