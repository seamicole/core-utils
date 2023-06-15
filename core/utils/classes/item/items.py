# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ GENERAL IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from __future__ import annotations

from typing import Any, Iterator, TYPE_CHECKING

# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ PROJECT IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

if TYPE_CHECKING:
    from core.utils.classes.collection.collection import Collection
    from core.utils.classes.item.item import Item


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ ITEMS
# └─────────────────────────────────────────────────────────────────────────────────────


class Items:
    """A utility class that represents a collection of Item instances"""

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ CLASS ATTRIBUTES
    # └─────────────────────────────────────────────────────────────────────────────────

    # Declare type of collection
    _collection: Collection

    # Declare type of operations
    _operations: tuple[Any, ...]

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ __INIT__
    # └─────────────────────────────────────────────────────────────────────────────────

    def __init__(self, collection: Collection, operations: tuple[Any, ...] = ()):
        """Init Method"""

        # Set collection
        self._collection = collection

        # Set operations
        self._operations = operations

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ __ITER__
    # └─────────────────────────────────────────────────────────────────────────────────

    def __iter__(self) -> Iterator[Item]:
        """Iter Method"""

        # Yield from collection
        yield from self._collection.collect(items=self)

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ _COPY
    # └─────────────────────────────────────────────────────────────────────────────────

    def _copy(self) -> Items:
        """Returns a copy of the current collection"""

        # Initialize and return a copy of the current collection
        return Items(collection=self._collection, operations=self._operations)

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ HEAD
    # └─────────────────────────────────────────────────────────────────────────────────

    def head(self, n: int = 10) -> Items:
        """Returns the first n items in the collection"""

        # Initialize and return a subset of items
        return self._collection.head(n=n, items=self._copy())

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ SLICE
    # └─────────────────────────────────────────────────────────────────────────────────

    def slice(self, start: int, stop: int) -> Items:
        """Returns a slice of items in the collection"""

        # Initialize and return a subset of items
        return self._collection.slice(start=start, stop=stop, items=self._copy())

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ TAIL
    # └─────────────────────────────────────────────────────────────────────────────────

    def tail(self, n: int = 10) -> Items:
        """Returns the last n items in the collection"""

        # Initialize and return a subset of items
        return self._collection.tail(n=n, items=self._copy())
