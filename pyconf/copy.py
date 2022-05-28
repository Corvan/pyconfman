from __future__ import annotations

import os
import pathlib
import shutil
from pathlib import Path
from shutil import SameFileError


def copy(
    source: str | pathlib.Path, destination: str | pathlib.Path, overwrite: bool = False
):
    """
    copy a resource (file or directory)
    """
    if isinstance(source, str):
        source: Path = pathlib.Path(source)
    if isinstance(destination, str):
        destination: Path = pathlib.Path(destination)
    if destination.exists() and overwrite:
        try:
            os.remove(destination)
        except IsADirectoryError:
            shutil.rmtree(destination)
    if destination.exists() and not destination.is_dir() and not overwrite:
        raise OSError("destination already exists, and overwrite has not been chosen")
    if source.is_dir():
        shutil.copytree(source, destination)
    elif source.is_file():
        try:
            shutil.copy(source, destination)
        except SameFileError:
            pass
    else:
        raise OSError("source must be either file or directory")
