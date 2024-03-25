"""
Class representing the Bottom constant.
"""

from __future__ import annotations

from .nullaryFormula import NullaryFormula

from ...constants import Constants

# Typing only imports
from ...variable.variable import Variable
from .constraint.constraint import Constraint

class Bottom(NullaryFormula):
    '''
    Class representing the Bottom constant.

    Attributes
    ----------
    children: None 
        The children of the current node.
    '''
        
    def __init__(self):
        raise NotImplementedError(self.__class__.__name__ + ' is not yet implemented') 
    
    def getVariables(self) -> set[Variable]:
        '''
        Method recurcivly returning a set containing all the variables used in
        Bottom, so None.

        Returns
        -------
        set of src.variable.variable.Variable
            All the variables used in Bottom, so None.
        '''
        
        return None
    
    def getAdherence(self) -> list[list[Constraint]]:
        '''
        Returns a 2D list containing all the constraints of the adherence of 
        Bottom, in Disjunctive Normal Form. In this case, an empty list.

        Returns
        -------
        list of list of src.formula.nullaryFormula.constraint.constraint.Constraint
            2D list containing all the constraints of the adherence of Bottom,
            in Disjunctive Normal Form. In this case, an empty list.
        '''
        
        return []
    
    def _getAdherenceNeg(self) -> list[list[Constraint]]:
        '''
        Protected method used in the algorithm to recursivly determine the
        constraints of the adherence of Bottom, used when a Negation is in play
        instead of getAdherence(). In this case, an empty list.

        Returns
        -------
        list of list of src.formula.nullaryFormula.constraint.constraint.Constraint
            2D list containing all the constraints of the adherence of Bottom,
            in Disjunctive Normal Form under Negation. In this case, an empty list. 
        '''
        
        return []
    
    def __str__(self):
        return Constants.BOTTOM_STRING_OPERATOR
    
    def toLatex(self):
        r"""
        Method returning a \(\LaTeX\) expression representing the Formula. Operators are customisable in `src.constants.Constants`.
        
        Returns
        -------
        String
            The \(\LaTeX\) expression representing the Formula.
        """
                
        return Constants.BOTTOM_LATEX_OPERATOR