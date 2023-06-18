# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ GENERAL IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from __future__ import annotations

from collections import deque
from copy import deepcopy
from typing import Any, Generator, TYPE_CHECKING

# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ PROJECT IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from core.utils.classes.collection.collection import Collection
from core.utils.exceptions import DuplicateKeyError

if TYPE_CHECKING:
    from core.utils.classes.item.item import Item
    from core.utils.classes.item.items import Items


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ DICT COLLECTION
# └─────────────────────────────────────────────────────────────────────────────────────


class DictCollection(Collection):
    """A utility class that represents a dictionary collection of items"""

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ INSTANCE ATTRIBUTES
    # └─────────────────────────────────────────────────────────────────────────────────

    # Initialize item ID
    _item_id: int

    # Declare type of items by ID
    _items_by_id: dict[int, Item]

    # Declare type of item IDs by key
    _item_ids_by_key: dict[Any, int]

    # Declare type of keys by item ID
    _keys_by_item_id: dict[int, list[Any]]

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ __INIT__
    # └─────────────────────────────────────────────────────────────────────────────────

    def __init__(self) -> None:
        """Init Method"""

        # Initialize item ID
        self._item_id = 0

        # Initialize items by ID
        self._items_by_id = {}

        # Initialize item IDs by key
        self._item_ids_by_key = {}

        # Initialize keys by item ID
        self._keys_by_item_id = {}

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ COLLECT
    # └─────────────────────────────────────────────────────────────────────────────────

    def collect(self, items: Items | None = None) -> Generator[Item, None, None]:
        """Yields items in the collection"""

        # Get operations
        operations = self.apply(items)._operations

        # Initialize collected items
        collected = iter(self._items_by_id.values())

        # Iterate over operations
        for operation in operations:
            # Check if callable
            if callable(operation):
                # Apply operation to collected
                collected = operation(collected)

        # Iterate over collected items
        for item in collected:
            # Deepcopy and yield item
            yield deepcopy(item)

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ COUNT
    # └─────────────────────────────────────────────────────────────────────────────────

    def count(self, items: Items | None = None) -> int:
        """Counts the number of items in the collection"""

        # Initialize items
        items = self.apply(items)

        # Return the number of items in the collection
        return sum(1 for _ in items)

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ FIRST
    # └─────────────────────────────────────────────────────────────────────────────────

    def first(self, items: Items | None = None) -> Item | None:
        """Returns the first item in the collection"""

        # Initialize items
        items = self.apply(items)

        # Return the first item in the collection
        return next(iter(items), None)

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ HEAD
    # └─────────────────────────────────────────────────────────────────────────────────

    def head(self, n: int, items: Items | None = None) -> Items:
        """Returns the first n items in the collection"""

        def operation(
            items: Generator[Item, None, None]
        ) -> Generator[Item, None, None]:
            """Yields the first n items in the collection"""

            # Iterate over items
            for i, item in enumerate(items):
                # Check if i is greater than or equal to n
                if i >= n:
                    # Break
                    break
                # Yield item
                yield item

        # Apply head operation to items
        return self.apply(items, lambda x: operation(x))

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ ISSUE ITEM ID
    # └─────────────────────────────────────────────────────────────────────────────────

    def issue_item_id(self) -> int:
        """Issues a new item ID"""

        # Increment item ID
        self._item_id += 1

        # Return item ID
        return self._item_id

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ LAST
    # └─────────────────────────────────────────────────────────────────────────────────

    def last(self, items: Items | None = None) -> Item | None:
        """Returns the last item in the collection"""

        # Initialize items
        items = self.apply(items)

        # Initialize window
        window = deque(items, maxlen=1)

        # Return the last item in the collection
        return window.pop() if window else None

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ PUSH
    # └─────────────────────────────────────────────────────────────────────────────────

    def push(self, item: Item) -> None:
        """Pushes an item to the collection"""

        # Get item ID
        item_id = (
            int(item._imeta.item_id)
            if item._imeta.item_id is not None
            else self.issue_item_id()
        )

        # Get keys by item ID
        keys_by_item_id = self._keys_by_item_id

        # Get item IDs by key
        item_ids_by_key = self._item_ids_by_key

        # Iterate over values
        for value in keys_by_item_id.pop(item_id, []):
            # Remove item ID from item IDs by key
            del item_ids_by_key[value]

        # Initialize values
        values = []

        # Iterate over keys
        for key in item._cmeta.KEYS:
            # Get value
            value = (
                tuple([getattr(item, k, None) for k in key])
                if isinstance(key, tuple)
                else getattr(item, key, None)
            )

            # Check if value in item IDs by key
            if value in item_ids_by_key:
                # Raise a duplicate key error
                raise DuplicateKeyError(
                    f"An item with the key '{value}' already exists."
                )

            # Append value to values
            values.append(value)

        # Iterate over values
        for value in values:
            # Add item ID to item IDs by key
            item_ids_by_key[value] = item_id

            # Add value to keys by item ID
            keys_by_item_id.setdefault(item_id, []).append(value)

        # Update item ID
        item._imeta.item_id = str(item_id)

        # Deepcopy and add item to items by ID
        self._items_by_id[item_id] = deepcopy(item)

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ SLICE
    # └─────────────────────────────────────────────────────────────────────────────────

    def slice(self, start: int, stop: int, items: Items | None = None) -> Items:
        """Returns a slice of items in the collection"""

        def operation(
            items: Generator[Item, None, None]
        ) -> Generator[Item, None, None]:
            """Yields a slice of items in the collection"""

            # Check if either start or stop is less than 0
            if start < 0 or stop < 0:
                # Convert items to list and yield slice
                yield from list(items)[start:stop]

            # Iterate over items
            for i, item in enumerate(items):
                # Check if i is greater than or equal to stop
                if i >= stop:
                    # Break
                    break

                # Check if i is greater than or equal to start
                if i >= start:
                    # Yield item
                    yield item

        # Apply slice operation to items
        return self.apply(items, lambda x: operation(x))

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ TAIL
    # └─────────────────────────────────────────────────────────────────────────────────

    def tail(self, n: int, items: Items | None = None) -> Items:
        """Returns the last n items in the collection"""

        def operation(
            items: Generator[Item, None, None]
        ) -> Generator[Item, None, None]:
            """Yields the last n items in the collection"""

            # Initialize window
            window: deque[Item] = deque(maxlen=n)

            # Iterate over items
            for item in items:
                # Append item to window
                window.append(item)

            # Iterate over window
            for item in window:
                # Yield item
                yield item

        # Apply tail operation to items
        return self.apply(items, lambda x: operation(x))
