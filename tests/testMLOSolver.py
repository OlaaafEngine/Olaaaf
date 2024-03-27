import unittest
from olaaaf.mlo_solver import ScipySolverRounded
from olaaaf.variable import RealVariable
from olaaaf.variable import IntegerVariable
from olaaaf.formula.nullaryFormula.constraint import ConstraintOperator
from olaaaf.mlo_solver import OptimizationValues
from fractions import Fraction

class TestMLOSolver(unittest.TestCase):
    global solver
    def test_farmer(self):
        corn = IntegerVariable.declareAnonymous()
        oat = IntegerVariable.declareAnonymous()
        objectif = [-40,-30]
        constraints = [
            ([2,1], ConstraintOperator.LEQ, 320), 
            ([1,1], ConstraintOperator.LEQ, 240), 
            ([-1,0], ConstraintOperator.LEQ, 0), 
            ([0,-1], ConstraintOperator.LEQ, 0)
            ]
        res = solver.solve([corn,oat], objectif, constraints)
        self.assertEqual(res[0], OptimizationValues.OPTIMAL, "Optimization of farmer problem is not correct.")
        self.assertEqual(res[1][0], 80, "Optimization of farmer problem is not correct. (corn value is not 80)")
        self.assertEqual(res[1][1], 160, "Optimization of farmer problem is not correct. (oat value is not 160)")
        self.assertEqual(res[2], -8000, "Optimization of farmer problem is not correct.")

    def test_triangle(self):
        x = RealVariable.declareAnonymous()
        y = IntegerVariable.declareAnonymous()
        objectif = [1,1]
        constraints = [
            ([4,Fraction(-1,3)], ConstraintOperator.EQ, 4), 
            ([3,Fraction(1,5)], ConstraintOperator.GEQ, 5), 
            ]
        res = solver.solve([x,y], objectif, constraints)
        self.assertEqual(res[0], OptimizationValues.OPTIMAL, "Optimization of triangle problem is not correct.")
        self.assertAlmostEqual(res[1][0], 1.41666666667, 7, "Optimization of triangle problem is not correct.")
        self.assertEqual(res[1][1], 5, "Optimization of triangle problem is not correct. (y value is not 5)")
        self.assertAlmostEqual(res[2], 6.41666666667, 7, "Optimization of triangle problem is not correct.")

        objectif = [-1,-1]
        res = solver.solve([x,y], objectif, constraints)
        self.assertEqual(res[0], OptimizationValues.UNBOUNDED, "Optimization of triangle problem is not correct.")

    def test_infeasible(self):
        x = RealVariable.declareAnonymous()
        y = IntegerVariable.declareAnonymous()
        z = RealVariable.declareAnonymous()

        objectif = [1,1,1]
        constraints = [
            ([4,2,3], ConstraintOperator.EQ, 4), 
            ([3,1,2], ConstraintOperator.GEQ, 5),
            ([4,2,3], ConstraintOperator.GEQ, 5),
            ]
        res = solver.solve([x,y,z], objectif, constraints)
        self.assertEqual(res[0], OptimizationValues.INFEASIBLE, "Optimization of an infeasible problem is not detected.")


# Put your mlo solver here to test it
solver = ScipySolverRounded()
if __name__ == '__main__': 
    unittest.main()