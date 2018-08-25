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

import pytest

from starpracticetool_lib.cifplib import Cifp
from starpracticetool_lib.fixparser import FixParser
from starpracticetool_lib.navparser import NavParser
from starpracticetool_lib.test.mock_xplm_wrapper import MockXplmWrapper
from starpracticetool_lib.waypointsreader import WaypointsReader


@pytest.fixture()
def lebb():
    waypoints_reader = WaypointsReader(None, FixParser('testdata/lebb/earth_fix.dat'),
                                       NavParser('testdata/lebb/earth_nav.dat'))
    return Cifp(MockXplmWrapper(), 'LEBB', file_path='testdata/lebb/LEBB.dat', waypoints_reader=waypoints_reader)


@pytest.fixture()
def egll():
    waypoints_reader = WaypointsReader(None, FixParser('testdata/egll/earth_fix.dat'),
                                       NavParser('testdata/egll/earth_nav.dat'))
    return Cifp(MockXplmWrapper(), 'EGLL', file_path='testdata/egll/EGLL.dat', waypoints_reader=waypoints_reader)


def test_there_are_437_lines(lebb):
    assert len(lebb.raw_lines) == 437


def test_get_star_names(lebb):
    assert lebb.star_names == ['CEGA1K', 'CEGA1Q', 'CEGA2T', 'DGO1L', 'DGO1Q', 'DGO1T', 'DGO1Z', 'DGO2X', 'DOSU1T',
                               'DOSU1Z', 'DOSU2K', 'DOSU2Q', 'MAPA1K', 'MAPA1Q', 'MAPA1T', 'MAPA1Z', 'SNR2K',
                               'SNR2Q', 'SNR2T', 'SNR2Z']


def test_star_beginning_with_two_named_waypoints(lebb):
    # DGO2X
    # STAR:010,2,DGO2X,RW12,DGO,LE,D, ,V   , ,   ,IF, , , , , ,      ,    ,    ,    ,    , ,     ,     ,     , ,   ,    ,   , , , , , , , , ;
    # STAR:020,2,DGO2X,RW12,VRA,LE,D, ,V   , ,   ,TF, , , , , ,      ,    ,    ,    ,    , ,     ,     ,     , ,   ,    ,   , , , , , , , , ;
    # STAR:030,2,DGO2X,RW12,D251O,LE,P,C,E   , ,   ,TF, , , , , ,      ,    ,    ,    ,    , ,     ,     ,     , ,   ,    ,   , , , , , , , , ;
    # STAR:040,2,DGO2X,RW12,SOMAN,LE,P,C,E C ,R,   ,AF, ,BLV,LE,D, ,      ,2790,0150,2510,    , ,     ,     ,     , ,   ,    ,   , , , , , , , , ;
    # STAR:045,2,DGO2X,RW12,D291O,LE,P,C,E   ,R,   ,AF, ,BLV,LE,D, ,      ,2910,0150,2790,    , ,     ,     ,     , ,   ,    ,   , , , , , , , , ;
    # STAR:050,2,DGO2X,RW12,KALDO,LE,P,C,E C ,R,   ,AF, ,BLV,LE,D, ,      ,3040,0150,2910,    , ,     ,     ,     , ,   ,    ,   , , , , , , , , ;
    # STAR:060,2,DGO2X,RW12,ROSTO,LE,P,C,EECH, ,   ,TF, , , , , ,      ,    ,    ,    ,    , ,     ,     ,     , ,   ,    ,   , , , , , , , , ;
    dgo2x = lebb.stars['DGO2X']
    assert dgo2x.waypoints == ['DGO', 'VRA', 'D251O', 'SOMAN', 'D291O', 'KALDO', 'ROSTO']
    assert dgo2x.init_lat == 42.453416667
    assert dgo2x.init_lon == -2.880583333
    assert dgo2x.init_heading == pytest.approx(003, 1)


def test_star_with_course_intercept_as_second_waypoint(lebb):
    # MAPA1K
    # STAR:010, 2, MAPA1K, RW30, MAPAX, LE, E, A, E,, , IF,, , , , , , , , , , , , , , , , , , , , , , , , , ;
    # STAR:020, 2, MAPA1K, RW30,, , , , , , , CI,, , , , , , , , 1690,, , , , , , , , , , , , , , , , ;
    # STAR:030, 2, MAPA1K, RW30, D067V, LE, P, C, E, R,, AF,, BLV, LE, D,, , 0670, 0220, 3490,, , , , , , , , , , , , , , , , ;
    # STAR:040, 2, MAPA1K, RW30, D092V, LE, P, C, E, R,, AF,, BLV, LE, D,, , 0 920, 0220, 0670,, , , , , , , , , , , , , , , , ;
    # STAR:050, 2, MAPA1K, RW30, D111V, LE, P, C, E, R,, AF,, BLV, LE, D,, , 1110, 0220, 0, 920,, , , , , , , , , , , , , , , , ;
    # STAR:060, 2, MAPA1K, RW30, PAKKI, LE, P, C, EEC,, , TF,, , , , , , , , , , , , , , , , , , , , , , , , , ;
    mapa1k = lebb.stars['MAPA1K']
    assert mapa1k.waypoints == ['MAPAX', 'INTC', 'D067V', 'D092V', 'D111V', 'PAKKI']
    assert mapa1k.init_lat == 43.683750000
    assert mapa1k.init_lon == -3.044083333
    assert mapa1k.init_heading == pytest.approx(169, 1)


def test_get_prev_star(lebb):
    assert lebb.get_prev_star('CEGA1K') == 'SNR2Z'
    assert lebb.get_prev_star('CEGA1Q') == 'CEGA1K'
    assert lebb.get_prev_star('SNR2Z') == 'SNR2T'


def test_get_next_star(lebb):
    assert lebb.get_next_star('CEGA1K') == 'CEGA1Q'
    assert lebb.get_next_star('CEGA1Q') == 'CEGA2T'
    assert lebb.get_next_star('SNR2Z') == 'CEGA1K'


def test_non_existing_airport():
    with pytest.raises(Exception) as e:
        Cifp(MockXplmWrapper(), 'garbage')
    assert "Airport not found" == e.value.message


def test_matchingname_procedure(egll):
    """ There is a limitation in the XP API. If you ask for example for a navaid called SAM it will return all
    the navaids which names start with SAM without having the option to look for exactly that name.
    In this case it will return SAM27 and it's not possible to get SAM.
    This test should verify this is not a problem anymore. """
    tomo2c = egll.stars['TOMO2C']
    assert tomo2c.waypoints == ['SAM', 'HAZEL', 'FIMLI', 'TOMMO']
    assert tomo2c.init_lat == 50.955250000
    assert tomo2c.init_lon == -1.345055556
    assert tomo2c.init_heading == pytest.approx(78, 1)
