from abc import ABC, abstractmethod

from ..formula import Formula

class DomainKnowledge(ABC):

    @abstractmethod
    def toConstraints(self) -> Formula:
        pass

    @abstractmethod
    def inferFrom(self, psi: Formula) -> Formula:
        pass