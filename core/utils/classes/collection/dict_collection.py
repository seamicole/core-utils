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

    # Declare type of item IDs by index
    _item_ids_by_index: dict[Any, set[int]]

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ __INIT__
    # └─────────────────────────────────────────────────────────────────────────────────

    def __init__(self) -> None:
        """Init Method"""

        # Initialize items by ID
        self._items_by_id = {}

        # Initialize item IDs by key
        self._item_ids_by_key = {}

        # Initialize item IDs by index
        self._item_ids_by_index = {}

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ COLLECT
    # └─────────────────────────────────────────────────────────────────────────────────

    def collect(self, items: Items | None = None) -> Generator[Item, None, None]:
        """Yields items in the collection"""

        # Get operations
        operations = self.apply(items)._operations

        # Iterate over operations
        for operation in operations:
            # Check if callable
            if callable(operation):
                # Yield from operation
                yield from operation(tuple(self._items_by_id.values()))

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ HEAD
    # └─────────────────────────────────────────────────────────────────────────────────

    def head(self, n: int, items: Items | None = None) -> Items:
        """Returns the first n items in the collection"""

        # Apply head operation to items
        return self.apply(items, lambda i: i[:n])

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ PUSH
    # └─────────────────────────────────────────────────────────────────────────────────

    def push(self, item: Item) -> None:
        """Pushes an item to the collection"""

        # Get item ID
        item_id = id(item)

        # Iterate over keys
        for key in item._meta.keys:
            # Get value
            value = (
                tuple([getattr(item, k, None) for k in key])
                if isinstance(key, tuple)
                else getattr(item, key, None)
            )

            # Continue if value is null
            if value in (None, ""):
                continue

            # Check if key already exists
            if value in self._item_ids_by_key:
                # Check item ID does not match the current item
                if self._item_ids_by_key[value] != item_id:
                    # Raise a duplicate key error
                    raise DuplicateKeyError(
                        f"An item with the key '{value}' already exists."
                    )

            # Add item ID to item IDs by key
            self._item_ids_by_key[value] = item_id

        # Add item to items by ID
        self._items_by_id[item_id] = item

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ SLICE
    # └─────────────────────────────────────────────────────────────────────────────────

    def slice(self, start: int, stop: int, items: Items | None = None) -> Items:
        """Returns a slice of items in the collection"""

        # Apply slice operation to items
        return self.apply(items, lambda x: x[start:stop])

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ TAIL
    # └─────────────────────────────────────────────────────────────────────────────────

    def tail(self, n: int, items: Items | None = None) -> Items:
        """Returns the last n items in the collection"""

        # Apply tail operation to items
        return self.apply(items, lambda x: x[-n:])
