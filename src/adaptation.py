from __future__ import annotations

from .formula import Formula, And
from .mlo_solver import MLOSolver
from .distance import DistanceFunction
from .constants import Constants
from .simplificator import Simplificator
from .projector import Projector
from .revision import Revision

class Adaptation:

    __revision : Revision

    def __init__(self, solverInit : MLOSolver, distance : DistanceFunction, simplifiers : list[Simplificator] = [], onlyOneSolution: bool = Constants.ONLY_ONE_SOLUTION, verbose: bool = Constants.SET_VERBOSE, projector: Projector = None) -> None:        
        
        self.__revision = Revision(solverInit, distance, simplifiers, onlyOneSolution, verbose, projector)

    def preload(self):
        self.__revision.preload()

    def execute(self, x_src : Formula, y_trgt : Formula, dk : Formula):

        return self.__revision.execute(x_src & dk, y_trgt & dk)