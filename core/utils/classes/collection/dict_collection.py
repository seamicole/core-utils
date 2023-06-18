# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ GENERAL IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from __future__ import annotations

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
    # │ CLASS ATTRIBUTES
    # └─────────────────────────────────────────────────────────────────────────────────

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
        collected = (i for i in self._items_by_id.values())

        # Iterate over operations
        for operation in operations:
            # Check if callable
            if callable(operation):
                # Apply operation to collected
                collected = operation(collected)

        # Yield collected items
        yield from collected

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
    # │ PUSH
    # └─────────────────────────────────────────────────────────────────────────────────

    def push(self, item: Item) -> None:
        """Pushes an item to the collection"""

        # Get item ID
        item_id = id(item)

        # Get keys by item ID
        keys_by_item_id = self._keys_by_item_id

        # Get item IDs by key
        item_ids_by_key = self._item_ids_by_key

        # Iterate over values
        for value in keys_by_item_id.pop(item_id, []):
            # Remove item ID from item IDs by key
            del item_ids_by_key[value]

        # Iterate over keys
        for key in item._meta.KEYS:
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

            # Add item ID to item IDs by key
            item_ids_by_key[value] = item_id

            # Add value to keys by item ID
            keys_by_item_id.setdefault(item_id, []).append(value)

        # Add item to items by ID
        self._items_by_id[item_id] = item

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

            # Iterate over items
            for i, item in enumerate(items):
                # Check if i is greater than or equal to n
                if i >= n:
                    # Yield item
                    yield item

        # Apply tail operation to items
        return self.apply(items, lambda x: operation(x))
