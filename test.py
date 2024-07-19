from src.olaaaf.taxonomy import Taxonomy
from src.olaaaf.formula import PropositionalVariable

tax = Taxonomy()

tax.addElement(PropositionalVariable("a"))
tax.addElement(PropositionalVariable("b"))
tax.addElement(PropositionalVariable("c"))
tax.addElement(PropositionalVariable("d"))
tax.addElement(PropositionalVariable("e"))

tax.addChild(src="a", trgt="b")
tax.addChild(src="b", trgt="c")
tax.addChild(src="d", trgt="e")

for elem in tax.getElements():
    print(tax[elem])

print("-------------")

tax.removeElement("b")

for elem in tax.getElements():
    print(tax[elem])