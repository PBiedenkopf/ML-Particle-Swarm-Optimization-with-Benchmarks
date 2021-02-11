#! /usr/bin/env python3

"""
Philipp Biedenkopf - 2021

N-dimensional implementation of the rosenbrock function.

Characteristics:
    - continuous
    - convex
    - differentiable
    - unimodal
    
Typical domain:
    Hypercube x_i ∈ [-5.1, 5.1] for all design variables
    
Global minimum:
    f(x) = 0 at (1, 1, ..., 1)
    
For more information refer to:
http://benchmarkfcns.xyz/benchmarkfcns/rosenbrockfcn.html
    
"""

def rosenbrock(x):
    f = 0
    for i in range(len(x)-1):
        f += 100 * (x[i]*x[i] -x[i+1])*(x[i]*x[i] -x[i+1]) + (x[i]-1)*(x[i]-1)
    return f

