"""
Representation of a PropositionalVariable in CPC.
"""

from __future__ import annotations
from fractions import Fraction

from ....formula.formula import Formula

from . import Constraint, LinearConstraint, ConstraintOperator
from ...formulaManager import FormulaManager
# Typing only imports
from ....variable.variable import Variable


class PropositionalVariable(Constraint):

    def __init__(self, name: str, fmName: str = None):
        self.name = name
       # Declare if name
        if(fmName is not None):
            FormulaManager.declare(fmName, self)
    
    def getVariables(self):
        '''
        Not applicable here
        '''
        raise NotImplementedError("getVariables cannot be use here, the Formula contains a PropositionalVariable")
    
    def getAdherence(self, var : Variable = None):
        '''
        Not applicable here
        '''
        raise NotImplementedError("getAdherence cannot be use here, the Formula contains a PropositionalVariable")

    def _getAdherenceNeg(self, var : Variable = None):
        '''
        Not applicable here
        '''
        raise NotImplementedError("_getAdherenceNeg cannot be use here, the Formula contains a PropositionalVariable")
    
    def __str__(self):

        return self.name
    
    def toLatex(self):

        return self.name
            
    def toLessOrEqConstraint(self):
        '''
        Not applicable here
        '''
        raise NotImplementedError("toLessOrEqConstraint cannot be use here, the Formula contains a PropositionalVariable")
    
    def toPCMLC(self, varDict) -> Formula:
        '''
        Method used to transform a `src.formula.formula.Formula` into a new one, in the PCMLC formalism.

        Returns
        -------
        src.formula.formula.Formula
            A `src.formula.formula.Formula` in the PCMLC formalism.
        '''
        LC = LinearConstraint("")
        LC.variables = {varDict[self]: Fraction(-1)}
        LC.operator = ConstraintOperator.LEQ
        LC.bound = Fraction(-1)
        return LC
    
    def _toPCMLCNeg(self, varDict) -> Formula:
        '''
        Method used to transform a `src.formula.formula.Formula` into a new one, in the PCMLC formalism.

        Returns
        -------
        src.formula.formula.Formula
            A `src.formula.formula.Formula` in the PCMLC formalism.
        '''
        LC = LinearConstraint("")
        LC.variables = {varDict[self]: Fraction(1)}
        LC.operator = ConstraintOperator.LEQ
        LC.bound = Fraction(0)
        return LC
    
    def clone(self) -> PropositionalVariable:
        """
        Method returning a clone of the current Formula.

        Returns
        -------
        src.formula.formula.Formula
            Clone of the current `src.formula.formula.Formula`.
        """
                
        clonedPv = PropositionalVariable("")
        clonedPv.name = self.name.copy()
        return clonedPv
      
    def __eq__(self, o) -> bool: #BRAVO
        if o.__class__ != self.__class__:
            return False
        else:
            return o.name == self.name
        
    def __hash__(self):
        return hash(str(self))
