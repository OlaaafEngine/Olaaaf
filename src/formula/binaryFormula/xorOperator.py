"""
Class representing the XOR operator.
"""

from __future__ import annotations

from .binaryFormula import BinaryFormula
from ...constants import Constants

# Typing only imports
from .. import Formula

class Xor(BinaryFormula):
    '''
     Class representing the XOR operator.

    Parameters
    ----------
    formulaTuple: tuple of Formulas
        The formulas meant as components of the XOR operator.

    Attributes
    ----------
    children: tuple of src.formula.formula.Formula
        The children of the current node.
    '''
    
    _symbol = "XOR"
    
    def _eliminate(self) -> Formula:
        '''
        Method returning the simplified form for the XOR operator, using only
        Not, And and Or.
        In this case, it's (a AND NOT b) OR (NOT a AND b).

        Returns
        -------
        src.formula.formula.Formula
            The simplified version of the implication operator.
            In this case, it's (a AND NOT b) OR (NOT a AND b).
        '''
        return (self.children[0] & ~self.children[1]) | (~self.children[0] & self.children[1])
        
    def __str__(self):
        return "(" + str(self.children[0]) + ") " + Constants.XOR_STRING_OPERATOR +  " (" + str(self.children[1]) + ")"

    def toLatex(self):
        return "(" + self.children[0].toLatex() + ") " + Constants.XOR_LATEX_OPERATOR +  " (" + self.children[1].toLatex() + ")"