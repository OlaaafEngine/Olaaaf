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
    children: tuple of `olaaaf.formula.formula.Formula`
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
        formula: `olaaaf.formula.formula.Formula`
            The simplified version of the binary operator.
        '''
        
        pass
    
    def getVariables(self) -> set[Variable]:
        '''
        Method recurcivly returning a set containing all the variables used in
        the Formula.

        Returns
        -------
        variables: set of olaaaf.variable.variable.Variable
            All the variables used in the Formula.
        '''
        
        return self.children[0].getVariables().union(self.children[1].getVariables())
    
    def toDNF(self) -> Formula:
        '''
        Method returning the current Formula in Disjunctive Normal Form.

        Returns
        -------
        variables: `olaaaf.formula.formula.Formula`
            The current Formula in Disjunctive Normal Form.
        '''
        
        return self._eliminate().toDNF()
    
    def _toDNFNeg(self) -> Formula:
        '''
        Protected method used in the algorithm to recursivly determine the
        Disjunctive Normal Form, used when a Negation is in play instead of toDNF().

        Returns
        -------
        variables: `olaaaf.formula.formula.Formula`
            The current Formula in Disjunctive Normal Form under Negation.
        '''
        
        return self._eliminate()._toDNFNeg()
    
    def toLessOrEqConstraint(self):
        '''
        Method used to transform a `olaaaf.formula.formula.Formula` into another one, with only `olaaaf.formula.nullaryFormula.constraint.constraintOperator.ConstraintOperator.LEQ` constraints.

        Returns
        ------
        `olaaaf.formula.formula.Formula`
            A `olaaaf.formula.formula.Formula` with only `olaaaf.formula.nullaryFormula.constraint.constraintOperator.ConstraintOperator.LEQ` constraints.
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
        res: list of list of olaaaf.formula.nullaryFormula.constraint.constraint.Constraint
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
        res: list of list of olaaaf.formula.nullaryFormula.constraint.constraint.Constraint
            2D list containing all the constraints of the adherence of the Formula,
            in Disjunctive Normal Form under Negation.
        '''
        return self._eliminate()._getAdherenceNeg(var)
    
    def toPCMLC(self, varDict) -> Formula:
        '''
        Method used to transform a `olaaaf.formula.formula.Formula` into a new one, in the PCMLC formalism.

        Parameters
        ----------
        varDict : dictionnary
            Dictionnary used to tell which variable should be replaced by which.

        Returns
        -------
        `olaaaf.formula.formula.Formula`
            A `olaaaf.formula.formula.Formula` in the PCMLC formalism.
        '''
        return self._eliminate().toPCMLC(varDict)
    
    def _toPCMLCNeg(self, varDict) -> Formula:
        return self._eliminate()._toPCMLCNeg(varDict)
    
    def _getBranches(self):
        '''
        Method used to get the branches of the analytic tableau representing the `olaaaf.formula.formula.Formula`,
        automatically removing any closed one once it's caught. 

        Returns
        ------
        `list[dict[Constraint, bool]]`
            A list of all branches, represented by a dictionnary matching every atom
            `olaaaf.formula.nullaryFormula.constraint.constraint.Constraint` to a `bool` representing if it has a negation (`False`)
            or not (`True`).
            If all branches are closed, return `None`.
        '''

        return self._eliminate()._getBranches()

    def _getBranchesNeg(self):
        '''
        Method used to get the branches of the analytic tableau representing the `olaaaf.formula.formula.Formula`,
        automatically removing any closed one once it's caught. 
        Used when a Negation is in play instead of `_getBranches()`.

        Returns
        ------
        `list[dict[Constraint, bool]]`
            A list of all branches, represented by a dictionnary matching every atom
            `olaaaf.formula.nullaryFormula.constraint.constraint.Constraint` to a `bool` representing if it has a negation (`False`)
            or not (`True`).
            If all branches are closed, return `None`.
        '''

        return self._eliminate()._getBranchesNeg()