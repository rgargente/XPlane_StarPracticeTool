"""
X Plane STAR Practice Tool Python plugin
Copyright (C) 2018 Rafael Garcia Argente
https://github.com/rgargente/XPlaneStarPracticeTool

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import os

import pytest

from starpracticetool_lib.cifplib import _get_file_path, Cifp
from starpracticetool_lib.test.mock_xplm_wrapper import MockXplmWrapper


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
    return Cifp(MockXplmWrapper(), 'LEBB', file_path='LEBB.dat')


def test_there_are_437_lines(cifp):
    assert len(cifp.raw_lines) == 437


def test_get_star_names(cifp):
    assert cifp.star_names == ['CEGA1K', 'CEGA1Q', 'CEGA2T', 'DGO1L', 'DGO1Q', 'DGO1T', 'DGO1Z', 'DGO2X', 'DOSU1T',
                               'DOSU1Z', 'DOSU2K', 'DOSU2Q', 'MAPA1K', 'MAPA1Q', 'MAPA1T', 'MAPA1Z', 'SNR2K',
                               'SNR2Q', 'SNR2T', 'SNR2Z']


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
    assert dgo2x.init_lat == 42.453305556
    assert dgo2x.init_lon == -2.880694444
    assert dgo2x.init_heading == pytest.approx(003, 1)


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
    assert mapa1k.init_lat == 43.683750000
    assert mapa1k.init_lon == -3.044083333
    assert mapa1k.init_heading == pytest.approx(169, 1)


def test_get_prev_star(cifp):
    assert cifp.get_prev_star('CEGA1K') == 'SNR2Z'
    assert cifp.get_prev_star('CEGA1Q') == 'CEGA1K'
    assert cifp.get_prev_star('SNR2Z') == 'SNR2T'


def test_get_next_star(cifp):
    assert cifp.get_next_star('CEGA1K') == 'CEGA1Q'
    assert cifp.get_next_star('CEGA1Q') == 'CEGA2T'
    assert cifp.get_next_star('SNR2Z') == 'CEGA1K'


def test_non_existing_airport():
    with pytest.raises(Exception) as e:
        Cifp(MockXplmWrapper(), 'garbage')
    assert "Airport not found" == e.value.message
