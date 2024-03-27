"""
Projector of a `olaaaf.formula.formula.Formula` to a sub-set of its variables, using floating numbers and SciPy's
`ConvexHull`.
"""

from __future__ import annotations

from ..formula import And, LinearConstraint, Not, ConstraintOperator
from ..simplificator import Simplificator
from .projector import Projector
from ..variable import Variable

import itertools
import numpy as np
from scipy.spatial import ConvexHull
from fractions import Fraction

np.set_printoptions(threshold=np.inf)

class FloatConvexHullProjector (Projector):
    r"""
    Projector of a `olaaaf.formula.formula.Formula` to a sub-set of its variables, using floating numbers and SciPy's
    `ConvexHull`.

    Parameters
    ----------
    rounding: int, optional
        The rounding you wish to have to eliminte floating point integers approximation errors. By default, is set to 12.
    simplifiers : list of olaaaf.simplificator.simplificator.Simplificator, optional
        List of all of the `olaaaf.simplificator.simplificator.Simplificator` that will be applied to the `olaaaf.formula.formula.Formula`, 
        in order given by the list.
    """

    __rounding: int
    __simplifier: list[Simplificator]

    """
    By default, used simplifier is a single Caron using lp_solve
    """
    def __init__(self, rounding: int = 12, simplifiers: list[Simplificator] = None):
        self.__rounding = rounding
        self.__simplifier = simplifiers

    def projectOn(self, phi: And, variables: set[Variable]):
        r"""
        Main method of `olaaaf.projector.floatConvexHullProjector.FloatConvexHullProjector`, allowing to project a given
        `olaaaf.formula.formula.Formula` to a subset of its `olaaaf.variable.variable.Variable`.

        Parameters
        ----------
        phi: `olaaaf.formula.formula.Formula`
            The`olaaaf.formula.formula.Formula`to project.
        variables: set of olaaaf.variable.variable.Variable
            The subset of `olaaaf.variable.variable.Variable` to project on.
        
        Returns
        -------
        `olaaaf.formula.formula.Formula`
            The projection of \(\varphi\) on the specified subset of its variables.
        """

        constraintSet = set()

        #print(phi)

        # First step: simplify
        for simplifier in self.__simplifier:
            phi = simplifier.run(phi.toLessOrEqConstraint().toDNF())

        #print(phi)

        # Second step: Get all variables
        allVariables = list(phi.getVariables())
        allVariables.sort(key = lambda v: v.name[::-1])
        #print(allVariables)
        variables = list(variables)
        variables.sort(key = lambda v: v.name[::-1])
        #print(variables)

        # Third step: Get all hyperplanes
        hyperplanes = list()

        for miniPhi in phi.children:

            hypVar = [np.array([])]

            if (isinstance(miniPhi, Not)):
                c = miniPhi.children.clone()
            else:
                c = miniPhi.clone()
            
            for var in allVariables:
                v = c.variables.get(var)
                if (v):
                    hypVar = np.append(hypVar, v)
                else:
                    hypVar = np.append(hypVar, Fraction(0))

            hyperplanes.append((hypVar, c.bound))

        #for h in hyperplanes:
            #print([float(a) for a in h[0]])

        # Fourth step: Get all non parallel combinations
        nonParallelCombinations = itertools.combinations(hyperplanes, len(phi.getVariables()))

