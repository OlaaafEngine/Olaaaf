"""
Class representing the equivalence operator.
"""

from __future__ import annotations

from .binaryFormula import BinaryFormula
from ...constants import Constants

# Typing only imports
from .. import Formula

class Equivalence(BinaryFormula):
    '''
    Class representing the equivalence operator.

    Parameters
    ----------
    formulaTuple: tuple of Formulas
        The formulas meant as components of the equivalence operator.

    Attributes
    ----------
    children: tuple of src.formula.formula.Formula
        The children of the current node.
    '''
    
    _symbol = "<->"
    
    def _eliminate(self) -> Formula:
        '''
        Method returning the simplified form for the equivalence operator,
        using only Not, And and Or.
        In this case, it's (a AND b) OR (NOT a AND NOT b).

        Returns
        -------
        src.formula.formula.Formula
            The simplified version of the equivalence operator.
            In this case, it's (a AND b) OR (NOT a AND NOT b).
        '''
           
        return (self.children[0] & self.children[1]) | (~self.children[0] & ~self.children[1])
    
    def __str__(self):
        return "(" + str(self.children[0]) + ") " + Constants.EQUIVALENCE_STRING_OPERATOR +  " (" + str(self.children[1]) + ")"

    def toLatex(self):
        return "(" + self.children[0].toLatex() + ") " + Constants.EQUIVALENCE_LATEX_OPERATOR +  " (" + self.children[1].toLatex() + ")"
