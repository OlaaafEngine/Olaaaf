# Garage collecting
import gc
gc.collect()

"""
     Example 1: adaptation of a banana milkshake recipe to a kiwi milkshake recipe.
"""

from src.olaaaf.formula import LinearConstraint, PropositionalVariable, FormulaManager
from src.olaaaf.mlo_solver import  ScipySolverRounded
from src.olaaaf import Adaptation
from src.olaaaf.variable import RealVariable, IntegerVariable, VariableManager
from src.olaaaf.distance import DiscreteL1DistanceFunction
from src.olaaaf.simplificator import Daalmans
from src.olaaaf.domainKnowledge import ExistenceKnowledge, ConversionKnowledge, Taxonomy, MiscellanousDomainKnowledge

from fractions import Fraction

"""
     DECLARATION OF THE VARIABLES AND THEIR WEIGHTS
"""

weights = {
    
    # Presence of almond milk, a boolean variable with a light weight corresponding to a specific ingredient
    PropositionalVariable("almondMilk", fmName="almondMilk"): Fraction(1),
    # Presence of banana, a boolean variable with a light weight corresponding to a specific ingredient
    PropositionalVariable("banana", fmName="banana"): Fraction(1),
    # Presence of bitterness, a boolean variable with a weight associated to a property of a recipe
    PropositionalVariable("bitter", fmName="bitter"): Fraction(10000),
    # Presence of cow milk, a boolean variable with a light weight corresponding to a specific ingredient
    PropositionalVariable("cowMilk", fmName="cowMilk"): Fraction(1),
    # Is the recipe a dessert, a boolean variable with a weight associated to a wide category of ingredients or a property of a recipe
    PropositionalVariable("dessert", fmName="dessert"): Fraction(10000),
    # Presence of fruit, a boolean variable with a weight associated to category of ingredients
    PropositionalVariable("fruit", fmName="fruit"): Fraction(100),
    # Presence of kiwi, a boolean variable with a light weight corresponding to a specific ingredient
    PropositionalVariable("kiwi", fmName="kiwi"): Fraction(1),
    # Presence of milk, a boolean variable with a weight associated to category of ingredients
    PropositionalVariable("milk", fmName="milk"): Fraction(100),
    # Is the recipe a milkshake, a boolean variable with a very heavy weight associated to a complete recipe
    PropositionalVariable("milkshake", fmName="milkshake"): Fraction(1000000),
    # Presence of soy milk, a boolean variable with a light weight corresponding to a specific ingredient
    PropositionalVariable("soyMilk", fmName="soyMilk"): Fraction(1),

    #Masses are measured in grams and volumes in liters and are nonnegative real with a lowerBound to 0.

    # Mass of almond milk, with a weight of 1, chosen as the weight of one gram of food
    RealVariable.declare("almondMilk_g", lowerBound = Fraction(0)): Fraction(1),
    # Liters of almond milk, with a weight equal to the volumic mass of one liter of milk: 1030g/L (multiplied by 1, the weight of one gram of milk)
    RealVariable.declare("almondMilk_L", lowerBound = Fraction(0)): Fraction(1030),
    # Mass of banana, with a weight of 1, chosen as the weight of one gram of food
    RealVariable.declare("banana_g", lowerBound = Fraction(0)): Fraction(1),
    # Mass of cow milk, with a weight of 1, chosen as the weight of one gram of food
    RealVariable.declare("cowMilk_g", lowerBound = Fraction(0)): Fraction(1),
    # Liters of cow milk, with a weight equal to the volumic mass of one liter of milk: 1030g/L
    RealVariable.declare("cowMilk_L", lowerBound = Fraction(0)): Fraction(1030),
    # Mass of food, variable used to preserve the total mass of ingredients (and therefore their proportions), with a weight associated
    # to a wide category of ingredients or a property of a recipe
    RealVariable.declare("food_g", lowerBound = Fraction(0)): Fraction(10000),
    # Mass of fruit, with a weight associated to a category of ingredients
    RealVariable.declare("fruit_g", lowerBound = Fraction(0)): Fraction(100),
    # Mass of granulated sugar, with a weight of 1, chosen as the weight of one gram of food
    RealVariable.declare("granulatedSugar_g", lowerBound = Fraction(0)): Fraction(1),
    # Mass of ice cube, with a weight of 1, chosen as the weight of one gram of food
    RealVariable.declare("iceCube_g", lowerBound = Fraction(0)): Fraction(1),
    # Mass of kiwi, with a weight of 1, chosen as the weight of one gram of food
    RealVariable.declare("kiwi_g", lowerBound = Fraction(0)): Fraction(1),
    # Mass of milk, with a weight associated to a category of ingredients
    RealVariable.declare("milk_g", lowerBound = Fraction(0)): Fraction(100),
    # Mass of soy milk, with a weight of 1, chosen as the weight of one gram of food
    RealVariable.declare("soyMilk_g", lowerBound = Fraction(0)): Fraction(1),
    # Liters of soy milk, with a weight equal to the volumic mass of one liter of milk: 1030g/L
    RealVariable.declare("soyMilk_L", lowerBound = Fraction(0)): Fraction(1030),
    # Sweetening power of the recipe in grams, variable that corresponds to the total amount of sugar in the recipe with a weight associated to a property of the recipe
    RealVariable.declare("sweeteningPower_g", lowerBound = Fraction(0)): Fraction(10000),
    # Mass of vanilla sugar, with a weight of 1, chosen as the weight of one gram of food
    RealVariable.declare("vanillaSugar_g", lowerBound = Fraction(0)): Fraction(1),

    #Numbers of units/tbsp/fruitTypes are nonnegative integer with a lowerBound to 0.

    # Number of bananas, with a weight corresponding to the average mass of a banana (115g/u)
    IntegerVariable.declare("banana_u", lowerBound = Fraction(0)): Fraction(115),
    # Number of tablespoons of granulated sugar, with a weight corresponding to the average mass of a tablespoon of granulated sugar (15g/tbsp)
    IntegerVariable.declare("granulatedSugar_tbsp", lowerBound = Fraction(0)): Fraction(15),
    # Number of ice cubes, with a weight corresponding to the average mass of an ice cube (25g/u)
    IntegerVariable.declare("iceCube_u", lowerBound = Fraction(0)): Fraction(25),
    # Number of kiwis, with a weight corresponding to the average mass of a kiwi (100g/u)
    IntegerVariable.declare("kiwi_u", lowerBound = Fraction(0)): Fraction(100),
    # Number of bags of vanilla sugar, with a weight corresponding to the average mass of a bag of vanilla sugar (7.5g/u)
    IntegerVariable.declare("vanillaSugar_u", lowerBound = Fraction(0)): Fraction(7.5),

}