#        for hyperplaneCombination in itertools.combinations(hyperplanes, len(phi.getVariables())):
#               
#            foundParallel = False
#       
#            for combinationPair in itertools.combinations(hyperplaneCombination, 2):
#       
#                x = combinationPair[0][0]
#                y = combinationPair[1][0]
#
#                ##print([float(a) for a in x])
#                ##print([float(a) for a in y])
#                ##print(np.dot(x,y)**2)
#                ##print(np.dot(x,x)*np.dot(y,y))
#                ##print("-")
#       
#                if (np.dot(x,y)**2 == np.dot(x,x)*np.dot(y,y)):
#                    foundParallel = True
#                    ##print("Bh")
#                    break
#        
#            if not foundParallel:
#                nonParallelCombinations.append(hyperplaneCombination)

        # Fifth step: Get all vertices from combinations
        vertices = list()

        for comb in nonParallelCombinations:

            a = []
            b = []

            for hyperplane in comb:
                a.append([float(x) for x in hyperplane[0]])
                b.append(float(hyperplane[1]))

            try:
                vertices.append(np.linalg.solve(a, b))
            except (np.linalg.LinAlgError):
                continue

        vertices = np.unique(np.array(vertices), axis=0)

        tempVertices = []

        for vertex in vertices:

            found = False
            for miniPhi in phi.children:

                if isinstance(miniPhi, Not):

                    sum = Fraction("0")
                    for var in miniPhi.children.variables:
                        sum += miniPhi.children.variables[var] * round(Fraction(vertex[allVariables.index(var)]), self.__rounding)

                    if sum < miniPhi.children.bound:
                        #print(sum)
                        #print(vertex)
                        #print(miniPhi)
                        found = True
                        break

                else:

                    sum = Fraction("0")
                    for var in miniPhi.variables:
                        sum += miniPhi.variables[var] * round(Fraction(vertex[allVariables.index(var)]), self.__rounding)

                    if sum > miniPhi.bound:
                        #print(sum)
                        #print(vertex)
                        #print(miniPhi)
                        found = True
                        break

            if not found:
                tempVertices.append(vertex)

        vertices = np.array(tempVertices)

        #print(vertices)
        #print(len(vertices))

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
        #print(projectedVertices)

        # Seventh step: Get convex Hull
        try:
            hull = ConvexHull(projectedVertices)
        except:

            # Remove fixed dimensions

            transposed = np.transpose(projectedVertices)

            index = 0

            toRemoveIndex = []
            toRemoveVar = []

            for dim in transposed:

                foundDifferent = False

                for c in dim:
                    if not(c == dim[0]):
                        foundDifferent = True
                        break

                if not foundDifferent:

                    toRemoveIndex.append(index)
                    toRemoveVar.append(variables[index])
                    
                    lc = LinearConstraint("")
                    lc.variables[variables[index]] = Fraction(1)
                    lc.operator = ConstraintOperator.EQ
                    lc.bound = round(Fraction(dim[0]), self.__rounding)

                    constraintSet.add(lc.clone())
                
                index += 1
            
            transposed = np.delete(transposed, toRemoveIndex, axis = 0)
            variables = [i for i in variables if i not in toRemoveVar]

            projectedVertices = np.transpose(transposed)

            hull = ConvexHull(projectedVertices)

        finally:

            if projectedVertices.shape[1] == 1:

                # If project on one dimension
                max = projectedVertices[-1][0]
                min = max

                # If only one dimension, do something
                for vertex in projectedVertices:
                    val = vertex[0]
                    if val >= max:
                        max = val
                    elif val <= min:
                        min = val
                    
                minLc = LinearConstraint("")
                minLc.variables[variables[0]] = Fraction(1)
                minLc.operator = ConstraintOperator.GEQ
                minLc.bound = round(Fraction(min), self.__rounding)
                constraintSet.add(minLc)

                maxLc = LinearConstraint("")
                maxLc.variables[variables[0]] = Fraction(1)
                maxLc.operator = ConstraintOperator.LEQ
                maxLc.bound = round(Fraction(max), self.__rounding)
                constraintSet.add(maxLc)

            else:

                if len(projectedVertices) >= 3:

                    # Else, eighth step: Get constraints from hull simplices
                    for simplex in hull.simplices:

                        # Get centroid and normal
                        points = projectedVertices[simplex]
                        centroid = np.mean(points, axis=0)
                        u, s, vh = np.linalg.svd(points - centroid, full_matrices=False)
                        normal = vh[-1]
                        normal = normal * np.linalg.norm(normal, 1)
                        normal = [round(Fraction(n), self.__rounding) for n in normal]
                        
                        #print(points)

                        # Build constraint
                        lc = LinearConstraint("")
                        for i in range(len(normal)):
                            if normal[i] != 0:
                                lc.variables[variables[i]] = normal[i]
                        lc.bound = round(Fraction(np.sum(normal * centroid)), self.__rounding)

                        s = ""
                        for vertex in projectedVertices:

                            sum = Fraction("0")
                            for i in range(len(variables)):
                                coef = lc.variables.get(variables[i])
                                if coef:
                                    ##print(coef)
                                    ##print(vertex)
                                    sum += round(Fraction(vertex[i]), self.__rounding)*coef
                                    ##print(sum)
                            if(sum < lc.bound):
                                s+= "< " + str(lc.bound)
                                lc.operator = ConstraintOperator.LEQ
                                break
                            elif(sum > lc.bound):
                                s += "> " + str(lc.bound)
                                lc.operator = ConstraintOperator.GEQ
                                break
                            
                        if sum is None:
                            lc.operator = ConstraintOperator.EQ

                        #print(simplex, ":", sum, s, ":", lc)

                        constraintSet.add(lc)

                elif len(projectedVertices) == 2:

                    constraintSet.add(self.__createConstraintSegment(projectedVertices[0], projectedVertices[1], variables))

                elif len(projectedVertices) == 1:

                    constraintSet.add(self.__createConstraintPoint(projectedVertices[0], variables))

                else:
                    print("Euuuuh")           

            return And(*constraintSet)

    def __createConstraintSegment(self, x, y, variables):
        
        # Get centroid and normal
        points = np.array([x, y])
        centroid = np.mean(points, axis=0)
        u, s, vh = np.linalg.svd(points - centroid, full_matrices=False)
        normal = vh[-1]
        normal = normal * np.linalg.norm(normal, 1)
        normal = [round(Fraction(n), self.__rounding) for n in normal]
        
        # Build constraint
        lc = LinearConstraint("")
        for i in range(len(normal)):
            if normal[i] != 0:
                lc.variables[variables[i]] = normal[i]
        lc.bound = round(Fraction(np.sum(normal * centroid)), self.__rounding)
        lc.operator = ConstraintOperator.EQ

        constraints = And(lc)

        constraints = constraints & self.__createConstraintPointSegment(x, y, variables) & self.__createConstraintPointSegment(y, x, variables)

        return constraints
    
    def __createConstraintPoint(self, point, variables):

        constraintSet = set()

        for i in range(len(point)):

            lc = LinearConstraint("")

            lc.variables[variables[i]] = Fraction(1)
            lc.bound = round(Fraction(point[i]), self.__rounding)
            lc.operator = ConstraintOperator.EQ

            constraintSet.add(lc)

        return And(*constraintSet)
    
    def __createConstraintPointSegment(self, x, y, variables):

        constraintSet = self.__createConstraintPoint(x, variables).children

        for lc in constraintSet:

            sum = Fraction("0")
            for i in range(len(variables)):
                coef = lc.variables.get(variables[i])
                if coef:
                    ##print(coef)
                    ##print(vertex)
                    sum += round(Fraction(y[i]), self.__rounding)*coef
                    ##print(sum)

                if(sum < lc.bound):
                    s+= "< " + str(lc.bound)
                    lc.operator = ConstraintOperator.LEQ
                    break
                elif(sum > lc.bound):
                    s += "> " + str(lc.bound)
                    lc.operator = ConstraintOperator.GEQ
                    break
                
            if sum is None:
                lc.operator = ConstraintOperator.EQ

            #print(simplex, ":", sum, s, ":", lc)

        return And(*constraintSet)