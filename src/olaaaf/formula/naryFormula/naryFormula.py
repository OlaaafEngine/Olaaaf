"""
Abstract class, representing an operator with an arity equal or greater
than 1 in PCMLC as a syntax tree.
The operator is asummed symmetric.
"""

from __future__ import annotations

from .. import Formula
from ..formulaManager import FormulaManager

# Typing only imports
from ...variable import Variable

class NaryFormula(Formula):
    r"""
    Abstract class, representing an operator with an arity equal or greater
    than 1 in PCMLC as a syntax tree.
    The operator is asummed symmetric.

    Parameters
    ----------
    *formulas: list of `olaaaf.formula.formula.Formula`
        The formulas meant as components of the \(n\)-ary operator.

    Attributes
    ----------
    children: set of `olaaaf.formula.formula.Formula`
        The children of the current node.
    """
        
    def __init__(self, *formulas: Formula, fmName: str = None):
        
        self.children = set(formulas)
                
        if len(self.children) >= 1:
            tempF = set()
            
            for formul in self.children:
                if isinstance(formul, type(self)):
                    tempF.add(formul)
                    self.children = self.children | formul.children
                    
            self.children = self.children - tempF

        else:
            raise Exception("nary operators need at least one child")
        
        if(fmName is not None):
            FormulaManager.declare(fmName, self)

    def getVariables(self) -> set[Variable]:
        r"""
        Method recurcivly returning a set containing all the variables used in
        the n-ary Formula's children.

        Returns
        -------
        set of olaaaf.variable.variable.Variable
            All the variables used in the \(n\)-ary `olaaaf.formula.formula.Formula` or its children.
        """
        
        tempChildren = self.children.copy()
        variables = tempChildren.pop().getVariables()
        
        for child in tempChildren:
            variables = variables | child.getVariables()
            
        return variables
    
    def clone(self) -> Formula:
        """
        Method returning a clone of the current Formula.

        Returns
        -------
        `olaaaf.formula.formula.Formula`
            Clone of the current `olaaaf.formula.formula.Formula`.
        """

        clone = self.__class__(*self.children)
        return clone