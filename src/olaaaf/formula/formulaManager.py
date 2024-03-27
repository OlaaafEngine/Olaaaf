"""
This class allows the user to easily declare a new `olaaaf.formula.formula.Formula` thanks to
`olaaaf.formula.formulaManager.FormulaManager.parser` and store in memory all previously named formulas,
either via their constructor or the function `olaaaf.formula.formulaManager.FormulaManager.declare`.
"""

from __future__ import annotations

from .formula import Formula
from ..constants import Constants

from pyparsing import Literal, Word, srange, infix_notation, OpAssoc, ParseResults, ParserElement

class FormulaManager():
    """
    Class compiling multiple tools used to declare any `olaaaf.formula.formula.Formula` in a more intuitive way.
    """

    #: A way to store all known and named `olaaaf.formula.formula.Formula` so they could be accessed again more easily.
    formulaDict: dict[str, Formula] = dict()

    @staticmethod
    def parser(string: str):
        '''
        Function allowing the user to intuitively parse a `olaaaf.formula.formula.Formula` from a string, using an infixed notation 
        and customizable operators.

        While more intuitive due to the less restrictive scope of usable operators, this method of declaring formulas assume you 
        previously named them, either via the `fmName` attribute in their constructor or thanks to `olaaaf.formula.formulaManager.FormulaManager.declare`.
        The operators could be customized in `olaaaf.constants.Constants` but are by default:\n

        * `&` for the and operator, represented by `olaaaf.formula.naryFormula.andOperator.And`\n
        * `|` for the or operator, represented by `olaaaf.formula.naryFormula.orOperator.Or`\n
        * `~` for the not operator, represented by `olaaaf.formula.unaryFormula.notOperator.Not`\n
        * `->` for the implication operator, represented by `olaaaf.formula.binaryFormula.implicationOperator.Implication`\n
        * `<->` for the equivalence operator, represented by `olaaaf.formula.binaryFormula.equivalenceOperator.Equivalence`\n
        * `<+>` for the xor operator, represented by `olaaaf.formula.binaryFormula.xorOperator.Xor`\n

        Attributes
        ----------
        string: String 
            The String to parse
        '''
        ParserElement.enablePackrat()
        
        formWord = Word(srange("[a-zA-Z_]"), srange("[a-zA-Z0-9_:]"))

        expr = infix_notation(formWord,
                              [(Literal(Constants.AND_PARSER_OPERATOR), 2, OpAssoc.LEFT),
                               (Literal(Constants.OR_PARSER_OPERATOR), 2, OpAssoc.LEFT),
                               (Literal(Constants.NOT_PARSER_OPERATOR), 1, OpAssoc.RIGHT),
                               (Literal(Constants.IMPLICATION_PARSER_OPERATOR), 2, OpAssoc.LEFT),
                               (Literal(Constants.XOR_PARSER_OPERATOR), 2, OpAssoc.LEFT),
                               (Literal(Constants.EQUIVALENCE_PARSER_OPERATOR), 2, OpAssoc.LEFT)],
                              lpar = "(",
                              rpar = ")")

        tokens = expr.parse_string(string)

        #return tokens
        return FormulaManager.__parserEvaluator(tokens)
    
    @staticmethod
    def __parserEvaluator(tokens: ParseResults) -> Formula:
        
        if isinstance(tokens, ParseResults) or isinstance(tokens, list):

            if(len(tokens) == 1):
                return FormulaManager.__parserEvaluator(tokens[0])
            elif(len(tokens) == 2):
                if(tokens[0] == Constants.NOT_PARSER_OPERATOR):
                    from .unaryFormula.notOperator import Not
                    return Not(FormulaManager.__parserEvaluator(tokens[1]))
            elif(len(tokens) % 2 == 1):
                
                formulaType = None

                match tokens[1]:

                    case Constants.AND_PARSER_OPERATOR:
                        from .naryFormula.andOperator import And
                        formulaType = And
                    case Constants.OR_PARSER_OPERATOR:
                        from .naryFormula.orOperator import Or
                        formulaType = Or
                    case Constants.XOR_PARSER_OPERATOR:
                        from .binaryFormula.xorOperator import Xor
                        formulaType = Xor
                    case Constants.IMPLICATION_PARSER_OPERATOR:
                        from .binaryFormula.implicationOperator import Implication
                        formulaType = Implication
                    case Constants.EQUIVALENCE_PARSER_OPERATOR:
                        from .binaryFormula.equivalenceOperator import Equivalence
                        formulaType = Equivalence

                return formulaType(FormulaManager.__parserEvaluator(tokens[0]), FormulaManager.__parserEvaluator(tokens[2:]))

            else:
                raise TypeError("oop")
                
        elif isinstance(tokens, str):

            return FormulaManager.formulaDict[tokens]

    @staticmethod
    def declare(name: str, formula: Formula) -> Formula:
        """
        Function allowing the user to easily declare and name a new `olaaaf.formula.formula.Formula` for it to be stored in
        `olaaaf.formula.formulaManager.FormulaManager.formulaDict`.

        Attributes
        ----------
        name: String 
            The name of the `olaaaf.formula.formula.Formula` to declare.
            If the name is already in use, the old `olaaaf.formula.formula.Formula` will be forgotten and replaced by the newly declared one.\n
            For now, no restriction on the name is given but that should change in the near future.
        
            
        formula: `olaaaf.formula.formula.Formula`
            The `olaaaf.formula.formula.Formula` to declare and name.
        """

        FormulaManager.formulaDict[name] = formula
        return formula