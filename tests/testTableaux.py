import unittest

from src.olaaaf.formula import LinearConstraint, PropositionalVariable, FormulaManager
from src.olaaaf.variable import IntegerVariable

class TestTableaux(unittest.TestCase):

    def setUp(self):
        # Set up any resources needed for the tests
        
        IntegerVariable.declare("x")
        IntegerVariable.declare("y")
        IntegerVariable.declare("z")

        PropositionalVariable("a", fmName="a")
        PropositionalVariable("b", fmName="b")
        PropositionalVariable("c", fmName="c")
        PropositionalVariable("d", fmName="d")

    def test_closed(self):
        """
        Case where the whole tree is found closed: should return None.
        """

        fm = FormulaManager.parser("a & (~a)")

        self.assertEqual(fm.toDNFWithTableaux(), None)

    def test_distribute(self):
        """
        Case where the tree is not found closed, and needs to be distributed.
        """

        fm = FormulaManager.parser("(a | b) & ((~a) | (~b))")
        expected = FormulaManager.parser("(a & (~b)) | ((~a) & b)")

        self.assertEqual(fm.toDNFWithTableaux(), expected)

    def test_negation(self):
        """
        Case where the negation needs to be transfered multiple times.
        """

        fm = FormulaManager.parser("~(a | (~(c & (~d))) & (~b))")
        expected = FormulaManager.parser("((~a) & b) | ((~a) & c & (~d))")

        self.assertEqual(fm.toDNFWithTableaux(), expected)

    def test_linearConstraint_as_atom(self):
        """
        Case where a branch is unsatisfiable due to linear constraints; can't be caught by tableaux.
        """

        fm = (LinearConstraint("x <= 0") & LinearConstraint("x >= 1")) | LinearConstraint(LinearConstraint("x <= 0") & ~LinearConstraint("x <= 0"))
        expected = (LinearConstraint("x <= 0") & LinearConstraint("x >= 1"))

        self.assertEqual(fm.toDNFWithTableaux(), expected)

if __name__ == '__main__':
    unittest.main()