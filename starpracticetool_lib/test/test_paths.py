import os

import pytest

from starpracticetool_lib import paths


def mock_file_exists(monkeypatch, custom_file_path, default_file_path, custom_exists):
    def mock_exists(path):
        if path == custom_file_path:
            return custom_exists
        if path == default_file_path:
            return True
        return False

    monkeypatch.setattr(os.path, 'exists', mock_exists)


@pytest.fixture()
def xplane_path():
    return 'xplanepath/'


@pytest.fixture()
def airport_icao():
    return 'LEBB'


@pytest.fixture()
def custom_file_path(xplane_path):
    return os.path.join(xplane_path, "Custom Data", "CIFP", "LEBB.dat")


@pytest.fixture()
def default_file_path(xplane_path):
    return os.path.join(xplane_path, "Resources", "default data", "CIFP", "LEBB.dat")


def test_custom_data_folder_is_prioritised(monkeypatch, xplane_path, custom_file_path, default_file_path, airport_icao):
    mock_file_exists(monkeypatch, custom_file_path, default_file_path, True)
    assert paths.get_airport_file_path(xplane_path, airport_icao) == custom_file_path


def test_default_data_is_used(monkeypatch, xplane_path, custom_file_path, default_file_path, airport_icao):
    mock_file_exists(monkeypatch, custom_file_path, default_file_path, False)
    assert paths.get_airport_file_path(xplane_path, airport_icao) == default_file_path
