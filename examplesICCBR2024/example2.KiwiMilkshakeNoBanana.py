import sys
sys.path.append(".")

from src.formula import LinearConstraint, PropositionalVariable, FormulaManager
from src.mlo_solver import  ScipySolverRounded
from src import Adaptation
from src.variable import RealVariable, IntegerVariable
from src.distance import discreteL1DistanceFunction
from src.simplificator import Daalmans

from fractions import Fraction

"""
     DECLARATION OF THE VARIABLES AND THEIR WEIGHTS
"""

weights = {
    
    #Two heuristics are used to define the weights. 
    #The first one is based on a taxonomy of the ingredient categories, with weights starting from 1 for simple ingredients
    #and multiplied by a factor of 1000 for each higher category, indicating its importance in the recipe.
    #The second one is based on the conversions between units and mass for each type of food. 
    #As there is a known correspondence of one unit to its mass for each food type, weights of unit variables are calculated according
    #to the weights of mass variables.
    
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

    #Masses are measured in grams and are nonnegative real with a lowerBound to 0.

    # Mass of almond milk, with a weight of 1, chosen as the weight of one gram of food
    RealVariable.declare("almondMilk_g", lowerBound = Fraction(0)): Fraction(1),
    # Liters of almond milk, with a weight equal to the volumic mass of one liter of milk : 1030g/L (multiplied by 1, the weight of one gram of milk)
    RealVariable.declare("almondMilk_L", lowerBound = Fraction(0)): Fraction(1030),
    # Mass of banana, with a weight of 1, chosen as the weight of one gram of food
    RealVariable.declare("banana_g", lowerBound = Fraction(0)): Fraction(1),
    # Mass of cow milk, with a weight of 1, chosen as the weight of one gram of food
    RealVariable.declare("cowMilk_g", lowerBound = Fraction(0)): Fraction(1),
    # Liters of cow milk, with a weight equal to the volumic mass of one liter of milk : 1030g/L
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
    # Liters of soy milk, with a weight equal to the volumic mass of one liter of milk : 1030g/L
    RealVariable.declare("soyMilk_L", lowerBound = Fraction(0)): Fraction(1030),
    # Sweetening power of the recipe in grams, variable that corresponds to the total amount of sugar in the recipe with a weight associated to a property of the recipe
    RealVariable.declare("sweeteningPower_g", lowerBound = Fraction(0)): Fraction(10000),
    # Mass of vanilla sugar, with a weight of 1, chosen as the weight of one gram of food
    RealVariable.declare("vanillaSugar_g", lowerBound = Fraction(0)): Fraction(1),

    #Numbers of units/tbsp/fruitTypes are nonnegative integer with a lowerBound to 0.

    # Number of bananas, with a with a weight corresponding to the average mass of a banana (115g/u)
    IntegerVariable.declare("banana_u", lowerBound = Fraction(0)): Fraction(115),
    # Number of tablespoons of granulated sugar, with a weight corresponding to the average mass of a tablespoon of granulated sugar (15g/tbsp)
    IntegerVariable.declare("granulatedSugar_tbsp", lowerBound = Fraction(0)): Fraction(15),
    # Number of ice cubes, with a weight corresponding to the average mass of an ice cube (25g/u)
    IntegerVariable.declare("iceCube_u", lowerBound = Fraction(0)): Fraction(25),
    # Number of kiwis, with a weight corresponding to the average mass of a kiwi (100g/u)
    IntegerVariable.declare("kiwi_u", lowerBound = Fraction(0)): Fraction(100),
    # Number of fruit types, variable that preserves the number of fruit types with a weight associated to a property of the recipe
    IntegerVariable.declare("nb_fruitTypes", lowerBound = Fraction(0)): Fraction(10000),
    # Number of bags of vanilla sugar, with a weight corresponding to the average mass of a bag of vanilla sugar(7.5g/u)
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
distanceFunction = discreteL1DistanceFunction(weights, epsilon=Fraction("1e-4"))

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
dk = FormulaManager.parser("(banana -> fruit) & (kiwi -> fruit)")

# DK2: For each food type and unit, there is a known correspondence of one unit of this food type to its mass,
#      e.g. the mass of 1 banana and the mass of 1 tablespoon of granulated sugar.
# Source: 
#    - Banana (https://www.aprifel.com/fr/fiche-nutritionnelle/banane/?tab=composition_analyse_nutritionnelles)
#    - Cow milk, soy milk and almond milk (rounded to the mass of cow milk) (https://conseilenagriculture.fr/calculettes/kglait-litre/)
#    - Kiwi (https://www.aprifel.com/fr/fiche-nutritionnelle/kiwi/?tab=composition_analyse_nutritionnelles)
#    - Vanilla sugar (https://www.vahine.fr/produits/sucres-et-levures/sucre-vanille)
#    - Tablespoon of granulated sugar (https://www.mgc-prevention.fr/cuisiner-sans-balance/)
#    - Ice cube of water of dimension 3x3x3cm : 27cm^3 * 0.917g/cm^3 = 24.759g, rounded to 25g (https://fr.wikipedia.org/wiki/Glace)
dk &=  LinearConstraint("banana_g - 120 * banana_u = 0")\
     & LinearConstraint("cowMilk_g - 1030 * cowMilk_L = 0")\
     & LinearConstraint("soyMilk_g - 1030 * soyMilk_L = 0")\
     & LinearConstraint("almondMilk_g - 1030 * almondMilk_L = 0")\
     & LinearConstraint("kiwi_g - 100 * kiwi_u = 0")\
     & LinearConstraint("vanillaSugar_g - 7.5 * vanillaSugar_u = 0")\
     & LinearConstraint("granulatedSugar_g - 15 * granulatedSugar_tbsp = 0")\
     & LinearConstraint("iceCube_g - 25 * iceCube_u = 0")

# DK3: Relation between each type of food and its subtypes in the taxonomy (TODO reprendre après envoie)
# The sweetening power is known for every ingredient type, e.g. 0.158 for bananas (1 gram of banana has the same sweetening power as 0.158 gram of granulated sugar), 1 for granulated sugar, etc.
# Source: The sweetening power of each ingredient is coming from USDA (https://fdc.nal.usda.gov/) apart from almond milk (https://www.bjorg.fr/produits/lait-amande-bio/)
# and vanilla sugar (https://www.vahine.fr/produits/sucres-et-levures/sucre-vanille)

dk &= LinearConstraint("sweeteningPower_g  - granulatedSugar_g\
                                           - 0.158 * banana_g\
                                           - 0.0899 * kiwi_g\
                                           - 0.98 * vanillaSugar_g\
                                           - 0.0489 * cowMilk_g\
                                           - 0.0368 * soyMilk_g\
                                           - 0.04 * almondMilk_g = 0")\
     & LinearConstraint("fruit_g - banana_g - kiwi_g = 0")\
     & LinearConstraint("food_g - fruit_g - milk_g - granulatedSugar_g - iceCube_g - vanillaSugar_g = 0")\
     & LinearConstraint("milk_g - almondMilk_g - cowMilk_g - soyMilk_g = 0")

# DK4: Almond milk, cow milk and soy milk are 3 types of milks (and, to make it simpler, it can be assumed that there
#      are no other types of milk in my fridge).
dk &= FormulaManager.parser("(almondMilk | cowMilk | soyMilk) <-> milk")

# DK5: Cow milk and soy milk associated to kiwis give a bitter taste.
dk &= FormulaManager.parser("((cowMilk | soyMilk) & kiwi) -> bitter")

# DK6: A milkshake is a dessert and a dessert must not be bitter.
dk &=  FormulaManager.parser("(milkshake -> dessert) & (dessert -> ~bitter)")

# DK7: Relations between propositional variables and numerical variables.
dk &=  (PropositionalVariable("banana") // ~LinearConstraint("banana_g <= 0"))\
     & (PropositionalVariable("kiwi") // ~LinearConstraint("kiwi_g <= 0"))\
     & (PropositionalVariable("cowMilk") // ~LinearConstraint("cowMilk_g <= 0"))\
     & (PropositionalVariable("soyMilk") // ~LinearConstraint("soyMilk_g <= 0"))\
     & (PropositionalVariable("almondMilk") // ~LinearConstraint("almondMilk_g <= 0"))\

"""
     SPECIFICATION OF THE SOURCE CASE AND OF THE TARGET PROBLEM
"""

# Source case
src =  LinearConstraint("banana_u = 2")\
     & LinearConstraint("granulatedSugar_tbsp = 4")\
     & LinearConstraint("vanillaSugar_u = 2")\
     & LinearConstraint("cowMilk_L = 1.")\
     & LinearConstraint("iceCube_u = 4")\
     & LinearConstraint("kiwi_g = 0.")\
     & LinearConstraint("soyMilk_g = 0.")\
     & LinearConstraint("almondMilk_g = 0.")\
     & PropositionalVariable("milkshake")\

# Target problem
tgt = FormulaManager.parser("kiwi & milkshake & ~banana")

res = adaptator.execute(src, tgt, dk)[1]

"""
     EXPECTED RESULT

00m35.671s | Solution found with distance of 10644:

        almondMilk_g = 1014.999999999972
        almondMilk_L = 0.985436893204
            banana_g = 0.0
            banana_u = 0
           cowMilk_g = 0.0
           cowMilk_L = 0.0
              food_g = 1445.0
             fruit_g = 200.0
   granulatedSugar_g = 75.0
granulatedSugar_tbsp = 5
           iceCube_g = 125.0
           iceCube_u = 5
              kiwi_g = 200.0
              kiwi_u = 2
              milk_g = 1014.999999999972
           soyMilk_g = 0.0
           soyMilk_L = 0.0
   sweeteningPower_g = 162.980000000003
      vanillaSugar_g = 30.0
      vanillaSugar_u = 4
"""
