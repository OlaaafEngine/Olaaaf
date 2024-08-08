from example import Example

from olaaaf.formula import LinearConstraint, PropositionalVariable, FormulaManager
from olaaaf.mlo_solver import  ScipySolverRounded
from olaaaf import Adaptation
from olaaaf.variable import RealVariable, IntegerVariable, VariableManager
from olaaaf.distance import DiscreteL1DistanceFunction
from olaaaf.simplificator import Daalmans
from olaaaf.domainKnowledge import ExistenceKnowledge, MiscellanousDomainKnowledge

from fractions import Fraction

class CarrotCabageSaladExample(Example):
    
     def __init__(self) -> None:
          
          self.weights = {
               PropositionalVariable("carrot"): Fraction(1),
               PropositionalVariable("greenCabbage"): Fraction(1),
               PropositionalVariable("lemonJuice"): Fraction(1),
               PropositionalVariable("oliveOil"): Fraction(1),
               PropositionalVariable("saladDish"): Fraction(1000000),
               PropositionalVariable("shallot"): Fraction(1),
               PropositionalVariable("soySauce"): Fraction(1),
               PropositionalVariable("vinegar"): Fraction(1),
               PropositionalVariable("water"): Fraction(1),

               RealVariable.declare("carrot_g", lowerBound = Fraction(0)): Fraction(1),
               RealVariable.declare("food_g", lowerBound = Fraction(0)): Fraction(10000),
               RealVariable.declare("greenCabbage_g", lowerBound = Fraction(0)): Fraction(1),
               RealVariable.declare("lemonJuice_g", lowerBound = Fraction(0)): Fraction(1),
               RealVariable.declare("lemonJuice_L", lowerBound = Fraction(0)): Fraction(1031.33),
               RealVariable.declare("oliveOil_g", lowerBound = Fraction(0)): Fraction(1),
               RealVariable.declare("oliveOil_L", lowerBound = Fraction(0)): Fraction(912.98),
               RealVariable.declare("shallot_g", lowerBound = Fraction(0)): Fraction(1),
               RealVariable.declare("soySauce_g", lowerBound = Fraction(0)): Fraction(1),
               RealVariable.declare("soySauce_L", lowerBound = Fraction(0)): Fraction(1077.82),
               RealVariable.declare("vinegar_g", lowerBound = Fraction(0)): Fraction(1),
               RealVariable.declare("vinegar_L", lowerBound = Fraction(0)): Fraction(1014.42),
               RealVariable.declare("water_g", lowerBound = Fraction(0)): Fraction(1),
               RealVariable.declare("water_L", lowerBound = Fraction(0)): Fraction(1000),

               IntegerVariable.declare("carrot_u", lowerBound = Fraction(0)): Fraction(125),
               IntegerVariable.declare("greenCabbage_cup", lowerBound = Fraction(0)): Fraction(94.05),
               IntegerVariable.declare("shallot_u", lowerBound = Fraction(0)): Fraction(25),

               RealVariable.declare("ak_deltaVinegarLemonJuiceWater"): Fraction(1e12),
               RealVariable.declare("ak_equalWaterLemonJuice"): Fraction(1e12)
          }


          self.solver = ScipySolverRounded()
          self.simplifiers = [Daalmans(self.solver)]
          self.distanceFunction = DiscreteL1DistanceFunction(self.weights)
          self.adaptator = Adaptation(self.solver, self.distanceFunction, self.simplifiers, onlyOneSolution=True, verbose=False)
          self.adaptator.preload()

          self.dk = dict()

          self.dk["existence"] = ExistenceKnowledge({PropositionalVariable("carrot"): VariableManager.get("carrot_g"),
                                                     PropositionalVariable("greenCabbage"): VariableManager.get("greenCabbage_g"),
                                                     PropositionalVariable("oliveOil"): VariableManager.get("oliveOil_g"),
                                                     PropositionalVariable("shallot"): VariableManager.get("shallot_g"),
                                                     PropositionalVariable("soySauce"): VariableManager.get("soySauce_g"),
                                                     PropositionalVariable("vinegar"): VariableManager.get("vinegar_g"),
                                                     PropositionalVariable("water"): VariableManager.get("water_g")})

          # Pas de tax - je modifie pour en rajouter une ?

          # self.dk["taxonomy"] = Taxonomy()
          # self.dk["taxonomy"].addElements(["meat", "beef", "chicken", "groundBeef", "beefSteak", "chickenBreast", "chickenThigh"])
          # self.dk["taxonomy"].addChildren("meat", ["beef", "chicken"])
          # self.dk["taxonomy"].addChildren("beef", ["groundBeef", "beefSteak"])
          # self.dk["taxonomy"].addChildren("chicken", ["chickenBreast", "chickenThigh"])

          self.dk["miscellanous"] = MiscellanousDomainKnowledge(miscDk=None)
          self.dk["miscellanous"].miscDk =  LinearConstraint("food_g - greenCabbage_g - carrot_g - shallot_g - soySauce_g - vinegar_g - oliveOil_g - lemonJuice_g - water_g = 0")
          self.dk["miscellanous"].miscDk &= PropositionalVariable("saladDish") >>\
                                             (LinearConstraint("ak_deltaVinegarLemonJuiceWater - vinegar_g - water_g - lemonJuice_g = 0")\
                                             & LinearConstraint("ak_equalWaterLemonJuice - water_g + lemonJuice_g = 0"))

          self.srce_case = PropositionalVariable("saladDish")\
                         & LinearConstraint("carrot_u = 2")\
                         & LinearConstraint("greenCabbage_cup = 4")\
                         & LinearConstraint("oliveOil_g = 50")\
                         & LinearConstraint("shallot_u = 1")\
                         & LinearConstraint("soySauce_g = 32")\
                         & LinearConstraint("vinegar_g = 20")

          self.tgt_problem = PropositionalVariable("saladDish")\
                           & PropositionalVariable("carrot")\
                           & PropositionalVariable("greenCabbage")\
                           & ~PropositionalVariable("vinegar")