# Olaaaf

Olaaaf is a general adaptation prototype based on belief revision whose long-term aim is to cover a broad range of adaptation processes. It is based on a formalism that covers both attribute-value pairs
(often used for representing cases) and taxonomies (often used for representing domain knowledge).

## Table of Contents

- [Migration](#migration)
- [Dependencies](#dependencies)
- [Usage](#usage)
- [Examples](#examples)
- [Video Demonstration](#video-demonstration)
- [Documentation](#documentation)
- [License](#license)

## Migration

As of august 2024, the v2 of Olaaaf came out and with it came some breaking changes. Mainly, the arguments of ``Adaptation.execute()`` changed to offer a more in-depth support for domain knowledges.
Although it is recommended to use the specific domain knowledges classes when applicable, the only step necessary to convert a Olaaaf v1 code to work with Olaaaf v2, is to change the ``dk`` argument in ``Adaptation.execute(psi, mu, dk)`` to a miscellanous domain knowledge like so ``Adaptation.execute(psi, mu, {"miscellanous": MiscellanousDomainKnowledge(dk)})``.

See the document for this method and for the multiple domain knowledges classes for more information on the way they work.

## Dependencies

Please note that each dependency might work with an earlier version.
However, they haven't been tested and aren't officialy supported.

### Necessary dependencies

- Python v3.10.13 or higher.
- [tqdm](https://tqdm.github.io) v4.65.0 or higher.
- [Pyparsing](https://github.com/pyparsing/pyparsing) v3.0.9 or higher.
- [SciPy](https://scipy.org) v1.11.4 or higher.

### Optional dependencies

- [LPSolve](https://lpsolve.sourceforge.net/5.5/) v5.5.2.0 or higher.
  - Since LPSolve isn't officially available for Python 3, [Chandrasekhar Atina's wrapper](https://github.com/chandu-atina/lp_solve_python_3x) is used.
- [matplotlib](https://matplotlib.org) v3.8.0 or higher.

## Usage

To install Olaaaf, first download the latest release [here](https://github.com/OlaaafEngine/Olaaaf/releases/latest) (although a .tar.gz is available if necessary, The .whl file is recommended)

Once downloaded, install the package using pip:

```
pip install ./olaaaf-2.0.1-py3-none-any.whl
```

Once installed, you can import olaaaf from anywhere like a standard Python package

```py
from olaaaf import *
```

For in-depth examples, feel free to look at the [Examples](#examples) and [Video Demonstration](#video-demonstration) sections.

## Examples

As of right now, four examples are availabe for you to go through. Namely:

- [Example 1](examplesICCBR2024/example1.KiwiMilkshake.py) is the adaptation of a banana milkshake recipe to obtain a kiwi milkshake recipe.
- [Example 2](examplesICCBR2024/example2.KiwiMilkshakeNoBanana.py) is the adaptation of a banana milkshake recipe to obtain a kiwi milkshake recipe, with no banana.
- [Example 3](examplesICCBR2024/example3.KiwiMilkshakeSameNumberOfFruitTypes.py) is the adaptation of a banana milkshake recipe to obtain a kiwi milkshake recipe, while conserving the same number of fruit types between the two recipes.
- [Example 4](examplesICCBR2024/example4.CarrotCabbageSalad.py) is the adaptation of a carrot and cabbage salad to remove the vinegar, using an adaptation rule.

## Video demonstration

The execution of Example 3 can be watched in this video:

https://github.com/OlaaafEngine/Olaaaf/assets/164156677/4cc68cda-258f-4fef-bf79-3212cff89632

## Documentation

Olaaaf's documentation is available [here](https://olaaafengine.github.io/Olaaaf/).

## License

Olaaaf is published under the [MIT License](LICENSE).
