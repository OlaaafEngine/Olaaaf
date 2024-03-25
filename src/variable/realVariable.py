r"""
Class representing a real number Variable, meaning a number \(x \in \mathbb{R}\)
"""

from __future__ import annotations

from .variable import Variable
from .variableManager import VariableManager

from fractions import Fraction

class RealVariable(Variable):
    r"""
    Class, representing a real number `src.variable.variable.Variable`, meaning a `src.variable.variable.Variable` defined in \(\mathbb{R}\).
    Most of the time, you **shouldn't** use the constructor
    of `src.variable.realVariable.RealVariable` and should rather look into `src.variable.realVariable.RealVariable.declare`, 
    `src.variable.realVariable.RealVariable.declareBulk` or `src.variable.realVariable.RealVariable.declareAnonymous`.

    Parameters
    ----------
    name : String
        The name of the `src.variable.realVariable.RealVariable`.
    """
    
    def isInteger(self) -> bool:
        """
        Method used to known if the variable must have intergers values.

        Returns
        -------
        res:
            True if the variable must have intergers values
            else False
        """

        return False