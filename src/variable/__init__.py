"""
Representation of variables and useful tools to use them.
Variable are split depending on what type of variables they represent, namely `src.variable.integerVariable.IntegerVariable`
and `src.variable.realVariable.RealVariable`, but the abstract class `src.variable.variable.Variable` should allow the user to
implement their own variables if they so choose.
"""

from .variable import Variable
from .integerVariable import IntegerVariable
from .realVariable import RealVariable
from .variableManager import VariableManager