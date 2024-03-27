"""
Class representing a discretized l1 distance function, also called cityblock or Manhattan.
"""

from __future__ import annotations

from .distanceFunctionOnNumericalTuple import DistanceFunctionOnNumericalTuple
from .l1DistanceFunction import l1DistanceFunction
from ..domain import Domain
from ...variable import Variable

from fractions import Fraction
from math import ceil

class DiscreteL1DistanceFunction(DistanceFunctionOnNumericalTuple):
    r"""
    Class representing a discretized l1 distance function \(d_\varepsilon\), also called cityblock or Manhattan, defined as such:

    \[
        d(x, y) = \sum_{j=1}^{n}w_j|y_j-x_j|\\
        d_{\varepsilon}(x,y)=\varepsilon \biggl\lceil \frac{d(x,y)}{\varepsilon} \biggl\rceil
    \]

    with \(w_j\) weights.

    Parameters
    ----------
    weights : a dictionnary of fractions.Fraction with olaaaf.variable.variable.Variable as key
        The weights of the l1 distance function
    epsilon : fractions.Fraction
        The value by which the l1 distance function will be discretized.
    domain: olaaaf.distance.domain.domain.Domain
        The `olaaaf.distance.domain.domain.Domain` on which the distance function is defined.
    """

    def __init__(self, weights : dict[Variable, Fraction], epsilon : Fraction = Fraction("1e-3"), domaine : Domain = None):
        self._distance = l1DistanceFunction(weights, domaine)
        self._epsilon = epsilon

    def dist(self, x : tuple, y : tuple):
        r"""
        Main method of a distance funciton, allowing to get the distance between two points \(x\) and \(y\).

        Parameters
        ----------
        x, y : tuple of olaaaf.variable.variable.Variable
            The two tuples of `olaaaf.variable.variable.Variable` you which to get the distance between.

        Returns
        -------
        fractions.Fraction
            The distance between \(x\) and \(y\).
        """

        return self._epsilon * ceil(self._distance.dist(x,y) / self._epsilon)
    
    def getWeights(self) -> Fraction:
        return self._distance.getWeights()
    
    def getEpsilon(self) -> Fraction:
        return self._epsilon