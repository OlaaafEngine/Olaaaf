"""
Abstract Formula class, representing a Formula in PCMLC as a syntax tree.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

# Typing only imports
from ..variable.variable import Variable
# import constraint

class Formula(ABC):
    '''
    Abstract Formula class, representing a Formula in PCMLC as a syntax tree.

    Attributes
    ----------
    children: 
        The children of the current node.
        Typing depends of the formula's arity.
    '''
    
    children = None
    
    @abstractmethod
    def getVariables(self) -> set[Variable]:
        '''
        Method recurcively returning a set containing all the variables used in
        the Formula.

        Returns
        -------
        set of olaaaf.variable.variable.Variable
            All the variables used in the `olaaaf.formula.formula.Formula`.
        '''
        pass
    
    @abstractmethod
    def toDNF(self) -> Formula:
        '''
        Method returning the current Formula in Disjunctive Normal Form.

        Returns
        -------
        `olaaaf.formula.formula.Formula`
            The current `olaaaf.formula.formula.Formula` in Disjunctive Normal Form.
        '''
        pass
    
    @abstractmethod
    def _toDNFNeg(self) -> Formula:
        '''
        Protected method used in the algorithm to recursivly determine the
        Disjunctive Normal Form, used when a Negation is in play instead of toDNF().

        Returns
        -------
        `olaaaf.formula.formula.Formula`
            The current Formula in Disjunctive Normal Form under Negation.
        '''
        pass

    @abstractmethod
    def getAdherence(self, var : Variable = None) -> list[list[Formula]]:
        '''
        Returns a 2D list containing all the constraints of the adherence of 
        the Formula, in Disjunctive Normal Form.

        Attributes
        ----------
        var : olaaaf.variable.variable.Variable
            variable used in case of inequality

        Returns
        -------
        list of list of olaaaf.formula.nullaryFormula.constraint.constraint.Constraint
            2D list containing all the constraints of discute vraiment de l'implémentationthe adherence of the Formula,
            in Disjunctive Normal Form.
        '''
        pass

    @abstractmethod
    def _getAdherenceNeg(self, var : Variable = None)  -> list[list[Formula]]:
        '''
        Protected method used in the algorithm to recursivly determine the
        constraints of the adherence of the Formula, used when a Negation is in play
        instead of getAdherence().

        Attributes
        ----------
        var : olaaaf.variable.variable.Variable
            `olaaaf.variable.variable.Variable` used in case of inequality

        Returns
        -------
        list of list of olaaaf.formula.nullaryFormula.constraint.constraint.Constraint
            2D list containing all the constraints of the adherence of the Formula,
            in Disjunctive Normal Form under Negation.
        '''
        pass
    
    @abstractmethod
    def toLessOrEqConstraint(self) -> Formula:
        '''
        Method used to transform a `olaaaf.formula.formula.Formula` into another one, with only `olaaaf.formula.nullaryFormula.constraint.constraintOperator.ConstraintOperator.LEQ` constraints.

        Returns
        ------
        `olaaaf.formula.formula.Formula`
            A `olaaaf.formula.formula.Formula` with only `olaaaf.formula.nullaryFormula.constraint.constraintOperator.ConstraintOperator.LEQ` constraints.
        '''
        pass

    @abstractmethod
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
        pass

    @abstractmethod
    def _toPCMLCNeg(self, varDict) -> Formula:
        pass

    def toDNFWithTableaux(self) -> Formula:
        '''
        Method returning the current Formula in Disjunctive Normal Form, using analytic tableaux to prune
        a part of the unsatisfiable branches, or `None` if the whole `olaaaf.formula.formula.Formula` is unsatisfiable.

        Returns
        -------
        `olaaaf.formula.formula.Formula`
            The current `olaaaf.formula.formula.Formula` in Disjunctive Normal Form, with pruned branches,
            or `None` if the whole `olaaaf.formula.formula.Formula` is unsatisfiable.
        '''

        from .naryFormula import Or, And

        orList = list()

        branchesList = self._getBranches()

        # Eveything is unsatisfiable
        if not branchesList:
            return None

        for branch in branchesList:
            
            andList = list()

            for atom, isNotNeg in branch.items():
                if isNotNeg:
                    andList.append(atom)
                else:
                    andList.append(~atom)

            orList.append(And(*andList))

        return(Or(*orList))

    @abstractmethod
    def _getBranches(self):
        '''
        Method used to get the branches of the analytic tableau representing the `olaaaf.formula.formula.Formula`,
        automatically removing any closed one once it's caught. 

        Returns
        ------
        `list[dict[Constraint, bool]]`
            A list of all branches, represented by a dictionnary matching every atom
            `olaaaf.formula.nullaryFormula.constraint.constraint.Constraint` to a `bool` representing if it has a negation (`False`)
            or not (`True`).
            If all branches are closed, return `None`.
        '''

        pass

    @abstractmethod 
    def _getBranchesNeg(self):
        '''
        Method used to get the branches of the analytic tableau representing the `olaaaf.formula.formula.Formula`,
        automatically removing any closed one once it's caught. 
        Used when a Negation is in play instead of `_getBranches()`.

        Returns
        ------
        `list[dict[Constraint, bool]]`
            A list of all branches, represented by a dictionnary matching every atom
            `olaaaf.formula.nullaryFormula.constraint.constraint.Constraint` to a `bool` representing if it has a negation (`False`)
            or not (`True`).
            If all branches are closed, return `None`.
        '''

        pass
    
    def clone(self) -> Formula:
        """
        Method returning a clone of the current Formula.

        Returns
        -------
        `olaaaf.formula.formula.Formula`
            Clone of the current `olaaaf.formula.formula.Formula`.
        """

        clone = self.__class__(self.children)
        return clone
    
    def __eq__(self, o) -> bool:
    
        if o.__class__ != self.__class__:
            return False
        else:
            return self.children == o.children
        
    def __hash__(self):
        return hash(frozenset(self.children))
    
    @abstractmethod
    def __str__(self):
        pass

    @abstractmethod
    def toLatex(self) -> str:
        r"""
        Method returning a \(\LaTeX\) expression representing the Formula. Operators are customisable in `olaaaf.constants.Constants`.
        
        Returns
        -------
        String
            The \(\LaTeX\) expression representing the Formula.
        """

        pass
    
    def __or__(self, a):
        from .naryFormula.orOperator import Or
        return Or(self, a)    
    
    def __and__(self, a):
        from .naryFormula.andOperator import And
        return And(self, a)
    
    def __invert__(self):
        from .unaryFormula.notOperator import Not
        return Not(self)

    def __floordiv__(self, a):
        from .binaryFormula.equivalenceOperator import Equivalence
        return Equivalence(self, a)
    
    def __ne__(self, a):
        from .binaryFormula.xorOperator import Xor
        return Xor(self, a)
    
    def __rshift__(self, a):
        from .binaryFormula.implicationOperator import Implication
        return Implication(self, a)