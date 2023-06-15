# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ GENERAL IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from __future__ import annotations

from typing import Any

# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ PROJECT IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from core.utils.classes.collection.collection import Collection
from core.utils.classes.item.items import Items
from core.utils.exceptions import UndefinedError


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ ITEM METACLASS
# └─────────────────────────────────────────────────────────────────────────────────────


class ItemMetaclass(type):
    """A metaclass for the Item class"""

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ CLASS ATTRIBUTES
    # └─────────────────────────────────────────────────────────────────────────────────

    # Declare type of meta
    _meta: Item.Meta

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ ITEMS
    # └─────────────────────────────────────────────────────────────────────────────────

    @property
    def items(cls) -> Items:
        """Returns the items of the item's meta instance"""

        # Get items
        items = cls._meta.items

        # Check if items is None
        if items is None:
            # Raise UndefinedError
            raise UndefinedError(f"{cls.__name__}.Meta.ITEMS is undefined")

        # Return items
        return items


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ ITEM
# └─────────────────────────────────────────────────────────────────────────────────────


class Item(metaclass=ItemMetaclass):
    """A utility class that represents an arbitrary Python object"""

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ INSTANCE ATTRIBUTES
    # └─────────────────────────────────────────────────────────────────────────────────

    # Declare type of meta
    _meta: Item.Meta

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ INIT SUBCLASS
    # └─────────────────────────────────────────────────────────────────────────────────

    def __init_subclass__(cls, **kwargs: Any) -> None:
        """Init Subclass Method"""

        # Initialize meta
        cls._meta = cls.Meta(ItemClass=cls)

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ __REPR__
    # └─────────────────────────────────────────────────────────────────────────────────

    def __repr__(self) -> str:
        """Representation Method"""

        # Get representation
        representation = self.__class__.__name__

        # Add angle brackets to representation
        representation = f"<{representation}: {self.__str__()}>"

        # Return representation
        return representation

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ __SETATTR__
    # └─────────────────────────────────────────────────────────────────────────────────

    def __setattr__(self, name: str, value: Any) -> None:
        """Set Attribute Method"""

        # Determine if altering an existing attribute
        altering = hasattr(self, name)

        # Call super method
        super().__setattr__(name, value)

        # Check if altering
        if altering:
            # Get keys altered
            keys_altered = self._meta.keys_altered

            # Iterate over keys
            for key in self._meta.keys:
                # Check if name relates to key
                if (isinstance(key, str) and name == key) or (
                    isinstance(key, tuple) and name in key
                ):
                    # Check if name is in keys altered
                    if key in keys_altered:
                        # Delete name from keys altered
                        del keys_altered[name]

                    # Otherwise record initial value
                    else:
                        # Add name to keys altered
                        keys_altered[name] = value

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ __STR__
    # └─────────────────────────────────────────────────────────────────────────────────

    def __str__(self) -> str:
        """String Method"""

        # Iterate over keys
        for key in self.Meta.KEYS:
            # Check if key is a string
            if isinstance(key, str):
                # Continue if item does not have key
                if not hasattr(self, key):
                    continue

                # Get value
                value = getattr(self, key)

                # Continue if value is null
                if value in (None, ""):
                    continue

                # Return the string of the value
                return str(value)

            # Otherwise check if key is a tuple
            elif isinstance(key, tuple):
                # Get values
                values = tuple(getattr(self, k, None) for k in key)

                # Continue if any value is null
                if any(value in (None, "") for value in values):
                    continue

                # Return the string of the values
                return "-".join(str(value) for value in values)

        # Return the hex ID of the item
        return hex(id(self))

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ META
    # └─────────────────────────────────────────────────────────────────────────────────

    class Meta:
        """Meta Class"""

        # ┌─────────────────────────────────────────────────────────────────────────────
        # │ CLASS ATTRIBUTES
        # └─────────────────────────────────────────────────────────────────────────────

        # Initialize indexes
        INDEXES: tuple[str | tuple[str, ...], ...] = ()

        # Initialize items
        ITEMS: Collection | Items | None = None

        # Initialize keys
        KEYS: tuple[str | tuple[str, ...], ...] = ()

        # ┌─────────────────────────────────────────────────────────────────────────────
        # │ INSTANCE ATTRIBUTES
        # └─────────────────────────────────────────────────────────────────────────────

        # Declare type of indexes
        indexes: tuple[str | tuple[str, ...], ...]

        # Declare type of items
        items: Items | None

        # Declare type of keys
        keys: tuple[str | tuple[str, ...], ...]

        # Declare type of keys altered
        keys_altered: dict[str | tuple[str, ...], Any]

        # ┌─────────────────────────────────────────────────────────────────────────────
        # │ __INIT__
        # └─────────────────────────────────────────────────────────────────────────────

        def __init__(self, ItemClass: type[Item]) -> None:
            """Init Method"""

            # Initialize and set items
            self.items = (
                self.ITEMS.all() if isinstance(self.ITEMS, Collection) else self.ITEMS
            )

            # Initialize and set keys
            self.keys = tuple(self.KEYS)

            # Initialize and set keys altered
            self.keys_altered = {}

            # Initialize and set indexes
            self.indexes = tuple(self.INDEXES)
