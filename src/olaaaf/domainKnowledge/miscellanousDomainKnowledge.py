from .domainKnowledge import DomainKnowledge

from ..formula import Formula

class MiscellanousDomainKnowledge(DomainKnowledge):

    miscDk: Formula

    def __init__(self, miscDk) -> None:
        self.miscDk = miscDk

    def toConstraints(self) -> Formula:
        return self.miscDk

    def inferFrom(self, psi: Formula) -> Formula:
        return psi
