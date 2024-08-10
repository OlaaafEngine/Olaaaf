
from olaaaf import VariableManager, FormulaManager

class Example:

    def run(self, dkInclusion, withTableaux, withMaxDist):
        return self.adaptator.execute(self.srce_case, self.tgt_problem, domainKnowledge=self.dk, domainKnowledgeInclusion=dkInclusion,\
                                        withTableaux=withTableaux, withMaxDist=withMaxDist)

    def __init__(self):
        VariableManager.instance = {}
        FormulaManager.formulaDict = {}