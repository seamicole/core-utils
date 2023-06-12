# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ GENERAL IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from __future__ import annotations

from typing import Any

# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ PROJECT IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────


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

        def __init__(self, ItemClass: type[Item]) -> None:
            """Init Method"""

            # Initialize and set keys
            self.keys = tuple(self.KEYS)