"""
     INITATIALIZATION OF THE SOLVER
"""

# Declaration of the MLO Solver used for this example.
# Here, we chose to use a rounded (to limit floating points erros) version of HiGHS using Scipy's wrapper.
solver = ScipySolverRounded()

# Declaration of the simplification algorithms used for this example.
# Here, we chose to only use Daalmans' algorithm.
simplifiers = [Daalmans(solver)]

# Declaration of the discretized Manhattan distance function used for this example, using the weights declared above and an epsilon of 1e-4.
distanceFunction = DiscreteL1DistanceFunction(weights)

# Declaration of the Adaptation object used for this example, using all the variables declared beforehand and specifying
# that we wish to have only one valid solution instead of all the possible ones.
adaptator = Adaptation(solver, distanceFunction, simplifiers, onlyOneSolution=True)

# Preloading the adaptator, initializaing all the b2i_ variables and making it so the user can use them in the following parts of the script
# (Necessary for DK8, the nb_fruitTypes constraint)
adaptator.preload()

"""
     SPECIFICATION OF DOMAIN KNOWLEDGE
"""

# DK1: Bananas and kiwis are fruits.
# dk = FormulaManager.parser("(banana -> fruit) & (kiwi -> fruit)")

tax = Taxonomy()
tax.addElements(["banana", "kiwi", "fruit", "almondMilk", "cowMilk", "soyMilk", "milk", "dessert", "milkshake"])
tax.addChildren("milk", ["almondMilk", "cowMilk", "soyMilk"])
tax.addChildren("fruit", ["banana", "kiwi"])
tax.addChildren("dessert", ["milkshake"])

# DK2: For each food type and unit, there is a known correspondence of one unit of this food type to its mass,
#      e.g. the mass of 1 banana and the mass of 1 tablespoon of granulated sugar.
# Source: 
#    - Banana (https://www.aprifel.com/en/nutritional-sheet/banana/?tab=composition_analyse_nutritionnelles)
#    - Cow milk, soy milk and almond milk (rounded to the mass of cow milk) (https://conseilenagriculture.fr/calculettes/kglait-litre/)
#    - Kiwi (https://www.aprifel.com/fr/fiche-nutritionnelle/kiwi/?tab=composition_analyse_nutritionnelles)
#    - Vanilla sugar (https://www.vahine.fr/produits/sucres-et-levures/sucre-vanille)
#    - Tablespoon of granulated sugar (https://www.mgc-prevention.fr/cuisiner-sans-balance/)
#    - Ice cube of water of dimension 3x3x3cm : 27cm^3 * 0.917g/cm^3 = 24.759g, rounded to 25g (https://fr.wikipedia.org/wiki/Glace)
ck = ConversionKnowledge()
ck.addConversions([((VariableManager.get("banana_g"), Fraction(120)), (VariableManager.get("banana_u"), Fraction(1))),
                   ((VariableManager.get("cowMilk_g"), Fraction(1030)), (VariableManager.get("cowMilk_L"), Fraction(1))),
                   ((VariableManager.get("soyMilk_g"), Fraction(1030)), (VariableManager.get("soyMilk_L"), Fraction(1))),
                   ((VariableManager.get("almondMilk_g"), Fraction(1030)), (VariableManager.get("almondMilk_L"), Fraction(1))),
                   ((VariableManager.get("kiwi_g"), Fraction(100)), (VariableManager.get("kiwi_u"), Fraction(1))),
                   ((VariableManager.get("vanillaSugar_g"), Fraction(7.5)), (VariableManager.get("vanillaSugar_u"), Fraction(1))),
                   ((VariableManager.get("granulatedSugar_g"), Fraction(15)), (VariableManager.get("granulatedSugar_tbsp"), Fraction(1))),
                   ((VariableManager.get("iceCube_g"), Fraction(25)), (VariableManager.get("iceCube_u"), Fraction(1)))])

