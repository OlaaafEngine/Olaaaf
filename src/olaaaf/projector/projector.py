"""
Abstract class, representating a projector of a `olaaaf.formula.formula.Formula` to a subset of its `olaaaf.variable.variable.Variable`.
"""

from __future__ import annotations

from ..formula import Formula, And
from ..variable import Variable

from abc import ABC, abstractmethod

class Projector (ABC):

    @abstractmethod
    def projectOn(self, phi: And, variables: set[Variable]) -> Formula:
        r"""
        Main method of `olaaaf.projector.projector.Projector`, allowing to project a given `olaaaf.formula.formula.Formula`
        to a subset of its `olaaaf.variable.variable.Variable`.

        Parameters
        ----------
        phi: `olaaaf.formula.formula.Formula`
            The `olaaaf.formula.formula.Formula` to project.
        variables: set of olaaaf.variable.variable.Variable
            The subset of `olaaaf.variable.variable.Variable` to project on.
        
        Returns
        -------
        `olaaaf.formula.formula.Formula`
            The projection of \(\varphi\) on the specified subset of its variables.
        """
        pass