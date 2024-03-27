"""
Abstract MLOSolver class, representing mixed linear constraint solver.
"""

from __future__ import annotations

from ..variable import Variable
from ..formula import ConstraintOperator
from .optimizationValues import OptimizationValues

from abc import ABC, abstractmethod
from fractions import Fraction

class MLOSolver(ABC):
    """
    Abstract MLOSolver class, representing mixed linear constraint solver.
    """
    
    @abstractmethod
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
        pass