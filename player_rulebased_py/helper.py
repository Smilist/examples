# File: helper.py
# Date: Jan. 23, 2018
# Description: Helper functions for the rule based algorithm example in Python
# Author(s): Luiz Felipe Vecchietti, Chansol Hong, Inbae Jeong
# Current Developer: Chansol Hong (cshong@rit.kaist.ac.kr)

import math

def distance(x1, x2, y1, y2):
    return math.sqrt(math.pow(x1 - x2, 2) + math.pow(y1 - y2, 2))

def degree2radian(deg):
    return deg * math.pi / 180

def radian2degree(rad):
    return rad * 180 / math.pi
