"""
Implementation of the Daalmans method for simplification of conjunction of literals (i.e `olaaaf.formula.nullaryFormula.constraint.linearConstraint.LinearConstraint` or
    `olaaaf.formula.unaryFormula.notOperator.Not`).
"""

from __future__ import annotations

from ..formula import Formula, LinearConstraint, ConstraintOperator, Not, And, NullaryFormula
from .simplificator import Simplificator
from ..variable import RealVariable
from ..mlo_solver import MLOSolver, OptimizationValues

from fractions import Fraction

class Daalmans(Simplificator):
    """
    Implementation of the Daalmans method for simplification of conjunction of literals (i.e `olaaaf.formula.nullaryFormula.constraint.linearConstraint.LinearConstraint` or
    `olaaaf.formula.unaryFormula.notOperator.Not`).
    This method is split into two algorithm :\n
    - The first algorithm is concerned with detecting fixed variables. Fixed variables are variables that can only have one value.\n
    - The second algorithm deals with the removal of redundant mixed linear constraints.

    Parameters
    ----------
    solver: olaaaf.mlo_solver.MLOSolver.MLOSolver
        The `olaaaf.mlo_solver.MLOSolver.MLOSolver` used to solve optimization problems.
    """

    _interpreter = None

    def __init__(self, solver: MLOSolver):
        self._solver = solver
    
    def run(self, phi: Formula) -> Formula:
        r"""
        Main method of `olaaaf.simplificator.daalmans.Daalmans`, allowing to simplify a given `olaaaf.formula.formula.Formula`.

        Parameters
        ----------
        phi: `olaaaf.formula.formula.Formula`
            The`olaaaf.formula.formula.Formula`to simplify.
        
        Returns
        -------
        `olaaaf.formula.formula.Formula`
            The simplified form of \(\varphi\)
        """

        if not self._interpreter.sat(phi): return phi
        if isinstance(phi, NullaryFormula): phi = And(phi)
        phiPrime = self.__fixedVariables(phi)
        phiPrime = self.__deleteConstraint(phiPrime)
        return phiPrime
    
    def __fixedVariables(self, phi : Formula) -> Formula:
        variablesToAnalyse = list(phi.getVariables())
        objectivFunction = [0] * (len(variablesToAnalyse) + 1)
        index = 0
        e = RealVariable("@")
        tabPhi = self._toTab(phi, e)
        variables = variablesToAnalyse + [e]
        fixedVariables = {}

        # For each variable x 
        for variable in variablesToAnalyse:
            # We will analyse the optimal value of the variable when we wants to maximize x and minimize x
            objectivFunction[index] = 1
            v1 = self.__solve(variables, objectivFunction, tabPhi)
            objectivFunction[index] = -1
            v2 = self.__solve(variables, objectivFunction, tabPhi)
            objectivFunction[index] = 0
            if v1[0] == OptimizationValues.OPTIMAL and v2[0] == OptimizationValues.OPTIMAL and v1[1][index] == v2[1][index] :
                # If x can have only one value, it is a fixed variable
                fixedVariables[variable] = Fraction(v1[1][index])

            index += 1
        return self.__removeVariables(phi, fixedVariables)

    def __removeVariables(self, phi : Formula, fixedVariables : dict) -> Formula:
        for variable in fixedVariables.keys():
            newChildren = set()
            for litteral in phi.children:
                try:
                    if isinstance(litteral, Not) :
                        litteral.children.replace(variable, -fixedVariables[variable])
                    else:
                        litteral.replace(variable, fixedVariables[variable])
                    newChildren.add(litteral)
                except:
                    # If the constraint is now useless, we dont keep it in the children of the formula
                    pass
            phi.children = newChildren
            
            # We adding = constraint between x and his only possible value
            newConstraint =  LinearConstraint("")
            newConstraint.variables[variable] = 1
            newConstraint.operator = ConstraintOperator.EQ
            newConstraint.bound = fixedVariables[variable]
            phi = phi & newConstraint
        return phi
            

    def __deleteConstraint(self, phi : Formula) -> Formula:
        actualConstraints : set
        actualConstraints = phi.children.copy()
        for constraint in phi.children:
            neg = ~constraint.clone()
            actualConstraints.remove(constraint)

            actualConstraints.add(neg)
            form = And(*actualConstraints).toLessOrEqConstraint().toDNF()
            if self._interpreter.sat(form) :
                actualConstraints.add(constraint)
            actualConstraints.remove(neg)

        return And(*actualConstraints)

    
    def __solve(self, variables, obj, constraints):
        return self._solver.solve(variables, obj, constraints)

