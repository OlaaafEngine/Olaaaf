from olaaaf.formula import LinearConstraint
from olaaaf.mlo_solver import LPSolverRounded
from olaaaf.revision import Revision
from olaaaf.variable import RealVariable
from olaaaf.distance import DiscreteL1DistanceFunction
from olaaaf.simplificator import Daalmans
from olaaaf.projector import FloatConvexHullProjector

from fractions import Fraction

weights = {
    RealVariable.declare("vol_tequila"): Fraction(1),
    RealVariable.declare("vol_sirop"): Fraction(1),
    RealVariable.declare("vol_alcool"): Fraction(20),
    RealVariable.declare("pouvoirSucrant"): Fraction(20),
}

solver = LPSolverRounded()
simplifier = [Daalmans(solver)]
projector = FloatConvexHullProjector(simplifiers=simplifier, rounding=10)

cd = LinearConstraint("vol_tequila >= 0") & LinearConstraint("0.35*vol_tequila - vol_alcool = 0")\
    & LinearConstraint("0.6*vol_sirop + 0.2 * vol_tequila - pouvoirSucrant = 0")
psi = LinearConstraint("vol_tequila = 4") & LinearConstraint("vol_sirop = 2") & cd
mu = LinearConstraint("vol_alcool = 0") & cd

rev = Revision(solver, DiscreteL1DistanceFunction(weights), simplifier, onlyOneSolution=False, projector=projector)
res = rev.execute(psi, mu)