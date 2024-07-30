"""
Interface with HiGHS, using SciPy's wrapper.
"""

from __future__ import annotations

from ..formula.nullaryFormula.constraint.constraintOperator import ConstraintOperator
from .optimizationValues import OptimizationValues
from ..variable import Variable
from .optimizationValues import OptimizationValues
from .MLOSolver import MLOSolver

from fractions import Fraction
import numpy as np
import warnings
from scipy.optimize import milp, Bounds, LinearConstraint

class ScipySolver(MLOSolver) :
    """
    Interface with HiGHS, using SciPy's wrapper.
    """

    def __init__(self):
        pass
        
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
        
        integers = []
        boundsLower = []
        boundsUpper = []
        for variable in variables: 
            integers.append(variable.isInteger())
            lower, upper = variable.getBounds()
            if(lower == None): lower = -np.inf
            if(upper == None): upper = np.inf
            boundsLower.append(float(lower))
            boundsUpper.append(float(upper))
        tab = []
        limitInf = []
        limitUp = []
        for constraint in constraints:
            tab.append(constraint[0])
            if constraint[1] == ConstraintOperator.LEQ:
                limitInf.append(-np.inf)
                limitUp.append(constraint[2])
            elif constraint[1] == ConstraintOperator.GEQ:
                limitInf.append(constraint[2])
                limitUp.append(np.inf)
            elif constraint[1] == ConstraintOperator.EQ:
                limitInf.append(constraint[2])
                limitUp.append(constraint[2])

        lc = LinearConstraint(tab, limitInf, limitUp)

        options ={"presolve":False,
                  "output_flag":False}

        # presolve at false to fixed status 4
        with warnings.catch_warnings(action="ignore"):
            result = milp(c=objectif, integrality=integers, constraints=lc, bounds=Bounds(boundsLower, boundsUpper), options=options)
        res : tuple
        if result.status == 0:
            res = (OptimizationValues.OPTIMAL, [Fraction(x) for x in result.x], result.fun)
        elif result.status == 3:
            res = (OptimizationValues.UNBOUNDED, [], float(np.inf))
        elif result.status == 4:
            # in fact status 4 can be return
            # to detect if the problem is unbounded we test if the objectiv function * -1 is unbounded
            # if it's not, the problem is infeasible
            for i in range(0,len(objectif)): objectif[i] *= -1
            with warnings.catch_warnings(action="ignore"):
                result = milp(c=objectif, integrality=integers, constraints=lc, bounds=Bounds(boundsLower, boundsUpper), options=options)
            if result.status == 0 or result.status == 3:
                res = (OptimizationValues.UNBOUNDED, [], float(np.inf))
            else: res = (OptimizationValues.INFEASIBLE, [], float(np.inf))
        else: res = (OptimizationValues.INFEASIBLE, [], float(np.inf))
        return res