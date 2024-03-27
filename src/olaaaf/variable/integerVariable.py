r"""
Class representing an integer number Variable, meaning a number \(x \in \mathbb{Z}\)
"""

from __future__ import annotations

from .variable import Variable
from .variableManager import VariableManager

from fractions import Fraction

class IntegerVariable(Variable):
    r"""
    Class, representing an integer number `olaaaf.variable.variable.Variable`, meaning a `olaaaf.variable.variable.Variable` defined in \(\mathbb{Z}\).
    Most of the time, you **shouldn't** use the constructor
    of `olaaaf.variable.integerVariable.IntegerVariable` and should rather look into `olaaaf.variable.integerVariable.IntegerVariable.declare`, 
    `olaaaf.variable.integerVariable.IntegerVariable.declareBulk` or `olaaaf.variable.integerVariable.IntegerVariable.declareAnonymous`.

    Parameters
    ----------
    name : String
        The name of the `olaaaf.variable.integerVariable.IntegerVariable`.
    lowerBound, upperBound : `fraction.Fraction`, optional
        Fractions représenting respectively the lower and upper bounds of the variable. If not defined, it is considered as if the variable is unbounded.

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

        return True