"""
Olaaaf is a general adaptation prototype based on belief revision whose long-term aim is to cover a broad range of adaptation processes.
It is based on a formalism that covers both attribute-value pairs (often used for representing cases) and taxonomies (often used for representing domain knowledge).

"""

from .distance import *
from .formula import *
from .mlo_solver import *
from .projector import *
from .simplificator import *
from .variable import *

from .constants import *
from .formulaInterpreter import *
from .revision import *
from .adaptation import *
from .taxonomy import *