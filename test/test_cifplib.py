import os
import pytest

from cifplib import Cifp, _get_file_path


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


def mock_file_exists(monkeypatch, custom_file_path, default_file_path, custom_exists):
    def mock_exists(path):
        if path == custom_file_path:
            return custom_exists
        if path == default_file_path:
            return True
        return False

    monkeypatch.setattr(os.path, 'exists', mock_exists)


def test_custom_data_folder_is_prioritised(monkeypatch, xplane_path, custom_file_path, default_file_path, airport_icao):
    mock_file_exists(monkeypatch, custom_file_path, default_file_path, True)
    assert _get_file_path(xplane_path, airport_icao) == custom_file_path


def test_default_data_is_used(monkeypatch, xplane_path, custom_file_path, default_file_path, airport_icao):
    mock_file_exists(monkeypatch, custom_file_path, default_file_path, False)
    assert _get_file_path(xplane_path, airport_icao) == default_file_path


@pytest.fixture()
def cifp():
    return Cifp(file_path='LEBB.dat')


def test_there_are_437_lines(cifp):
    assert len(cifp.raw_lines) == 437


def test_get_star_names(cifp):
    assert cifp.star_names == set(['CEGA1K', 'CEGA1Q', 'CEGA2T', 'DGO1L', 'DGO1Q', 'DGO1T', 'DGO1Z', 'DGO2X', 'DOSU1T',
                               'DOSU1Z', 'DOSU2K', 'DOSU2Q', 'MAPA1K', 'MAPA1Q', 'MAPA1T', 'MAPA1Z', 'SNR2K', 'SNR2Q',
                               'SNR2T', 'SNR2Z'])
