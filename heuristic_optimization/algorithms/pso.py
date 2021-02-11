#! /usr/bin/env python3

""" 
Philipp Biedenkopf - 2021

Flexible implementation of a particle swarm optimization algorithm
with inertia weight and different static neighborhood topology options.


Implemented topology types:
    - global best
    - local best (number of neghborhoods can be defined)
    

"""

import numpy as np
import random
import sys
from heuristic_optimization import Algorithm, Population
from utility import splitList, MinimizationException
import concurrent.futures 

try:
    import tqdm as tqdm
    useTqdm = True
except ImportError:
    useTqdm = False


class Particle:
    """ class to represent a particle in particle swarm optimization """
    def __init__(self, index, initSol, lb, ub, w, c1, c2):
        self.index = index
        self.lb = np.array(lb)
        self.ub = np.array(ub)
        self.w = w
        self.c1 = c1
        self.c2 = c2
        self.fitness = np.inf
        
        pos, vel = [], []
        for i in range(len(initSol)):
            pos.append(random.uniform(lb[i], ub[i]))
            vel.append(0.0) # initial velocity is zero
        self.pos = np.array(pos)
        self.vel = np.array(vel)
        
        self.indivBestFit = self.fitness
        self.indivbestSol = self.pos.copy()
        
        self.localBestFit = self.fitness
        self.localbestSol = self.pos.copy()
        
        
    def evaluate(self, costFun):
        self.fitness = costFun(self.pos)
        
        # check if current position is the individual best
        if self.fitness < self.indivBestFit:
            self.indivbestSol = self.pos.copy()
            self.indivBestFit = self.fitness


    def updatePosition(self):
        """ Updates the position of the particle by adding the velocity. """
        self.pos += self.vel
        
        # make sure that particle does not violate one of the bounds
        for i in range(len(self.pos)):
            if self.pos[i] > self.ub[i]:
                self.pos[i] = self.ub[i]
            if self.pos[i] < self.lb[i]:
                self.pos[i] = self.lb[i]
    
    def updateVelocity(self):
        """ Updates the velocity of the particle """
        # create vector with random numbers between [0 1]
        # rand1 = np.random.uniform(0,1,len(self.pos))
        # rand2 = np.random.uniform(0,1,len(self.pos)) 
        
        # create two single random numbers between [0 1]
        rand1 = random.random() 
        rand2 = random.random()
        
        self.vel = self.w*self.vel + self.c1*rand1*(self.indivbestSol-self.pos) + self.c2*rand2*(self.localbestSol-self.pos)
        
        
    def setFitness(self, fit):
        self.fitness = fit
        
        
    def __str__(self):
        return ("Particle " + str(self.index) + ": " + str(round(self.fitness, 3)) + ' [{:s}]'.format(', '.join(['{:.2f}'.format(x) for x in self.pos])))
        
    
class Topology(Population):
    """ class to represent a swarm topology in particle swarm optimization """
    def __init__(self, index=0, particles=None, centralParticle=None):
        super().__init__(index)
        self.centralParticle = centralParticle
        if particles == None:
            self.particles = []
        else:
            self.particles = particles
            
    def updateBestSolution(self, fit, pos):
        if fit < self.bestFit:
            self.bestFit = fit
            self.bestSol = pos.copy()
            
            for p in self.particles:
                p.localBestFit = fit
                p.localbestSol = pos.copy()


