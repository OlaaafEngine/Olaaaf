r"""
Main class of the module, allowing the user to make the knowledge revision between two `olaaaf.formula.formula.Formula`
\(\psi\) and \(\mu\) that are constraints.
"""

from __future__ import annotations


from .formula import Formula, Or, And, UnaryFormula, NullaryFormula, LinearConstraint, Not, ConstraintOperator, PropositionalVariable, EnumeratedType
from .formulaInterpreter import FormulaInterpreter
from .mlo_solver import MLOSolver
from .distance import DistanceFunction
from .constants import Constants
from .simplificator import Simplificator
from .projector import Projector
from .variable import IntegerVariable

from fractions import Fraction
from tqdm import tqdm
import time
from contextlib import ExitStack

import math

class Revision:
    r"""
    Main class of the module, allowing the user to make the knowledge revision between two `olaaaf.formula.formula.Formula`
    \(\psi\) and \(\mu\) that are mixed integer linear constraints.

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
    onlyOneSolution : boolean, optional
        If set to `True`, the revision algorithm will only return one point that satisfies \(\psi \circ \mu\).
        If not, it will return all solutions.
        By default, this constant is set to whichever one was chosen in `olaaaf.constants.Constants`.
    verbose : boolean, optional
        If set to `True`, the revision algorithm will have a verbose display in the terminal.
        By default, this constant is set to whichever one was chosen in `olaaaf.constants.Constants`.
    projector : boolean, optional
        Projector algorithm to use, only necessary if `onlyOneSolution` is set to `False`.
    """
    
    __distance : DistanceFunction
    __interpreter : FormulaInterpreter
    __e2bConstraints: set[Formula]
    _onlyOneSolution: bool

    def __init__(self, solverInit : MLOSolver, distance : DistanceFunction, simplifiers : list[Simplificator] = [], onlyOneSolution: bool = Constants.ONLY_ONE_SOLUTION, verbose: bool = Constants.SET_VERBOSE, projector: Projector = None) -> None:        
        self.__distance = distance 
        self.__interpreter = FormulaInterpreter(solverInit, distance, simplifiers)
        self._onlyOneSolution = onlyOneSolution
        self.__verbose = verbose

        self.__e2bConstraints = set()

        self.__projector = projector

    def preload(self):
        r"""
        Methd used to preload the revision algorithm.

        This step is necessary before using `execute` since it translates every non-`olaaaf.formula.nullaryFormula.constraint.linearConstraint.LinearConstraint`
        into one and introduces new under-the-box variables that the user might want to use.
        """

        weights = self.__distance.getWeights()
        self.boolToInt = dict()

        for var in weights.copy().keys():

            if isinstance(var, PropositionalVariable):
                self.__b2iPreload(var, weights)

            if isinstance(var, EnumeratedType):

                self.__e2bConstraints.add(var.generateConstraints())

                for value in var.values.values():
                    weights[value] = weights[var]
                    self.__b2iPreload(value, weights)

    def __b2iPreload(self, var, weights):

        intVar = IntegerVariable.declare("b2i_" + var.name, lowerBound=Fraction(0), upperBound=Fraction(1))

        self.boolToInt[var] = intVar
        weights[intVar] = weights[var]

    def execute(self, psi : Formula, mu : Formula, withTableaux = True, withMaxDist = True) -> tuple[Fraction, Formula]:
        r"""
        Execute the revision of \(\psi\) by \(\mu\).

        Parameters
        ----------
        psi : `olaaaf.formula.formula.Formula`
            \(\psi\), left part of the knowledge revision operator and `olaaaf.formula.formula.Formula` that will be revised.
        mu : `olaaaf.formula.formula.Formula`
            \(\mu\), right part of the knowledge revision operator and `olaaaf.formula.formula.Formula` that will be used to revise \(\psi\) by.
        withTableaux: `boolean`
            Wether the analytic tableaux method should be used to prune unsatisfiable branches. By default, set to `True`.

        Returns
        -------
        Fraction
            Distance (calculated with the `olaaaf.distance.distance_function.distanceFunction.DistanceFunction`
            given at the initialization of the class) between \(\psi\) and \(\mu\).
        `olaaaf.formula.formula.Formula`
            Result of the knowledge revison of \(\psi\) by \(\mu\).
        """

        self.__withMaxDist = withMaxDist

        self.__timeStart = time.perf_counter()

        if len(self.__e2bConstraints) >= 1:
            psi &= And(*self.__e2bConstraints)
            mu &= And(*self.__e2bConstraints)

        if self.__verbose:
            print("\n" + self.__getTime(), "Transforming Psi in DNF form")

        if withTableaux:
            psiDNF = psi.toDNFWithTableaux().toPCMLC(self.boolToInt).toLessOrEqConstraint().toDNFWithTableaux()
            if not psiDNF:
                raise(AttributeError("Psi is not satisfiable"))
        else:
            psiDNF = psi.toPCMLC(self.boolToInt).toLessOrEqConstraint().toDNF()

        if self.__verbose:
            print("\n" + self.__getTime(), "Transforming Mu in DNF form")

        if withTableaux:
            muDNF = mu.toDNFWithTableaux().toPCMLC(self.boolToInt).toLessOrEqConstraint().toDNFWithTableaux()
            if not muDNF:
                raise(AttributeError("Mu is not satisfiable"))
        else:
            muDNF = mu.toPCMLC(self.boolToInt).toLessOrEqConstraint().toDNF()

        res = self.__executeDNF(self.__convertExplicit(psiDNF), self.__convertExplicit(muDNF))

        if self.__verbose:
            print("\n" + self.__getTime(), f"Solution found with distance of {res[0]}:\n")
            try:
                self.__organizedPrintResult(res[1])
            except:
                print(res[1])

        return res
        
    def __executeDNF(self, psi: Formula, mu: Formula) -> tuple[Fraction, Formula]:
        
        res = None
        disRes = None

        if self.__verbose:
            print("")
            psiIter = tqdm(psi.children, desc=f"{self.__getTime()} Testing satisfiability of every child of Psi", mininterval=0.5)
        else:
            psiIter = psi.children

        satPsi = set()
        for miniPsi in psiIter:
            if self.__interpreter.sat(miniPsi):
                satPsi.add(miniPsi)

        if len(satPsi) == 0:
            raise(AttributeError("Psi is not satisfiable"))

        if self.__verbose:
            print(self.__getTime(), f"{len(satPsi)} satisfiable children of Psi found\n")
            muIter = tqdm(mu.children, desc=f"{self.__getTime()} Testing satisfiability of every child of Mu", mininterval=0.5)
        else:
            muIter = mu.children
            
        satMu = set()
        for miniMu in muIter:
            if self.__interpreter.sat(miniMu):
                satMu.add(miniMu)

        if len(satMu) == 0:
            raise(AttributeError("Mu is not satisfiable"))

        maxIter = len(satPsi)*len(satMu)

        if self.__verbose:
            print(self.__getTime(), f"{len(satMu)} satisfiable children of Mu found")
            print("\n" + self.__getTime(), f"{maxIter} combinations of conjunctions found")

        if(self._onlyOneSolution):

            with ExitStack() as stack:

                if self.__verbose:
                    pbar = stack.enter_context(tqdm(total=maxIter, desc=f"{self.__getTime()} Revision of every combination", mininterval=0.5))

                for miniPsi in satPsi:
                    for miniMu in satMu:

                        # print("-----------------")
                        # print("miniPsi:", miniPsi)
                        # print("miniMu:", miniMu)
                        if self.__withMaxDist:      
                            lit = self.__executeLiteral(miniPsi, miniMu, disRes)
                        else:
                            lit = self.__executeLiteral(miniPsi, miniMu)

                        if lit is None:
                            pass
                        elif self.__interpreter.sat(lit[1]):

                            if not (lit[0] is None):
                                if (disRes is None):
                                    disRes = lit[0]
                                    res = lit[1]
                                elif (disRes > lit[0]):
                                    disRes = lit[0]
                                    res = lit[1]
                            else:
                                if (disRes is None) & (res is None):
                                    res = lit[1]
                        else:
                            print("\nWarning: one revised litteral isn't satisfiable, consider using a bigger Epsilon value for the distance function.\n")

                        if self.__verbose:
                            pbar.update(1)

        else:

            setRes = set()
            
            with ExitStack() as stack:

                if self.__verbose:
                    pbar = stack.enter_context(tqdm(total=maxIter, desc=f"{self.__getTime()} Revision of every combination", mininterval=0.5))

                for miniPsi in satPsi:
                    for miniMu in satMu:

                        if self.__withMaxDist:      
                            lit = self.__executeLiteral(miniPsi, miniMu, disRes)
                        else:
                            lit = self.__executeLiteral(miniPsi, miniMu)
                        
                        if lit is None:
                            pass
                        if not (lit[0] is None):
                            if (disRes is None):
                                disRes = lit[0]
                                setRes = {lit[1]}
                            elif (disRes == lit[0]):
                                setRes.add(lit[1])
                            elif (disRes > lit[0]):
                                disRes = lit[0]
                                setRes = {lit[1]}
                        else:
                            if (disRes is None):
                                setRes.add(lit[1])

                        if self.__verbose:
                            pbar.update(1)

            res = Or(*setRes).toDNF()

        return (disRes, self.__interpreter.simplifyMLC(res.toLessOrEqConstraint().toDNF()))
    
    def __executeLiteral(self, psi: Formula, mu: Formula, maxDist: Fraction = None) -> tuple[Fraction, Formula]:
        
        from . import InfeasableException

        epsilon = self.__distance._epsilon

        # second step: find dStar (and psiPrime if onlyOneSoltuion)
        try:
            dStar, psiPrime = self.__executeConstraint(self.__interpreter.removeNot(psi), self.__interpreter.removeNot(mu), maxDist)
        except InfeasableException as e:
            return None

        # third step: lambdaEpsilon
        if dStar % epsilon == 0:
            lambdaEpsilon = dStar
        else:
            lambdaEpsilon = epsilon * math.ceil(dStar / epsilon)
            
        # print(lambdaEpsilon, psiPrime)
        # fourth step: find psiPrime (only if not onlyOneSolution)
        if(not self._onlyOneSolution):
            psiPrime = self.__expand(psi, lambdaEpsilon)
    
        # fifth step
        if dStar % epsilon != 0:
            # print("dStar % epsilon != 0")
            if self._onlyOneSolution & (not self.__interpreter.sat(psiPrime & mu)):
                try:
                    psiPrime = self.__interpreter.optimizeCoupleWithLimit(self.__interpreter.removeNot(psi, epsilon), self.__interpreter.removeNot(mu, epsilon), lambdaEpsilon, maxDist)[1]
                except InfeasableException as e:
                    return None
            # print("psiPrime2:", psiPrime)
            return (lambdaEpsilon, psiPrime & mu)
        elif self.__interpreter.sat(psiPrime & mu):
            return (dStar, psiPrime & mu)
        else:
            # print("else")
            lambdaEpsilon = dStar + epsilon
            if (self._onlyOneSolution):
                try:
                    psiPrime = self.__interpreter.optimizeCoupleWithLimit(self.__interpreter.removeNot(psi, epsilon), self.__interpreter.removeNot(mu, epsilon), lambdaEpsilon, maxDist)[1]
                except InfeasableException as e:
                    return None
            else:
                psiPrime = self.__expand(psi, lambdaEpsilon)
            # print("psiPrime2:", psiPrime)
            return(dStar, psiPrime & mu)
    
    def __executeConstraint(self, phi: Formula, mu: Formula, maxDist: Fraction) -> tuple[Fraction, Formula]:
        return self.__interpreter.optimizeCouple(phi, mu, maxDist)
    
    def __convertExplicit(self, phi: Formula) -> Formula:
        
        if isinstance(phi, And):
            return Or(phi)
        elif isinstance(phi, UnaryFormula) | isinstance(phi, NullaryFormula):
            return Or(And(phi))
        else:
            orSet = set()
            for miniPhi in phi.children:
                if isinstance(miniPhi, And):
                    orSet.add(miniPhi)
                else:
                    orSet.add(And(miniPhi))
            return Or(*orSet)

    def __expand(self, psi: Formula, lambdaEpsilon: Fraction) -> Formula:
        
        yVariables = {v: v.__class__.declareAnonymous(ending = ("y" + str(v.name))) for v in psi.getVariables()}

        constraints = list()

        # Create x in M(psi) constraints and change variables
        for miniPsi in psi.children:
            if isinstance(miniPsi, Not):
                const = miniPsi.children.clone()
                iterVar = const.variables.copy()
                for key in iterVar:
                    const.variables[yVariables[key]] = const.variables[key]
                    del const.variables[key]
                constraints.append(Not(const))
            else:
                const = miniPsi.clone()
                iterVar = const.variables.copy()
                for key in iterVar:
                    const.variables[yVariables[key]] = const.variables[key]
                    del const.variables[key]
                constraints.append(const)

        # Add distance function constraints
        zVariables = {v: v.__class__.declareAnonymous(ending = ("z" + str(v.name))) for v in psi.getVariables()}
        for yVar in yVariables:
            z = zVariables[yVar]
            # Creating link between x, y and z
            const = LinearConstraint("")
            const.variables[yVar] = Fraction(-1)
            const.variables[yVariables[yVar]] = Fraction(1)
            const.variables[z] = Fraction(-1)
            const.operator = ConstraintOperator.LEQ
            const.bound = Fraction(0)
            constraints.append(const)
            const = LinearConstraint("")
            const.variables[yVar] = Fraction(1)
            const.variables[yVariables[yVar]] = Fraction(-1)
            const.variables[z] = Fraction(-1)
            const.operator = ConstraintOperator.LEQ
            const.bound = Fraction(0)
            constraints.append(const)
            # Keeping z in memory
            zVariables[yVar] = z

        # TODO pas sûr de mon code, à tester
        # TODO fonction de distance, les poids ?
        # Generate distance constraint
        distanceConstraint = LinearConstraint("")
        distanceConstraint.operator = ConstraintOperator.LEQ
        distanceConstraint.bound = lambdaEpsilon
        for z in zVariables:
            distanceConstraint.variables[zVariables[z]] = self.__distance.getWeights()[z]
        constraints.append(distanceConstraint)

        expandConstraint = And(*constraints)

        return self.__projector.projectOn(expandConstraint, yVariables.keys())
    
    def __getTime(self):

        timeNow = time.perf_counter()-self.__timeStart
        m = int(timeNow//60)

        s = timeNow%60
        sbfr = int(s)
        saftr = int((s-sbfr)*1000)

        return "{:0>2d}m{:0>2d}.{:0>3d}s |".format(m, sbfr, saftr)
    
    def __organizedPrintResult(self, res):

        variables = list()

        if self._onlyOneSolution:
            
            resAnd = None
            if len(res.children) > 1:
                raise AttributeError("res isn't a \"onlyoneSolution\"")
            else:
                for formula in res.children:
                    resAnd = formula

            for const in resAnd.children:

                lc = const.clone()

                if not lc.operator == ConstraintOperator.EQ:
                    # TODO, min/max pour déterminer bound de chaque variable
                    raise AttributeError("Can't print (yet) if not EQ")
                elif len(lc.variables) > 1:
                    raise AttributeError("Can't print (yet) if more than one variable per constraint")
                else:
                    var = lc.variables.popitem()
                    if (not var[0].name.startswith("b2i_")) & (not var[0].name[1].isnumeric()) & (not var[0].name.startswith("ak_")):
                        variables.append((var[0], lc.bound / var[1])) # Taking coefficients into account, even though it should always be 1

            maxVarLength = max([len(var[0].name) for var in variables])

            for var, value in sorted(variables, key=lambda x: x[0].name.lower()):

                if isinstance(var, IntegerVariable):
                    print("{} = {}".format(var.name.rjust(maxVarLength), int(value)))
                else:
                    if (value == int(value)):
                        print("{} = {}.".format(var.name.rjust(maxVarLength), int(value)))
                    elif (value >= 1e6) | (value <= 1e-3):
                        print("{} = {:#.3e}".format(var.name.rjust(maxVarLength), float(value)))
                    else:
                        print("{} = {:#.3g}".format(var.name.rjust(maxVarLength), float(value)))

            print("")

        else:
            raise NotImplementedError("")