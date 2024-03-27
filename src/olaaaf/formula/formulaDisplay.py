"""
Utility class, allowing the user to get a visualisation of a `olaaaf.formula.formula.Formula`.
"""

from __future__ import annotations

from . import Formula
from .naryFormula import And, Or
from .unaryFormula import Not
from ..variable.variable import Variable

import matplotlib.pyplot as plt
import numpy as np
from fractions import Fraction
import itertools
from scipy.spatial import ConvexHull
class FormulaDisplay:
    '''
    FormulaDisplay class, using for get a visualisation of a Formula.

    Attributes
    ----------
        _solver : MLOSolver
            A solver that used by the display
    '''
    def __init__(self):
        from ..mlo_solver.LPSolverRounded import LPSolverRounded

        self._solver = LPSolverRounded()

    def display(self, formulas: dict[Formula, str], variables: set[Variable]):
        '''
        Function used to display a formula in dnf form.

        Parameters
        ----------
        formulas : dictionary of String with`olaaaf.formula.formula.Formula`as key
            Dictionary witch link a formula with a color
        variables: set of olaaaf.variable.variable.Variable
            List of variables witch will be displayed
        '''
        for phi in formulas.keys():
            key = phi
            phi = phi.toDNF()
            try:
                if isinstance(phi, Or):
                    for miniPhi in phi.children:
                        try:
                            self.__displayConjunction(miniPhi.toLessOrEqConstraint(), variables, formulas[key])
                        except Exception as e:
                            print("can't display : ", miniPhi)
                            print("error : ", e)
                            pass
                if isinstance(phi, And):
                    self.__displayConjunction(phi.toLessOrEqConstraint(), variables, formulas[key])
                else:
                    #print("Non.")
                    pass
            except:
                #print("can't display : ", key)
                pass

        plt.show()

    def __test(self, phi:Formula, variables:list[Variable], values:list[Fraction]):
        '''
        Function used to test if an interpretion satisfer une formule(oui bon là c'est pas anglais faut changer).

        Params
        ----------
        phi:
            A formula
        variables: set of olaaaf.variable.variable.Variable
            List of variables 
        values : list of fracitons.Fraction
            List of values for each formulas
        '''
        res : bool
        res = True
        for litteral in phi.children:
            constraint = litteral
            if isinstance(litteral, Not):
                constraint = litteral.children
            sum = 0
            for i in range(0, len(values)):
                sum += values[i] * constraint.variables[variables[i]] if variables[i] in constraint.getVariables() else 0
            if isinstance(litteral, Not):
                res = res and sum > constraint.bound
            else:
                 res = res and sum <= constraint.bound
        return res

    def __displayConjunction(self, phi: Formula, variables: set[Variable], color):

        # Second step: Get all variables
        allVariables = list(phi.getVariables())
        allVariables.sort(key = lambda v: v.name[::-1])
        variables = list(variables)
        variables.sort(key = lambda v: v.name[::-1])
        # Third step: Get all hyperplanes
        hyperplanes = list()

        for miniPhi in phi.children:

            hypVar = [np.array([])]

            if (isinstance(miniPhi, Not)):
                c = miniPhi.children.clone()
            else:
                c = miniPhi.clone()
            
            s = ""
            for var in allVariables:
                s += str(var) + ", "
                v = c.variables.get(var)
                if (v):
                    hypVar = np.append(hypVar, v)
                else:
                    hypVar = np.append(hypVar, Fraction(0))

            hyperplanes.append((hypVar, c.bound))

        # Fourth step: Get all non parallel combinations
        nonParallelCombinations = itertools.combinations(hyperplanes, len(phi.getVariables()))

        # Fifth step: Get all vertices from combinations
        vertices = list()

        i = 0
        for comb in nonParallelCombinations:

            a = []
            b = []

            for hyperplane in comb:
                a.append([float(x) for x in hyperplane[0]])
                b.append(float(hyperplane[1]))

            try:
                vertices.append(np.linalg.solve(a, b))
            except (np.linalg.LinAlgError):
                #print(str(i) + "Ah")
                i += 1
                continue

        vertices = np.unique(np.array(vertices), axis=0)

        tempVertices = []

        for vertex in vertices:

            found = False
            for miniPhi2 in phi.children:
                if (isinstance(miniPhi2, Not)):
                    constraint = miniPhi2.children.clone()
                    for var in constraint.variables.keys():
                        constraint.variables[var] *= -1
                    constraint.bound *= -1
                else:
                    constraint = miniPhi2.clone()

                sum = Fraction("0")
                for var in constraint.variables:
                    sum += constraint.variables[var] * round(Fraction(vertex[variables.index(var)]), 12)

                if sum > constraint.bound:
                    found = True
                    break

            if not found:
                tempVertices.append(vertex)

        vertices = np.array(tempVertices)

        if len(vertices) == 0:
            raise RuntimeError("Couldn't find any vertex")
        
        # Sixth step: project all vertices

        variablesBool = np.array([], dtype=bool)
        newVar = np.array([])
        for var in allVariables:
            if var in variables:
                variables = np.delete(variables, np.where(variables == var))
                newVar = np.append(newVar, var)
                variablesBool = np.append(variablesBool, True)
            else:
                variablesBool = np.append(variablesBool, False)

        projectedVertices = list()
        for v in vertices:
            projectedVertices.append(v[variablesBool])

        variables = newVar

        projectedVertices = np.unique(np.array(projectedVertices), axis=0)
        # Seventh step: Get convex Hull
        try:
            hull = ConvexHull(projectedVertices)
        except:
            pass
        finally:
            if (len(projectedVertices) == 2) & (len(projectedVertices[0]) == 1): 
                projectedVertices = [[projectedVertices[0][0], projectedVertices[1][0]]]
            if(len(projectedVertices) >= 3):
                # CA CA MARCHE QUE POUR UN TRUC QUI A 3 POINTS OU PLUS, FAIT UN CHECK ICI SUR LE NOMBRE DE PROJECTEDVERTICES JE PENSE
                test = []
                test2 = []
                for simplex in hull.simplices:
                    x = (projectedVertices[simplex, 0][0] + projectedVertices[simplex, 0][1])/2
                    y = (projectedVertices[simplex, 1][0] + projectedVertices[simplex, 1][1])/2
                    if self.__test(phi, variables, (x,y)):
                        plt.plot(projectedVertices[simplex, 0], projectedVertices[simplex, 1], color, marker='o')
                    else:
                        plt.plot(projectedVertices[simplex, 0], projectedVertices[simplex, 1], color, marker='o', linestyle='dashed')
                for ver in projectedVertices[hull.vertices]:
                    test.append(ver[0])
                    test2.append(ver[1])

                plt.fill(test, test2, color, alpha=0.3)
            elif(len(projectedVertices) == 2) :
                    test = [[projectedVertices[0][0], projectedVertices[1][0]], [projectedVertices[0][1], projectedVertices[1][1]]]
                    plt.plot(test[0],test[1], color=color, marker='o')
            elif(len(projectedVertices) == 1):
                plt.plot([vertex[0]], [vertex[1]], color=color, marker='o')