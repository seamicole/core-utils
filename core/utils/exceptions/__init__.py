# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ ERROR
# └─────────────────────────────────────────────────────────────────────────────────────


class Error(Exception):
    """A base class for exception subclasses"""

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ __INIT__
    # └─────────────────────────────────────────────────────────────────────────────────

    def __init__(self, message: str) -> None:
        """Init Method"""
        # Set message
        self.message = message

        # Call super init
        super().__init__(message)


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ DOES NOT EXIST ERROR
# └─────────────────────────────────────────────────────────────────────────────────────


class DoesNotExistError(Error):
    """Raised when an expected resource does not exist"""


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ INVALID KEY ERROR
# └─────────────────────────────────────────────────────────────────────────────────────


class InvalidKeyError(Error):
    """Raised when an invalid key is encountered"""


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ DUPLICATE KEY ERROR
# └─────────────────────────────────────────────────────────────────────────────────────


class DuplicateKeyError(Error):
    """Raised when a duplicate key is found"""


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ UNDEFINED ERROR
# └─────────────────────────────────────────────────────────────────────────────────────


class UndefinedError(Error):
    """Raised when an expected resource is undefined"""
