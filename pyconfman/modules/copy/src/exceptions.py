from __future__ import annotations


class SourceDoesNotExistError(OSError):
    def __init__(self, message: str):
        super().__init__(message)


class SourceMustBeDirectoryOrFileError(OSError):
    def __init__(self, message: str):
        super().__init__(message)


class DestinationExistsError(OSError):
    def __init__(self, message: str):
        super().__init__(message)


class DestinationDoesNotExistError(OSError):
    def __init__(self, message: str):
        super().__init__(message)
