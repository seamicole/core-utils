# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ GENERAL IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from abc import ABC, abstractmethod

# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ PROJECT IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from core.utils.classes.items import Items


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ COLLECTION
# └─────────────────────────────────────────────────────────────────────────────────────


class Collection(ABC):
    """An abstract class that represents a collection of items"""

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ ALL
    # └─────────────────────────────────────────────────────────────────────────────────

    def all(self) -> Items:
        """Returns all items in the collection"""

        # Return all items
        return Items(collection=self)

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ HEAD
    # └─────────────────────────────────────────────────────────────────────────────────

    @abstractmethod
    def head(self, n: int, items: Items | None = None) -> Items:
        """Returns the first n items in the collection"""

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ SLICE
    # └─────────────────────────────────────────────────────────────────────────────────

    @abstractmethod
    def slice(self, start: int, stop: int, items: Items | None = None) -> Items:
        """Returns a slice of items in the collection"""

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ TAIL
    # └─────────────────────────────────────────────────────────────────────────────────

    @abstractmethod
    def tail(self, n: int, items: Items | None = None) -> Items:
        """Returns the last n items in the collection"""