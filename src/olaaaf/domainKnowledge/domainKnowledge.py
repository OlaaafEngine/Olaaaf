"""
Abstract class, representing a domain knowledge.
"""

from abc import ABC, abstractmethod

from ..formula import Formula

class DomainKnowledge(ABC):
    """
    Abstract class, representing a domain knowledge.
    """
    
    @abstractmethod
    def toConstraints(self) -> Formula:
        """
        Converts the domain knowledge object to constraints.
        
        Returns
        -------
        `olaaaf.formula.formula.Formula`
            The formula representing the domain knowledges.
        """
        pass

    @abstractmethod
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
        pass