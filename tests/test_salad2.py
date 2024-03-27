from olaaaf.formula import LinearConstraint, PropositionalVariable, EnumeratedType
from olaaaf.mlo_solver import  ScipySolverRounded
from olaaaf import Adaptation
from olaaaf.variable import RealVariable, IntegerVariable
from olaaaf.distance import DiscreteL1DistanceFunction
from olaaaf.simplificator import Daalmans
from olaaaf.projector import FloatConvexHullProjector

from fractions import Fraction

"""
     DECLARATION OF THE VARIABLES AND THEIR WEIGHTS
"""

weights = {

    #Two heuristics are used to define the weights. 
    #The first one is based on a taxonomy of the ingredient categories, with weights starting from 1 for simple ingredients
    #and multiplied by a factor of 100 for each higher category, indicating its importance in the recipe.
    #The second one is based on the conversions between units/liters and mass for each type of food. 
    #As there is a known correspondence of one unit to its mass for each food type, weights of unit variables are calculated according
    #to the weights of mass variables.

    # Presence of green cabbage, a boolean variable with a light weight corresponding to a specific ingredient
    PropositionalVariable("greenCabbage"): Fraction(1),
    # Presence of carrot, a boolean variable with a light weight corresponding to a specific ingredient
    PropositionalVariable("carrot"): Fraction(1),
    # Presence of shallot, a boolean variable with a light weight corresponding to a specific ingredient
    PropositionalVariable("shallot"): Fraction(1),
    # Presence of soy sauce, a boolean variable with a light weight corresponding to a specific ingredient
    PropositionalVariable("soySauce"): Fraction(1),
    # Presence of vinegar, a boolean variable with a light weight corresponding to a specific ingredient
    PropositionalVariable("vinegar"): Fraction(1),
    # Is the recipe a salad dish, a boolean variable with a very heavy weight associated to a complete recipe
    PropositionalVariable("saladDish"): Fraction(1000000),
    # Presence of olive oil, a boolean variable with a light weight corresponding to a specific ingredient
    PropositionalVariable("oliveOil"): Fraction(1),
    # Presence of lemon juice, a boolean variable with a light weight corresponding to a specific ingredient
    PropositionalVariable("lemonJuice"): Fraction(1),
    # Presence of water, a boolean variable with a light weight corresponding to a specific ingredient
    PropositionalVariable("water"): Fraction(1),


    RealVariable.declare("greenCabbage_g", lowerBound = Fraction(0)): Fraction(1),
    RealVariable.declare("carrot_g", lowerBound = Fraction(0)): Fraction(1),
    RealVariable.declare("shallot_g", lowerBound = Fraction(0)): Fraction(1),
    RealVariable.declare("soySauce_g", lowerBound = Fraction(0)): Fraction(1),
    RealVariable.declare("vinegar_g", lowerBound = Fraction(0)): Fraction(1),
    RealVariable.declare("oliveOil_g", lowerBound = Fraction(0)): Fraction(1),
    RealVariable.declare("lemonJuice_g", lowerBound = Fraction(0)): Fraction(1),
    RealVariable.declare("water_g", lowerBound = Fraction(0)): Fraction(1),
    RealVariable.declare("food_g", lowerBound = Fraction(0)): Fraction(1e6),
    RealVariable.declare("vinegar_L", lowerBound = Fraction(0)): Fraction(1010),
    RealVariable.declare("oliveOil_L", lowerBound = Fraction(0)): Fraction(913.7),
    RealVariable.declare("lemonJuice_L", lowerBound = Fraction(0)): Fraction(1100),
    RealVariable.declare("water_L", lowerBound = Fraction(0)): Fraction(1000),
    RealVariable.declare("soySauce_L", lowerBound = Fraction(0)): Fraction(1077),

    IntegerVariable.declare("greenCabbage_cup", lowerBound = Fraction(0)): Fraction(94),
    IntegerVariable.declare("carrot_u", lowerBound = Fraction(0)): Fraction(61),
    IntegerVariable.declare("shallot_u", lowerBound = Fraction(0)): Fraction(30),

    RealVariable.declare("ak1"): Fraction(1e12),
    RealVariable.declare("ak2"): Fraction(1e12)
}

"""
     INITATIALIZATION OF THE SOLVER
"""

solver = ScipySolverRounded()
simplifier = [Daalmans(solver)]
adaptator = Adaptation(solver, DiscreteL1DistanceFunction(weights, epsilon=Fraction("1e-4")), simplifier, onlyOneSolution=True)

adaptator.preload()

"""
     SPECIFICATION OF DOMAIN KNOWLEDGE
"""

# Règle...
dk = LinearConstraint("food_g - greenCabbage_g - carrot_g - shallot_g - soySauce_g - vinegar_g - oliveOil_g - lemonJuice_g - water_g = 0")

# Règle...
dk &= LinearConstraint("water_g - 1000 * water_L = 0")\
    & LinearConstraint("vinegar_g - 1010 * vinegar_L = 0")\
    & LinearConstraint("oliveOil_g - 913.7 * oliveOil_L = 0")\
    & LinearConstraint("lemonJuice_g - 1100 * lemonJuice_L = 0")\
    & LinearConstraint("greenCabbage_g - 94 * greenCabbage_cup = 0")\
    & LinearConstraint("carrot_g - 61 * carrot_u = 0")\
    & LinearConstraint("shallot_g - 30 * shallot_u = 0")\
    & LinearConstraint("soySauce_g - 1077 * soySauce_L = 0")

# Règle...
dk &= (PropositionalVariable("water") // ~LinearConstraint("water_g <= 0"))\
    & (PropositionalVariable("vinegar") // ~LinearConstraint("vinegar_g <= 0"))\
    & (PropositionalVariable("oliveOil") // ~LinearConstraint("oliveOil_g <= 0"))\
    & (PropositionalVariable("lemonJuice") // ~LinearConstraint("lemonJuice_g <= 0"))\
    & (PropositionalVariable("greenCabbage") // ~LinearConstraint("greenCabbage_g <= 0"))\
    & (PropositionalVariable("carrot") // ~LinearConstraint("carrot_g <= 0"))\
    & (PropositionalVariable("shallot") // ~LinearConstraint("shallot_g <= 0"))\
    & (PropositionalVariable("soySauce") // ~LinearConstraint("soySauce_g <= 0"))

# Adaptation Knowledge...
ak = PropositionalVariable("saladDish") >>\
        (LinearConstraint("ak1 - vinegar_g - water_g - lemonJuice_g = 0")\
        & LinearConstraint("ak2 - water_g + lemonJuice_g = 0"))

"""
     SPECIFICATION OF THE SOURCE CASE AND OF THE TARGET PROBLEM
"""

# Source case... (variables dans le même ordre que article)
x_src = PropositionalVariable("saladDish")\
    & LinearConstraint("carrot_u = 4")\
    & LinearConstraint("greenCabbage_cup = 4")\
    & LinearConstraint("vinegar_g = 20")\
    & LinearConstraint("oliveOil_g = 50")\
    & LinearConstraint("soySauce_g = 32")\
    & LinearConstraint("shallot_u = 1")

# Target problem...
y_trgt = PropositionalVariable("saladDish")\
    & PropositionalVariable("carrot")\
    & PropositionalVariable("greenCabbage")\
    & ~PropositionalVariable("vinegar")

res = adaptator.execute(x_src, y_trgt, dk & ak)