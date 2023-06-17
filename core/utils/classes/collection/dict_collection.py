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

    # Declare type of item IDs by key or index
    _item_ids_by_key_or_index: dict[Any, set[int]]

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ __INIT__
    # └─────────────────────────────────────────────────────────────────────────────────

    def __init__(self) -> None:
        """Init Method"""

        # Initialize items by ID
        self._items_by_id = {}

        # Initialize item IDs by key or index
        self._item_ids_by_key_or_index = {}

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

        # Get item IDs by key or index
        item_ids_by_key_or_index = self._item_ids_by_key_or_index

        # Initialize values
        values = set()

        # Iterate over keys
        for key in item._meta.KEYS:
            # Get value
            value = (
                tuple([getattr(item, k, None) for k in key])
                if isinstance(key, tuple)
                else getattr(item, key, None)
            )

            # Get item IDs
            item_ids = item_ids_by_key_or_index.get(value, set())

            # Continue if item ID already exists
            if item_id in item_ids:
                continue

            # Check if there is an existing item with the same key
            if item_ids and item_id not in item_ids:
                # Raise a duplicate key error
                raise DuplicateKeyError(
                    f"An item with the key '{value}' already exists."
                )

            # Add item ID to item IDs by key or index
            self._item_ids_by_key_or_index[value] = {item_id}

            # Add key value to values
            values.add(value)

        # Check if there are any values
        if values:
            # Iterate over item IDs by key or index
            for value in list(item_ids_by_key_or_index):
                # Get item IDs
                item_ids = item_ids_by_key_or_index[value]

                # Continue if value in values
                if value in values:
                    continue

                # Remove item ID from item IDs
                item_ids.remove(item_id)

                # Check if item IDs is empty
                if not item_ids:
                    # Remove item IDs by key or index
                    del item_ids_by_key_or_index[value]

        # Add item to items by ID
        self._items_by_id[item_id] = item

        # WONT WORK BECAUSE IF ONE KEY CHANGES BUT ANOTHER DOESNT,
        # THEN THE UNCHANGED KEY WILL BE REMOVED FROM THE INDEX

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
