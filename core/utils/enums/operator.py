# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ GENERAL IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from enum import Enum


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ OPERATOR
# └─────────────────────────────────────────────────────────────────────────────────────


class Operator(Enum):
    """An enum representing the different operators that can be used in a query"""

    EQUALS = "equals"
    GT = "gt"
    GTE = "gte"
    IEQUALS = "iequals"
    LT = "lt"
    LTE = "lte"
