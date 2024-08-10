"""
Class representing a taxonomy.
"""

from __future__ import annotations

from .domainKnowledge import DomainKnowledge
from ..formula import Formula, PropositionalVariable, And, Not, Or

from collections import namedtuple

class Taxonomy(DomainKnowledge):
    """
    Class representing a taxonomy, i.e. knowledges of the form "a is a subtype of b".
    """

    _elements = dict()

    ElementTuple = namedtuple("element", "children parents")

    def __init__(self) -> None:
        self._elements["_TOP"] = self.ElementTuple(children=set(), parents=set())

    def addElement(self, propVar: PropositionalVariable):
        """
        Adds a new element to the taxonomy.

        Parameters
        ----------
        propVar: `olaaaf.formula.formula.PropositionalVariable`
            The new element.
        """

        # TODO error checking and handling

        if isinstance(propVar, PropositionalVariable):
            propVar = propVar.name
        
        self._elements[propVar] = self.ElementTuple(children=set(), parents={"_TOP"})
        self._elements["_TOP"].children.add(propVar)

    def addElements(self, propVars: list[PropositionalVariable]):
        """
        Adds new elements to the taxonomy.

        Parameters
        ----------
        propVars: `list[olaaaf.formula.formula.PropositionalVariable]`
            The new elements.
        """

        for propVar in propVars:
            self.addElement(propVar)

    def addChild(self, src, trgt):
        """
        Adds a new child to a given element.

        Parameters
        ----------
        src: `olaaaf.formula.formula.PropositionalVariable`
            The element to add a child to.
        trgt: `olaaaf.formula.formula.PropositionalVariable`
            The child to add.
        """

        # TODO error checking and handling

        if isinstance(src, PropositionalVariable):
            src = src.name
        if isinstance(trgt, PropositionalVariable):
            trgt = trgt.name

        self._elements[src].children.add(trgt)

        self._elements[trgt].parents.add(src)
        self._elements[trgt].parents.discard("_TOP")
        self._elements["_TOP"].children.discard(trgt)

    def addChildren(self, src, trgts):
        """
        Adds new children to a given element.

        Parameters
        ----------
        src: `olaaaf.formula.formula.PropositionalVariable`
            The element to add children to.
        trgts: `list[olaaaf.formula.formula.PropositionalVariable]`
            The children to add.
        """

        for trgt in trgts:
            self.addChild(src, trgt)

    def addParent(self, src, trgt):
        """
        Adds a new parent to a given element.

        Parameters
        ----------  
        src: `olaaaf.formula.formula.PropositionalVariable`
            The element to add a parent to.
        trgt: `olaaaf.formula.formula.PropositionalVariable`
            The parent to add.
        """
        self.addChild(trgt, src)

    def addParents(self, src, trgts):
        """
        Adds new parents to a given element.

        Parameters
        ----------
        src: `olaaaf.formula.formula.PropositionalVariable`
            The element to add parents to.
        trgts: `list[olaaaf.formula.formula.PropositionalVariable]`
            The parents to add.
        """
        for trgt in trgts:
            self.addParent(src, trgt)

    def removeElement(self, propVar):
        """
        Removes an element from the taxonomy.

        Parameters
        ----------
        propVar: `olaaaf.formula.formula.PropositionalVariable`
            The element to remove.
        """
        # TODO error checking and handling

        if isinstance(propVar, PropositionalVariable):
            propVar = propVar.name

        for child in self._elements[propVar].children:

            self._elements[child].parents.discard(propVar)

            if len(self._elements[child].parents) == 0:
                self._elements[child].parents.add("_TOP")
                self._elements["_TOP"].children.add(child)

        for parent in self._elements[propVar].parents:
            self._elements[parent].children.discard(propVar)

        del self._elements[propVar]

    def removeElements(self, propVars):
        """
        Removes elements from the taxonomy.

        Parameters
        ----------
        propVars: `list[olaaaf.formula.formula.PropositionalVariable]`
            The elements to remove.
        """

        for propVar in propVars:
            self.removeElement(propVar)

    def removeChild(self, src, trgt):
        """
        Removes a child from a given element.

        Parameters
        ----------
        src: `olaaaf.formula.formula.PropositionalVariable`
            The element to remove a child from.
        trgt: `olaaaf.formula.formula.PropositionalVariable`
            The child to remove.
        """

        # TODO error checking and handling

        if isinstance(src, PropositionalVariable):
            src = src.name
        if isinstance(trgt, PropositionalVariable):
            trgt = trgt.name

        self._elements[src].children.discard(trgt)

        self._elements[trgt].parents.discard(src)
        if len(self._elements[trgt].parents) == 0:
            self._elements[trgt].parents.add("_TOP")
            self._elements["_TOP"].children.add(trgt)


    def removeChildren(self, src, trgts):
        """
        Removes children from a given element.

        Parameters
        ----------
        src: `olaaaf.formula.formula.PropositionalVariable`
            The element to remove children from.
        trgts: `list[olaaaf.formula.formula.PropositionalVariable]`
            The children to remove.
        """

        for trgt in trgts:
            self.removeChild(src, trgt)

    def removeParent(self, src, trgt):
        """
        Removes a parent from a given element.

        Parameters
        ----------
        src: `olaaaf.formula.formula.PropositionalVariable`
            The element to remove a parent from.
        trgt: `olaaaf.formula.formula.PropositionalVariable`
            The parent to remove.
        """
        self.removeChild(trgt, src)

    def removeParents(self, src, trgts):
        """
        Removes parents from a given element.

        Parameters
        ----------
        src: `olaaaf.formula.formula.PropositionalVariable`
            The element to remove parents from.
        trgts: `list[olaaaf.formula.formula.PropositionalVariable]`
            The parents to remove.
        """

        for trgt in trgts:  
            self.removeParent(src, trgt)

    def getAncestors(self, src):
        """
        Returns the ancestors of a given element, i.e. the parents of its parents, recursively.

        Parameters
        ----------
        src: `olaaaf.formula.formula.PropositionalVariable`
            The element to get the ancestors of.

        Returns
        -------
        `set[olaaaf.formula.formula.PropositionalVariable]`
            The ancestors of the given element.
        """

        if isinstance(src, PropositionalVariable):
            src = src.name
        
        ancestors = self._elements[src].parents.copy()
        ancestors.discard("_TOP")

        toCheck = ancestors.copy()

        while len(toCheck) != 0:
            
            a = toCheck.pop()
            parents = self._elements[a].parents

            for p in parents:
                if (not p in ancestors):
                    toCheck.add(p)

            ancestors |= parents

        ancestors.discard("_TOP")

        return ancestors

    def getDescendants(self, src):
        """
        Returns the descendants of a given element, i.e. the children of its children, recursively.

        Parameters  
        ----------
        src: `olaaaf.formula.formula.PropositionalVariable`
            The element to get the descendants of.

        Returns
        -------
        `set[olaaaf.formula.formula.PropositionalVariable]`
            The descendants of the given element.
        """

        if isinstance(src, PropositionalVariable):
            src = src.name
        
        descendants = self._elements[src].children.copy()
        toCheck = descendants.copy()

        while len(toCheck) != 0:
            
            a = toCheck.pop()
            children = self._elements[a].children

            for c in children:
                if (not c in descendants):
                    toCheck.add(c)

            descendants |= children

        descendants.discard("_TOP")

        return descendants

    def toConstraints(self) -> Formula:
        """
        Converts the domain knowledge object to constraints.
        
        Returns
        -------
        `olaaaf.formula.formula.Formula`
            The formula representing the domain knowledges.
        """

        fmSet = set()

        realElements = self._elements.copy()
        del realElements["_TOP"]

        for elem in realElements:
            for child in self._elements[elem].children:
                fmSet.add(PropositionalVariable(child) >> PropositionalVariable(elem))
            # if len(self._elements[elem].children) != 0:
            #     fmSet.add(Or(*{PropositionalVariable(child) for child in self._elements[elem].children}) >> PropositionalVariable(elem))

        return And(*fmSet)
    
    def inferFrom(self, psi: Formula) -> Formula:
        """
        Infer new knowledges from a given formula using the domain knowledges.

        Parameters
        ----------
        psi: `olaaaf.formula.formula.Formula`
            The formula to infer from.

        Returns
        -------
        `olaaaf.formula.formula.Formula`
            The inferred formula.
        """

        inferedChildren = set()

        if isinstance(psi, And):
            
            for c in psi.children:

                if isinstance(c, Not) and isinstance(c.children, PropositionalVariable):
                    try:
                        inferedChildren |= {~PropositionalVariable(d) for d in self.getDescendants(c.children)}
                    except KeyError:
                        pass
                elif isinstance(c, PropositionalVariable):
                    try:
                        inferedChildren |= {PropositionalVariable(a) for a in self.getAncestors(c)}
                    except KeyError:
                        pass

        if len(inferedChildren) != 0:
            return psi & And(*inferedChildren)
        
        return psi

    def getElements(self) -> dict:
        return self._elements

    def __getitem__(self, key: str):

        # TODO check erreur
        return (key, self._elements[key])