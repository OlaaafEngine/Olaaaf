"""
Class allowing `src.revision.Revision` to interact with a `src.mlo_solver.MLOSolver.MLOSolver`.
"""

from __future__ import annotations

from .formula import Formula, Or, Not, LinearConstraint, ConstraintOperator, And
from .variable import Variable, RealVariable
from .mlo_solver import OptimizationValues
from .mlo_solver import MLOSolver
from .distance import DistanceFunction
from .simplificator import Simplificator

from fractions import Fraction

class FormulaInterpreter:
    r"""
    Class allowing `src.revision.Revision` to interact with a `src.mlo_solver.MLOSolver.MLOSolver`.
    
    Parameters
    ----------
    solverInit : src.mlo_solver.MLOSolver.MLOSolver
        The solver that will be used for optimization.
    distance : src.distance.distance_function.distanceFunction.DistanceFunction
        The distance function that will be used and, more importantly, the weights \((w_i)\) and \(\varepsilon\) arguments of it.
        The original algorithm is meant to be used with a `src.distance.distance_function.discreteL1DistanceFunction.discreteL1DistanceFunction`.
    simplifiers : list of src.simplificator.simplificator.Simplificator, optional
        List of all of the `src.simplificator.simplificator.Simplificator` that will be applied to the `src.formula.formula.Formula`, 
        in order given by the list.
    """

    def __init__(self, mloSolver : MLOSolver, distanceFunction : DistanceFunction, simplifications : list[Simplificator] = []) -> None:
        self.__MLOSolver = mloSolver
        self.__distanceFunction = distanceFunction
        self.__simplifiers = simplifications

        for simplifier in self.__simplifiers:
            simplifier._interpreter = self
            
        self._eVar = RealVariable("@")

    def simplifyMLC(self, phi : Formula):
        """
        Method used to simplify a conjonction of mixed linear constraints.

        Parameters
        ----------
        phi : src.formula.formula.Formula
            The `src.formula.formula.Formula` to simplify.

        Returns
        -------
        src.formula.formula.Formula
            The simplified `src.formula.formula.Formula`.
        """

        if self.__simplifiers == None:
            # If no simplifier was entered, we return the original phi
            return phi
        else:
            if not isinstance(phi, Or) : phi = Or(phi)
            orChild = []
            for miniPhi in phi.children:
                newMiniPhi = miniPhi
                for simplifier in self.__simplifiers:
                    newMiniPhi = simplifier.run(newMiniPhi.toLessOrEqConstraint().toDNF())
                orChild.append(newMiniPhi)
            return Or(*orChild)

    def sat(self, phi : Formula) -> bool:
        r"""
        Method used to verify the feasability of a `src.formula.formula.Formula`.

        Parameters
        ----------
        phi : `src.formula.formula.Formula`
            The `src.formula.formula.Formula` you want to verify the feasability.

        Returns
        -------
        boolean
            Booean symbolizing if \(\varphi\) is feasable (`True`) or not (`False`).
        
        """
        variables = list(phi.getVariables())
        variables.append(self._eVar)

        for lc in phi.getAdherence(self._eVar):
            # build tabs for solver
            constraints = []
            for constraint in lc:
                constraintP = []
                for variable in variables:
                    if variable in constraint.variables:
                        constraintP.append(constraint.variables[variable])
                    else:
                        constraintP.append(Fraction(0))
                constraints.append((constraintP, constraint.operator, constraint.bound))
            constraintP = []
            for var in variables: 
                if(var == self._eVar) :
                    constraintP.append(Fraction(-1))
                else :
                    constraintP.append(Fraction(0))
            constraints.append((constraintP, ConstraintOperator.LEQ, Fraction(0)))

            res = self.__MLOSolver.solve(variables, list(map(lambda v : Fraction(-1) if v == self._eVar else Fraction(0), variables)), constraints)

            # Interpretion of the mlo solver result
            if res[0] == OptimizationValues.OPTIMAL :
                if res[1][variables.index(self._eVar)] != Fraction(0):
                    return True
            if res[0] == OptimizationValues.UNBOUNDED:
                return True
            
        return False

    def findOneSolution(self, variables : list[Variable], psi : And, mu : And) -> tuple[Fraction, Formula]:
        r"""
        Method used to interact with the initialy specified `src.mlo_solver.MLOSolver.MLOSolver`, thus finding one solution of
        the optimization of the following system when \(\psi\) and \(\mu\) are conjunctions of
        `src.formula.nullaryFormula.constraint.linearConstraint.LinearConstraint`, with \(d\) the  `src.distance.distance_function.distanceFunction.DistanceFunction`
        given at the initialization of the class.

        \[
            \begin{cases}
                x \in \mathcal{M}(\psi) \\
                y \in \mathcal{M}(\mu) \\
                \text{minimize } d(x, y)
            \end{cases}
        \]

        Parameters
        ----------
        variables : list of `src.variable.variable.Variable`
            List of all the `src.variable.variable.Variable` in use in both \(\psi\) and \(\mu\).
        psi, mu : `src.formula.naryFormula.andOperator.And`
            \(\psi\) and \(\mu\), conjunctions of litterals as used in the optimization problem above.

        Returns
        -------
        Fraction
            Minimal distance (calculated with the `src.distance.distance_function.distanceFunction.DistanceFunction`
            given at the initialization of the class) that satisfies the optimization problem above. 
        src.formula.formula.Formula
            `src.formula.formula.Formula` representing a point \(y \in \mathcal{M}(\mu)\) that satisfies the optimization problem above. 
        """
        # Reorder variables order
        variables = list(variables)
        constraints = self.__buildConstraints(variables, psi, mu)

        # creation of the objective function
        obj = [0]*len(variables)*2
        for variable in variables:
            obj.append(self.__distanceFunction.getWeights()[variable])
        res = self.__MLOSolver.solve(variables*3, obj, constraints)

        # interpretation of the mlo solver result
        if(res[0] == OptimizationValues.INFEASIBLE): 
            raise Exception("Optimize couple impossible") 
        
        values = res[1]
        resSet = set([])
        for i in range(0,len(variables)):
            lc = LinearConstraint("") 
            lc.variables = {variables[i]: Fraction(1)}
            lc.operator = ConstraintOperator.EQ
            lc.bound = Fraction(values[len(variables)+i])
            resSet.add(lc)
        return (res[2], And(*resSet))

    def __buildConstraints(self, variables : list[Variable], psi : And, mu : And) -> dict[tuple[dict[Fraction], ConstraintOperator, Fraction]]:
        '''
        Method used to build table of constraints, for the solver, linked to phi and mu
        
        Attributes
        ----------
        variables : list of variables
        phi : a formula (And)
        mu : a formula (And)

        Returns
        -------
        res: table of constraint wich simbolyze all of constraints of phi and mu
        '''
        constraints = []
        i = 0
        for formula in [psi, mu]:
            for lc in formula.getAdherence():
                for constraint in lc:
                    constraintP = []
                    for _ in range(0,(len(variables)) *i):
                        constraintP.append(0)
                    for variable in variables:
                        if variable in constraint.variables:
                            constraintP.append(constraint.variables[variable])
                        else:
                            constraintP.append(0)
                    for _ in range(0,(len(variables)) *(2-i)):
                        constraintP.append(0)
                    constraints.append((constraintP, constraint.operator, constraint.bound))
            i += 1
        for variable in variables:
            constraintP = []
            constraintN = []
            index = variables.index(variable)
            for i in range(0, len(variables)*3):
                if i == index:
                    constraintP.append(1)
                    constraintN.append(-1)
                elif i == index + len(variables):
                    constraintP.append(-1)
                    constraintN.append(1)
                elif i == index + len(variables)*2:
                    constraintP.append(-1)
                    constraintN.append(-1)
                else:
                    constraintP.append(0)
                    constraintN.append(0)
            constraints.append((constraintP, ConstraintOperator.LEQ, 0))
            constraints.append((constraintN, ConstraintOperator.LEQ, 0))
        return constraints

    def optimizeCouple(self, psi : And, mu : And) -> tuple[Fraction, Formula]:
        r"""
        Method used to interact with the initialy specified `src.mlo_solver.MLOSolver.MLOSolver`, thus finding one solution of
        the optimization of the following system when \(\psi\) and \(\mu\) are conjunctions of
        `src.formula.nullaryFormula.constraint.linearConstraint.LinearConstraint`, with \(d\) the  `src.distance.distance_function.distanceFunction.DistanceFunction`
        given at the initialization of the class.

        \[
            \begin{cases}
                x \in \mathcal{M}(\psi) \\
                y \in \mathcal{M}(\mu) \\
                \text{minimize } d(x, y)
            \end{cases}
        \]

        Parameters
        ----------
        psi, mu : `src.formula.naryFormula.andOperator.And`
            \(\psi\) and \(\mu\), conjunctions of litterals as used in the optimization problem above.

        Returns
        -------
        Fraction
            Minimal distance (calculated with the `src.distance.distance_function.distanceFunction.DistanceFunction`
            given at the initialization of the class) that satisfies the optimization problem above. 
        src.formula.formula.Formula
            `src.formula.formula.Formula` representing a point \(y \in \mathcal{M}(\mu)\) that satisfies the optimization problem above. 
        """

        variables = list(And(psi,mu).getVariables())

        return self.findOneSolution(variables, psi, mu)    

    def removeNot(self, phi: And, epsilon = 0) -> And:
        r"""
        Method used to transform a conjunction of litterals (i.e `src.formula.nullaryFormula.constraint.linearConstraint.LinearConstraint`
        and `src.formula.unaryFormula.notOperator.Not` of `src.formula.nullaryFormula.constraint.linearConstraint.LinearConstraint`) in a conjunction of `src.formula.nullaryFormula.constraint.linearConstraint.LinearConstraint`,
        where every `src.formula.unaryFormula.notOperator.Not` of `src.formula.nullaryFormula.constraint.linearConstraint.LinearConstraint`
        \(\neg(\sum_{j=1}^{n}a_jx_j \leqslant b) = \sum_{j=1}^{n}a_jx_j > b\) is replaced by a `src.formula.nullaryFormula.constraint.linearConstraint.LinearConstraint`
        of the form \(\sum_{j=1}^{n}-a_jx_j \leqslant -b\).

        Parameters
        ----------
        phi : `src.formula.naryFormula.andOperator.And`
            Conjunctions of litterals to transform, as specified above.

        Returns
        -------
        src.formula.naryFormula.andOperator.And
            Conjunctions of `src.formula.nullaryFormula.constraint.linearConstraint.LinearConstraint` transformed from \(\varphi\),
            as specified above.

        """

        andSet = set()

        for andChild in phi.children:
            if isinstance(andChild, Not):
                andSet.add(andChild.copyNegLitteral(epsilon))
            else:
                andSet.add(andChild)
            
        return And(*andSet)

    def findOneSolutionWithLimit(self, variables : list[Variable], psi : And, mu : And, lambdaEpsilon) -> tuple[Fraction, Formula]:

            # Reorder variables order
            variables = list(variables)
            constraints = self.__buildConstraints(variables, psi, mu)

            # creation of the objective function
            obj = [0]*len(variables)*2
            constraintLambdaEpsilon = [0]*len(variables)*2
            for variable in variables:
                obj.append(self.__distanceFunction.getWeights()[variable])
                constraintLambdaEpsilon.append(-self.__distanceFunction.getWeights()[variable])
            constraints.append((constraintLambdaEpsilon, ConstraintOperator.LEQ, -lambdaEpsilon))
            res = self.__MLOSolver.solve(variables*3, obj, constraints)

            # interpretation of the mlo solver result
            if(res[0] == OptimizationValues.INFEASIBLE): 
                raise Exception("Optimize couple impossible") 
            
            values = res[1]
            resSet = set([])
            for i in range(0,len(variables)):
                lc = LinearConstraint("") 
                lc.variables = {variables[i]: Fraction(1)}
                lc.operator = ConstraintOperator.EQ
                lc.bound = Fraction(values[len(variables)+i])
                resSet.add(lc)
            return (res[2], And(*resSet))

    def optimizeCoupleWithLimit(self, psi : And, mu : And, lambdaEpsilon) -> tuple[Fraction, Formula]:

        variables = list(And(psi,mu).getVariables())

        return self.findOneSolutionWithLimit(variables, psi, mu, lambdaEpsilon)  