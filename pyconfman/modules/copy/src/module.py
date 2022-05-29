from __future__ import annotations
import pathlib

from pyconfman.modules.copy.src.models import Copy


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
