"""
Class allowing `olaaaf.revision.Revision` to interact with a `olaaaf.mlo_solver.MLOSolver.MLOSolver`.
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
    Class allowing `olaaaf.revision.Revision` to interact with a `olaaaf.mlo_solver.MLOSolver.MLOSolver`.
    
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
        phi : `olaaaf.formula.formula.Formula`
            The `olaaaf.formula.formula.Formula` to simplify.

        Returns
        -------
        `olaaaf.formula.formula.Formula`
            The simplified `olaaaf.formula.formula.Formula`.
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
        Method used to verify the feasability of a `olaaaf.formula.formula.Formula`.

        Parameters
        ----------
        phi : `olaaaf.formula.formula.Formula`
            The `olaaaf.formula.formula.Formula` you want to verify the feasability.

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

    def findOneSolution(self, variables : list[Variable], psi : And, mu : And, maxDist: Fraction) -> tuple[Fraction, Formula]:
        r"""
        Method used to interact with the initialy specified `olaaaf.mlo_solver.MLOSolver.MLOSolver`, thus finding one solution of
        the optimization of the following system when \(\psi\) and \(\mu\) are conjunctions of
        `olaaaf.formula.nullaryFormula.constraint.linearConstraint.LinearConstraint`, with \(d\) the  `olaaaf.distance.distance_function.distanceFunction.DistanceFunction`
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
        variables : list of `olaaaf.variable.variable.Variable`
            List of all the `olaaaf.variable.variable.Variable` in use in both \(\psi\) and \(\mu\).
        psi, mu : `olaaaf.formula.naryFormula.andOperator.And`
            \(\psi\) and \(\mu\), conjunctions of litterals as used in the optimization problem above.

        Returns
        -------
        Fraction
            Minimal distance (calculated with the `olaaaf.distance.distance_function.distanceFunction.DistanceFunction`
            given at the initialization of the class) that satisfies the optimization problem above. 
        `olaaaf.formula.formula.Formula`
            `olaaaf.formula.formula.Formula` representing a point \(y \in \mathcal{M}(\mu)\) that satisfies the optimization problem above. 
        """

        from . import InfeasableException

        weights = self.__distanceFunction.getWeights()
        constraints = self.__buildConstraints(variables, psi, mu)

        if maxDist is not None:
            # Ptet faire ça plus tôt mais bon, ça fonctionne comme ça c'est du prototypage
            minDistLc = ([0] * len(variables) * 2 + [weights[variable] for variable in variables], ConstraintOperator.LEQ, maxDist)
            constraints.append(minDistLc)

        # Creation of the objective function
        obj = [0] * len(variables) * 2 + [weights[variable] for variable in variables]
        
        # Solve the optimization problem
        res = self.__MLOSolver.solve(variables * 3, obj, constraints)

        # Interpretation of the MLO solver result
        if res[0] == OptimizationValues.INFEASIBLE: 
            raise InfeasableException("Optimize couple impossible") 

        values = res[1]
        resSet = set()
        for i, variable in enumerate(variables):
            lc = LinearConstraint("")
            lc.variables = {variable: Fraction(1)}
            lc.operator = ConstraintOperator.EQ
            lc.bound = Fraction(values[len(variables) + i])
            resSet.add(lc)
        
        return res[2], And(*resSet)


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

    def optimizeCouple(self, psi : And, mu : And, maxDist: Fraction) -> tuple[Fraction, Formula]:
        r"""
        Method used to interact with the initialy specified `olaaaf.mlo_solver.MLOSolver.MLOSolver`, thus finding one solution of
        the optimization of the following system when \(\psi\) and \(\mu\) are conjunctions of
        `olaaaf.formula.nullaryFormula.constraint.linearConstraint.LinearConstraint`, with \(d\) the  `olaaaf.distance.distance_function.distanceFunction.DistanceFunction`
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
        psi, mu : `olaaaf.formula.naryFormula.andOperator.And`
            \(\psi\) and \(\mu\), conjunctions of litterals as used in the optimization problem above.

        Returns
        -------
        Fraction
            Minimal distance (calculated with the `olaaaf.distance.distance_function.distanceFunction.DistanceFunction`
            given at the initialization of the class) that satisfies the optimization problem above. 
        `olaaaf.formula.formula.Formula`
            `olaaaf.formula.formula.Formula` representing a point \(y \in \mathcal{M}(\mu)\) that satisfies the optimization problem above. 
        """

        variables = list(And(psi,mu).getVariables())

        return self.findOneSolution(variables, psi, mu, maxDist)    

    def removeNot(self, phi: And, epsilon = Fraction(0)) -> And:
        r"""
        Method used to transform a conjunction of litterals (i.e `olaaaf.formula.nullaryFormula.constraint.linearConstraint.LinearConstraint`
        and `olaaaf.formula.unaryFormula.notOperator.Not` of `olaaaf.formula.nullaryFormula.constraint.linearConstraint.LinearConstraint`) in a conjunction of `olaaaf.formula.nullaryFormula.constraint.linearConstraint.LinearConstraint`,
        where every `olaaaf.formula.unaryFormula.notOperator.Not` of `olaaaf.formula.nullaryFormula.constraint.linearConstraint.LinearConstraint`
        \(\neg(\sum_{j=1}^{n}a_jx_j \leqslant b) = \sum_{j=1}^{n}a_jx_j > b\) is replaced by a `olaaaf.formula.nullaryFormula.constraint.linearConstraint.LinearConstraint`
        of the form \(\sum_{j=1}^{n}-a_jx_j \leqslant -b\).

        Parameters
        ----------
        phi : `olaaaf.formula.naryFormula.andOperator.And`
            Conjunctions of litterals to transform, as specified above.
        epsilon : Fraction, optional
            The approximation for the removed Not. By default, equals \(0\).

        Returns
        -------
        olaaaf.formula.naryFormula.andOperator.And
            Conjunctions of `olaaaf.formula.nullaryFormula.constraint.linearConstraint.LinearConstraint` transformed from \(\varphi\),
            as specified above.

        """

        andSet = set()

        for andChild in phi.children:
            if isinstance(andChild, Not):
                andSet.add(andChild.copyNegLitteral(epsilon))
            else:
                andSet.add(andChild)
            
        return And(*andSet)

    def findOneSolutionWithLimit(self, variables : list[Variable], psi : And, mu : And, lambdaEpsilon, maxDist: Fraction) -> tuple[Fraction, Formula]:
        r"""
        Method used to interact with the initialy specified `olaaaf.mlo_solver.MLOSolver.MLOSolver`, thus finding one solution of
        the optimization of the following system when \(\psi\) and \(\mu\) are conjunctions of
        `olaaaf.formula.nullaryFormula.constraint.linearConstraint.LinearConstraint`, with \(d\) the  `olaaaf.distance.distance_function.distanceFunction.DistanceFunction`
        given at the initialization of the class.

        \[
            \begin{cases}
                x \in \mathcal{M}(\psi) \\
                y \in \mathcal{M}(\mu) \\
                d(x,y) \geq \lambda_\epsilon\\
                \text{minimize } d(x, y)
            \end{cases}
        \]

        Parameters
        ----------
        variables : list of `olaaaf.variable.variable.Variable`
            List of all the `olaaaf.variable.variable.Variable` in use in both \(\psi\) and \(\mu\).
        psi, mu : `olaaaf.formula.naryFormula.andOperator.And`
            \(\psi\) and \(\mu\), conjunctions of litterals as used in the optimization problem above.
        lambdaEpsilon: `fraction.Fraction`
            The \(\lambda_\epsilon\) specified in the system above.

        Returns
        -------
        Fraction
            Minimal distance (calculated with the `olaaaf.distance.distance_function.distanceFunction.DistanceFunction`
            given at the initialization of the class) that satisfies the optimization problem above. 
        `olaaaf.formula.formula.Formula`
            `olaaaf.formula.formula.Formula` representing a point \(y \in \mathcal{M}(\mu)\) that satisfies the optimization problem above. 
        """

        from . import InfeasableException

        # Reorder variables order
        variables = list(variables)
        constraints = self.__buildConstraints(variables, psi, mu)

        weights = self.__distanceFunction.getWeights()

        if maxDist is not None:
            # Ptet faire ça plus tôt mais bon, ça fonctionne comme ça c'est du prototypage
            minDistLc = ([0] * len(variables) * 2 + [weights[variable] for variable in variables], ConstraintOperator.LEQ, maxDist)
            constraints.append(minDistLc)

        # creation of the objective function
        obj = [0]*len(variables)*2
        constraintLambdaEpsilon = [0]*len(variables)*2
        for variable in variables:
            obj.append(weights[variable])
            constraintLambdaEpsilon.append(-weights[variable])
        constraints.append((constraintLambdaEpsilon, ConstraintOperator.LEQ, -lambdaEpsilon))

        res = self.__MLOSolver.solve(variables*3, obj, constraints)

        # interpretation of the mlo solver result
        if(res[0] == OptimizationValues.INFEASIBLE): 
            raise InfeasableException("Optimize couple impossible") 
        
        values = res[1]
        resSet = set([])
        for i in range(0,len(variables)):
            lc = LinearConstraint("") 
            lc.variables = {variables[i]: Fraction(1)}
            lc.operator = ConstraintOperator.EQ
            lc.bound = Fraction(values[len(variables)+i])
            resSet.add(lc)
        return (res[2], And(*resSet))

    def optimizeCoupleWithLimit(self, psi : And, mu : And, lambdaEpsilon, maxDist: Fraction) -> tuple[Fraction, Formula]:
        r"""
        Method used to interact with the initialy specified `olaaaf.mlo_solver.MLOSolver.MLOSolver`, thus finding one solution of
        the optimization of the following system when \(\psi\) and \(\mu\) are conjunctions of
        `olaaaf.formula.nullaryFormula.constraint.linearConstraint.LinearConstraint`, with \(d\) the  `olaaaf.distance.distance_function.distanceFunction.DistanceFunction`
        given at the initialization of the class.

        \[
            \begin{cases}
                x \in \mathcal{M}(\psi) \\
                y \in \mathcal{M}(\mu) \\
                d(x,y) \geq \lambda_\epsilon\\
                \text{minimize } d(x, y)
            \end{cases}
        \]

        Parameters
        ----------
        variables : list of `olaaaf.variable.variable.Variable`
            List of all the `olaaaf.variable.variable.Variable` in use in both \(\psi\) and \(\mu\).
        psi, mu : `olaaaf.formula.naryFormula.andOperator.And`
            \(\psi\) and \(\mu\), conjunctions of litterals as used in the optimization problem above.
        lambdaEpsilon: `fraction.Fraction`
            The \(\lambda_\epsilon\) specified in the system above.

        Returns
        -------
        Fraction
            Minimal distance (calculated with the `olaaaf.distance.distance_function.distanceFunction.DistanceFunction`
            given at the initialization of the class) that satisfies the optimization problem above. 
        `olaaaf.formula.formula.Formula`
            `olaaaf.formula.formula.Formula` representing a point \(y \in \mathcal{M}(\mu)\) that satisfies the optimization problem above. 
        """

        variables = list(And(psi,mu).getVariables())

        return self.findOneSolutionWithLimit(variables, psi, mu, lambdaEpsilon, maxDist)
    
