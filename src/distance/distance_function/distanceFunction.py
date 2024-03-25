"""
Abstract class representing a distance function.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from ..domain import Domain

from ...variable import Variable
from fractions import Fraction

class DistanceFunction(ABC):
    """
    Abstract class representing a distance function.

    Parameters
    ----------
    domain: src.distance.domain.domain.Domain
        The `src.distance.domain.domain.Domain` on which the distance function is defined.
    """
    
    _domain : Domain

    def __init__(self, domain : Domain):
        self._domain = domain
    
    @abstractmethod
    def dist(x: tuple[Variable], y: tuple[Variable]) -> Fraction:
        r"""
        Main method of a distance funciton, allowing to get the distance between two points \(x\) and \(y\).

        Parameters
        ----------
        x, y : tuple of src.variable.variable.Variable
            The two tuples of `src.variable.variable.Variable` you which to get the distance between.

        Returns
        -------
        fractions.Fraction
            The distance between \(x\) and \(y\).
        """

        pass