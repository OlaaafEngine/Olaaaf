"""
Class representing the And operator as a relation with an arity equal or
greater than 1 in PCMLC as a syntax tree.
"""

from __future__ import annotations

from .naryFormula import NaryFormula
from ...constants import Constants
# local import of Or

# Typing only imports
from .. import Formula
from ..nullaryFormula import Constraint
from ...variable import Variable

class And(NaryFormula):
    '''
    Class representing the And operator as a relation with an arity equal or
    greater than 1 in PCMLC as a syntax tree.

    Parameters
    ----------
    *formulas: list of src.formula.formula.Formula
        The formulas meant as components of the And operator.

    Attributes
    ----------
    children: set of src.formula.formula.Formula
        The children of the current node.
    '''
    
    _symbol = "AND"
    
    def toDNF(self) -> Formula:
        '''
        Method returning the current Formula in Disjunctive Normal Form.

        Returns
        -------
        src.formula.formula.Formula
            The current Formula in Disjunctive Normal Form.
        '''
                
        from .orOperator import Or

        dnfChildren = {child.toDNF() for child in self.children}
			
        orChildren = set()
			
        for dnfChild in dnfChildren:
            if isinstance(dnfChild, Or):
                orChildren.add(dnfChild)

        dnfChildren = dnfChildren - orChildren
                
        if len(orChildren) == 0:
            return And(*dnfChildren)
        
        combinations = [{orChild} for orChild in orChildren.pop().children]

        tempcomb = []
        for orChild in orChildren:
            for elem in orChild.children:
                for comb in combinations:
                    tempc = comb.copy()
                    tempc.add(elem)
                    tempcomb.append(tempc)
            combinations = tempcomb
            tempcomb = []
        dnfFormula = {And(*comb.union(dnfChildren)) for comb in combinations}

        return Or(*dnfFormula)
    
    def _toDNFNeg(self) -> Formula:
        '''
        Protected method used in the algorithm to recursivly determine the
        Disjunctive Normal Form, used when a Negation is in play instead of toDNF().

        Returns
        -------
        src.formula.formula.Formula
            The current Formula in Disjunctive Normal Form under Negation.
        '''
        
        from .orOperator import Or
        
        return Or(*{child._toDNFNeg() for child in self.children})
    
    def toPCMLC(self, varDict) -> Formula:
        '''
        Method used to transform a `src.formula.formula.Formula` into a new one, in the PCMLC formalism.

        Returns
        -------
        src.formula.formula.Formula
            A `src.formula.formula.Formula` in the PCMLC formalism.
        '''
        return And(*{formul.toPCMLC(varDict) for formul in self.children})

    def _toPCMLCNeg(self, varDict) -> Formula:

        from .orOperator import Or

        return Or(*{formul._toPCMLCNeg(varDict) for formul in self.children})

    def getAdherence(self, var : Variable = None) -> list[list[Constraint]]:
        '''
        Returns a 2D list containing all the constraints of the adherence of 
        the Formula, in Disjunctive Normal Form.

        Attributes
        ----------
        var : src.variable.variable.Variable
            Variable used in case of inequality.


        Returns
        -------
        list of list of src.formula.nullaryFormula.constraint.constraint.Constraint
            2D list containing all the constraints of discute vraiment de l'implémentationthe adherence of the Formula,
            in Disjunctive Normal Form.
        '''
        
        res = []
        
        for children in self.children:
            for reschildren in children.getAdherence(var):
                for const in reschildren:  
                    res.append(const)
                    
        return [res]
    
    def _getAdherenceNeg(self, var : Variable = None)  -> list[list[Constraint]]:
        '''
        Protected method used in the algorithm to recursivly determine the
        constraints of the adherence of the Formula, used when a Negation is in play
        instead of getAdherence().

        Attributes
        ----------
        var : src.variable.variable.Variable
            Variable used in case of inequality.


        Returns
        -------
        list of list of src.formula.nullaryFormula.constraint.constraint.Constraint
            2D list containing all the constraints of the adherence of the Formula,
            in Disjunctive Normal Form under Negation.
        '''
        
        res = []
        
        for children in self.children:
            for reschildren in children._getAdherenceNeg(var):
                res.append(reschildren)
                
        return res

    def toLessOrEqConstraint(self):
        '''
        Method used to transform a `src.formula.formula.Formula` into another one, with only `src.formula.nullaryFormula.constraint.constraintOperator.ConstraintOperator.LEQ` constraints.

        Returns
        ------
        src.formula.formula.Formula
            A `src.formula.formula.Formula` with only `src.formula.nullaryFormula.constraint.constraintOperator.ConstraintOperator.LEQ` constraints.
        '''
        childrenModified = set()
        
        for child in self.children:
            childrenModified.add(child.toLessOrEqConstraint())

        return And(*childrenModified)
    
    def __str__(self):

        symbol = Constants.AND_STRING_OPERATOR

        if len(self.children) == 1:
            return str(list(self.children)[0])
        
        s = ""
        for child in self.children:
            s += "(" + str(child) + ") " + symbol + " "
        toRemove = len(symbol) + 2
        s = s[:-toRemove] + ""
        return s
    
    def toLatex(self):
        r"""
        Method returning a \(\LaTeX\) expression representing the Formula. Operators are customisable in `src.constants.Constants`.
        
        Returns
        -------
        String
            The \(\LaTeX\) expression representing the Formula.
        """

        symbol = Constants.AND_LATEX_OPERATOR

        if len(self.children) == 1:
            return list(self.children)[0].toLatex()
        
        s = ""
        for child in self.children:
            s += "(" + child.toLatex() + ") " + symbol + " "
        toRemove = len(symbol) + 2
        s = s[:-toRemove] + ""
        return s