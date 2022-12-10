"""
the models module for copying resources
"""
from __future__ import annotations

import pathlib
import shutil
from typing import Optional

import pyconfman.models

from pyconfman.modules.copy.src.exceptions import (
    SourceDoesNotExistError,
    DestinationExistsError,
    DestinationDoesNotExistError,
    SourceMustBeDirectoryOrFileError,
)


class Source(pyconfman.models.Resource):
    """
    Class representing a source resource to be copied from
    """

    def __init__(self, path: pathlib.Path | str):
        super().__init__(path)
        if self.path and not self.path.exists():
            raise SourceDoesNotExistError("source does not exist")
        if self.path and not (self.path.is_dir() or self.path.is_file()):
            raise SourceMustBeDirectoryOrFileError(
                "source must be either regular file or directory"
            )


class Destination(pyconfman.models.Resource):
    """
    class representing a destination resource to be copied to
    """

    def __init__(self, path: pathlib.Path, create: bool, overwrite: bool):
        super().__init__(path)
        self.create: bool = create
        self.overwrite: bool = overwrite
        self.directory: bool = False

        if self.path and self.path.exists() and self.path.is_file():
            if not self.overwrite:
                raise DestinationExistsError(
                    "destination already exists, and overwrite has not been chosen"
                )
            self.path.unlink()
        elif self.path and self.path.is_dir() and self.overwrite:
            shutil.rmtree(self.path)
        else:
            if not self.create:
                raise DestinationDoesNotExistError(
                    "destination does not exist, and create has not been chosen"
                )


class Copy(pyconfman.models.Action):
    """
    class representing the copy action
    """

    def __init__(
        self,
        source: pathlib.Path | str,
        destination: pathlib.Path | str,
        update: bool,
        create: bool,
        overwrite: bool,
        same_file_ok: bool,
    ):  # pylint: disable = too-many-arguments
        super().__init__()
        self.update = update
        self.same_file_ok = same_file_ok
        self.source: Source = Source(source)
        self.destination: Destination = Destination(
            pathlib.Path(destination) if isinstance(destination, str) else destination,
            create,
            overwrite,
        )
        if self.update:
            if self.has_changed(self.destination.path):
                self.overwrite = True
        else:
            if not self.has_changed(self.destination.path):
                pass

    def copy(self):
        """
        actually run the copy action
        """
        if self.source.path.is_dir():
            shutil.copytree(self.source.path, self.destination.path)
        elif self.source.path.is_file():
            try:
                shutil.copy(self.source.path, self.destination.path)
            except shutil.SameFileError:
                if not self.same_file_ok:
                    raise

    def has_changed(self, destination: Optional[pathlib.Path] = None) -> bool:
        """
        query whether the source is different from the destination and therefore maybe
        has to be copied again
        :param destination: the destination to check
        :return: True if the source is different from the destination, False otherwise
        """
        if destination:
            if self.source.hash == Destination.calculate_hash(
                destination,
            ):
                return True
        return False
