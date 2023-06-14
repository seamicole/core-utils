# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ GENERAL IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from abc import ABC, abstractmethod
from typing import Any, Generator, TYPE_CHECKING

# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ PROJECT IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from core.utils.classes.item.items import Items

if TYPE_CHECKING:
    from core.utils.classes.item.item import Item


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
    # │ APPLY
    # └─────────────────────────────────────────────────────────────────────────────────

    def apply(self, items: Items | None, *operations: Any) -> Items:
        """Applies a series of operations to a collection of items"""

        # Initialize items
        items = items if items is not None else self.all()

        # Append head operation to operations
        items._operations += operations

        # Return items
        return items

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ COLLECT
    # └─────────────────────────────────────────────────────────────────────────────────

    @abstractmethod
    def collect(self, items: Items | None = None) -> Generator[Item, None, None]:
        """Yields items in the collection"""

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
