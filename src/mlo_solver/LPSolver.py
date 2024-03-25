"""
Interface with lp_solve 5.5, using Conda's Lpsolve55 package (available at https://anaconda.org/conda-forge/lpsolve55).
"""

from __future__ import annotations

from ..formula.nullaryFormula.constraint.constraintOperator import ConstraintOperator
from ..variable import Variable
from .optimizationValues import OptimizationValues
from .MLOSolver import MLOSolver

from fractions import Fraction
import lpsolve55 as lp_solve

class LPSolver(MLOSolver):
    """
    Interface with lp_solve 5.5, using Conda's Lpsolve55 package (available at https://anaconda.org/conda-forge/lpsolve55).
    """

    def __init__(self):
        pass
        
    def solve(self, variables : list[Variable], objectif : list[Fraction], constraints : list[tuple[list[Fraction], ConstraintOperator, Fraction]])\
        -> tuple[OptimizationValues, list[Fraction], Fraction]:
        """
        Method returning the result of a mixed linear problem.

        Parameters
        ----------
        variables : list of src.variable.variable.Variable
            Variables used in constraints.
        objectif : list of fractions.Fraction
            Weights of the objective function to optimize.
        constraints : list of tuple of the form (list of fractions.Fraction, src.formula.nullaryFormula.constraint.constraintOperator.ConstraintOperator, fractions.Fraction)
            Each tuple represents a linear constraint, with the first element being the weights, the second the operator and the third the bound.

        Returns
        -------
        src.mlo_solver.optimizationValues.OptimizationValues
            Information of the final state of the problem.
        list of fractions.Fraction
            The point at the optimal, if found.
        fractions.Fraction
            The optimal value, if found.
        """
        
        lp = lp_solve.lpsolve('make_lp', 0, len(variables))
        lp_solve.lpsolve('set_verbose', lp, lp_solve.IMPORTANT)

        infinite = lp_solve.lpsolve("get_infinite", lp)

        for i in range(0,len(variables)):
            if(variables[i].isInteger()): 
                lp_solve.lpsolve('set_int', lp,i+1, 1)

            getBoundL, getBoundR = variables[i].getBounds()
            if(not getBoundL and not getBoundR):
                lp_solve.lpsolve('set_unbounded', lp, i+1)
            else:
                lower, upper = variables[i].getBounds()
                if(lower == None): lower = -infinite
                if(upper == None): upper = infinite
                lp_solve.lpsolve('set_bounds', lp, i+1, float(lower), float(upper))

        lp_solve.lpsolve('set_obj', lp, objectif)
        for constraint in constraints:
            comp = lp_solve.LE
            if(constraint[1] == ConstraintOperator.EQ):
                comp = lp_solve.EQ
            elif (constraint[1] == ConstraintOperator.GEQ):
                comp = lp_solve.GE
            lp_solve.lpsolve('add_constraint', lp, constraint[0], comp, constraint[2])
        tmp = lp_solve.lpsolve('solve', lp)
        if tmp not in [0,3]:
            return (OptimizationValues.INFEASIBLE, [], 0)
        if tmp == 3:
            val = lp_solve.lpsolve('get_variables', lp)[0]
            return (OptimizationValues.UNBOUNDED, val, lp_solve.lpsolve('get_objective', lp))
        return (OptimizationValues.OPTIMAL, lp_solve.lpsolve('get_variables', lp)[0], lp_solve.lpsolve('get_objective', lp))