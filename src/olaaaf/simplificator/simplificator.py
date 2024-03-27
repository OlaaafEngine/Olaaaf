"""
Abstract class, representing a simplificator of conjunction of litterals (i.e `olaaaf.formula.nullaryFormula.constraint.linearConstraint.LinearConstraint` or
`olaaaf.formula.unaryFormula.notOperator.Not`).
"""

from __future__ import annotations

from ..formula import Formula, ConstraintOperator

from abc import ABC, abstractmethod

class Simplificator(ABC):
    """
    Abstract class, representing a simplificator of conjunction of litterals (i.e `olaaaf.formula.nullaryFormula.constraint.linearConstraint.LinearConstraint` or
    `olaaaf.formula.unaryFormula.notOperator.Not`).
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
        Main method of a `olaaaf.simplificator.simplificator.Simplificator`, allowing to simplify a given `olaaaf.formula.formula.Formula`.

        Parameters
        ----------
        phi: `olaaaf.formula.formula.Formula`
            The`olaaaf.formula.formula.Formula`to simplify.
        
        Returns
        -------
        `olaaaf.formula.formula.Formula`
            The simplified form of \(\varphi\)
        """

        pass