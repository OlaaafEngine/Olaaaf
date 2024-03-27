"""
Class storing all global variables, allowing the user to easily customise the program to their liking.
"""

class Constants():
    

    ONLY_ONE_SOLUTION = True
    """
    If set to `True`, the revision algorithm will by default only return one point that satisfies \(\psi \circ \mu\).
    If not, it will return all solutions.
    By default, this constant is set to `True`.

    Note that this only change the default value of the `onlyOneSolution` parameter of `olaaaf.revision.Revision`, it could still be changed
    on a case-by-case basis for every new instance of this class.
    """

    SET_VERBOSE = True #: Select the default value for the verbose display of the algorithm.
    DISPLAY_DEPENDENCIES_WARNING = True #: Choose to display dependencies warning for optional packages.

    # ---------------------------------------------------
    # Operator used in `olaaaf.formula.formulaManager.FormulaManager.parser`.

    AND_PARSER_OPERATOR = "&" #: Value for the operator used in `olaaaf.formula.formulaManager.FormulaManager.parser` for the `olaaaf.formula.naryFormula.andOperator.And` operator, defaulted as `&`.
    OR_PARSER_OPERATOR = "|" #: Value for the operator used in `olaaaf.formula.formulaManager.FormulaManager.parser` for the `olaaaf.formula.naryFormula.orOperator.Or` operator, defaulted as `|`.
    NOT_PARSER_OPERATOR = "~" #: Value for the operator used in `olaaaf.formula.formulaManager.FormulaManager.parser` for the `olaaaf.formula.unaryFormula.notOperator.Not` operator, defaulted as `~`.
    XOR_PARSER_OPERATOR = "<+>" #: Value for the operator used in `olaaaf.formula.formulaManager.FormulaManager.parser` for the `olaaaf.formula.binaryFormula.xorOperator.Xor` operator, defaulted as `<+>`.
    IMPLICATION_PARSER_OPERATOR = "->" #: Value for the operator used in `olaaaf.formula.formulaManager.FormulaManager.parser` for the `olaaaf.formula.binaryFormula.implicationOperator.Implication` operator, defaulted as `->`.
    EQUIVALENCE_PARSER_OPERATOR = "<->" #: Value for the operator used in `olaaaf.formula.formulaManager.FormulaManager.parser` for the `olaaaf.formula.binaryFormula.equivalenceOperator.Equivalence` operator, defaulted as `<->`.

    # ---------------------------------------------------
    # Display-only constants

    LINEAR_CONSTRAINT_STRING_DISPLAY_MULT = True
    """
    If set to `True`, the string display of a `olaaaf.formula.nullaryFormula.constraint.linearConstraint.LinearConstraint` will put
    multiplicaiton signs between each variable and their coefficient.
    By default, this constant is set to `True`.\n
    """

    AND_STRING_OPERATOR = "&" #: Value for the operator used in `olaaaf.formula.formula.Formula`'s string display for the `olaaaf.formula.naryFormula.andOperator.And` operator, defaulted as `&`.
    OR_STRING_OPERATOR = "|" #: Value for the operator used in `olaaaf.formula.formula.Formula`'s string display for the `olaaaf.formula.naryFormula.orOperator.Or` operator, defaulted as `|`.
    NOT_STRING_OPERATOR = "~" #: Value for the operator used in `olaaaf.formula.formula.Formula`'s string display for the `olaaaf.formula.unaryFormula.notOperator.Not` operator, defaulted as `~`.
    XOR_STRING_OPERATOR = "XOR" #: Value for the operator used in `olaaaf.formula.formula.Formula`'s string display for the `olaaaf.formula.binaryFormula.xorOperator.Xor` operator, defaulted as `XOR`.
    IMPLICATION_STRING_OPERATOR = "->" #: Value for the operator used in `olaaaf.formula.formula.Formula`'s string display for the `olaaaf.formula.binaryFormula.implicationOperator.Implication` operator, defaulted as `->`.
    EQUIVALENCE_STRING_OPERATOR = "<->" #: Value for the operator used in `olaaaf.formula.formula.Formula`'s string display for the `olaaaf.formula.binaryFormula.equivalenceOperator.Equivalence` operator, defaulted as `<->`.
    TOP_STRING_OPERATOR = "TOP" #: Value for the operator used in `olaaaf.formula.formula.Formula`'s string display for the `olaaaf.formula.nullaryFormula.top.Top` operator, defaulted as `TOP`.
    BOTTOM_STRING_OPERATOR = "BOT" #: Value for the operator used in `olaaaf.formula.formula.Formula`'s string display for the `olaaaf.formula.nullaryFormula.bottom.Bottom` operator, defaulted as `BOT`.

    AND_LATEX_OPERATOR = "\\land" #: Value for the operator used in ``olaaaf.formula.formula.Formula`.toLatex` for the `olaaaf.formula.naryFormula.andOperator.And` operator, defaulted as `\land`.
    OR_LATEX_OPERATOR = "\\lor" #: Value for the operator used in ``olaaaf.formula.formula.Formula`.toLatex` for the `olaaaf.formula.naryFormula.orOperator.Or` operator, defaulted as `\lor`.
    NOT_LATEX_OPERATOR = "\\lnot" #: Value for the operator used in ``olaaaf.formula.formula.Formula`.toLatex` for the `olaaaf.formula.unaryFormula.notOperator.Not` operator, defaulted as `\lnot`.
    XOR_LATEX_OPERATOR = "\\oplus" #: Value for the operator used in ``olaaaf.formula.formula.Formula`.toLatex` for the `olaaaf.formula.binaryFormula.xorOperator.Xor` operator, defaulted as `\oplus`.
    IMPLICATION_LATEX_OPERATOR = "\\rightarrow" #: Value for the operator used in ``olaaaf.formula.formula.Formula`.toLatex` for the `olaaaf.formula.binaryFormula.implicationOperator.Implication` operator, defaulted as `\rightarrow`.
    EQUIVALENCE_LATEX_OPERATOR = "\\leftrightarrow" #: Value for the operator used in ``olaaaf.formula.formula.Formula`.toLatex` for the `olaaaf.formula.binaryFormula.equivalenceOperator.Equivalence` operator, defaulted as `\leftrightarrow`.
    TOP_LATEX_OPERATOR = "\\top" #: Value for the operator used in ``olaaaf.formula.formula.Formula`.toLatex` for the `olaaaf.formula.nullaryFormula.top.Top` operator, defaulted as `\top`.
    BOTTOM_LATEX_OPERATOR = "\\bot" #: Value for the operator used in ``olaaaf.formula.formula.Formula`.toLatex` for the `olaaaf.formula.nullaryFormula.bottom.Bottom` operator, defaulted as `\bot`.
    EQ_LATEX_OPERATOR = "=" #: Value for the operator used in ``olaaaf.formula.formula.Formula`.toLatex` for the `olaaaf.formula.nullaryFormula.constraint.constraintOperator.ConstraintOperator.EQ` operator, defaulted as `=`.
    LEQ_LATEX_OPERATOR = "\\leqslant" #: Value for the operator used in ``olaaaf.formula.formula.Formula`.toLatex` for the `olaaaf.formula.nullaryFormula.constraint.constraintOperator.ConstraintOperator.LEQ` operator, defaulted as `\leqslant`.
    GEQ_LATEX_OPERATOR = "\\geqslant" #: Value for the operator used in ``olaaaf.formula.formula.Formula`.toLatex` for the `olaaaf.formula.nullaryFormula.constraint.constraintOperator.ConstraintOperator.GEQ` operator, defaulted as `\geqslant`.