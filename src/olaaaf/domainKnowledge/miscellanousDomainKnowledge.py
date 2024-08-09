"""
Class representing miscellaneous domain knowledges.
"""

from .domainKnowledge import DomainKnowledge

from ..formula import Formula

class MiscellanousDomainKnowledge(DomainKnowledge):
    """
    Class representing miscellaneous domain knowledges, i.e. a plain formula.
    """

    miscDk: Formula

    def __init__(self, miscDk) -> None:
        self.miscDk = miscDk

    def toConstraints(self) -> Formula:
        """
        Converts the domain knowledge object to constraints.
        
        Returns
        -------
        `olaaaf.formula.formula.Formula`
            The formula representing the domain knowledges.
        """
        return self.miscDk

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
        return psi
