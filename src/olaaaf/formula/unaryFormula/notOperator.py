"""
Class representing the Not operator.
"""

from __future__ import annotations

from .unaryFormula import UnaryFormula
from ...constants import Constants

from fractions import Fraction

# Typing only imports
from .. import Formula
from ..nullaryFormula.constraint.constraint import Constraint
from ...variable.variable import Variable
from ..nullaryFormula.constraint.constraintOperator import ConstraintOperator

class Not(UnaryFormula):
    '''
    Class representing the Not operator.

    Attributes
    ----------
    children: `olaaaf.formula.formula.Formula`
        The child of the current node.
    '''
        
    def toDNF(self) -> Formula:
        '''
        Method returning the current Formula in Disjunctive Normal Form.

        Returns
        -------
        `olaaaf.formula.formula.Formula`
            The current `olaaaf.formula.formula.Formula` in Disjunctive Normal Form.
        '''
        
        return self.children._toDNFNeg()
    
    def _toDNFNeg(self) -> Formula:
        '''
        Protected method used in the algorithm to recursivly determine the
        Disjunctive Normal Form, used when a Negation is in play instead of toDNF().

        Returns
        -------
        `olaaaf.formula.formula.Formula`
            The current `olaaaf.formula.formula.Formula` in Disjunctive Normal Form.
        '''
        
        return self.children.toDNF()
    
    def getAdherence(self, var : Variable = None) -> list[list[Constraint]]:
        '''
        Returns a 2D list containing all the constraints of the adherence of 
        the Formula, in Disjunctive Normal Form.

        Attributes
        ----------
        var : olaaaf.variable.variable.Variable
            variable used in case of inequality.

        Returns
        -------
        list of list of olaaaf.formula.nullaryFormula.constraint.constraint.Constraint
            2D list containing all the constraints of discute vraiment de l'implémentationthe adherence of the Formula,
            in Disjunctive Normal Form.
        '''
        
        return self.children._getAdherenceNeg(var)
    
    def _getAdherenceNeg(self, var : Variable = None)  -> list[list[Constraint]]:
        '''
        Protected method used in the algorithm to recursivly determine the
        constraints of the adherence of the Formula, used when a Negation is in play
        instead of getAdherence().

        Attributes
        ----------
        var : olaaaf.variable.variable.Variable
            variable used in case of inequality.

        Returns
        -------
        list of list of olaaaf.formula.nullaryFormula.constraint.constraint.Constraint
            2D list containing all the constraints of the adherence of the Formula,
            in Disjunctive Normal Form under Negation.
        '''
        
        return self.children.getAdherence(var)
    
    def toLessOrEqConstraint(self):
        '''
        Method used to transform a `olaaaf.formula.formula.Formula` into another one, with only `olaaaf.formula.nullaryFormula.constraint.constraintOperator.ConstraintOperator.LEQ` constraints.

        Returns
        ------
        `olaaaf.formula.formula.Formula`
            A `olaaaf.formula.formula.Formula` with only `olaaaf.formula.nullaryFormula.constraint.constraintOperator.ConstraintOperator.LEQ` constraints.
        '''
        return Not(self.children.toLessOrEqConstraint())
    
    def copyNegLitteral(self, epsilon = Fraction(0)) -> Constraint:
        """
        Method used to transform the strict operators (i.e the negation) in an open one.

        Parameters
        ----------
        epsilon : Fraction, optional
            The approximation for the removed Not. By default, equals \(0\).

        Returns
        -------
        olaaaf.formula.nullaryFormula.constraint.constraint.Constraint
            The transformed `olaaaf.formula.nullaryFormula.constraint.constraint.Constraint`
        """
        
        if not isinstance(self.children, Constraint):
            raise TypeError("This method can only be called on a litteral")
                
        copyNeg = self.children.clone()

        for key in copyNeg.variables:
            copyNeg.variables[key] = -copyNeg.variables[key]
        copyNeg.bound = -(copyNeg.bound + epsilon)
                
        return copyNeg
    
    def toPCMLC(self, varDict) -> Formula:
        '''
        Method used to transform a `olaaaf.formula.formula.Formula` into a new one, in the PCMLC formalism.

        Parameters
        ----------
        varDict : dictionnary
            Dictionnary used to tell which variable should be replaced by which.

        Returns
        -------
        `olaaaf.formula.formula.Formula`
            A `olaaaf.formula.formula.Formula` in the PCMLC formalism.
        '''
        return self.children._toPCMLCNeg(varDict)
    
    def _toPCMLCNeg(self, varDict) -> Formula:
        '''
        Method used to transform a `olaaaf.formula.formula.Formula` into a new one, in the PCMLC formalism.

        Parameters
        ----------
        varDict : dictionnary
            Dictionnary used to tell which variable should be replaced by which.

        Returns
        -------
        `olaaaf.formula.formula.Formula`
            A `olaaaf.formula.formula.Formula` in the PCMLC formalism.
        '''
        return self.children.toPCMLC(varDict)

    def __str__(self):
        return Constants.NOT_STRING_OPERATOR + "(" + str(self.children) + ")"
    
    def toLatex(self):
        r"""
        Method returning a \(\LaTeX\) expression representing the Formula. Operators are customisable in `olaaaf.constants.Constants`.
        
        Returns
        -------
        String
            The \(\LaTeX\) expression representing the Formula.
        """

        return Constants.NOT_LATEX_OPERATOR + "(" + self.children.toLatex + ")"