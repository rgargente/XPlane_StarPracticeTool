import pytest

from starpracticetool_lib.mathlib import heading_and_speed_to_xyz_vector


def test_heading_and_speed_to_xyz_vector_north():
    assert heading_and_speed_to_xyz_vector(0, 100) == [pytest.approx(0), 0, -100]


def test_heading_and_speed_to_xyz_vector_east():
    assert heading_and_speed_to_xyz_vector(90, 100) == [100, 0, pytest.approx(0)]


def test_heading_and_speed_to_xyz_vector_south():
    assert heading_and_speed_to_xyz_vector(180, 100) == [pytest.approx(0), 0, 100]


def test_heading_and_speed_to_xyz_vector_west():
    assert heading_and_speed_to_xyz_vector(270, 100) == [-100, 0, pytest.approx(0)]


def test_heading_and_speed_to_xyz_vector_nne():
    assert heading_and_speed_to_xyz_vector(60, 100) == [pytest.approx(86.6, 1), 0, pytest.approx(-50)]
