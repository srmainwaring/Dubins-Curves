"""
Tests for the Python implementation of Dubins curves.
"""

import math
import pytest
from pytest import approx

from dubins import DubinsPathType
from dubins import EDUBOK, EDUBBADRHO, EDUBNOPATH, EDUBPARAM
from dubins import dubins_path
from dubins import dubins_shortest_path
from dubins import dubins_path_length
from dubins import dubins_segment_length
from dubins import dubins_segment_length_normalized
from dubins import dubins_path_sample
from dubins import dubins_path_sample_many
from dubins import dubins_path_type
from dubins import dubins_path_endpoint
from dubins import dubins_extract_subpath


def print_path(path):
    print("qi:      {}".format(path.qi))
    print("param:   {}".format(path.param))
    print("rho:     {}".format(path.rho))
    print("type:    {}".format(path.type))


class DubinsConfig:
    def __init__(self):
        self.q0 = [0.0] * 3
        self.q1 = [0.0] * 3
        self.turning_radius = 0.0

    def setup(self):
        self.turning_radius = 1.0
        self.configure_inputs(0.0, 0.0, 1.0)

    def configure_inputs(self, a, b, d):
        self.q0[0] = 0.0
        self.q0[1] = 0.0
        self.q0[2] = a
        self.q1[0] = d
        self.q1[1] = 0.0
        self.q1[2] = b


@pytest.fixture
def dubins_config():
    config = DubinsConfig()
    config.setup()
    return config


def test_shortest_path(dubins_config):
    q0 = dubins_config.q0
    q1 = dubins_config.q1
    turning_radius = dubins_config.turning_radius

    # find the shortest path
    err, path = dubins_shortest_path(q0, q1, turning_radius)
    assert err == EDUBOK


def test_invalid_turning_radius(dubins_config):
    q0 = dubins_config.q0
    q1 = dubins_config.q1

    # find the shortest path
    err, path = dubins_shortest_path(q0, q1, -1.0)
    assert err == EDUBBADRHO


def test_no_path(dubins_config):
    dubins_config.configure_inputs(0.0, 0.0, 10.0)
    q0 = dubins_config.q0
    q1 = dubins_config.q1
    turning_radius = dubins_config.turning_radius

    # find the path
    err, path = dubins_path(q0, q1, turning_radius, DubinsPathType.LRL)
    assert err == EDUBNOPATH


def test_path_length(dubins_config):
    dubins_config.configure_inputs(0.0, 0.0, 4.0)
    q0 = dubins_config.q0
    q1 = dubins_config.q1
    turning_radius = dubins_config.turning_radius

    # find the shortest path
    err, path = dubins_shortest_path(q0, q1, turning_radius)
    res = dubins_path_length(path)
    assert res == 4.0


def test_simple_path(dubins_config):
    q0 = dubins_config.q0
    q1 = dubins_config.q1
    turning_radius = dubins_config.turning_radius

    # find the shortest path
    err, path = dubins_path(q0, q1, turning_radius, DubinsPathType.LSL)
    assert err == EDUBOK


def test_segment_lengths(dubins_config):
    dubins_config.configure_inputs(0.0, 0.0, 4.0)
    q0 = dubins_config.q0
    q1 = dubins_config.q1
    turning_radius = dubins_config.turning_radius

    # find the parameters for a single Dubins word
    err, path = dubins_path(q0, q1, turning_radius, DubinsPathType.LSL)
    assert err == EDUBOK
    assert dubins_segment_length(path, -1) == math.inf
    assert dubins_segment_length(path, 0) == 0.0
    assert dubins_segment_length(path, 1) == 4.0
    assert dubins_segment_length(path, 2) == 0.0
    assert dubins_segment_length(path, 3) == math.inf


def test_segment_length_normalized(dubins_config):
    dubins_config.configure_inputs(0.0, 0.0, 4.0)
    q0 = dubins_config.q0
    q1 = dubins_config.q1
    turning_radius = dubins_config.turning_radius

    # find the parameters for a single Dubins word
    err, path = dubins_path(q0, q1, turning_radius, DubinsPathType.LSL)
    assert err == EDUBOK
    assert dubins_segment_length_normalized(path, -1) == math.inf
    assert dubins_segment_length_normalized(path, 0) == 0.0
    assert dubins_segment_length_normalized(path, 1) == 4.0
    assert dubins_segment_length_normalized(path, 2) == 0.0
    assert dubins_segment_length_normalized(path, 3) == math.inf


