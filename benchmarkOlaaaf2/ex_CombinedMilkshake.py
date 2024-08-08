from example import Example

from olaaaf.formula import LinearConstraint, PropositionalVariable, FormulaManager
from olaaaf.mlo_solver import  ScipySolverRounded
from olaaaf import Adaptation
from olaaaf.variable import RealVariable, IntegerVariable, VariableManager
from olaaaf.distance import DiscreteL1DistanceFunction
from olaaaf.simplificator import Daalmans
from olaaaf.domainKnowledge import ExistenceKnowledge, ConversionKnowledge, Taxonomy, MiscellanousDomainKnowledge

from fractions import Fraction

class CombinedMilkshakeExample(Example):
    
     def __init__(self) -> None:
          
          self.weights = {
               PropositionalVariable("almondMilk", fmName="almondMilk"): Fraction(1),
               PropositionalVariable("banana", fmName="banana"): Fraction(1),
               PropositionalVariable("bitter", fmName="bitter"): Fraction(10000),
               PropositionalVariable("cowMilk", fmName="cowMilk"): Fraction(1),
               PropositionalVariable("dessert", fmName="dessert"): Fraction(10000),
               PropositionalVariable("fruit", fmName="fruit"): Fraction(100),
               PropositionalVariable("kiwi", fmName="kiwi"): Fraction(1),
               PropositionalVariable("milk", fmName="milk"): Fraction(100),
               PropositionalVariable("milkshake", fmName="milkshake"): Fraction(1000000),
               PropositionalVariable("soyMilk", fmName="soyMilk"): Fraction(1),

               RealVariable.declare("almondMilk_g", lowerBound = Fraction(0)): Fraction(1),
               RealVariable.declare("almondMilk_L", lowerBound = Fraction(0)): Fraction(1030),
               RealVariable.declare("banana_g", lowerBound = Fraction(0)): Fraction(1),
               RealVariable.declare("cowMilk_g", lowerBound = Fraction(0)): Fraction(1),
               RealVariable.declare("cowMilk_L", lowerBound = Fraction(0)): Fraction(1030),
               RealVariable.declare("food_g", lowerBound = Fraction(0)): Fraction(10000),
               RealVariable.declare("fruit_g", lowerBound = Fraction(0)): Fraction(100),
               RealVariable.declare("granulatedSugar_g", lowerBound = Fraction(0)): Fraction(1),
               RealVariable.declare("iceCube_g", lowerBound = Fraction(0)): Fraction(1),
               RealVariable.declare("kiwi_g", lowerBound = Fraction(0)): Fraction(1),
               RealVariable.declare("milk_g", lowerBound = Fraction(0)): Fraction(100),
               RealVariable.declare("soyMilk_g", lowerBound = Fraction(0)): Fraction(1),
               RealVariable.declare("soyMilk_L", lowerBound = Fraction(0)): Fraction(1030),
               RealVariable.declare("sweeteningPower_g", lowerBound = Fraction(0)): Fraction(10000),
               RealVariable.declare("vanillaSugar_g", lowerBound = Fraction(0)): Fraction(1),

               IntegerVariable.declare("banana_u", lowerBound = Fraction(0)): Fraction(115),
               IntegerVariable.declare("granulatedSugar_tbsp", lowerBound = Fraction(0)): Fraction(15),
               IntegerVariable.declare("iceCube_u", lowerBound = Fraction(0)): Fraction(25),
               IntegerVariable.declare("kiwi_u", lowerBound = Fraction(0)): Fraction(100),
               IntegerVariable.declare("vanillaSugar_u", lowerBound = Fraction(0)): Fraction(7.5),

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

          self.dk["conversion"] = ConversionKnowledge()
          self.dk["conversion"].addConversions([((VariableManager.get("banana_g"), Fraction(120)), (VariableManager.get("banana_u"), Fraction(1))),
                                                ((VariableManager.get("cowMilk_g"), Fraction(1030)), (VariableManager.get("cowMilk_L"), Fraction(1))),
                                                ((VariableManager.get("soyMilk_g"), Fraction(1030)), (VariableManager.get("soyMilk_L"), Fraction(1))),
                                                ((VariableManager.get("almondMilk_g"), Fraction(1030)), (VariableManager.get("almondMilk_L"), Fraction(1))),
                                                ((VariableManager.get("kiwi_g"), Fraction(100)), (VariableManager.get("kiwi_u"), Fraction(1))),
                                                ((VariableManager.get("vanillaSugar_g"), Fraction(7.5)), (VariableManager.get("vanillaSugar_u"), Fraction(1))),
                                                ((VariableManager.get("granulatedSugar_g"), Fraction(15)), (VariableManager.get("granulatedSugar_tbsp"), Fraction(1))),
                                                ((VariableManager.get("iceCube_g"), Fraction(25)), (VariableManager.get("iceCube_u"), Fraction(1)))])

          self.dk["existence"] = ExistenceKnowledge({PropositionalVariable("banana"): VariableManager.get("banana_g"),
                                                     PropositionalVariable("kiwi"): VariableManager.get("kiwi_g"),
                                                     PropositionalVariable("cowMilk"): VariableManager.get("cowMilk_g"),
                                                     PropositionalVariable("soyMilk"): VariableManager.get("soyMilk_g"),
                                                     PropositionalVariable("almondMilk"): VariableManager.get("almondMilk_g"),
                                                     PropositionalVariable("carrot"): VariableManager.get("carrot_g"),
                                                     PropositionalVariable("greenCabbage"): VariableManager.get("greenCabbage_g"),
                                                     PropositionalVariable("oliveOil"): VariableManager.get("oliveOil_g"),
                                                     PropositionalVariable("shallot"): VariableManager.get("shallot_g"),
                                                     PropositionalVariable("soySauce"): VariableManager.get("soySauce_g"),
                                                     PropositionalVariable("vinegar"): VariableManager.get("vinegar_g"),
                                                     PropositionalVariable("water"): VariableManager.get("water_g")})

          self.dk["taxonomy"] = Taxonomy()
          self.dk["taxonomy"].addElements(["banana", "kiwi", "fruit", "almondMilk", "cowMilk", "soyMilk", "milk", "dessert", "milkshake"])
          self.dk["taxonomy"].addChildren("milk", ["almondMilk", "cowMilk", "soyMilk"])
          self.dk["taxonomy"].addChildren("fruit", ["banana", "kiwi"])
          self.dk["taxonomy"].addChildren("dessert", ["milkshake"])

          self.dk["miscellanous"] = MiscellanousDomainKnowledge(miscDk=None)
          self.dk["miscellanous"].miscDk =  LinearConstraint("sweeteningPower_g  - granulatedSugar_g\
                                                                                 - 0.158 * banana_g\
                                                                                 - 0.0899 * kiwi_g\
                                                                                 - 0.98 * vanillaSugar_g\
                                                                                 - 0.0489 * cowMilk_g\
                                                                                 - 0.0368 * soyMilk_g\
                                                                                 - 0.04 * almondMilk_g = 0")\
                                         &  LinearConstraint("fruit_g - banana_g - kiwi_g = 0")\
                                         &  LinearConstraint("food_g - fruit_g - milk_g - granulatedSugar_g - iceCube_g - vanillaSugar_g = 0")\
                                         &  LinearConstraint("milk_g - almondMilk_g - cowMilk_g - soyMilk_g = 0")
          self.dk["miscellanous"].miscDk &= FormulaManager.parser("((cowMilk | soyMilk) & kiwi) -> bitter")
          self.dk["miscellanous"].miscDk &= FormulaManager.parser("dessert -> ~bitter")
          self.dk["miscellanous"].miscDk &= LinearConstraint("food_g - greenCabbage_g - carrot_g - shallot_g - soySauce_g - vinegar_g - oliveOil_g - lemonJuice_g - water_g = 0")
          self.dk["miscellanous"].miscDk &= PropositionalVariable("saladDish") >>\
                                             (LinearConstraint("ak_deltaVinegarLemonJuiceWater - vinegar_g - water_g - lemonJuice_g = 0")\
                                             & LinearConstraint("ak_equalWaterLemonJuice - water_g + lemonJuice_g = 0"))

          self.srce_case = self.srce_case = (LinearConstraint("banana_u = 2")\
                              & LinearConstraint("granulatedSugar_tbsp = 4")\
                              & LinearConstraint("vanillaSugar_u = 2")\
                              & LinearConstraint("cowMilk_L = 1.")\
                              & LinearConstraint("iceCube_u = 4")\
                              & LinearConstraint("kiwi_g = 0.")\
                              & LinearConstraint("soyMilk_g = 0.")\
                              & LinearConstraint("almondMilk_g = 0.")\
                              & PropositionalVariable("milkshake"))\
                         | (PropositionalVariable("saladDish")\
                              & LinearConstraint("carrot_u = 2")\
                              & LinearConstraint("greenCabbage_cup = 4")\
                              & LinearConstraint("oliveOil_g = 50")\
                              & LinearConstraint("shallot_u = 1")\
                              & LinearConstraint("soySauce_g = 32")\
                              & LinearConstraint("vinegar_g = 20"))

          self.tgt_problem = FormulaManager.parser("kiwi & milkshake")