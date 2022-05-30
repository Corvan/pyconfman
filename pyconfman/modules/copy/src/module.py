from __future__ import annotations
import pathlib

from pyconfman.modules.copy.src.models import Copy


def local_copy(
    source: str | pathlib.Path,
    destination: str | pathlib.Path,
    create: bool = True,
    overwrite: bool = False,
):
    """
    copy a resource (file or directory)

    this function triggers to copy a resource from a source path to a destination path.
    It only works with regular files and directories.

    If source and destination are passed as strings the difference between referring to
    a file or a directory are trailing slashes. A file does not have a trailing slash;
    a directory has got one

    E.g.:

    - "/tmp/file"
    - "/tmp/directory/"

    :parameter source: the source (file or directory) to copy from
    :parameter destination: the destination (file or directory) to copy to
    :parameter create: create the destination if it does not exist
    :parameter overwrite: overwrite the destination if it exists
    :raises SourceDoesNotExistError: when source does not exist
    :raises SourceMustBeDirectoryOrFileError: when source is not a regular file or
            directory
    :raises DestinationExistsError: when destination exists and overwrite is False
    :raises DestinationDoesNotExistError: when create is False and destination does not
            exist
    """

    Copy(source, destination, create, overwrite).copy()
