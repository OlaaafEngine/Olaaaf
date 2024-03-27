"""
Rounded approximation of `olaaaf.mlo_solver.LPSolver.LPSolver`, reducing floating point approximations.
"""

from __future__ import annotations

from .LPSolver import LPSolver
from ..formula.nullaryFormula.constraint import ConstraintOperator
from ..variable import Variable
from .optimizationValues import OptimizationValues
from math import isnan

from fractions import Fraction

class LPSolverRounded(LPSolver):
    """
    Rounded approximation of `olaaaf.mlo_solver.LPSolver.LPSolver`, reducing floating point approximations.

    Parameters
    ----------
    round: int
        The decimal to which all numbers are rounded.
    """

    __round: int

    def __init__(self, round: int = 12):
        self.__round = round
        
    def solve(self, variables : list[Variable], objectif : list[Fraction], constraints : list[tuple[list[Fraction], ConstraintOperator, Fraction]])\
        -> tuple[OptimizationValues, list[Fraction], Fraction]:
        """
        Method returning the result of a mixed linear problem.

        Parameters
        ----------
        variables : list of olaaaf.variable.variable.Variable
            Variables used in constraints.
        objectif : list of fractions.Fraction
            Weights of the objective function to optimize.
        constraints : list of tuple of the form (list of fractions.Fraction, olaaaf.formula.nullaryFormula.constraint.constraintOperator.ConstraintOperator, fractions.Fraction)
            Each tuple represents a linear constraint, with the first element being the weights, the second the operator and the third the bound.

        Returns
        -------
        olaaaf.mlo_solver.optimizationValues.OptimizationValues
            Information of the final state of the problem.
        list of fractions.Fraction
            The point at the optimal, if found.
        fractions.Fraction
            The optimal value, if found.
        """

        LPsolverRes = super().solve(variables, objectif, constraints)
        
        res = []

        res.append(LPsolverRes[0])
        res.append([Fraction(0) if isnan(x) else round(Fraction(x), self.__round) for x in LPsolverRes[1]])
        res.append(round(Fraction(LPsolverRes[2]), self.__round))

        return res