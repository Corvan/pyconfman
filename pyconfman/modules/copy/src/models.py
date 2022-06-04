from __future__ import annotations

import pathlib
import shutil

import pyconfman.models

from pyconfman.modules.copy.src.exceptions import (
    SourceDoesNotExistError,
    DestinationExistsError,
    DestinationDoesNotExistError,
    SourceMustBeDirectoryOrFileError,
)


class Source(pyconfman.models.Resource):
    def __init__(self, path: pathlib.Path | str):
        super().__init__(path)

    def check_preconditions(self):
        if not self.path.exists():
            raise SourceDoesNotExistError("source does not exist")
        if not (self.path.is_dir() or self.path.is_file()):
            raise SourceMustBeDirectoryOrFileError(
                "source must be either regular file or directory"
            )


class Destination(pyconfman.models.Resource):
    def __init__(self, path: pathlib.Path, create: bool, overwrite: bool):
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


class Copy(pyconfman.models.Action):
    def __init__(
        self,
        source: pathlib.Path,
        destination: pathlib.Path,
        create: bool,
        overwrite: bool,
        same_file_ok: bool,
    ):
        self.source: Source = Source(source)
        self.destination: Destination = Destination(destination, create, overwrite)
        self.same_file_ok = same_file_ok

    def copy(self):
        self.source.check_preconditions()
        try:
            self.destination.check_preconditions()
        except DestinationExistsError:
            if not self.same_file_ok and self.source.path.samefile(
                self.destination.path
            ):
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
