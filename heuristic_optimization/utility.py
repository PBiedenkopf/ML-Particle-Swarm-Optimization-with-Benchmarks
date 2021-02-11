
"""
Philipp Biedenkopf - 2021

Utility functions for heuristic optimization library
    
"""


def splitList(li, n):
    """ splits a list into n approximately equal parts """
    k, m = divmod(len(li), n)
    return (li[i * k + min(i, m):(i + 1) * k + min(i + 1, m)] for i in range(n))



# Exceptions
class MinimizationException(Exception):
    """ Exception for runtime errors in minimization process """
    pass
    
class ProblemException(Exception):
    """ Exception for runtime errors in the problem creation """
    pass