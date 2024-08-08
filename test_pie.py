# Garage collecting
import gc
gc.collect()

from src.olaaaf.formula import LinearConstraint, PropositionalVariable, FormulaManager
from src.olaaaf.mlo_solver import  ScipySolverRounded
from src.olaaaf import Adaptation
from src.olaaaf.variable import RealVariable, IntegerVariable, VariableManager
from src.olaaaf.distance import DiscreteL1DistanceFunction
from src.olaaaf.simplificator import Daalmans
from src.olaaaf.domainKnowledge import Taxonomy, ExistenceKnowledge, ConversionKnowledge, MiscellanousDomainKnowledge

from fractions import Fraction

"""
     DECLARATION OF THE VARIABLES AND THEIR WEIGHTS
"""

weights = {
    
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

"""
     INITATIALIZATION OF THE SOLVER
"""

# Declaration of the MLO Solver used for this example.
# Here, we chose to use a rounded (to limit floating points erros) version of HiGHS using Scipy's wrapper.
solver = ScipySolverRounded()

# Declaration of the simplification algorithms used for this example.
# Here, we chose to only use Daalmans' algorithm.
simplifiers = [Daalmans(solver)]

# Declaration of the discretized Manhattan distance function used for this example, using the weights declared above.
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

# Taxonomy

tax = Taxonomy()
tax.addElements(["meat", "beef", "chicken", "groundBeef", "beefSteak", "chickenBreast", "chickenThigh"])
tax.addChildren("meat", ["beef", "chicken"])
tax.addChildren("beef", ["groundBeef", "beefSteak"])
tax.addChildren("chicken", ["chickenBreast", "chickenThigh"])

# Existence Knowledge

ek = ExistenceKnowledge({
    PropositionalVariable("beef"): VariableManager.get("beef_g"),
    PropositionalVariable("groundBeef"): VariableManager.get("groundBeef_g"),
    PropositionalVariable("beefSteak"): VariableManager.get("beefSteak_g"),
    PropositionalVariable("chicken"): VariableManager.get("chicken_g"),
    PropositionalVariable("chickenBreast"): VariableManager.get("chickenBreast_g"),
    PropositionalVariable("chickenThigh"): VariableManager.get("chickenThigh_g"),
    PropositionalVariable("eggYolk"): VariableManager.get("eggYolk_g"),
    PropositionalVariable("puffPastry"): VariableManager.get("puffPastry_g"),
    PropositionalVariable("cream"): VariableManager.get("cream_g"),
})

# Conversion Knowledge

ck = ConversionKnowledge()
ck.addConversions([((VariableManager.get("eggYolk_u"), Fraction(1)), (VariableManager.get("eggYolk_g"), Fraction(17))),
                   ((VariableManager.get("puffPastry_u"), Fraction(1)), (VariableManager.get("puffPastry_g"), Fraction(130)))])

# DK: protein and fat
dk = LinearConstraint("protein_g - 0.259*groundBeef_g\
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
                                 - chickenThigh_g = 0")\
                              
dk &= (PropositionalVariable("beef") // ~LinearConstraint("beef_g = 0"))\
    & (PropositionalVariable("groundBeef") // ~LinearConstraint("groundBeef_g = 0"))\
    & (PropositionalVariable("beefSteak") // ~LinearConstraint("beefSteak_g = 0"))\
    & (PropositionalVariable("chicken") // ~LinearConstraint("chicken_g = 0"))\
    & (PropositionalVariable("chickenBreast") // ~LinearConstraint("chickenBreast_g = 0"))\
    & (PropositionalVariable("chickenThigh") // ~LinearConstraint("chickenThigh_g = 0"))\
    & (PropositionalVariable("eggYolk") // ~LinearConstraint("eggYolk_g = 0"))\
    & (PropositionalVariable("puffPastry") // ~LinearConstraint("puffPastry_g = 0"))\
    & (PropositionalVariable("cream") // ~LinearConstraint("cream_g = 0"))

# dk &= LinearConstraint("eggYolk_u - 17*eggYolk_g = 0")\
#     & LinearConstraint("puffPastry_u - 130*puffPastry_g = 0")\

dk &= FormulaManager.parser("pie -> (puffPastry & eggYolk)")

# Source case
srce_case = LinearConstraint("groundBeef_g = 200.")\
          & LinearConstraint("puffPastry_u = 2")\
          & LinearConstraint("eggYolk_u = 1")\
          & LinearConstraint("beefSteak_g = 0.")\
          & LinearConstraint("chicken_g = 0.")\
          & LinearConstraint("cream_g = 0.")\
          & PropositionalVariable("pie")

# Target problem
tgt_problem = FormulaManager.parser("pie & chicken & (~beef)")

min_dist, tgt_case = adaptator.execute(srce_case, tgt_problem, domainKnowledge={"conversion": ck,
                                                                                "existence": ek,
                                                                                "taxonomy": tax,
                                                                                "miscellanous": MiscellanousDomainKnowledge(dk)},\
                                                               domainKnowledgeInclusion={"existence": False,
                                                                                         "taxonomy": False},
                                                               withMaxDist=True, withTableaux=True)