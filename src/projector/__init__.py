"""
Allows to project a closed conjunction of `src.formula.formula.Formula` to a sub-set of its variables.
"""

from .projector import Projector

try:
    from .floatConvexHullProjector import FloatConvexHullProjector
except ModuleNotFoundError:

    from ..constants import Constants
    
    if Constants.DISPLAY_DEPENDENCIES_WARNING:
        print("Missing SciPy or Numpy dependency: FloatConvexHullProjector cannot be used without it. If you wish to disable these warnings, set the DISPLAY_DEPENDENCIES_WARNING constant to False.")