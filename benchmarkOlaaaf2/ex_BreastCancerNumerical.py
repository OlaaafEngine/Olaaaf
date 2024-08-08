from example import Example

from olaaaf.formula import LinearConstraint, PropositionalVariable, FormulaManager
from olaaaf.mlo_solver import  ScipySolverRounded
from olaaaf import Adaptation
from olaaaf.variable import IntegerVariable, VariableManager
from olaaaf.distance import DiscreteL1DistanceFunction
from olaaaf.simplificator import Daalmans
from olaaaf.domainKnowledge import Taxonomy, MiscellanousDomainKnowledge, ExistenceKnowledge

from fractions import Fraction

class BreastCancerNumericalExample(Example):
    
     # TODO (Le FEC en numérique, à réfléchir)

     def __init__(self) -> None:
          
          self.weights = {
               PropositionalVariable("man", fmName="man"): Fraction(1),
               PropositionalVariable("woman", fmName="woman"): Fraction(1),
               PropositionalVariable("oc", fmName="oc"): Fraction(1),

               PropositionalVariable("antiOestrogen", fmName="antiOestrogen"): Fraction(100),
               PropositionalVariable("antiAromatases", fmName="antiAromatases"): Fraction(1),
               PropositionalVariable("ovariolysis", fmName="ovariolysis"): Fraction(1),
               PropositionalVariable("tamoxifen", fmName="tamoxifen"): Fraction(1),
               PropositionalVariable("partialMastectomy", fmName="partialMastectomy"): Fraction(1),

               IntegerVariable.declare("fec", lowerBound = Fraction(0)): Fraction(1),
               PropositionalVariable("fec", fmName="fec"): Fraction(1),
               PropositionalVariable("fec50", fmName="fec50"): Fraction(1),
               PropositionalVariable("fec100", fmName="fec100"): Fraction(1),
               PropositionalVariable("fec150", fmName="fec150"): Fraction(1),
          }

          self.solver = ScipySolverRounded()
          self.simplifiers = [Daalmans(self.solver)]
          self.distanceFunction = DiscreteL1DistanceFunction(self.weights)
          self.adaptator = Adaptation(self.solver, self.distanceFunction, self.simplifiers, onlyOneSolution=True, verbose=False)
          self.adaptator.preload()

          self.dk = dict()

          self.dk["existence"] = ExistenceKnowledge({PropositionalVariable("fec"): VariableManager.get("fec")})

          self.dk["taxonomy"] = Taxonomy()
          self.dk["taxonomy"].addElements(["antiOestrogen", "antiAromatases", "ovariolysis", "tamoxifen",\
                                                            "fec", "fec50", "fec100", "fec150"])
          self.dk["taxonomy"].addChildren("antiOestrogen", ["antiAromatases", "ovariolysis", "tamoxifen"])
          self.dk["taxonomy"].addChildren("fec", ["fec50", "fec100", "fec150"])

          self.dk["miscellanous"] = MiscellanousDomainKnowledge(miscDk=None)
          self.dk["miscellanous"].miscDk  =  FormulaManager.parser("(man <+> woman)")
          self.dk["miscellanous"].miscDk &= FormulaManager.parser("man -> (~(ovariolysis))")
          self.dk["miscellanous"].miscDk &= (PropositionalVariable("fec50") // LinearConstraint("fec = 50"))\
                                          & (PropositionalVariable("fec100") // LinearConstraint("fec = 100"))\
                                          & (PropositionalVariable("fec150") // LinearConstraint("fec = 150"))

          self.srce_case = FormulaManager.parser("woman & oc & fec50 & ovariolysis & partialMastectomy")

          self.tgt_problem = FormulaManager.parser("man & oc") & LinearConstraint("fec <= 80")