#! /usr/bin/env python3


"""
Philipp Biedenkopf - 2021

N-dimensional implementation of the auckley function.

Characteristics:
    - continuous
    - convex
    - multimodal
    
Typical domain:
    Hypercube: x_i ∈ [-32, 32] for all design variables
    
Global minimum:
    f(x) = 0 at (0,0, ..., 0)
    
For more inforamtion refer to: 
http://benchmarkfcns.xyz/benchmarkfcns/ackleyfcn.html
    
"""

import math

def auckley(x):
	""""""
	sum1 = 0
	sum2 = 0
	for i in x:
		sum1 += i**2.0
		sum2 += math.cos(2.0*math.pi*i)
	return -20*math.exp(-0.2*math.sqrt(sum1/len(x))) - math.exp(sum2/len(x)) + 20 + math.e
    