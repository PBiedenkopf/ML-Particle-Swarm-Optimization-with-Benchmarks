# Particle Swarm Optimization 
A lightweight library for particle swarm optimization. The library is designed to be easily extended 
with new metaheuristic optimization algorithms and optimization problem types in the future.

## Use
To define an continuous optimization problem, the "ContinuousProblem"-class is used. 
```
problem = ContinuousProblem(objective=benchmarks.rosenbrock, initSol=[0,0,0], lb=-5.12, ub=5.12)
```
The objective can be an custom function or one of the predefined benchmarks. To define the problem 
dimension you have to specify some initial solution. Note that this solution is not used in the 
optimization as starting solution. Optional you can specify upper and lower boundaries, which is 
recommended. The boundaries can be a list with a value for each dimension or a single number if the 
problem has symmetric boundaries for each dimension.

After defining the problem instance, you have to define an algorithm instance for the particle swarm 
optimization.
```
pso = algorithms.pso(maxIter=200, topoType="lbest", neighb=3, popSize=24)
```
In the constructor you can specify different parameters for the pso implementation as the inertia and the 
constants c1 and c2 as well as the population size.
The implementation of the algorithm offers two neighbourhood topologies currently:
- gbest: Here the complete population is organized in one neighbourhood, so each particle is influenced 
by the global best position found so far.
- lbest: Here the population is organized in multiple neighbourhoods. The number of the neighbourhoods
can be defined with the "neighb" parameter

After the algorithm instance is defined, the problem can be solved with the "minimze"-method.
```
pso.minimize(problem, verbose=True)
```
If verbose is set to True (False by default) the convergence history is plotted and all the neighbourhoods 
are printed to the console.
![Alt text](./Result_Rosenbrock_5_dimensional.png?raw=true "Title")

## Benchmark Functions
The library contains several benchmark functions that are implemented for arbitrary dimensions.
- Rosenbrock function
- Rastrigin function
- Auckley function
- Schwefel function
- Sphere function

## License
MIT License

Copyright (c) 2020 Philipp Biedenkopf