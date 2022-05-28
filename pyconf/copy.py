from __future__ import annotations
import abc
import os
import pathlib
import shutil
from shutil import SameFileError


class Resource(abc.ABC):
    def __init__(self, path: pathlib.Path | str):
        self._path: pathlib.Path = None
        self.path = path

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


class Destination(Resource):
    def __init__(self, path: pathlib.Path, create: bool, overwrite: bool):
        super().__init__(path)
        self.create: bool = create
        self.overwrite: bool = overwrite
        self.directory: bool = False

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
        if not self.source.path.exists():
            raise OSError("source does not exist")
        if self.destination.path.exists():
            if self.destination.path.is_file():
                if not self.destination.overwrite:
                    raise OSError(
                        "destination already exists, and overwrite has not been chosen"
                    )
                os.remove(self.destination.path)
            elif self.destination.path.is_dir():
                if self.destination.overwrite:
                    shutil.rmtree(self.destination.path)
        else:
            if not self.destination.create:
                raise OSError(
                    "destination does not exist, and create has not been chosen"
                )

        if self.source.path.is_dir():
            shutil.copytree(self.source.path, self.destination.path)
        elif self.source.path.is_file():
            try:
                shutil.copy(self.source.path, self.destination.path)
            except SameFileError:
                pass
        else:
            raise OSError("source must be either file or directory")


def copy(
    source: str | pathlib.Path,
    destination: str | pathlib.Path,
    create: bool = True,
    overwrite: bool = False,
):
    """
    copy a resource (file or directory)
    """

    Copy(source, destination, create, overwrite).copy()
