"""
Abstract class, representing a unary operator.
"""

from __future__ import annotations

from .. import Formula
from ..formulaManager import FormulaManager

# Typing only imports
from ...variable.variable import Variable

class UnaryFormula(Formula):
    '''
    Abstract class, representing a unary operator.

    Attributes
    ----------
    children: `olaaaf.formula.formula.Formula`
        The child of the current node.
    '''

    def __init__(self, formulaInit: Formula, fmName: str = None):
        
        self.children = formulaInit

        if(fmName is not None):
            FormulaManager.declare(fmName, self)
        
    def getVariables(self) -> set[Variable]:
        '''
        Method recurcivly returning a set containing all the variables used in
        the Formula.

        Returns
        -------
        set of olaaaf.variable.variable.Variable
            All the variables used in the `olaaaf.formula.unaryFormula.unaryFormula.UnaryFormula`.
        '''
        
        return self.children.getVariables()
    
    def __hash__(self):
        return hash(self.children)