#! /usr/bin/env python3

"""
Philipp Biedenkopf - 2021

Example to show the use of the build-in benchmark functions.

"""

from sys import path
path.append('..\\heuristic_optimization')

from heuristic_optimization import ContinuousProblem
import algorithms
import benchmarks


# define problem instance
problem = ContinuousProblem(objective=benchmarks.rosenbrock, initSol=[0 for i in range(5)], lb=-5.12, ub=5.12)

# define algorithm instance
pso = algorithms.pso(maxIter=200, topoType="lbest", neighb=3, popSize=24)

# minimize problem instance
pso.minimize(problem, verbose=True)
