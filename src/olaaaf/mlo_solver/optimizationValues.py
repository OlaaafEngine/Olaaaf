"""
Enumeration informing of the final state of an optimization task.
"""

from __future__ import annotations

import enum

class OptimizationValues(enum.Enum):
    """
    Enumeration informing of the final state of an optimization task.
    """

    INFEASIBLE = -1 #: If the problem is infeasible.
    OPTIMAL = 0 #: If an optimum was found.
    UNBOUNDED = 1 #: If the optimum is at infinite.