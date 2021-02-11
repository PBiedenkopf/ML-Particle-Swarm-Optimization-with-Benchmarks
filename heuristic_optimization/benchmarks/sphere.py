#! /usr/bin/env python3

"""
Philipp Biedenkopf - 2021

N-dimensional implementation of the sphere function.

Characteristics:
    - continuous
    - convex
    - unimodal
    - differentiable
    
Typical domain:
    Hypercube x_i ∈ [-5.12, 5.12] for all design variables
    
Global minimum:
    f(x) = 0 at (0,0, ..., 0)
    
"""



def sphere(x):
    total = 0
    for i in range(len(x)):
        total += x[i]**2
    return total
