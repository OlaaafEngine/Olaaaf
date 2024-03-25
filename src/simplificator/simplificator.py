"""
Abstract class, representing a simplificator of conjunction of litterals (i.e `src.formula.nullaryFormula.constraint.linearConstraint.LinearConstraint` or
`src.formula.unaryFormula.notOperator.Not`).
"""

from __future__ import annotations

from ..formula import Formula, ConstraintOperator

from abc import ABC, abstractmethod

class Simplificator(ABC):
    """
    Abstract class, representing a simplificator of conjunction of litterals (i.e `src.formula.nullaryFormula.constraint.linearConstraint.LinearConstraint` or
    `src.formula.unaryFormula.notOperator.Not`).
    """

    def __init__(self):
        pass

    def _toTab(self, formula, e, variables : list = None):
        constraints = []
        if variables == None : 
            variables = list(formula.getVariables())
            variables.append(e)
        for lc in formula.getAdherence(e):
            for constraint in lc:
                constraintP = []
                for variable in variables:
                    if variable in constraint.variables:
                        constraintP.append(constraint.variables[variable])
                    else:
                        constraintP.append(0)
                constraints.append((constraintP, constraint.operator, constraint.bound))
        lastConstraint = []
        for variable in variables: 
            lastConstraint.append(-1 if variable == e else 0)
        return constraints + [(lastConstraint, ConstraintOperator.LEQ, 0)]

    @abstractmethod
    def run(self, phi: Formula) -> Formula:
        r"""
        Main method of a `src.simplificator.simplificator.Simplificator`, allowing to simplify a given `src.formula.formula.Formula`.

        Parameters
        ----------
        phi: src.formula.formula.Formula
            The src.formula.formula.Formula to simplify.
        
        Returns
        -------
        src.formula.formula.Formula
            The simplified form of \(\varphi\)
        """

        pass