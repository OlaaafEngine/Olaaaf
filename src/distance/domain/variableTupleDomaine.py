"""
Class reprensenting a domain on which a distance function is defined on a tuple of `src.variable.variable.Variable`.
"""

from __future__ import annotations

from ...variable.variable import Variable
from .domain import Domain

class VariableTupleDomaine(Domain):
    """
    Class reprensenting a domain on which a distance function is defined on a tuple of `src.variable.variable.Variable`.

    Parameters
    ----------
    variable : list of src.variable.variable.Variable
        The variables on which the domain is defined.
    """

    def __init__(self, *variable : Variable):

        self._variable = tuple(variable)