def test_sample(dubins_config):
    dubins_config.configure_inputs(0.0, 0.0, 4.0)
    q0 = dubins_config.q0
    q1 = dubins_config.q1
    turning_radius = dubins_config.turning_radius

    # find the parameters for a single Dubins word
    err, path = dubins_path(q0, q1, turning_radius, DubinsPathType.LSL)
    assert err == EDUBOK

    err, qsamp = dubins_path_sample(path, 0.0)
    assert err == EDUBOK
    assert qsamp[0] == q0[0]
    assert qsamp[1] == q0[1]
    assert qsamp[2] == q0[2]

    err, qsamp = dubins_path_sample(path, 4.0)
    assert err == EDUBOK
    assert qsamp[0] == q1[0]
    assert qsamp[1] == q1[1]
    assert qsamp[2] == q1[2]


def test_sample_out_of_bounds(dubins_config):
    dubins_config.configure_inputs(0.0, 0.0, 4.0)
    q0 = dubins_config.q0
    q1 = dubins_config.q1
    turning_radius = dubins_config.turning_radius

    # find the parameters for a single Dubins word
    err, path = dubins_path(q0, q1, turning_radius, DubinsPathType.LSL)
    assert err == EDUBOK

    err, qsamp = dubins_path_sample(path, -1.0)
    assert err == EDUBPARAM

    err, qsamp = dubins_path_sample(path, 5.0)
    assert err == EDUBPARAM


class CallBackData:
    def __init__(self):
        self.value = 0


# int out_out_early_callback(double q[3], double t, void* data)
def out_out_early_callback(q, t, data):
    if data.value > 2:
        return 1

    data.value += 1
    return EDUBOK


def test_sample_many_opt_out_early(dubins_config):
    dubins_config.configure_inputs(0.0, 0.0, 4.0)
    q0 = dubins_config.q0
    q1 = dubins_config.q1
    turning_radius = dubins_config.turning_radius

    # find the parameters for a single Dubins word
    err, path = dubins_path(q0, q1, turning_radius, DubinsPathType.LSL)
    assert err == EDUBOK

    count = 0
    data = CallBackData()
    data.value = count
    err = dubins_path_sample_many(path, 1.0, out_out_early_callback, data)
    count = data.value
    assert err, 1
    assert count, 3


def test_path_type(dubins_config):
    q0 = dubins_config.q0
    q1 = dubins_config.q1
    turning_radius = dubins_config.turning_radius

    for i in range(6):
        t = DubinsPathType(i)
        # find the parameters for a single Dubins word
        err, path = dubins_path(q0, q1, turning_radius, t)
        if err == EDUBOK:
            assert t == dubins_path_type(path)


def test_end_point(dubins_config):
    dubins_config.configure_inputs(0.0, 0.0, 4.0)
    q0 = dubins_config.q0
    q1 = dubins_config.q1
    turning_radius = dubins_config.turning_radius

    # find the parameters for a single Dubins word
    err, path = dubins_path(q0, q1, turning_radius, DubinsPathType.LSL)
    assert err == EDUBOK

    err, qsamp = dubins_path_endpoint(path)
    assert err == EDUBOK
    assert qsamp[0] == approx(q1[0])
    assert qsamp[1] == approx(q1[1])
    assert qsamp[2] == approx(q1[2])


def test_extract_subpath(dubins_config):
    dubins_config.configure_inputs(0.0, 0.0, 4.0)
    q0 = dubins_config.q0
    q1 = dubins_config.q1
    turning_radius = dubins_config.turning_radius

    # find the parameters for a single Dubins word
    err, path = dubins_path(q0, q1, turning_radius, DubinsPathType.LSL)
    assert err == EDUBOK

    err, subpath = dubins_extract_subpath(path, 2.0)
    assert err == EDUBOK

    err, qsamp = dubins_path_endpoint(subpath)
    assert err == EDUBOK
    assert qsamp[0] == approx(2.0)
    assert qsamp[1] == approx(0.0)
    assert qsamp[2] == approx(0.0)


def test_extract_invalid_subpath(dubins_config):
    dubins_config.configure_inputs(0.0, 0.0, 4.0)
    q0 = dubins_config.q0
    q1 = dubins_config.q1
    turning_radius = dubins_config.turning_radius

    # find the parameters for a single Dubins word
    err, path = dubins_path(q0, q1, turning_radius, DubinsPathType.LSL)
    assert err == EDUBOK

    err, subpath = dubins_extract_subpath(path, 8.0)
    assert err != EDUBOK


# if __name__ == "__main__":
#     dubins_config = DubinsConfig()
#     dubins_config.setup()
#     test_path_type(dubins_config)
