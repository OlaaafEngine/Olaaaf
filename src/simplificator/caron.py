"""
Implementation of the Caron algorithm for simplification of conjunction of literals (i.e `src.formula.nullaryFormula.constraint.linearConstraint.LinearConstraint` or
    `src.formula.unaryFormula.notOperator.Not`).
"""

from __future__ import annotations

from ..formula import Formula, LinearConstraint, Not, And, NullaryFormula
from .simplificator import Simplificator
from ..variable import RealVariable
from ..mlo_solver import MLOSolver, OptimizationValues


class Caron(Simplificator):
    """
    Implementation of the Caron algorithm for simplification of conjunction of literals (i.e `src.formula.nullaryFormula.constraint.linearConstraint.LinearConstraint` or
    `src.formula.unaryFormula.notOperator.Not`).
    Caron’s algorithm deals with the removal of redundant mixed linear constraints.

    Parameters
    ----------
    solver: src.mlo_solver.MLOSolver.MLOSolver
        The `src.mlo_solver.MLOSolver.MLOSolver` used to solve optimization problems.
    """

    _interpreter = None
    def __init__(self, solver : MLOSolver):
        self._solver = solver

    def run(self, phi):
        r"""
        Main method of `src.simplificator.caron.Caron`, allowing to simplify a given `src.formula.formula.Formula`.

        Parameters
        ----------
        phi: src.formula.formula.Formula
            The src.formula.formula.Formula to simplify.
        
        Returns
        -------
        src.formula.formula.Formula
            The simplified form of \(\varphi\)
        """

        if not self._interpreter.sat(phi): return phi
        if isinstance(phi, NullaryFormula): phi = And(phi)
        return self.__deleteConstraint(phi)
    
    def __deleteConstraint(self, phi : Formula):
        finalConstraints : list
        finalConstraints = list(phi.children.copy())
        e = RealVariable("@")
        variables = list(phi.getVariables())
        variables.append(e)
        for litteral in phi.children:
            constraint : LinearConstraint
            constraint = litteral.children if isinstance(litteral, Not) else litteral
            
            # for all litteral, want to maximise his values
            finalConstraints.remove(litteral)
            newPhi = And(*finalConstraints)
            phiTab = self._toTab(newPhi, e, variables=variables) 
            objectif = []
            for variable in variables:
                objectif.append(0 if not variable in constraint.variables.keys() else constraint.variables[variable]*-1)
            res = self._solver.solve(variables, objectif, phiTab)
            xStar = res[1]
            if res[0] == OptimizationValues.OPTIMAL:
                mustBeDeleted = False
                # if the maximum values is <= bound we deleted the litteral
                if isinstance(constraint, NullaryFormula):
                    sum = 0
                    for i in range(0,len(variables)): 
                        if variables[i] in constraint.variables: sum += xStar[i]*constraint.variables[variables[i]]
                    mustBeDeleted = (sum <= constraint.bound)
                else:
                    sum = 0
                    for i in range(0,len(variables)): 
                        if variables[i] in constraint.variables: sum += xStar[i]*constraint.variables[variables[i]]*-1
                    mustBeDeleted = (sum < constraint.bound)
                if not mustBeDeleted: finalConstraints.append(litteral)
            else : finalConstraints.append(litteral)

        return And(*finalConstraints)
