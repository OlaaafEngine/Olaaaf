import unittest
from olaaaf.variable import RealVariable
from fractions import Fraction
from olaaaf.formula.nullaryFormula import LinearConstraint
from olaaaf.mlo_solver import LPSolverRounded
from olaaaf.simplificator import Daalmans
from olaaaf.projector import FloatConvexHullProjector
from olaaaf.revision import Revision
from olaaaf.distance import DiscreteL1DistanceFunction


class TestRevision(unittest.TestCase):
    def test_triangle_and_polygone(self):
        weights = {
            RealVariable.declare("x"): Fraction(1),
            RealVariable.declare("y"): Fraction(1),
        }

        solver = LPSolverRounded()
        simplifier = [Daalmans(solver)]
        projector = FloatConvexHullProjector(simplifiers=simplifier, rounding=12)

        psi = LinearConstraint("x >= 0") & LinearConstraint("y >= 0") & LinearConstraint("x + y <= 4")
        mu = (LinearConstraint("x + y >= 6") & LinearConstraint("5*x + y <= 25") & LinearConstraint("-0.5*x + y <= 3") & LinearConstraint("1/3*x + y >= 4"))\
            | (LinearConstraint("5*x + y >= 25") & LinearConstraint("3*x + y >= 16") & LinearConstraint("-x + y >= -4") & LinearConstraint("x <= 6") & LinearConstraint("x + y <= 9"))

        rev = Revision(solver, DiscreteL1DistanceFunction(weights), simplifier, onlyOneSolution=False, projector=projector)
        res = rev.execute(psi, mu)
        self.assertEqual(res[1], (LinearConstraint("- 1/2*x + y <= 3") & LinearConstraint("x + y <= 6") & LinearConstraint("- x - y <= -6") & LinearConstraint("-1/3*x - y <= -4")) | (LinearConstraint("x = 5") & LinearConstraint("y = 1")), "The revision of triangle and polygone isn't what we expected.")

        self.assertTrue(simplifier[0]._interpreter.sat(res[1].toLessOrEqConstraint().toDNF()), "The revision of triangle and polygone is insat.")

    def test_cocktail_simplified(self):
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

        self.assertTrue(simplifier[0]._interpreter.sat(res[1].toLessOrEqConstraint().toDNF()), "The revision of cocktail simplified is insat.")

    def test_rectangle(self):
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

        self.assertEqual(res[1], (LinearConstraint("x = 5") & LinearConstraint("y <= 5") & LinearConstraint("- y <= -2")) | (LinearConstraint("x <= 5") & LinearConstraint("- x <= -2") & LinearConstraint("y = 2")) | (LinearConstraint("x <= 5") & LinearConstraint("- x <= -2") & LinearConstraint("y = 5")) | (LinearConstraint("x = 2") & LinearConstraint("- y <= -2") & LinearConstraint("y <= 5")))

        self.assertTrue(simplifier[0]._interpreter.sat(res[1].toLessOrEqConstraint().toDNF()), "The revision of two rectangles is insat.")
    
if __name__ == '__main__': unittest.main()