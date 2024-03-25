"""
This module is an implementation of a logical belief revision operator, built with scalability in mind.
By design choice, each class is split into its own file, i.e. it's own sub-module, and overall mimick Java's conventions.

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