"""
Abstract class, representing a Node with an arity of 0, i.e. without 
any children.
"""

from __future__ import annotations

from .. import Formula
#local import of Not

class NullaryFormula(Formula):
    '''
    Abstract class, representing a Node with an arity of 0, i.e. without 
    any children.

    Attributes
    ----------
    children: None
        The children of the current node. Since there isn't any, it's None.
    '''
    
    children = None
    
    def toDNF(self) -> Formula:
        '''
        Method returning the current Formula in Disjunctive Normal Form.
        Since the arity is null, returns self.

        Returns
        -------
        `olaaaf.formula.formula.Formula`
            The current Formula in Disjunctive Normal Form. Since the arity
            is null, returns self.
        '''
        
        return self
    
    def _toDNFNeg(self) -> Formula:
        '''
        Protected method used in the algorithm to recursivly determine the
        Disjunctive Normal Form, used when a Negation is in play instead of toDNF().
        Since the arity is null, returns Not(self).

        Returns
        -------
        `olaaaf.formula.formula.Formula`
            The current Formula in Disjunctive Normal Form under Negation. Since
            the arity is null, returns Not(self).
        '''
        from ..unaryFormula.notOperator import Not

        return Not(self)