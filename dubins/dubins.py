"""
Pure Python implementation of Dubins-Curves

Copyright (c) 2024 Rhys Mainwaring
"""

"""
Copyright (c) 2008-2018, Andrew Walker

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

from enum import Enum


class DubinsPathType(Enum):
    LSL = (0,)
    LSR = (1,)
    RSL = (2,)
    RSR = (3,)
    RLR = (4,)
    LRL = 5


class DubinsPath:
    def __init__(self):
        # the initial configuration
        self.qi = [0.0] * 3
        # the lengths of the three segments
        self.param = [0.0] * 3
        # model forward velocity / model angular velocity
        self.rho = 0.0
        # the path type described
        self.type = DubinsPathType


EDUBOK = 0  # No error
EDUBCOCONFIGS = 1  # Colocated configurations
EDUBPARAM = 2  # Path parameterisitation error
EDUBBADRHO = 3  # the rho value is invalid
EDUBNOPATH = 4  # no connection between configurations with this word

"""
Callback function for path sampling

@note the q parameter is a configuration
@note the t parameter is the distance along the path
@note the user_data parameter is forwarded from the caller
@note return non-zero to denote sampling should be stopped
"""
def DubinsPathSamplingCallback(q, t, user_data):
    return 0


"""
Generate a path from an initial configuration to
a target configuration, with a specified maximum turning
radii

A configuration is (x, y, theta), where theta is in radians, with zero
along the line x = 0, and counter-clockwise is positive

@param path  - the resultant path
@param q0    - a configuration specified as an array of x, y, theta
@param q1    - a configuration specified as an array of x, y, theta
@param rho   - turning radius of the vehicle (forward velocity divided by maximum angular velocity)
@return      - non-zero on error
"""
def dubins_shortest_path(path, q0, q1, rho):
    return 0

"""
 Generate a path with a specified word from an initial configuration to
 a target configuration, with a specified turning radius 

@param path     - the resultant path
@param q0       - a configuration specified as an array of x, y, theta
@param q1       - a configuration specified as an array of x, y, theta
@param rho      - turning radius of the vehicle (forward velocity divided by maximum angular velocity)
@param pathType - the specific path type to use
@return         - non-zero on error
"""
def dubins_path(path, q0, q1, rho, pathType):
    return 0

"""
Calculate the length of an initialised path

@param path - the path to find the length of
"""
def dubins_path_length(path):
    return 0.0

"""
Return the length of a specific segment in an initialized path

@param path - the path to find the length of
@param i    - the segment you to get the length of (0-2)
"""
def dubins_segment_length(path, i):
    return 0.0

"""
Return the normalized length of a specific segment in an initialized path

@param path - the path to find the length of
@param i    - the segment you to get the length of (0-2)
"""
def dubins_segment_length_normalized(path, i );
    return 0.0

"""
Extract an integer that represents which path type was used

@param path    - an initialised path
@return        - one of LSL, LSR, RSL, RSR, RLR or LRL 
"""
def dubins_path_type(path):
    return DubinsPathType.LSL

"""
Calculate the configuration along the path, using the parameter t

@param path - an initialised path
@param t    - a length measure, where 0 <= t < dubins_path_length(path)
@param q    - the configuration result
@returns    - non-zero if 't' is not in the correct range
"""
def dubins_path_sample(path, t, q):
    return 0

"""
Walk along the path at a fixed sampling interval, calling the
callback function at each interval

The sampling process continues until the whole path is sampled, or the callback returns a non-zero value

@param path      - the path to sample
@param stepSize  - the distance along the path for subsequent samples
@param cb        - the callback function to call for each sample
@param user_data - optional information to pass on to the callback

@returns - zero on successful completion, or the result of the callback
"""
def dubins_path_sample_many(path, stepSize, cb, user_data):
    return 0

"""
Convenience function to identify the endpoint of a path
 
 @param path - an initialised path
 @param q    - the configuration result
 """
def dubins_path_endpoint(path, q):
    return 0

"""
Convenience function to extract a subset of a path

@param path    - an initialised path
@param t       - a length measure, where 0 < t < dubins_path_length(path)
@param newpath - the resultant path
"""
def dubins_extract_subpath(path, t, newpath):
    return 0

