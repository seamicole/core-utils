# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ ITEM
# └─────────────────────────────────────────────────────────────────────────────────────


class Item:
    """A utility class that represents an arbitrary Python object instance"""

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

        # Initialize keys
        KEYS: tuple[str, ...] = ()
