"""
     Example 4: adaptation of a carrot and cabage salad to remove the vinegar, using an adaptation rule.
"""

from src.olaaaf.formula import LinearConstraint, PropositionalVariable
from src.olaaaf.mlo_solver import  ScipySolverRounded
from src.olaaaf import Adaptation
from src.olaaaf.variable import RealVariable, IntegerVariable
from src.olaaaf.distance import DiscreteL1DistanceFunction
from src.olaaaf.simplificator import Daalmans

from fractions import Fraction

"""
     DECLARATION OF THE VARIABLES AND THEIR WEIGHTS
"""

weights = {
    
    # Presence of carrot, a boolean variable with a light weight corresponding to a specific ingredient.
    PropositionalVariable("carrot"): Fraction(1),
    # Presence of green cabbage, a boolean variable with a light weight corresponding to a specific ingredient.
    PropositionalVariable("greenCabbage"): Fraction(1),
    # Presence of lemon juice, a boolean variable with a light weight corresponding to a specific ingredient.
    PropositionalVariable("lemonJuice"): Fraction(1),
    # Presence of olive oil, a boolean variable with a light weight corresponding to a specific ingredient.
    PropositionalVariable("oliveOil"): Fraction(1),
    # Is the recipe a salad dish, a boolean variable with a very heavy weight associated to a complete recipe.
    PropositionalVariable("saladDish"): Fraction(1000000),
    # Presence of shallot, a boolean variable with a light weight corresponding to a specific ingredient.
    PropositionalVariable("shallot"): Fraction(1),
    # Presence of soy sauce, a boolean variable with a light weight corresponding to a specific ingredient.
    PropositionalVariable("soySauce"): Fraction(1),
    # Presence of vinegar, a boolean variable with a light weight corresponding to a specific ingredient.
    PropositionalVariable("vinegar"): Fraction(1),
    # Presence of water, a boolean variable with a light weight corresponding to a specific ingredient.
    PropositionalVariable("water"): Fraction(1),

    # Masses are measured in grams and are nonnegative real with a lowerBound to 0.
    # Volumes are measured in liters and are nonnegative real with a lowerBound to 0.

    # Mass of carrot, with a weight of 1, chosen as the weight of one gram of food.
    RealVariable.declare("carrot_g", lowerBound = Fraction(0)): Fraction(1),
    # Mass of food, variable used to preserve the total mass of ingredients (and therefore their proportions), with a weight associated
    #to a wide category of ingredients or a property of a recipe.
    RealVariable.declare("food_g", lowerBound = Fraction(0)): Fraction(10000),
    # Mass of green cabbage, with a weight of 1, chosen as the weight of one gram of food.
    RealVariable.declare("greenCabbage_g", lowerBound = Fraction(0)): Fraction(1),
    # Mass of lemon juice, with a weight of 1, chosen as the weight of one gram of food.
    RealVariable.declare("lemonJuice_g", lowerBound = Fraction(0)): Fraction(1),
    # Liters of lemon juice, with a weight equal to the volumic mass of one liter of juice: 1031.33g/L
    RealVariable.declare("lemonJuice_L", lowerBound = Fraction(0)): Fraction(1031.33),
    # Mass of olive oil, with a weight of 1, chosen as the weight of one gram of food.
    RealVariable.declare("oliveOil_g", lowerBound = Fraction(0)): Fraction(1),
    # Liters of olive oil, with a weight equal to the volumic mass of one liter of oil: 912.98g/L
    RealVariable.declare("oliveOil_L", lowerBound = Fraction(0)): Fraction(912.98),
    # Mass of shallot, with a weight of 1, chosen as the weight of one gram of food.
    RealVariable.declare("shallot_g", lowerBound = Fraction(0)): Fraction(1),
    # Mass of soy sauce, with a weight of 1, chosen as the weight of one gram of food.
    RealVariable.declare("soySauce_g", lowerBound = Fraction(0)): Fraction(1),
    # Liters of soy sauce, with a weight equal to the volumic mass of one liter of sauce: 1077.82g/L
    RealVariable.declare("soySauce_L", lowerBound = Fraction(0)): Fraction(1077.82),
    # Mass of vinegar, with a weight of 1, chosen as the weight of one gram of food.
    RealVariable.declare("vinegar_g", lowerBound = Fraction(0)): Fraction(1),
    # Liters of vinegar, with a weight equal to the volumic mass of one liter of vinegar: 1014.42g/L
    RealVariable.declare("vinegar_L", lowerBound = Fraction(0)): Fraction(1014.42),
    # Mass of water, with a weight of 1, chosen as the weight of one gram of food.
    RealVariable.declare("water_g", lowerBound = Fraction(0)): Fraction(1),
    # Liters of water, with a weight equal to the volumic mass of one liter of water: 1000g/L
    RealVariable.declare("water_L", lowerBound = Fraction(0)): Fraction(1000),

    # Numbers of units/cups are nonnegative integer with a lowerBound to 0.
    # _cup refers to metric cups.

    # Number of carrots, with a weight corresponding to the average mass of a carrot (125g/u).
    IntegerVariable.declare("carrot_u", lowerBound = Fraction(0)): Fraction(125),
    # Number of cups of sliced green cabbage, with a weight corresponding to the average mass of a metric cup of green cabbage (94.05g/cup).
    IntegerVariable.declare("greenCabbage_cup", lowerBound = Fraction(0)): Fraction(94.05),
    # Number of shallots, with a weight corresponding to the average mass of a shallot (25g/u).
    IntegerVariable.declare("shallot_u", lowerBound = Fraction(0)): Fraction(25),

    # The two adaptation rules that form the Adaptation Knowledge receive a real variable each, which allows to set a very high weight to both.

    RealVariable.declare("ak_deltaVinegarLemonJuiceWater"): Fraction(1e12),
    RealVariable.declare("ak_equalWaterLemonJuice"): Fraction(1e12)
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
distanceFunction = DiscreteL1DistanceFunction(weights, epsilon=Fraction("1e-4"))

# Declaration of the Adaptation object used for this example, using all the variables declared beforehand and specifying
#that we wish to have only one valid solution instead of all the possible ones.
adaptator = Adaptation(solver, distanceFunction, simplifiers, onlyOneSolution=True)

# Preloading the adaptator, initializaing all the b2i_ variables and making it so the user can use them in the following parts of the script.
adaptator.preload()

"""
     SPECIFICATION OF DOMAIN KNOWLEDGE
"""

# DK1: For each food type and unit, there is a known correspondence of one unit/liter/metric cup of this food type to its mass,
#      e.g. the mass of 1 carrot and the mass of 1 metric cup of sliced green cabbage.
# Source: 
#    - Carrot (https://www.aprifel.com/en/nutritional-sheet/carot/?tab=composition_analyse_nutritionnelles).
#    - Shallot (https://www.aprifel.com/en/nutritional-sheet/shallot/?tab=composition_analyse_nutritionnelles).
#    - Green cabbage, lemon juice, olive oil, soy sauce and vinegar are all calculated from the same source (https://www.aqua-calc.com/calculate/food-volume-to-weight),
#      the most generic type being selected each time.
dk = LinearConstraint("carrot_g - 125 * carrot_u = 0")\
    & LinearConstraint("greenCabbage_g - 94.05 * greenCabbage_cup = 0")\
    & LinearConstraint("lemonJuice_g - 1031.33 * lemonJuice_L = 0")\
    & LinearConstraint("oliveOil_g - 912.98 * oliveOil_L = 0")\
    & LinearConstraint("shallot_g - 25 * shallot_u = 0")\
    & LinearConstraint("soySauce_g - 1077.82 * soySauce_L = 0")\
    & LinearConstraint("vinegar_g - 1014.42 * vinegar_L = 0")\
    & LinearConstraint("water_g - 1000 * water_L = 0")

# DK2: The mass of the entire recipe is stored in the variable food_g.
dk &= LinearConstraint("food_g - greenCabbage_g - carrot_g - shallot_g - soySauce_g - vinegar_g - oliveOil_g - lemonJuice_g - water_g = 0")

# DK3: Relations between propositional variables and numerical variables.
dk &= (PropositionalVariable("carrot") // ~LinearConstraint("carrot_g <= 0"))\
    & (PropositionalVariable("greenCabbage") // ~LinearConstraint("greenCabbage_g <= 0"))\
    & (PropositionalVariable("lemonJuice") // ~LinearConstraint("lemonJuice_g <= 0"))\
    & (PropositionalVariable("oliveOil") // ~LinearConstraint("oliveOil_g <= 0"))\
    & (PropositionalVariable("shallot") // ~LinearConstraint("shallot_g <= 0"))\
    & (PropositionalVariable("soySauce") // ~LinearConstraint("soySauce_g <= 0"))\
    & (PropositionalVariable("vinegar") // ~LinearConstraint("vinegar_g <= 0"))\
    & (PropositionalVariable("water") // ~LinearConstraint("water_g <= 0"))

# AK: The two adaptation rules applied to the source case when the recipe is a salad dish.
#    - ak_deltaVinegarLemonJuiceWater states that vinegar can be replaced by an equal combined amount (in grams) of lemon juice and water.
#    - ak_equalWaterLemonJuice states that there should be always the same proportions of water and lemon juice in the recipe.
ak = PropositionalVariable("saladDish") >>\
        (LinearConstraint("ak_deltaVinegarLemonJuiceWater - vinegar_g - water_g - lemonJuice_g = 0")\
        & LinearConstraint("ak_equalWaterLemonJuice - water_g + lemonJuice_g = 0"))

"""
     SPECIFICATION OF THE SOURCE CASE AND OF THE TARGET PROBLEM
"""

# Source case
srce_case = PropositionalVariable("saladDish")\
    & LinearConstraint("carrot_u = 2")\
    & LinearConstraint("greenCabbage_cup = 4")\
    & LinearConstraint("oliveOil_g = 50")\
    & LinearConstraint("shallot_u = 1")\
    & LinearConstraint("soySauce_g = 32")\
    & LinearConstraint("vinegar_g = 20")

# Target problem
tgt_problem = PropositionalVariable("saladDish")\
    & PropositionalVariable("carrot")\
    & PropositionalVariable("greenCabbage")\
    & ~PropositionalVariable("vinegar")

min_dist, tgt_case = adaptator.execute(srce_case, tgt_problem, dk & ak, withMaxDist=True)

"""
     RESULT

00m09.522s | Solution found with distance of 81:

        carrot_g = 250.
        carrot_u = 2
          food_g = 753.
greenCabbage_cup = 4
  greenCabbage_g = 376.
    lemonJuice_g = 10.
    lemonJuice_L = 0.00970
      oliveOil_g = 50.
      oliveOil_L = 0.0548
       shallot_g = 25.
       shallot_u = 1
      soySauce_g = 32.
      soySauce_L = 0.0297
       vinegar_g = 0.
       vinegar_L = 0.
         water_g = 10.
         water_L = 0.0100
         
"""
