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
                                   'DOSU1Z', 'DOSU2K', 'DOSU2Q', 'MAPA1K', 'MAPA1Q', 'MAPA1T', 'MAPA1Z', 'SNR2K',
                                   'SNR2Q', 'SNR2T', 'SNR2Z'])


def test_star_beginning_with_two_named_waypoints(cifp):
    # DGO2X
    # STAR:010,2,DGO2X,RW12,DGO,LE,D, ,V   , ,   ,IF, , , , , ,      ,    ,    ,    ,    , ,     ,     ,     , ,   ,    ,   , , , , , , , , ;
    # STAR:020,2,DGO2X,RW12,VRA,LE,D, ,V   , ,   ,TF, , , , , ,      ,    ,    ,    ,    , ,     ,     ,     , ,   ,    ,   , , , , , , , , ;
    # STAR:030,2,DGO2X,RW12,D251O,LE,P,C,E   , ,   ,TF, , , , , ,      ,    ,    ,    ,    , ,     ,     ,     , ,   ,    ,   , , , , , , , , ;
    # STAR:040,2,DGO2X,RW12,SOMAN,LE,P,C,E C ,R,   ,AF, ,BLV,LE,D, ,      ,2790,0150,2510,    , ,     ,     ,     , ,   ,    ,   , , , , , , , , ;
    # STAR:045,2,DGO2X,RW12,D291O,LE,P,C,E   ,R,   ,AF, ,BLV,LE,D, ,      ,2910,0150,2790,    , ,     ,     ,     , ,   ,    ,   , , , , , , , , ;
    # STAR:050,2,DGO2X,RW12,KALDO,LE,P,C,E C ,R,   ,AF, ,BLV,LE,D, ,      ,3040,0150,2910,    , ,     ,     ,     , ,   ,    ,   , , , , , , , , ;
    # STAR:060,2,DGO2X,RW12,ROSTO,LE,P,C,EECH, ,   ,TF, , , , , ,      ,    ,    ,    ,    , ,     ,     ,     , ,   ,    ,   , , , , , , , , ;
    dgo2x = cifp.stars['DGO2X']
    assert dgo2x.waypoints == ['DGO', 'VRA', 'D251O', 'SOMAN', 'D291O', 'KALDO', 'ROSTO']
    # assert dgo2x.init_lat == 42.453305556
    # assert dgo2x.init_lon == -2.880694444
    # assert dgo2x.init_heading == 003


def test_star_with_course_intercept_as_second_waypoint(cifp):
    # MAPA1K
    # STAR:010, 2, MAPA1K, RW30, MAPAX, LE, E, A, E,, , IF,, , , , , , , , , , , , , , , , , , , , , , , , , ;
    # STAR:020, 2, MAPA1K, RW30,, , , , , , , CI,, , , , , , , , 1690,, , , , , , , , , , , , , , , , ;
    # STAR:030, 2, MAPA1K, RW30, D067V, LE, P, C, E, R,, AF,, BLV, LE, D,, , 0670, 0220, 3490,, , , , , , , , , , , , , , , , ;
    # STAR:040, 2, MAPA1K, RW30, D092V, LE, P, C, E, R,, AF,, BLV, LE, D,, , 0 920, 0220, 0670,, , , , , , , , , , , , , , , , ;
    # STAR:050, 2, MAPA1K, RW30, D111V, LE, P, C, E, R,, AF,, BLV, LE, D,, , 1110, 0220, 0, 920,, , , , , , , , , , , , , , , , ;
    # STAR:060, 2, MAPA1K, RW30, PAKKI, LE, P, C, EEC,, , TF,, , , , , , , , , , , , , , , , , , , , , , , , , ;
    mapa1k = cifp.stars['MAPA1K']
    assert mapa1k.waypoints == ['MAPAX', 'INTC', 'D067V', 'D092V', 'D111V', 'PAKKI']
    # assert mapa1k.init_lat == 43.683750000
    # assert mapa1k.init_lon == -3.044083333
    assert mapa1k.init_heading == 169
