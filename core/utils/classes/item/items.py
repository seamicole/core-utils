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

    # ┌────────────────────────────────────────────────────────────────────────────────
    # │ __ITER__
    # └─────────────────────────────────────────────────────────────────────────────────

    def __iter__(self) -> Iterator[Item]:
        """Iter Method"""

        # Yield from collection
        yield from self._collection.collect(items=self)

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ __REPR__
    # └─────────────────────────────────────────────────────────────────────────────────

    def __repr__(self) -> str:
        """Representation Method"""

        # Initialize representation to class name
        representation = self.__class__.__name__

        # Get item count
        count = self.count()

        # Add count to representation
        representation += f": {count}"

        # Define n
        n = 20

        # Get head
        head = self.head(n=n)

        # Get items
        items = [item.__repr__() for item in head]

        # Check if there are more than n items total
        if count > n:
            # Add truncation message to items list
            items.append("...(remaining items truncated)... ")

        # Add items to representation
        representation = f"{representation} {'[' + ', '.join(items) + ']'}"

        # Add angle brackets to the representation
        representation = f"<{representation}>"

        # Return representation
        return representation

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ _COPY
    # └─────────────────────────────────────────────────────────────────────────────────

    def _copy(self) -> Items:
        """Returns a copy of the current collection"""

        # Initialize and return a copy of the current collection
        return Items(collection=self._collection, operations=self._operations)

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ COUNT
    # └─────────────────────────────────────────────────────────────────────────────────

    def count(self) -> int:
        """Returns the number of items in the collection"""

        # Return the number of items in the collection
        return self._collection.count(items=self)

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ HEAD
    # └─────────────────────────────────────────────────────────────────────────────────

    def head(self, n: int = 10) -> Items:
        """Returns the first n items in the collection"""

        # Initialize and return a subset of items
        return self._collection.head(n=n, items=self._copy())

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ PUSH
    # └─────────────────────────────────────────────────────────────────────────────────

    def push(self, item: Item) -> None:
        """Pushes an item to the collection"""

        # Push item to collection
        self._collection.push(item=item)

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
