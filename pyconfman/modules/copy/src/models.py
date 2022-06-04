"""
Module containing the classes that are used by copy's function module
"""
from __future__ import annotations

import abc
import pathlib
import shutil

from pyconfman.modules.copy.src.exceptions import (
    SourceDoesNotExistError,
    DestinationExistsError,
    DestinationDoesNotExistError,
    SourceMustBeDirectoryOrFileError,
)


class Resource(abc.ABC):
    """
    Defining the base functionality of a resource, like a regular file or a directory
    """

    def __init__(self, path: pathlib.Path | str):
        self._path: pathlib.Path | None = None
        self.directory = False
        self.path = path

    @abc.abstractmethod
    def check_preconditions(self):
        """
        Check if preconditions for using a resource are met. Depending on the resource
        type this is to be overridden. If a precodition is not met, respective
        Exceptions are to be raised
        """
        raise NotImplementedError

    @property
    def path(self) -> pathlib.Path:
        """
        :return: a resources path
        """
        return self._path

    @path.setter
    def path(self, path: pathlib.Path | str):
        """
        :param path: the resource's path to be set
        """
        if isinstance(path, str):
            if path[-1] == "/":
                self.directory = True
            self.path = pathlib.Path(path)
        else:
            self._path = path


class Source(Resource):
    """
    A resource that is the source of a copy operation, can be a regular file or a
    directory
    """

    def __init__(self, path: pathlib.Path | str):
        super().__init__(path)

    def check_preconditions(self):
        """
        Check if preconditions for using a source are met.

        :raises `SourceDoesNotExistsError`: when no filesystem object can be found at
                the given path
        :raises `SourceMustBeDirectoryOrFileError`: when the filesystem object at the
                given path exists but is no regular file, like a socket, a blockdevice,
                etc.
        """
        if not self.path.exists():
            raise SourceDoesNotExistError("source does not exist")
        if not (self.path.is_dir() or self.path.is_file()):
            raise SourceMustBeDirectoryOrFileError(
                "source must be either regular file or directory"
            )


class Destination(Resource):
    """
    A resource that is the destination of a copy operation, can be a regular file or a
    directory
    """

    def __init__(self, path: pathlib.Path, create: bool, overwrite: bool):
        """
        create a destination resource

        :param path: Path of the filesystem object represented by this class
        :param create: If the filesystem object does not exist yet, create it
        :param overwrite: If the filesystem object exists, overwrite it. *WARNING*: Use
               this responsibly, data may get lost, because it will be deleted without
               further notice when `Copy.copy()` is called
        """
        super().__init__(path)
        self.create: bool = create
        self.overwrite: bool = overwrite
        self.directory: bool = False

    def check_preconditions(self):
        """
        Check if preconditions for using a destination are met.
        :raises `DestinationExistsError`:
        :raises `DestinationDoesNotExistError`:
        """
        if self.path.exists() and self.path.is_file():
            if not self.overwrite:
                raise DestinationExistsError(
                    "destination already exists, and overwrite has not been chosen"
                )
            self.path.unlink()
        elif self.path.is_dir() and self.overwrite:
            shutil.rmtree(self.path)
        else:
            if not self.create:
                raise DestinationDoesNotExistError(
                    "destination does not exist, and create has not been chosen"
                )


class Copy:
    """
    Representation of a copy operation.

    Is only prepared with its construction. To actually execute the operation,
    call `copy()`
    """

    def __init__(
        self,
        source: pathlib.Path,
        destination: pathlib.Path,
        create: bool,
        overwrite: bool,
        same_file_ok: bool,
    ):
        """
        prepare the copy operation.

        :param source: TODO
        :param destination: TODO
        :param create: TODO
        :param overwrite: TODO
        :param same_file_ok: TODO
        """
        self.source: Source = Source(source)
        self.destination: Destination = Destination(destination, create, overwrite)
        self.same_file_ok = same_file_ok

    def copy(self):
    """
    execute the actual copy operation. # TODO: describe copy inside dirs

    :raises DestinationExistsError: if the destination exists and
            `self.same_file_ok`
            is `False`, while source and destination are not the same.
    :raises `shutil.SameFileError`: when source and destination are the same and
            `self.same_file_ok` is `False`
    """
    self.source.check_preconditions()
    try:
        self.destination.check_preconditions()
    except DestinationExistsError:
        if not self.same_file_ok and self.source.path.samefile(self.destination.path):
            pass
        else:
            raise
        if self.source.path.is_dir():
            shutil.copytree(self.source.path, self.destination.path)
        elif self.source.path.is_file():
            try:
                shutil.copy(self.source.path, self.destination.path)
            except shutil.SameFileError:
                if not self.same_file_ok:
                    raise
