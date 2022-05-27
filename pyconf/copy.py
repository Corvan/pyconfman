import os
import pathlib
import shutil
from shutil import SameFileError


def copy(source: str | pathlib.Path, destination: str | pathlib.Path, overwrite: bool = None):
    """
    copy a resource (file or directory)
    """
    if isinstance(source, str):
        source = pathlib.Path(source)
    if isinstance(destination, str):
        destination = pathlib.Path(destination)
    if destination.exists():
        if overwrite:
            try:
                os.remove(destination)
            except IsADirectoryError:
                os.rmdir(destination)
    if source.is_dir():
        shutil.copytree(source, destination)


    elif source.is_file():
        try:
            shutil.copy(source, destination)
        except SameFileError:
            pass

