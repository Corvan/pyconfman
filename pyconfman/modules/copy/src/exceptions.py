"""
Exceptions for the copy package
"""
from __future__ import annotations


class SourceDoesNotExistError(OSError):
    """
    To be raised, when a source resource is given but it does not exist and ist not
    to be created
    """

    def __init__(self, message: str):
        super().__init__(message)


class SourceMustBeDirectoryOrFileError(OSError):
    """
    To be raised, when a source resource is not a directory or file; e.g. a socket
    """

    def __init__(self, message: str):
        super().__init__(message)


class DestinationExistsError(OSError):
    """
    To be raised, when a given destination resource exists but is to be created
    """

    def __init__(self, message: str):
        super().__init__(message)


class DestinationDoesNotExistError(OSError):
    """
    To be raised, when a given destination resource does not exist and is
    not to be created
    """

    def __init__(self, message: str):
        super().__init__(message)
