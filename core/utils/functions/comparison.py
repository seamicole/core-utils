# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ GENERAL IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from typing import Any


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ EVALUATE
# └─────────────────────────────────────────────────────────────────────────────────────


def evaluate(left: Any, right: Any, operator: str) -> bool | None:
    """Returns a boolean comparison of two values based on an operator"""

    # Initialize try-except block
    try:
        # Handle case of equal to
        if operator in ("eq", "equals"):
            return left == right  # type: ignore

        # Otherwise, handle case of less than
        if operator == "lt":
            return left < right  # type: ignore

        # Otherwise handle case of less than or equal to
        elif operator in ("le", "lte"):
            return left <= right  # type: ignore

        # Otherwise handle case of greater than
        elif operator == "gt":
            return left > right  # type: ignore

        # Otherwise handle case of greater than or equal to
        elif operator in ("ge", "gte"):
            return left >= right  # type: ignore

    # Handle TypeError
    except TypeError:
        pass

    # Return None by default
    return None
