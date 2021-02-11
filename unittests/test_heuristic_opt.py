
from sys import path
path.append('..\\heuristic_opt')

import unittest

from heuristic_optimization import ContinuousProblem, DiscreteProblem
from benchmarks import rosenbrock, tsp



class TestProblem(unittest.TestCase):
    
    def test_boundary_creation(self):
        """ Tests the different creation methods for the boundaries. """
        p = ContinuousProblem(objective=rosenbrock, initPos=[0 for i in range(3)], lb=-5, ub=[5,5,5,5,5])
        for l, u in zip(p.lb, p.ub):
            self.assertAlmostEqual(u, -l)
