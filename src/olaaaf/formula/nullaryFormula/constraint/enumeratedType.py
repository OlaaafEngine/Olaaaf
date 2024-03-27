"""
Representation of an enumerated Type.
"""

from . import PropositionalVariable

from itertools import combinations

class EnumeratedType:
    """
    Representation of a PropositionalVariable in CPC.

    Parameters
    ----------
    name : str
        The name of the enumerated type, either to get (if `values` is `None`) or to create.
    values : list[str], optional
        List of the names of the values the enumerated type can have.
    """

    name: str
    values: dict[str, PropositionalVariable]

    __instances = {}

    def __init__(self, name: str, values: list[str] = None):
        
        if values is None:
            self.name = name
            et = self.get(name)
            self.values = et.values
        elif len(values) >= 3:
            self.values = {val:PropositionalVariable("e2b_" + name + ":" + val) for val in values}
            self.name = name
        else:
            raise(AttributeError("values array should contain at least three elements"))


    @staticmethod
    def declare(name: str, values: list[str]):
        """
        Function to declare a new `EnumeratedType`, accessible either via the constructor or the `get()` function.

        Parameters
        ----------
        name : str
            The name of the enumerated type to declare.
        values : list[str]
            List of the names of the values the enumerated type can have.

        Returns
        -------
        `EnumeratedType`
            The newly declared enumerated type.

        """
        
        #TODO Check if name already declared
        newType = EnumeratedType(name, values)
        __class__.__instances[name] = newType

        return newType
    
    @staticmethod
    def get(name: str):
        """
        Function to get a previously declared `EnumeratedType`.

        Parameters
        ----------
        name : str
            The name of the enumerated type to get.

        Returns
        -------
        `EnumeratedType`
            The enumerated type to get.
        """

        # TODO check erreur
        return __class__.__instances[name]

    def __getitem__(self, key: str):

        # TODO check erreur
        return self.values[key]
    
    def generateConstraints(self):
        """
        Method to generate the necessary constraints to translate an enumerated type into multiple propositional constraints.

        Returns
        -------
        `olaaaf.formula.formula.Formula`
            The necessary constraints.
        """

        from ...naryFormula import And, Or

        propSet = self.values.values()
        
        constraints = Or(*propSet)

        for propTuple in combinations(propSet, len(propSet)-1):
            constraints &= ~And(*propTuple)

        return constraints
    
    def __eq__(self, o) -> bool:
        if o.__class__ != self.__class__:
            return False
        else:
            return (o.name == self.name)
        
    def __hash__(self):
        return hash(str(self))