"""
Representation of interfacing with MLO solvers, used to solve MLO problems.
"""

from .MLOSolver import MLOSolver

try:
    from .LPSolver import LPSolver
    from .LPSolverRounded import LPSolverRounded
except ModuleNotFoundError:

    from ..constants import Constants
    
    if Constants.DISPLAY_DEPENDENCIES_WARNING:
        print("Missing lpsolve55 dependency: LPSolver and LPSolverRounded cannot be used without it. If you wish to disable these warnings, set the DISPLAY_DEPENDENCIES_WARNING constant to False.")

try:
    from .scipySolver import ScipySolver
    from .scipySolverRounded import ScipySolverRounded
except ModuleNotFoundError:

    from ..constants import Constants
    
    if Constants.DISPLAY_DEPENDENCIES_WARNING:
        print("Missing SciPy or Numpy dependency: SciPySolver and SciPySolverRounded cannot be used without it. If you wish to disable these warnings, set the DISPLAY_DEPENDENCIES_WARNING constant to False.")

from .optimizationValues import OptimizationValues