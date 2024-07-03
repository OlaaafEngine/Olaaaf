r"""
Main class of the module, allowing the user to make the adaptation between two `olaaaf.formula.formula.Formula`
\(src\) and \(tgt\) that are constraints.
"""

from __future__ import annotations

from .formula import Formula
from .mlo_solver import MLOSolver
from .distance import DistanceFunction
from .constants import Constants
from .simplificator import Simplificator
from .projector import Projector
from .revision import Revision

class Adaptation:
    r"""
    Main class of the module, allowing the user to make the adaptation between two `olaaaf.formula.formula.Formula`
    \(src\) and \(tgt\) that are constraints.

    Parameters
    ----------
    solverInit : olaaaf.mlo_solver.MLOSolver.MLOSolver
        The solver that will be used for optimization.
    distance : olaaaf.distance.distance_function.distanceFunction.DistanceFunction
        The distance function that will be used and, more importantly, the weights \((w_i)\) and \(\varepsilon\) arguments of it.
        The original algorithm is meant to be used with a `olaaaf.distance.distance_function.discreteL1DistanceFunction.DiscreteL1DistanceFunction`.
    simplifiers : list of olaaaf.simplificator.simplificator.Simplificator, optional
        List of all of the `olaaaf.simplificator.simplificator.Simplificator` that will be applied to the `olaaaf.formula.formula.Formula`, 
        in order given by the list.
    onlyOneSolution : boolean, optional
        If set to `True`, the adaptation algorithm will only return one solution.
        If not, it will return all solutions.
        By default, this constant is set to whichever one was chosen in `olaaaf.constants.Constants`.
    verbose : boolean, optional
        If set to `True`, the adaptation algorithm will have a verbose display in the terminal.
        By default, this constant is set to whichever one was chosen in `olaaaf.constants.Constants`.
    projector : boolean, optional
        Projector algorithm to use, only necessary if `onlyOneSolution` is set to `False`.
    """

    __revision : Revision

    def __init__(self, solverInit : MLOSolver, distance : DistanceFunction, simplifiers : list[Simplificator] = [], onlyOneSolution: bool = Constants.ONLY_ONE_SOLUTION, verbose: bool = Constants.SET_VERBOSE, projector: Projector = None) -> None:        
        
        self.__revision = Revision(solverInit, distance, simplifiers, onlyOneSolution, verbose, projector)

    def preload(self):
        r"""
        Methd used to preload the adaptation algorithm.

        This step is necessary before using `execute` and recommended before the domain knowledge definition since it translates every
        non-`olaaaf.formula.nullaryFormula.constraint.linearConstraint.LinearConstraint` into one and introduces new under-the-box variables that the user might want to use.
        """

        self.__revision.preload()

    def execute(self, srce_case : Formula, trgt : Formula, dk : Formula, withTableaux = True):
        r"""
        Execute the adaptation of \(srce_case\) by \(tgt_problem\), with the domain knowledge \(DK\).

        Parameters
        ----------
        srce_case : `olaaaf.formula.formula.Formula`
            \(srce_case\), source case for the adaptation and `olaaaf.formula.formula.Formula` that will be adapted.
        tgt_problem : `olaaaf.formula.formula.Formula`
            \(tgt_problem\), target problem for the adaptation and `olaaaf.formula.formula.Formula` that will be used to adapt \(srce_case\) by.
        dk : `olaaaf.formula.formula.Formula`
            \(DK\), the domain knowledge.
        withTableaux: `boolean`
            Wether the analytic tableaux method should be used to prune unsatisfiable branches. By default, set to `True`.

        Returns
        -------
        Fraction
            Distance (calculated with the `olaaaf.distance.distance_function.distanceFunction.DistanceFunction`
            given at the initialization of the class) between \(srce_case\) and \(tgt_problem\).
        `olaaaf.formula.formula.Formula`
            Result of the adaptation of \(srce_case\) by \(tgt_problem\).
        """

        return self.__revision.execute(srce_case & dk, trgt & dk, withTableaux)