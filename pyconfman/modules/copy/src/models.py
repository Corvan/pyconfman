from __future__ import annotations

import abc
import pathlib
import shutil
from shutil import SameFileError

from pyconfman.modules.copy.src.exceptions import (
    SourceDoesNotExistError,
    DestinationExistsError,
    DestinationDoesNotExistError,
    SourceMustBeDirectoryOrFileError,
)


class Resource(abc.ABC):
    def __init__(self, path: pathlib.Path | str):
        self._path: pathlib.Path = None
        self.path = path

    @abc.abstractmethod
    def check_preconditions(self):
        raise NotImplementedError

    @property
    def path(self) -> pathlib.Path:
        return self._path

    @path.setter
    def path(self, path: pathlib.Path | str):
        if isinstance(path, str):
            self._path = pathlib.Path(path)
        else:
            self._path = path


class Source(Resource):
    def __init__(self, path: pathlib.Path | str):
        super().__init__(path)

    def check_preconditions(self):
        if not self.path.exists():
            raise SourceDoesNotExistError("source does not exist")


class Destination(Resource):
    def __init__(self, path: pathlib.Path, create: bool, overwrite: bool):
        super().__init__(path)
        self.create: bool = create
        self.overwrite: bool = overwrite
        self.directory: bool = False

    def check_preconditions(self):
        if self.path.exists():
            if self.path.is_file():
                if not self.overwrite:
                    raise DestinationExistsError(
                        "destination already exists, and overwrite has not been chosen"
                    )
                self.path.unlink()
            elif self.path.is_dir():
                if self.overwrite:
                    shutil.rmtree(self.path)
        else:
            if not self.create:
                raise DestinationDoesNotExistError(
                    "destination does not exist, and create has not been chosen"
                )

    @Resource.path.setter
    def path(self, path: pathlib.Path | str):
        if isinstance(path, str):
            if path[-1] == "/":
                self.directory = True
        else:
            self._path = path


class Copy:
    def __init__(
        self,
        source: pathlib.Path,
        destination: pathlib.Path,
        create: bool,
        overwrite: bool,
    ):
        self.source: Source = Source(source)
        self.destination: Destination = Destination(destination, create, overwrite)

    def copy(self):
        self.source.check_preconditions()
        self.destination.check_preconditions()
        if self.source.path.is_dir():
            shutil.copytree(self.source.path, self.destination.path)
        elif self.source.path.is_file():
            try:
                shutil.copy(self.source.path, self.destination.path)
            except SameFileError:
                pass
        else:
            raise SourceMustBeDirectoryOrFileError(
                "source must be either file or directory"
            )
