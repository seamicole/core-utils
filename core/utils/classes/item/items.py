# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ GENERAL IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from __future__ import annotations

from typing import Any, Iterator, TYPE_CHECKING

# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ PROJECT IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from core.utils.functions.datetime import utc_now

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
        """Returns a count of items in the collection"""

        # Return the number of items in the collection
        return self._collection.count(items=self)

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ FILTER
    # └─────────────────────────────────────────────────────────────────────────────────

    def filter(self, **kwargs: Any) -> Items:
        """Returns a filtered collection of items"""

        # Define operators
        operators = (
            "equals",
            "iequals",
            "lt",
            "lte",
            "gt",
            "gte",
        )

        # Initialize conditions
        conditions = []

        # Iterate over kwargs
        for key, value in kwargs.items():
            # Iterate over operators
            for operator in operators:
                # Get operator suffix
                operator_suffix = "__" + operator

                # Check if key ends with operator suffix
                if key.endswith(operator_suffix):
                    # Remove suffix from key
                    key = key.removesuffix(operator_suffix)

                    # Append condition to conditions and break
                    conditions.append((key, operator, value))
                    break

            # Otherwise set default operator
            else:
                # Append condition to conditions
                conditions.append((key, "equals", value))

        # Initialize and return a filtered collection of items
        return self._collection.filter(tuple(conditions), items=self._copy())

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ FIRST
    # └─────────────────────────────────────────────────────────────────────────────────

    def first(self) -> Item | None:
        """Returns the first item in the collection"""

        # Return the first item in the collection
        return self._collection.first(items=self)

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ HEAD
    # └─────────────────────────────────────────────────────────────────────────────────

    def head(self, n: int = 10) -> Items:
        """Returns the first n items in the collection"""

        # Initialize and return a subset of items
        return self._collection.head(n=n, items=self._copy())

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ KEY
    # └─────────────────────────────────────────────────────────────────────────────────

    def key(self, key: Any) -> Item:
        """Returns an item by key lookup"""

        # Return the item by key lookup
        return self._collection.key(key=key, items=self)

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ LAST
    # └─────────────────────────────────────────────────────────────────────────────────

    def last(self) -> Item | None:
        """Returns the last item in the collection"""

        # Return the last item in the collection
        return self._collection.last(items=self)

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ PUSH
    # └─────────────────────────────────────────────────────────────────────────────────

    def push(self, item: Item) -> None:
        """Pushes an item to the collection"""

        # Push item to collection
        self._collection.push(item=item)

        # Update pushed at timestamp
        item._imeta.pushed_at = utc_now()

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
