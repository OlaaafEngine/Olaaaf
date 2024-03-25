from . import PropositionalVariable

from itertools import combinations

class EnumeratedType:

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
        
        #TODO Check if name already declared
        newType = EnumeratedType(name, values)
        __class__.__instances[name] = newType

        return newType
    
    @staticmethod
    def get(name: str):

        # TODO check erreur
        return __class__.__instances[name]

    def __getitem__(self, key: str):

        # TODO check erreur
        return self.values[key]
    
    def generateConstraints(self):

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