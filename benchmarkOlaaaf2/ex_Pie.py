from example import Example

from olaaaf.formula import LinearConstraint, PropositionalVariable, FormulaManager
from olaaaf.mlo_solver import  ScipySolverRounded
from olaaaf import Adaptation
from olaaaf.variable import RealVariable, IntegerVariable, VariableManager
from olaaaf.distance import DiscreteL1DistanceFunction
from olaaaf.simplificator import Daalmans
from olaaaf.domainKnowledge import ExistenceKnowledge, ConversionKnowledge, Taxonomy, MiscellanousDomainKnowledge

from fractions import Fraction

class PieExample(Example):
    
     def __init__(self) -> None:
          
          self.weights = {
               PropositionalVariable("meat", fmName="meat"): Fraction(10000),
               PropositionalVariable("beef", fmName="beef"): Fraction(100),
               PropositionalVariable("groundBeef", fmName="groundBeef"): Fraction(1),
               PropositionalVariable("beefSteak", fmName="beefSteak"): Fraction(1),
               PropositionalVariable("chicken", fmName="chicken"): Fraction(100),
               PropositionalVariable("chickenBreast", fmName="chickenBreast"): Fraction(1),
               PropositionalVariable("chickenThigh", fmName="chickenThigh"): Fraction(1),

               PropositionalVariable("eggYolk", fmName="eggYolk"): Fraction(1),
               PropositionalVariable("puffPastry", fmName="puffPastry"): Fraction(1),
               PropositionalVariable("pie", fmName="pie"): Fraction(1),

               PropositionalVariable("cream", fmName="cream"): Fraction(1),

               RealVariable.declare("protein_g", lowerBound = Fraction(0)): Fraction(10000),
               RealVariable.declare("fat_g", lowerBound = Fraction(0)): Fraction(10000),
               RealVariable.declare("food_g", lowerBound = Fraction(0)): Fraction(1000000),

               RealVariable.declare("meat_g", lowerBound = Fraction(0)): Fraction(10000),
               RealVariable.declare("beef_g", lowerBound = Fraction(0)): Fraction(100),
               RealVariable.declare("groundBeef_g", lowerBound = Fraction(0)): Fraction(1),
               RealVariable.declare("beefSteak_g", lowerBound = Fraction(0)): Fraction(1),
               RealVariable.declare("chicken_g", lowerBound = Fraction(0)): Fraction(100),
               RealVariable.declare("chickenBreast_g", lowerBound = Fraction(0)): Fraction(1),
               RealVariable.declare("chickenThigh_g", lowerBound = Fraction(0)): Fraction(1),

               RealVariable.declare("cream_g", lowerBound = Fraction(0)): Fraction(1),

               RealVariable.declare("eggYolk_g", lowerBound = Fraction(0)): Fraction(1),
               IntegerVariable.declare("eggYolk_u", lowerBound = Fraction(0)): Fraction(0),
               RealVariable.declare("puffPastry_g", lowerBound = Fraction(0)): Fraction(1),
               IntegerVariable.declare("puffPastry_u", lowerBound = Fraction(0)): Fraction(0),
          }

          self.solver = ScipySolverRounded()
          self.simplifiers = [Daalmans(self.solver)]
          self.distanceFunction = DiscreteL1DistanceFunction(self.weights)
          self.adaptator = Adaptation(self.solver, self.distanceFunction, self.simplifiers, onlyOneSolution=True, verbose=False)
          self.adaptator.preload()

          self.dk = dict()

          self.dk["conversion"] = ConversionKnowledge()
          self.dk["conversion"].addConversions([((VariableManager.get("eggYolk_u"), Fraction(1)), (VariableManager.get("eggYolk_g"), Fraction(17))),
                                                ((VariableManager.get("puffPastry_u"), Fraction(1)), (VariableManager.get("puffPastry_g"), Fraction(130)))])

          self.dk["existence"] = ExistenceKnowledge({PropositionalVariable("beef"): VariableManager.get("beef_g"),
                                                     PropositionalVariable("groundBeef"): VariableManager.get("groundBeef_g"),
                                                     PropositionalVariable("beefSteak"): VariableManager.get("beefSteak_g"),
                                                     PropositionalVariable("chicken"): VariableManager.get("chicken_g"),
                                                     PropositionalVariable("chickenBreast"): VariableManager.get("chickenBreast_g"),
                                                     PropositionalVariable("chickenThigh"): VariableManager.get("chickenThigh_g"),
                                                     PropositionalVariable("eggYolk"): VariableManager.get("eggYolk_g"),
                                                     PropositionalVariable("puffPastry"): VariableManager.get("puffPastry_g"),
                                                     PropositionalVariable("cream"): VariableManager.get("cream_g")})

          self.dk["taxonomy"] = Taxonomy()
          self.dk["taxonomy"].addElements(["meat", "beef", "chicken", "groundBeef", "beefSteak", "chickenBreast", "chickenThigh"])
          self.dk["taxonomy"].addChildren("meat", ["beef", "chicken"])
          self.dk["taxonomy"].addChildren("beef", ["groundBeef", "beefSteak"])
          self.dk["taxonomy"].addChildren("chicken", ["chickenBreast", "chickenThigh"])

          self.dk["miscellanous"] = MiscellanousDomainKnowledge(miscDk=None)
          self.dk["miscellanous"].miscDk = LinearConstraint("protein_g - 0.259*groundBeef_g\
                                                                       - 0.201*beefSteak_g\
                                                                       - 0.225*chickenBreast_g\
                                                                       - 0.185*chickenThigh_g\
                                                                       - 0.020*cream_g\
                                                                       - 0.162*eggYolk_g\
                                                                       - 0.073*puffPastry_g = 0")\
                                         & LinearConstraint("fat_g - 0.154*groundBeef_g\
                                                                   - 0.094*beefSteak_g\
                                                                   - 0.019*chickenBreast_g\
                                                                   - 0.079*chickenThigh_g\
                                                                   - 0.356*cream_g\
                                                                   - 0.288*eggYolk_g\
                                                                   - 0.381*puffPastry_g = 0")\
                                         & LinearConstraint("food_g - meat_g\
                                                                    - cream_g\
                                                                    - eggYolk_g\
                                                                    - puffPastry_g = 0")\
                                         & LinearConstraint("meat_g - beef_g\
                                                                    - chicken_g = 0")\
                                         & LinearConstraint("beef_g - groundBeef_g\
                                                                    - beefSteak_g = 0")\
                                         & LinearConstraint("chicken_g - chickenBreast_g\
                                                                       - chickenThigh_g = 0")
          self.dk["miscellanous"].miscDk &= FormulaManager.parser("pie -> (puffPastry & eggYolk)")

          self.srce_case = LinearConstraint("groundBeef_g = 200.")\
                         & LinearConstraint("puffPastry_u = 2")\
                         & LinearConstraint("eggYolk_u = 1")\
                         & LinearConstraint("beefSteak_g = 0.")\
                         & LinearConstraint("chicken_g = 0.")\
                         & LinearConstraint("cream_g = 0.")\
                         & PropositionalVariable("pie")

          self.tgt_problem = FormulaManager.parser("pie & chicken & (~beef)")