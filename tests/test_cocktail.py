from olaaaf.formula import LinearConstraint
from olaaaf.mlo_solver import LPSolverRounded
from olaaaf.revision import Revision
from olaaaf.variable import RealVariable, IntegerVariable
from olaaaf.distance import DiscreteL1DistanceFunction
from olaaaf.simplificator import Daalmans
from olaaaf.projector import FloatConvexHullProjector

from fractions import Fraction

weights = {
    IntegerVariable.declare("quant_rondelleCitron"): Fraction(1),
    RealVariable.declare("vol_tequila"): Fraction(1),
    RealVariable.declare("vol_sirop"): Fraction(1),
    RealVariable.declare("vol_jusCitronVert"): Fraction(1),
    RealVariable.declare("vol_vodka"): Fraction(1),
    RealVariable.declare("vol_alcool"): Fraction(20),
    RealVariable.declare("pouvoirSucrant"): Fraction(20),
}

solver = LPSolverRounded()
simplifier = [Daalmans(solver)]
projector = FloatConvexHullProjector(simplifiers=simplifier, rounding=10)

cd = LinearConstraint("vol_tequila >= 0") & LinearConstraint("vol_vodka >= 0")\
    & LinearConstraint("0.35*vol_tequila + 0.45*vol_vodka  - vol_alcool = 0")\
    & LinearConstraint("0.6*vol_sirop + 0.2 * vol_tequila - pouvoirSucrant = 0")
psi = LinearConstraint("vol_tequila = 4") & LinearConstraint("vol_sirop = 2")\
    & LinearConstraint("quant_rondelleCitron = 1") & LinearConstraint("vol_jusCitronVert >= 2")\
    & LinearConstraint("vol_jusCitronVert <= 3") & cd
mu = LinearConstraint("vol_alcool = 0") & cd

rev = Revision(solver, DiscreteL1DistanceFunction(weights), simplifier, onlyOneSolution=False, projector=projector)
res = rev.execute(psi, mu)