from olaaaf.formula import FormulaDisplay, LinearConstraint
from olaaaf.mlo_solver import LPSolverRounded
from olaaaf.revision import Revision
from olaaaf.variable import RealVariable
from olaaaf.distance import DiscreteL1DistanceFunction
from olaaaf.simplificator import Daalmans
from olaaaf.projector import FloatConvexHullProjector

from fractions import Fraction

x = RealVariable.declare("x")
y = RealVariable.declare("y")

weights = {
    RealVariable.declare("x"): Fraction(1),
    RealVariable.declare("y"): Fraction(1),
}

solver = LPSolverRounded()
simplifier = [Daalmans(solver)]
projector = FloatConvexHullProjector(simplifiers=simplifier, rounding=10)

mu = LinearConstraint("x >= 2") & LinearConstraint("x <= 5") & LinearConstraint("y >= 2") & LinearConstraint("y <= 5")
psi = LinearConstraint("x >= 0") & LinearConstraint("x <= 7") & LinearConstraint("y >= 7") & LinearConstraint("y <= 9")\
| LinearConstraint("x >= 0") & LinearConstraint("x <= 7") & LinearConstraint("y >= -1") & LinearConstraint("y <= 0")\
| LinearConstraint("x >= 7") & LinearConstraint("x <= 9") & LinearConstraint("y >= 0") & LinearConstraint("y <= 7")\
| LinearConstraint("x >= -2") & LinearConstraint("x <= 0") & LinearConstraint("y >= 0") & LinearConstraint("y <= 7")

rev = Revision(solver, DiscreteL1DistanceFunction(weights), simplifier, onlyOneSolution=False, projector=projector)
res = rev.execute(psi, mu)

from olaaaf.formula.formulaDisplay import FormulaDisplay
display = FormulaDisplay()
display.display({psi.toLessOrEqConstraint() : 'blue', mu.toLessOrEqConstraint() : 'green', res[1].toLessOrEqConstraint() : 'red'}, [x,y])
