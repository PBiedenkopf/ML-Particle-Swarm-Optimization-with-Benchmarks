#! /usr/bin/env python3

"""
Philipp Biedenkopf - 2021

N-dimensional implementation of the schwefel function.

Characteristics:
    - continuous
    - non-convex
    - multimodal
    
Typical domain:
    Hypercube x_i ∈ [-500, 500] for all design variables
    
Global minimum:
    f(x) = 0 at (420.9687, 420.9687, ..., 420.9687)
    
For more information refer to:
http://benchmarkfcns.xyz/benchmarkfcns/schwefelfcn.html
    
"""


import numpy as np


def schwefel(x):
    return 418.982887 * len(x) - np.sum(np.dot(x, np.sin(np.sqrt(np.abs(x)))));
