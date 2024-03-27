r"""
Class representing a real number Variable, meaning a number \(x \in \mathbb{R}\)
"""

from __future__ import annotations

from .variable import Variable
from .variableManager import VariableManager

from fractions import Fraction

class RealVariable(Variable):
    r"""
    Class, representing a real number `olaaaf.variable.variable.Variable`, meaning a `olaaaf.variable.variable.Variable` defined in \(\mathbb{R}\).
    Most of the time, you **shouldn't** use the constructor
    of `olaaaf.variable.realVariable.RealVariable` and should rather look into `olaaaf.variable.realVariable.RealVariable.declare`, 
    `olaaaf.variable.realVariable.RealVariable.declareBulk` or `olaaaf.variable.realVariable.RealVariable.declareAnonymous`.

    Parameters
    ----------
    name : String
        The name of the `olaaaf.variable.realVariable.RealVariable`.
    lowerBound, upperBound : `fraction.Fraction`, optional
        Fractions représenting respectively the lower and upper bounds of the variable. If not defined, it is considered as if the variable is unbounded.

    """
    
    def isInteger(self) -> bool:
        """
        Method used to known if the variable must have intergers values.

        Returns
        -------
        res:
            True if the variable must have integers values
            else False
        """

        return False