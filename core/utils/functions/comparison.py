# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ GENERAL IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from typing import Any

# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ PROJECT IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from core.utils.enums.operator import Operator


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ COMPARE VALUES
# └─────────────────────────────────────────────────────────────────────────────────────


def compare_values(left: Any, right: Any, operator: Operator) -> bool | None:
    """Returns a boolean comparison of two values based on an operator"""

    # Initialize try-except block
    try:
        # Handle case of equal to
        if operator == Operator.EQUALS:
            return left == right  # type: ignore

        # Otherwise, handle case of less than
        if operator == Operator.LT:
            return left < right  # type: ignore

        # Otherwise handle case of less than or equal to
        elif operator == Operator.LTE:
            return left <= right  # type: ignore

        # Otherwise handle case of greater than
        elif operator == Operator.GT:
            return left > right  # type: ignore

        # Otherwise handle case of greater than or equal to
        elif operator == Operator.GTE:
            return left >= right  # type: ignore

    # Handle TypeError
    except TypeError:
        pass

    # Return None by default
    return None
