from src.olaaaf.taxonomy import Taxonomy
from src.olaaaf.formula import And, Or, Not, NullaryFormula, Formula
from src.olaaaf.formula import PropositionalVariable

a = PropositionalVariable("a")
b = PropositionalVariable("b")
c = PropositionalVariable("c")
d = PropositionalVariable("d")

psi = a & (~c | d | ~b)

print(psi.toDNFWithTableaux())