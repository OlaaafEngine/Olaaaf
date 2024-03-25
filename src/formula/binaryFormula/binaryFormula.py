"""
Abstract class, representing a binary operator.
"""

from __future__ import annotations

from ..formula import Formula
from ..formulaManager import FormulaManager

# Typing only imports
from ...variable import Variable
from ..nullaryFormula import Constraint

from abc import abstractmethod

class BinaryFormula(Formula):
    '''
    Abstract class, representing a binary operator.

    Parameters
    ----------
    formulaTuple: tuple of Formulas
        The formulas meant as components of the binary operator.

    Attributes
    ----------
    children: tuple of src.formula.formula.Formula
        The children of the current node.
    '''
        
    def __init__(self, formulaLeft: Formula, formulaRight: Formula, fmName: str = None):

        self.children = (formulaLeft, formulaRight)

        if(fmName is not None):
            FormulaManager.declare(fmName, self)

    @abstractmethod
    def _eliminate(self) -> Formula:
        '''
        Method returning the simplified form for the binary operator, using only
        Not, And and Or.

        Returns
        -------
        formula: src.formula.formula.Formula
            The simplified version of the binary operator.
        '''
        
        pass
    
    def getVariables(self) -> set[Variable]:
        '''
        Method recurcivly returning a set containing all the variables used in
        the Formula.

        Returns
        -------
        variables: set of src.variable.variable.Variable
            All the variables used in the Formula.
        '''
        
        return self.children[0].getVariables().union(self.children[1].getVariables())
    
    def toDNF(self) -> Formula:
        '''
        Method returning the current Formula in Disjunctive Normal Form.

        Returns
        -------
        variables: src.formula.formula.Formula
            The current Formula in Disjunctive Normal Form.
        '''
        
        return self._eliminate().toDNF()
    
    def _toDNFNeg(self) -> Formula:
        '''
        Protected method used in the algorithm to recursivly determine the
        Disjunctive Normal Form, used when a Negation is in play instead of toDNF().

        Returns
        -------
        variables: src.formula.formula.Formula
            The current Formula in Disjunctive Normal Form under Negation.
        '''
        
        return self._eliminate()._toDNFNeg()
    
    def toLessOrEqConstraint(self):
        '''
        Method used to transform a `src.formula.formula.Formula` into another one, with only `src.formula.nullaryFormula.constraint.constraintOperator.ConstraintOperator.LEQ` constraints.

        Returns
        ------
        src.formula.formula.Formula
            A `src.formula.formula.Formula` with only `src.formula.nullaryFormula.constraint.constraintOperator.ConstraintOperator.LEQ` constraints.
        '''
        childrenModified = []
        for child in self.children: childrenModified.append(child.toLessOrEqConstraint())

        return self.__class__(childrenModified[0], childrenModified[1])
        
    def getAdherence(self, var : Variable = None) -> list[list[Constraint]]:
        '''
        Returns a 2D list containing all the constraints of the adherence of 
        the Formula, in Disjunctive Normal Form.

        Attributes
        ----------
        var : variable used in case of inequality

        Returns
        -------
        res: list of list of src.formula.nullaryFormula.constraint.constraint.Constraint
            2D list containing all the constraints of discute vraiment de l'implémentationthe adherence of the Formula,
            in Disjunctive Normal Form.
        '''
        return self._eliminate().getAdherence(var)

    def _getAdherenceNeg(self, var : Variable = None)  -> list[list[Constraint]]:
        '''
        Protected method used in the algorithm to recursivly determine the
        constraints of the adherence of the Formula, used when a Negation is in play
        instead of getAdherence().

        Attributes
        ----------
        var : variable used in case of inequality

        Returns
        -------
        res: list of list of src.formula.nullaryFormula.constraint.constraint.Constraint
            2D list containing all the constraints of the adherence of the Formula,
            in Disjunctive Normal Form under Negation.
        '''
        return self._eliminate()._getAdherenceNeg(var)
    
    def toPCMLC(self, varDict) -> Formula:
        '''
        Method used to transform a `src.formula.formula.Formula` into a new one, in the PCMLC formalism.

        Returns
        -------
        src.formula.formula.Formula
            A `src.formula.formula.Formula` in the PCMLC formalism.
        '''
        return self._eliminate().toPCMLC(varDict)
    
    def _toPCMLCNeg(self, varDict) -> Formula:
        return self._eliminate()._toPCMLCNeg(varDict)