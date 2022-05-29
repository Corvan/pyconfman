from __future__ import annotations
import abc
import pathlib
import shutil
from shutil import SameFileError


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


def copy(
    source: str | pathlib.Path,
    destination: str | pathlib.Path,
    create: bool = True,
    overwrite: bool = False,
):
    """
    copy a resource (file or directory)



    :parameter source: the source (file or directory) to copy from
    :parameter destination: the destination (file or directory) to copy to
    :parameter create: create the destination if it does not exist
    :parameter overwrite: overwrite the destination if it exists
    :raises SourceDoesNotExistError: when source does not exist
    :raises SourceMustBeDirectoryOrFileError: when source is not a file or directory
    :raises DestinationExistsError: when destination exists and overwrite is False
    :raises DestinationDoesNotExistError: when create is False and destination does not
            exist
    """

    Copy(source, destination, create, overwrite).copy()
