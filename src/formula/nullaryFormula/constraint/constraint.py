"""
Abstract Constraint class, representing a Constraint in PCMLC.
"""

from __future__ import annotations

from ..nullaryFormula import NullaryFormula

class Constraint(NullaryFormula):
    '''
    Abstract Constraint class, representing a Constraint in PCMLC.

    Attributes
    ----------
    children: None
        The children of the current node.
        Since a cosntraint doesn't have any, it's None.
    '''
    
        