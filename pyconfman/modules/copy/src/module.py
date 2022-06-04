from __future__ import annotations
import pathlib

from pyconfman.modules.copy.src.models import Copy


def local_copy(
    source: str | pathlib.Path,
    destination: str | pathlib.Path,
    create: bool = True,
    overwrite: bool = False,
    same_file_ok: bool = True,
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

    TODO: describe copy behaviour with destination directories

    :parameter source: the source (file or directory) to copy from
    :parameter destination: the destination (file or directory) to copy to
    :parameter create: create the destination if it does not exist
    :parameter overwrite: overwrite the destination if it exists TODO: add warning
    :parameter same_file_ok: indicate if an Exception should be raised when source and
               destination are the same file. If this is True no exception will be
               raised
    :raises SourceDoesNotExistError: when source does not exist
    :raises SourceMustBeDirectoryOrFileError: when source is not a regular file or
            directory
    :raises DestinationExistsError: when destination exists and overwrite is False
    :raises DestinationDoesNotExistError: when create is False and destination does not
            exist
    :raises `shutil.SameFileError`: if same_file_ok is False and source as well as
            destination are the same file
    """

    Copy(source, destination, create, overwrite, same_file_ok).copy()