# DK3: Relation between each type of food and its subtypes in the taxonomy (e.g. the mass of fruits is the sum of the masses of bananas,kiwis, etc.).
# The sweetening power is known for every ingredient type, e.g. 0.158 for bananas (1 gram of banana has the same sweetening power as 0.158 gram of granulated sugar), 1 for granulated sugar, etc.
# Source: The sweetening power of each ingredient is coming from USDA (https://fdc.nal.usda.gov/) apart from almond milk (https://www.bjorg.fr/produits/lait-amande-bio/)
# and vanilla sugar (https://www.vahine.fr/produits/sucres-et-levures/sucre-vanille)

dk = LinearConstraint("sweeteningPower_g  - granulatedSugar_g\
                                           - 0.158 * banana_g\
                                           - 0.0899 * kiwi_g\
                                           - 0.98 * vanillaSugar_g\
                                           - 0.0489 * cowMilk_g\
                                           - 0.0368 * soyMilk_g\
                                           - 0.04 * almondMilk_g = 0")\
     & LinearConstraint("fruit_g - banana_g - kiwi_g = 0")\
     & LinearConstraint("food_g - fruit_g - milk_g - granulatedSugar_g - iceCube_g - vanillaSugar_g = 0")\
     & LinearConstraint("milk_g - almondMilk_g - cowMilk_g - soyMilk_g = 0")

# DK5: Cow milk and soy milk associated to kiwis give a bitter taste.
dk &= FormulaManager.parser("((cowMilk | soyMilk) & kiwi) -> bitter")

# DK6: A milkshake is a dessert and a dessert must not be bitter.
dk &=  FormulaManager.parser("dessert -> ~bitter")

ek = ExistenceKnowledge({
    PropositionalVariable("banana"): VariableManager.get("banana_g"),
     PropositionalVariable("kiwi"): VariableManager.get("kiwi_g"),
     PropositionalVariable("cowMilk"): VariableManager.get("cowMilk_g"),
     PropositionalVariable("soyMilk"): VariableManager.get("soyMilk_g"),
     PropositionalVariable("almondMilk"): VariableManager.get("almondMilk_g")
})

"""
     SPECIFICATION OF THE SOURCE CASE AND OF THE TARGET PROBLEM
"""

# Source case
srce_case =  LinearConstraint("banana_u = 2")\
     & LinearConstraint("granulatedSugar_tbsp = 4")\
     & LinearConstraint("vanillaSugar_u = 2")\
     & LinearConstraint("cowMilk_L = 1.")\
     & LinearConstraint("iceCube_u = 4")\
     & LinearConstraint("kiwi_g = 0.")\
     & LinearConstraint("soyMilk_g = 0.")\
     & LinearConstraint("almondMilk_g = 0.")\
     & PropositionalVariable("milkshake")\

# Target problem
tgt_problem = FormulaManager.parser("kiwi & milkshake")

min_dist, tgt_case = adaptator.execute(srce_case, tgt_problem, domainKnowledge={"conversion": ck,
                                                                                "existence": ek,
                                                                                "taxonomy": tax,
                                                                                "miscellanous": MiscellanousDomainKnowledge(dk)})

"""
     RESULT

00m37.095s | Solution found with distance of 9743:

        almondMilk_g = 978.
        almondMilk_L = 0.949
            banana_g = 120.
            banana_u = 1
           cowMilk_g = 0.
           cowMilk_L = 0.
              food_g = 1445.
             fruit_g = 220.
   granulatedSugar_g = 15.
granulatedSugar_tbsp = 1
           iceCube_g = 150.
           iceCube_u = 6
              kiwi_g = 100.
              kiwi_u = 1
              milk_g = 978.
           soyMilk_g = 0.
           soyMilk_L = 0.
   sweeteningPower_g = 163.
      vanillaSugar_g = 82.5
      vanillaSugar_u = 11
      
"""
