"""
Reprensation of the Constraint operators
"""

from __future__ import annotations

from ....constants import Constants

import enum

class ConstraintOperator(enum.Enum):
    LEQ = "<="
    GEQ = ">="
    EQ = "="

    def getLatexOperator(self):

        match(self):
            case ConstraintOperator.LEQ:
                return Constants.LEQ_LATEX_OPERATOR
            case ConstraintOperator.EQ:
                return Constants.EQ_LATEX_OPERATOR
            case ConstraintOperator.GEQ:
                return Constants.GEQ_LATEX_OPERATOR