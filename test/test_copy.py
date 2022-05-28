import os.path

import pyconf
import pytest
from test.fixtures_copy import (
    prefix,
    source_file,
    destination_file,
    source_directory,
    destination_directory,
)


def test_source_file_to_destination_file(source_file, destination_file):
    with pytest.raises(OSError) as exc_info:
        pyconf.copy(source_file, destination_file)
    assert exc_info.type == OSError
    assert (
        exc_info.value.args[0]
        == "destination already exists, and overwrite has not been chosen"
    )


def test_source_file_to_destination_file_with_overwrite(source_file, destination_file):
    pyconf.copy(source_file, destination_file, overwrite=True)

    assert os.path.exists(destination_file)
    assert os.path.isfile(source_file)

    with open(destination_file, "r") as destination:
        assert destination.readlines()[0] == "test"


def test_source_file_to_destination_directory(source_file, destination_directory):
    pyconf.copy(source_file, destination_directory)

    assert os.path.exists(destination_directory)
    assert os.path.isdir(destination_directory)
    assert os.path.exists(f"{destination_directory}/{os.path.split(source_file)[-1]}")

    with open(
        f"{destination_directory}/{os.path.split(source_file)[-1]}"
    ) as destination:
        destination.readlines()[0] = "test"


def test_source_directory_to_destination_file(source_directory, destination_file):
    with pytest.raises(OSError) as exc_info:
        pyconf.copy(source_directory, destination_file)
    assert exc_info.type == OSError
    assert (
        exc_info.value.args[0]
        == "destination already exists, and overwrite has not been chosen"
    )
