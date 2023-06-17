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
from core.utils.exceptions import InvalidKeyError, UndefinedError


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ ITEM METACLASS
# └─────────────────────────────────────────────────────────────────────────────────────


class ItemMetaclass(type):
    """A metaclass for the Item class"""

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ CLASS ATTRIBUTES
    # └─────────────────────────────────────────────────────────────────────────────────

    # Declare type of Meta
    Meta: type[Item.Meta]

    # Declare type of meta
    _meta: Item.Meta

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ __CALL__
    # └─────────────────────────────────────────────────────────────────────────────────

    def __call__(cls, *args: Any, **kwargs: Any) -> Item:
        """Call Method"""

        # Create instance
        instance: Item = super().__call__(*args, **kwargs)

        # Initialize meta
        instance._meta = cls.Meta()

        # Return instance
        return instance

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ __INIT__
    # └─────────────────────────────────────────────────────────────────────────────────

    def __init__(
        cls, name: str, bases: tuple[type, ...], attrs: dict[str, Any]
    ) -> None:
        """Init Method"""

        # Call super method
        super().__init__(name, bases, attrs)

        # Ensure that keys is a tuple
        cls.Meta.KEYS = tuple(cls.Meta.KEYS)

        # Ensure that indexes is a tuple
        cls.Meta.INDEXES = tuple(cls.Meta.INDEXES)

        # Initialize items
        cls.Meta.ITEMS = (
            cls.Meta.ITEMS.all()
            if isinstance(cls.Meta.ITEMS, Collection)
            else cls.Meta.ITEMS
        )

        # Initialize meta
        cls._meta = cls.Meta()

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ ITEMS
    # └─────────────────────────────────────────────────────────────────────────────────

    @property
    def items(cls) -> Collection | Items:
        """Returns the items of the item's meta instance"""

        # Get items
        items = cls.Meta.ITEMS

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

        # Iterate over keys
        for key in self._meta.KEYS:
            # Check if name relates to key
            if (isinstance(key, str) and name == key) or (
                isinstance(key, tuple) and name in key
            ):
                # Check if value is null
                if value in (None, ""):
                    # Raise a InvalidKeyError
                    raise InvalidKeyError("A key cannot have a null value.")

        # Call super method
        super().__setattr__(name, value)

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
    # │ PUSH
    # └─────────────────────────────────────────────────────────────────────────────────

    def push(self) -> None:
        """Pushes an item to the collection"""

        # Push item to items collection
        self.__class__.items.push(self)

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
