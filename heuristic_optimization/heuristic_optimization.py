#! /usr/bin/env python3

""" 
Philipp Biedenkopf - 2021

A lightweight optimization library for metaheuristic algorithms.

Implemented optimization algorithms:
    - Particle swarm optimization (pso)
    
Implemented benchmark functions:
    - Auckley (N-dimensional)
    - Rosenbrock (N-dimensional)
    - Rastrigin (N-dimensional)
    - Schwefel (N-dimensional)
    - Sphere (N-dimensional)
    
Implemented parallelisation methods:
    - multithreading
    - multiprocessing (not recommended because implementation is inefficient)
    
Follow on Github:
    

"""

import matplotlib.pyplot as plt
import numpy as np
from utility import ProblemException


class Problem:
    def __init__(self, objective=None, initSol=None):
        self.objective = objective
        
        self.bestFit = np.inf
        self.bestSol = []
        
        if initSol == None:
            self.initSol = []
        else:
            self.initSol = initSol
        
        self.fitHist =[]
        self.solHist = []
        
    def addToHist(self, fit, sol):
        """ Adds a solution to the convergence history """
        self.solHist.append(sol)
        self.fitHist.append(fit) 
        
    def plotConvergence(self, algorithm):
        """ Plots the convergence history of the optimization run. """
        plt.figure(2)
        plt.plot([i for i in range(len(self.fitHist))], self.fitHist, label=algorithm.name)
        plt.title(self.objective.__name__+" ("+str(len(self.initSol))+" dimensional)")
        plt.xlabel("generations")
        plt.ylabel("fitness")
        plt.legend()
        plt.grid(True)



class ContinuousProblem(Problem):
    """ 
    Class to define an arbitrary continuous optimization problem. 
    
    May be used for included benchmarks or 
    user-defined problems. The initial position is needed to compute the dimension of the
    problem and is not used by the metaheuristic optimization algorithms as a start position.
    
    """
    
    def __init__(self, objective=None, initSol=None, lb=None, ub=None, constraints=None, constTol=1E-6):
        super().__init__(objective, initSol)
        
        # constraints are not supported yet
        self.constraints = constraints 
        self.constTol = constTol
        
        if lb == None:
            self.lb = [-np.inf for dim in range(len(initSol))]
        elif (type(lb)==int or type(lb)==float):
            self.lb = [lb for i in range(len(initSol))]
        else:
            self.lb=lb
        
        if ub == None:
            self.ub = [np.inf for dim in range(len(initSol))]
        elif (type(ub)==int or type(ub)==float):
            self.ub = [ub for i in range(len(initSol))]
        else:
            self.ub=ub
            
            
    def check(self):
        """ Performs some plausibility checks of the problem instance. """
        try:
            assert len(self.lb) == len(self.ub) == len(self.initSol)
        except AssertionError:
            raise ProblemException("Length of start value and boundaries does not match!")
            
        try:
            assert np.all(np.array(self.ub) > np.array(self.lb))
        except AssertionError:
            raise ProblemException("All upper boundaries have to be greater than the lowers!")
            
        try:
            assert callable(self.objective)
        except AssertionError:
            raise ProblemException("Invalid objective function!")
            


class Algorithm:
    """ 
    superclass for all optimization algorithms. 
    
    """
    def __init__(self, name, popSize=25, maxIter=500, parallelization=None):
        self.parallelization = parallelization
        self.name = name
        self.popSize = popSize
        self.maxIter = maxIter
        
    def __str__(self):
        return self.name
    
    
class Population:
    """ 
    Represents general population of arbitrary individuals 
    
    """
    def __init__(self, index=0):
        self.index = index
        self.bestFit = np.inf
        self.bestSol = []
    