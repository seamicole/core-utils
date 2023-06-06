# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ GENERAL IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from __future__ import annotations

from typing import Any

# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ PROJECT IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ ITEM METACLASS
# └─────────────────────────────────────────────────────────────────────────────────────


class ItemMetaclass(type):
    """A custom metaclass for the Item utility class"""

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ CLASS ATTRIBUTES
    # └─────────────────────────────────────────────────────────────────────────────────

    # Declare type of Meta
    Meta: type[Item.Meta]

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ INSTANCE ATTRIBUTES
    # └─────────────────────────────────────────────────────────────────────────────────

    # Declare type of meta
    _meta: Item.Meta

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ __NEW__
    # └─────────────────────────────────────────────────────────────────────────────────

    def __new__(
        cls, name: str, bases: tuple[type, ...], attrs: dict[str, Any]
    ) -> ItemMetaclass:
        """New Method"""

        # Create new class
        cls_new = super().__new__(cls, name, bases, attrs)

        # Initialize meta
        cls_new._meta = cls_new.Meta()

        # Return new class
        return cls_new


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ ITEM
# └─────────────────────────────────────────────────────────────────────────────────────


class Item:
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
    # │ __STR__
    # └─────────────────────────────────────────────────────────────────────────────────

    def __str__(self) -> str:
        """String Method"""

        # Iterate over keys
        for key in self.Meta.KEYS:
            # Continue if item does not have key
            if not hasattr(self, key):
                continue

            # Get value
            value = getattr(self, key)

            # Return the string of the value
            return str(value)

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

        # Initialize keys
        KEYS: tuple[str, ...] = ()

        # ┌─────────────────────────────────────────────────────────────────────────────
        # │ INSTANCE ATTRIBUTES
        # └─────────────────────────────────────────────────────────────────────────────

        # Declare type of keys
        keys: tuple[str, ...]

        # ┌─────────────────────────────────────────────────────────────────────────────
        # │ __INIT__
        # └─────────────────────────────────────────────────────────────────────────────

        def __init__(self) -> None:
            """Init Method"""

            # Initialize and set keys
            self.keys = tuple(self.KEYS)
