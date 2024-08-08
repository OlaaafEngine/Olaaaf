from .domainKnowledge import DomainKnowledge

from ..formula import And, Formula, LinearConstraint, ConstraintOperator
from ..variable import Variable

from fractions import Fraction

class ConversionKnowledge(DomainKnowledge):

    __unitsConversion: dict[Variable, dict[Variable, Fraction]]

    def __init__(self) -> None:
        self.__unitsConversion = {}

    def addConversion(self, src: tuple[Variable, Fraction], trgt: tuple[Variable, Fraction]):

        src_var, src_coef = src
        trgt_var, trgt_coef = trgt

        if self.__unitsConversion.get(src_var) is None:
            self.__unitsConversion[src_var] = dict()
        self.__unitsConversion[src_var][trgt_var] = trgt_coef/src_coef
        
        if self.__unitsConversion.get(trgt_var) is None:
            self.__unitsConversion[trgt_var] = dict()
        self.__unitsConversion[trgt_var][src_var] = src_coef/trgt_coef

    def addConversions(self, conversions: list[tuple[tuple[Variable, Fraction], tuple[Variable, Fraction]]]):

        for conv in conversions:
            self.addConversion(*conv)

    def removeConversion(self, src: Variable, trgt: Variable):

        if (self.__unitsConversion.get(src) is not None) and (self.__unitsConversion[src].get(trgt) is not None):
            del self.__unitsConversion[src][trgt]
            if len(self.__unitsConversion[src]) == 0:
                del self.__unitsConversion[src]

        if (self.__unitsConversion.get(trgt) is not None) and (self.__unitsConversion[trgt].get(src) is not None):
            del self.__unitsConversion[trgt][src]
            if len(self.__unitsConversion[trgt]) == 0:
                del self.__unitsConversion[trgt]

    def getConversions(self):
        return self.__unitsConversion

    def toConstraints(self):
        
        copyCk = self.copy()
        fmSet = set()

        while len(copyCk.__unitsConversion) != 0:

            leftVar, unitConversions = copyCk.__unitsConversion.popitem()

            for rightVar, coef in unitConversions.items():

                lc = LinearConstraint("")

                lc.variables[rightVar] = Fraction(1)
                lc.variables[leftVar] = -coef
                lc.operator = ConstraintOperator.EQ
                lc.bound = 0

                fmSet.add(lc)
                copyCk.removeConversion(leftVar, rightVar)

        return And(*fmSet)
    
    def inferFrom(self, psi: Formula):
        
        inferedChildren = set()
        knownVariables = set()

        if isinstance(psi, And):
            for c in psi.children:
                inferedChildren |= (self.__inferFromLc(c, knownVariables))
        elif isinstance(psi, LinearConstraint):
            inferedChildren |= (self.__inferFromLc(psi, knownVariables))

        if len(inferedChildren) != 0:
            return psi & And(*inferedChildren)
                
        return psi
    
    def __inferFromLc(self, psi: LinearConstraint, knownVariables: set[Variable]):

        inferedChildren = set()

        if isinstance(psi, LinearConstraint) and (len(psi.variables) == 1) and (psi.operator == ConstraintOperator.EQ):
            
            lcVar = list(psi.variables.keys())[0]
            knownVariables.add(lcVar)

            toDoVariables = {(lcVar, 1)}

            while len(toDoVariables) != 0:
                
                (toDoVar, toDoCoef) = toDoVariables.pop()

                if self.__unitsConversion.get(toDoVar) is None:
                    continue

                for var, coef in self.__unitsConversion[toDoVar].items():

                    if (var not in knownVariables):

                        lc = LinearConstraint("")

                        lc.variables[var] = Fraction(1)
                        lc.operator = ConstraintOperator.EQ
                        lc.bound = psi.bound * coef*toDoCoef

                        inferedChildren.add(lc)
                        knownVariables.add(var)
                        toDoVariables.add((var, coef*toDoCoef))

        return inferedChildren
    
    def copy(self):

        from copy import deepcopy

        copy = ConversionKnowledge()
        copy.__unitsConversion = deepcopy(self.__unitsConversion)
        return copy