class pso(Algorithm):
    """ class to represent a flexible particle swarm optimization algorithm """
    
    def __init__(self, popSize=24, maxIter=400, parallelization=None, topoType="gbest", neighb=2 , inertia=0.72984, c1=1.49617, c2=1.49617):
        super().__init__("Particle Swarm Optimization", popSize, maxIter, parallelization)
        self.topoType = topoType
        self.neighb = neighb
        self.w=inertia
        self.c1=c1
        self.c2=c2
        self.topologies = []
                
    def getBestOfTopo(self, topo):
        """ returns fitness and position of the topology's best particle """
        
        # sort list for fitness value
        sortedParticles = sorted(topo.particles, key=lambda x: x.fitness)
        
        # updates the neightbourhoods best value IF it is an improovement
        bestFit = sortedParticles[0].fitness
        bestSol = sortedParticles[0].pos

        return bestFit, bestSol
            
    def minimize(self, problem, verbose=False):
        """ minimizes the defined problem instance after checking it for plausibility. """
        try:
            # check consistency of problem definition
            problem.check()
            
            # initialize the particles
            try:
                # temporary stores particles
                particleCloud = [] 
                for i in range(1, self.popSize+1):
                    particleCloud.append( Particle(i, problem.initSol, problem.lb, problem.ub, self.w, self.c1, self.c2) )
            except Exception as e:
                raise MinimizationException("Error in particle initialization: "+e.args[0])
                
            # evaluate fitness of each particle
            for particle in particleCloud:
                particle.fitness = problem.objective(particle.pos)
                
            # initialize neighbourhood and store belonging particles
            if self.topoType == "gbest":
                """ Global best topology containts only one swarm """
                self.topologies.append( Topology(index=1, particles=particleCloud) )
                
            elif self.topoType == "lbest":
                """ Local best topology containts multiple sub-swarms """
                # split particle cloud into the defined number of neighbourhoods
                particleSets = list( splitList(particleCloud, self.neighb) )
                
                # generate self.neighb neighbourhoods
                for i in range(self.neighb):
                    self.topologies.append( Topology(index=i+1, particles=particleSets[i]) )
                
            # elif self.topoType == "vonNeumann":
            #     """ Von Neumann ragards the two neighbours of each element in a ring topology """
            ### @todo: implement von neumann neighbourhood ###
            
            else:
                raise MinimizationException("Unknown neighbourhood type for paticle swarm!")
            
            # main pso-loop (uses tqdm if installed)
            for i in tqdm.tqdm(range(self.maxIter)) if useTqdm else range(self.maxIter):
                for t in self.topologies:
                    for p in t.particles:
                        # compute new positions of the particles in the neightbourhood
                        p.updateVelocity()
                        p.updatePosition()
                        
                        # Serial computation of the objective
                        if self.parallelization == None:
                            p.evaluate(problem.objective)
                        
                        # Use multithreading
                        elif self.parallelization == "multithread":
                            with concurrent.futures.ThreadPoolExecutor() as executor:
                                executor.submit(p.evaluate(problem.objective))
                        
                        # Use multiprocessing
                        elif self.parallelization == "multiprocess":
                            with concurrent.futures.ProcessPoolExecutor() as executor:
                                executor.submit(p.evaluate(problem.objective))
                                
                        else:
                            raise MinimizationException("Unknown parallelization method!")
                        
                    # Update the global best fitness
                    bestFit, bestSol = self.getBestOfTopo(t)
                    t.updateBestSolution(bestFit, bestSol)
                    
                # sort topologies for fitness value and add global best to convergence history
                sortedTopos = sorted(self.topologies, key=lambda x: x.bestFit)
                problem.addToHist(sortedTopos[0].bestFit, sortedTopos[0].bestSol)
                
                if verbose:
                    print("it: {}, best: {:.2f}, {}".format(i, problem.fitHist[-1], problem.solHist[-1]))

        except Exception as e:
            sys.exit("Minimization has failed: "+e.args[0])
            
        else:
            if verbose:
                self.printNeighb()
                print("\nMinimization complete! \nMinimum found: {:.2f} \nSolution: {}".format(problem.fitHist[-1], problem.solHist[-1]))
                problem.plotConvergence(self)
            else:
                print("\nMinimization complete!  Minimum found: {:.2f}".format(problem.fitHist[-1]))
            
            try:
                return (problem.fitHist[-1], problem.solHist[-1])
            except:
                raise MinimizationException("Convergence history is invalid!")
    
    
    def printNeighb(self):
        """ prints the particle of each neighbourhood to the screen """
        for t in self.topologies:
            print("\nNeighb.:", str(t.index))
            for p in t.particles:
                print(p)
