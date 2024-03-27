"""
Abstract class, representing a variable.
"""

from __future__ import annotations

# local import of VariableManager

from fractions import Fraction
from abc import ABC, abstractmethod

class Variable(ABC):
    """
    Abstract class, representing a variable. Most of the time, you **shouldn't** use the constructor
    of a `olaaaf.variable.variable.Variable` and should rather look into `olaaaf.variable.variable.Variable.declare`, 
    `olaaaf.variable.variable.Variable.declareBulk` or `olaaaf.variable.variable.Variable.declareAnonymous`.

    Parameters
    ----------
    name : String
        The name of the `olaaaf.variable.variable.Variable`.
    lowerBound, upperBound : `fraction.Fraction`, optional
        Fractions représenting respectively the lower and upper bounds of the variable. If not defined, it is considered as if the variable is unbounded.
    """
    
    #: Name of the variable, by which they are identified.
    name : str = ""

    def __init__(self, name, lowerBound = None, upperBound = None):
        self.name = name
        self.bounds = (lowerBound, upperBound)

    @classmethod
    def declareAnonymous(cls, ending: str = None, lowerBound = None, upperBound = None) -> Variable:
        """
        Class method, allowing the user to declare an anonymous variable meant to be used inside algorithms without risking any
        naming conflit with the standardly defined variables.\n
        Anonymous variables aren't stored in `olaaaf.variable.variableManager.VariableManager.instance` and, as such,
        can't be used in `olaaaf.formula.nullaryFormula.constraint.linearConstraint.LinearConstraint`'s constructor.\n

        Since they can't be used in the usual constructor, one must first declare an empty
        `olaaaf.formula.nullaryFormula.constraint.linearConstraint.LinearConstraint` before adding them manualy.

        To prevent naming conflicts with regular variables, an anonymous variable's name always start with
        it's object's id. The user can also specify an ending to an anonymous variable name.

        Attributes
        ----------
        ending : String
            The string to concatenate at the end of an anonymous variable's name, after its object id.
        lowerBound, upperBound : `fraction.Fraction`, optional
            Fractions représenting respectively the lower and upper bounds of the variable. If not defined, it is considered as if the variable is unbounded.

        Usage exemple
        -------------
        ```py
            lc = LinearConstraint("")

            for i in range(5):
                lc.variables[IntegerVariable.declareAnonymous("anonymous")] = 1

            lc.operator = ConstraintOperator.LEQ
            lc.bound = Fraction("5/2")

            print(lc)
            >>> 1949361817056anonymous + 1949361816720anonymous + 1949372682384anonymous + 1949435231104anonymous + 1949435231200anonymous <= 5/2
        ```
        """

        v = cls("")
        name = str(id(v))
        if ending:
            name += ending
        v.name = name
        v.bounds = (lowerBound, upperBound)
        return v 

    @classmethod
    def declare(cls, name : str, lowerBound = None, upperBound = None) -> Variable:
        """
        Class method used to declare a new variable based on its name.
        A Variable name should respect the following naming conventions:
        - A name is unique and shouldn't be declared multiple times\n
        - Names are case sensitives\n
        - Name must begin with a letter\n
        - It can be followed by alphanumerical character or _\n
        - Name can't contain any of the following symbols: +-*/@:
        - Names shouldn't begin with the prefix `b2i_` or `ak_`

        If this variable already exist under another type, an Exception will be raised.

        Attributes
        ----------
        name : String
            The name of the `olaaaf.variable.variable.Variable` to be declared.
        lowerBound, upperBound : `fraction.Fraction`, optional
            Fractions représenting respectively the lower and upper bounds of the variable. If not defined, it is considered as if the variable is unbounded.

        Returns
        -------
        olaaaf.variable.variable.Variable
            The newly declared `olaaaf.variable.variable.Variable`.
        """

        from .variableManager import VariableManager

        return VariableManager.add(cls(name, lowerBound, upperBound))

    @classmethod
    def declareBulk(cls, *lname: str, lowerBound = None, upperBound = None) -> list[Variable]:
        """
        Class method used to declare multiple new instances of `olaaaf.variable.variable.Variable` at the same time.
        A Variable name should respect the following naming conventions:
        - A name is unique and shouldn't be declared multiple times\n
        - Names are case sensitives\n
        - Name must begin with a letter\n
        - It can be followed by alphanumerical character or _\n
        - Name can't contain any of the following symbols: +-*/@

        If one variable already exist under another type, an Exception will be raised.

        Attributes
        ----------
        lname : list of String
            The names of the `olaaaf.variable.variable.Variable` to be declared.
        lowerBound, upperBound : `fraction.Fraction`, optional
            Fractions représenting respectively the lower and upper bounds of the variables. If not defined, it is considered as if the variable is unbounded.

        Returns
        -------
        list of olaaaf.variable.variable.Variable
            A list containing all the newly declared instances of `olaaaf.variable.variable.Variable`.
        """

        from .variableManager import VariableManager

        vars = []
        for name in lname:
            vars.append(VariableManager.add(cls(name, lowerBound, upperBound)))
        return vars

    def getBounds(self) -> tuple[Fraction, Fraction]:
        """
        Method use to known bounds of the variables

        Returns
        -------
        res: 
            can be None, None if the variable have no limits,
            or Fraction, Fraction.
        """
        return self.bounds
    
    @abstractmethod
    def isInteger(self) -> bool:
        """
        Method used to known if the variable must have intergers values.

        Returns
        -------
        res:
            True if the variable must have integers values
            else False
        """
        pass

    def __str__(self):
        if self.name[0] in "0123456789":
            return self.name[len(str(id(self))):]

        return self.name
    
    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.name == other.name
        return False
    
    def __hash__(self) -> int:
        return self.name.__hash__()