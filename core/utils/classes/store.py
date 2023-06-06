# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ GENERAL IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from abc import ABC, abstractmethod

# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ PROJECT IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from core.utils.classes.collection import Collection


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ STORE
# └─────────────────────────────────────────────────────────────────────────────────────


class Store(ABC):
    """An abstract class that represents a store that houses collections of items"""

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ CLASS ATTRIBUTES
    # └─────────────────────────────────────────────────────────────────────────────────

    # Initialize collection class
    CollectionClass: Collection = DictCollection

    # Declare type of collections by key
    _collections_by_key: dict[str, Collection]

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ CREATE
    # └─────────────────────────────────────────────────────────────────────────────────

    def create(
        self, key: str, CollectionClass: type[Collection] | Collection | None = None
    ) -> Collection:
        """Creates a collection by key"""

        # Initialize collection class
        CollectionClass = CollectionClass or self.CollectionClass

        # Initialize collection instance
        collection = (
            CollectionClass
            if isinstance(CollectionClass, Collection)
            else CollectionClass()
        )

        # Add collection to store
        self._collections_by_key[key] = collection

        # Return collection
        return collection

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ DELETE
    # └─────────────────────────────────────────────────────────────────────────────────

    def delete(self, key: str) -> None:
        """Deletes a collection by key"""

        # Delete collection
        del self._collections_by_key[key]

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ GET
    # └─────────────────────────────────────────────────────────────────────────────────

    def get(self, key: str) -> Collection | None:
        """Returns a collection by key"""

        # Return collection
        return self._collections_by_key.get(key, None)

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ GET OR CREATE
    # └─────────────────────────────────────────────────────────────────────────────────

    def get_or_create(
        self, key: str, CollectionClass: type[Collection] | Collection | None = None
    ) -> Collection:
        """Returns a collection by key, creating it if it doesn't exist"""

        # Get or create collection
        return self.get(key=key) or self.create(
            key=key, CollectionClass=CollectionClass
        )
