from src.olaaaf.domainKnowledge import ConversionKnowledge
from src.olaaaf.formula import LinearConstraint
from src.olaaaf.variable import IntegerVariable, RealVariable

from fractions import Fraction

ck = ConversionKnowledge()

RealVariable.declare("milk_g")
RealVariable.declare("milk_mL")
RealVariable.declare("milk_L")
IntegerVariable.declare("milk_u")

ck.addConversion((RealVariable("milk_g"), Fraction(1030)), (RealVariable("milk_L"), Fraction(1)))
ck.addConversion((RealVariable("milk_L"), Fraction(1)), (RealVariable("milk_mL"), Fraction(1000)))
ck.addConversion((IntegerVariable("milk_u"), Fraction(1)), (RealVariable("milk_g"), Fraction(1030)))

print(ck.toConstraints())
print(ck.inferFrom(LinearConstraint("milk_u = 1")))