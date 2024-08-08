from .domainKnowledge import DomainKnowledge

from ..formula import Formula, And, PropositionalVariable, LinearConstraint, Not, ConstraintOperator
from ..variable import Variable

from fractions import Fraction

class ExistenceKnowledge(DomainKnowledge):

    existenceLinks: dict[PropositionalVariable, Variable] = dict()

    def __init__(self, existenceLinks: dict[PropositionalVariable, Variable]) -> None:
        self.existenceLinks = existenceLinks

    def toConstraints(self) -> Formula:

        fmSet = set()

        for k, v in self.existenceLinks.items():
            
            lc = LinearConstraint("")
            lc.variables[v] = Fraction(1)
            lc.operator = ConstraintOperator.LEQ
            lc.bound = Fraction(0)

            fmSet.add(k // ~lc)

        return And(*fmSet)
    
    def inferFrom(self, psi: Formula) -> Formula:
        
        inferedChildren = set()

        inversedEkLinks = {v: k for k, v in self.existenceLinks.items()}

        if isinstance(psi, And):
            
            for c in psi.children:

                if isinstance(c, LinearConstraint) and len(c.variables) == 1 and (c.operator == ConstraintOperator.EQ):
                    try:
                        if c.bound == Fraction(0):
                            inferedChildren.add(~inversedEkLinks[list(c.variables.keys())[0]])
                        else:
                            inferedChildren.add(inversedEkLinks[list(c.variables.keys())[0]])
                    except:
                        pass
                        
                elif isinstance(c, Not) and isinstance(c.children, PropositionalVariable):
                    try:
                        inferedLc = LinearConstraint("")

                        inferedLc.variables[self.existenceLinks[c.children]] = Fraction(1)
                        inferedLc.operator = ConstraintOperator.EQ
                        inferedLc.bound = Fraction(0)

                        inferedChildren.add(inferedLc)
                    except KeyError:
                        pass
                elif isinstance(c, PropositionalVariable):
                    try:
                        inferedLc = LinearConstraint("")
                        
                        inferedLc.variables[self.existenceLinks[c.children]] = Fraction(1)
                        inferedLc.operator = ConstraintOperator.LEQ
                        inferedLc.bound = Fraction(0)

                        inferedChildren.add(~inferedLc)
                    except KeyError:
                        pass

        if len(inferedChildren) != 0:
            return psi & And(*inferedChildren)
        
        return psi