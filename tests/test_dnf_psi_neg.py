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

psi = ~LinearConstraint("x <= 0") & ~LinearConstraint("y <= 0") & ~LinearConstraint("x + y >= 4")
mu = (LinearConstraint("x + y >= 6") & LinearConstraint("5*x + y <= 25") & LinearConstraint("-0.5*x + y <= 3") & LinearConstraint("1/3*x + y >= 4"))\
    | (LinearConstraint("5*x + y >= 25") & LinearConstraint("3*x + y >= 16") & LinearConstraint("-x + y >= -4") & LinearConstraint("x <= 6") & LinearConstraint("x + y <= 9"))

rev = Revision(solver, DiscreteL1DistanceFunction(weights), simplifier, onlyOneSolution=False, projector=projector)
res = rev.execute(psi, mu)

from olaaaf.formula.formulaDisplay import FormulaDisplay
display = FormulaDisplay()
display.display({psi.toLessOrEqConstraint() : 'blue', mu.toLessOrEqConstraint() : 'green', res[1].toLessOrEqConstraint() : 'red'}, [x,y])
