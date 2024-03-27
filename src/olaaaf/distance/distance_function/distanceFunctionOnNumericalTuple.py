"""
Abstract class representing a distance function applied on numerical tuples.
"""

from __future__ import annotations

from .distanceFunction import DistanceFunction
from ..domain import VariableTupleDomaine
from fractions import Fraction

from abc import abstractmethod

class DistanceFunctionOnNumericalTuple(DistanceFunction):
    """
    Abstract class representing a distance function applied on numerical tuples.

    Parameters
    ----------
    domain: olaaaf.distance.domain.variableTupleDomaine.VariableTupleDomaine
        The `olaaaf.distance.domain.variableTupleDomaine.VariableTupleDomaine` on which the distance function is defined.
    """

    def __init__(self, domaine : VariableTupleDomaine):
        self._domaine = domaine

    @abstractmethod
    def getWeights(self) -> Fraction:
        pass

    @abstractmethod
    def getEpsilon(self) -> Fraction:
        pass