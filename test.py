from src.olaaaf.formula import LinearConstraint
from src.olaaaf.variable import RealVariable
from src.olaaaf.mlo_solver import ScipySolverRounded
from src.olaaaf.simplificator import Daalmans
from src.olaaaf.distance import DiscreteL1DistanceFunction
from src.olaaaf.revision import Revision

from fractions import Fraction

weights = {
    RealVariable.declare("x"): Fraction(1),
}

solver = ScipySolverRounded()
simplifiers = [Daalmans(solver)]

distanceFunction = DiscreteL1DistanceFunction(weights, epsilon=Fraction("1e-4"))

revisor = Revision(solver, distanceFunction, simplifiers, onlyOneSolution=True)

revisor.preload()

psi = LinearConstraint("x <= 0")
mu = ~LinearConstraint("x <= 1")

print(revisor.execute(psi, mu))
