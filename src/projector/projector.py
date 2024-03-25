"""
Abstract class, representating a projector of a `src.formula.formula.Formula` to a subset of its `src.variable.variable.Variable`.
"""

from __future__ import annotations

from ..formula import Formula, And
from ..variable import Variable

from abc import ABC, abstractmethod

class Projector (ABC):

    @abstractmethod
    def projectOn(self, phi: And, variables: set[Variable]) -> Formula:
        r"""
        Main method of `src.projector.projector.Projector`, allowing to project a given `src.formula.formula.Formula`
        to a subset of its `src.variable.variable.Variable`.

        Parameters
        ----------
        phi: src.formula.formula.Formula
            The `src.formula.formula.Formula` to project.
        variables: set of src.variable.variable.Variable
            The subset of `src.variable.variable.Variable` to project on.
        
        Returns
        -------
        src.formula.formula.Formula
            The projection of \(\varphi\) on the specified subset of its variables.
        """
        pass