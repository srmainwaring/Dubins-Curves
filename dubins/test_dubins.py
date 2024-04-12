"""
Tests for the Python implementation of Dubins curves.
"""

# from dubins import DubinsPath
from dubins import dubins_shortest_path
from dubins import EDUBOK, EDUBBADRHO

# test globals
q0 = [0.0] * 3
q1 = [0.0] * 3
turning_radius = 0.0


def configure_inputs(a, b, d):
    global q0
    global q1
    q0[0] = 0.0
    q0[1] = 0.0
    q0[2] = a
    q1[0] = d
    q1[1] = 0.0
    q1[2] = b


def setup():
    global turning_radius
    turning_radius = 1.0
    configure_inputs(0.0, 0.0, 1.0)


def print_path(path):
    print("qi:      {}".format(path.qi))
    print("param:   {}".format(path.param))
    print("rho:     {}".format(path.rho))
    print("type:    {}".format(path.type))


def test_shortest_path():
    global q0
    global q1
    global turning_radius
    setup()

    err, path = dubins_shortest_path(q0, q1, turning_radius)
    if err != EDUBOK:
        print("test_shortest_path: FAIL")
    else:
        print("test_shortest_path: PASS")
        # print_path(path)


def test_invalid_turning_radius():
    global q0
    global q1
    global turning_radius
    setup()

    err, path = dubins_shortest_path(q0, q1, -1.0)
    if err != EDUBBADRHO:
        print("test_invalid_turning_radius: FAIL")
    else:
        print("test_invalid_turning_radius: PASS")



def main():
    test_shortest_path()
    test_invalid_turning_radius()


if __name__ == "__main__":
    main()
