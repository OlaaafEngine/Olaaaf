"""
Class representing a l1 distance function, also called cityblock or Manhattan.
"""

from __future__ import annotations

from .distanceFunctionOnNumericalTuple import distanceFunctionOnNumericalTuple
from ..domain import Domain
from ...variable import Variable

from fractions import Fraction

class l1DistanceFunction(distanceFunctionOnNumericalTuple):
    r"""
    Class representing a l1 distance function, also called cityblock or Manhattan, defined as such:

    \[
        d(x, y) = \sum_{j=1}^{n}w_j|y_j-x_j|
    \]

    with \(w_j\) weights.

    Parameters
    ----------
    weights : a dictionnary of fractions.Fraction with src.variable.variable.Variable as key
        The weights of the l1 distance function
    domain: src.distance.domain.domain.Domain
        The `src.distance.domain.domain.Domain` on which the distance function is defined.
    """

    _weights : dict[Variable, Fraction]

    def __init__(self, weights : dict[Variable, Fraction], domaine : Domain = None):
        self._domaine = domaine
        self._weights = weights

    def dist(self, x : tuple[Variable], y :tuple[Variable]):
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
        
        if(len(x) != len(y)): raise Exception("x and y are not in the same domaine")
        res = 0
        for i in range(0, len(x)):
            res += self._fractions[i] * abs(x[i] - y[i])
        return res

    def getWeights(self) -> Fraction:
        return self._weights

    def getEpsilon(self) -> Fraction:
        return Fraction(1,1)