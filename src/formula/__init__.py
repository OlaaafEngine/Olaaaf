"""
Representation of logical formulas and multiple tools to use them, abstracted depending on the operator's formula.\n

## Declaration of a new `src.formula.formula.Formula`

To declare a new `src.formula.formula.Formula`, you have multiple options:\n

* Use the usual class constructors. Depending on the operator's arity, the arguments that are expected might change
(namely, those represents the arguments of the operators and, as such, a different number of them could be expected).
Please note that they have an optional argument `name` that we'll talk about in the point after next.\n

* Use Python's built-in (but restrictive) operators between two existing formulas, namely:\n

    * `&` for the and operator, represented by `src.formula.naryFormula.andOperator.And`\n
    * `|` for the or operator, represented by `src.formula.naryFormula.orOperator.Or`\n
    * `~` for the not operator, represented by `src.formula.unaryFormula.notOperator.Not`\n
    * `>>` for the implication operator, represented by `src.formula.binaryFormula.implicationOperator.Implication`\n
    * `//` for the equivalence operator, represented by `src.formula.binaryFormula.equivalenceOperator.Equivalence`\n
    * `!=` for the xor operator, represented by `src.formula.binaryFormula.xorOperator.Xor`\n

* Use `src.formula.formulaManager.FormulaManager.parser` to declare a formula using a parser with customizable operators.
While more intuitive due to the less restrictive scope of usable operators, this method of declaring formulas assume you 
previously named them, either via the `name` attribute in their constructor or thanks to `src.formula.formulaManager.FormulaManager.declare`.
The operators could be customized in `src.constants.Constants` but are by default:

    * `&` for the and operator, represented by `src.formula.naryFormula.andOperator.And`\n
    * `|` for the or operator, represented by `src.formula.naryFormula.orOperator.Or`\n
    * `~` for the not operator, represented by `src.formula.unaryFormula.notOperator.Not`\n
    * `->` for the implication operator, represented by `src.formula.binaryFormula.implicationOperator.Implication`\n
    * `<->` for the equivalence operator, represented by `src.formula.binaryFormula.equivalenceOperator.Equivalence`\n
    * `<+>` for the xor operator, represented by `src.formula.binaryFormula.xorOperator.Xor`\n

### Exemple of declaration

```py
IntegerVariable.declare("x")

a = Not(LinearConstraint("x <= 7/9"))
b = LinearConstraint("2.4*x >= 4")

And(formulaName = "phi", a, b)
Implication(formulaName = "psi", ~(a | b), ~b)
```

"""

from .formula import Formula
from .formulaManager import FormulaManager

try:
    from .formulaDisplay import FormulaDisplay
except ModuleNotFoundError:

    from ..constants import Constants

    if Constants.DISPLAY_DEPENDENCIES_WARNING:
        print("Missing MatPlotLib, Scipy or Numpy dependency: FormulaDisplay cannot be used without it. If you wish to disable these warnings, set the DISPLAY_DEPENDENCIES_WARNING constant to False.")

from .nullaryFormula import *
from .unaryFormula import *
from .binaryFormula import *
from .naryFormula import *
