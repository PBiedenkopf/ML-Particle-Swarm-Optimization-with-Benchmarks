#! /usr/bin/env python3

"""
Philipp Biedenkopf - 2021

N-dimensional implementation of the rastrigin function.

Characteristics:
    - continuous
    - differentiable
    - multimodal
    
Typical domain:
    Hypercube x_i ∈ [-5.12, 5.12] for all design variables
    
Global minimum:
    f(x) = 0 at (0, 0, ..., 0)
    
For more information refer to:
http://benchmarkfcns.xyz/benchmarkfcns/rastriginfcn.html
    
"""

from numpy import cos, power, pi


def rastrigin(x):
    return (10 * len(x)) + (sum(power(x, 2) - 10 * cos(2 * pi * x)));
