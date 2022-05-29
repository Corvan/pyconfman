import pathlib

import pyconfman
import pytest

from test.fixtures_copy import (
    prefix,
    source_file,
    destination_file,
    source_directory,
    destination_directory,
    DESTINATION_PATH,
)


def test_source_file_to_destination_file(source_file):
    destination_file = pathlib.Path(DESTINATION_PATH)
    assert not destination_file.exists()

    pyconfman.copy(source_file, destination_file)

    assert destination_file.exists()
    assert destination_file.read_text() == "test"
    destination_file.unlink()


def test_source_file_to_destination_file_create_false(source_file, destination_file):
    with pytest.raises(pyconfman.DestinationExistsError) as exc_info:
        pyconfman.copy(source_file, destination_file, create=False)

    assert exc_info.type == pyconfman.DestinationExistsError
    assert (
        exc_info.value.args[0]
        == "destination already exists, and overwrite has not been chosen"
    )


def test_source_file_to_destination_file_with_overwrite(source_file, destination_file):
    pyconfman.copy(source_file, destination_file, overwrite=True)

    assert destination_file.exists()
    assert source_file.is_file()

    assert destination_file.read_text() == "test"


def test_source_file_to_destination_directory(source_file, destination_directory):
    pyconfman.copy(source_file, destination_directory)

    assert destination_directory.exists()
    assert destination_directory.is_dir()

    destination_file = destination_directory / source_file.name
    assert destination_file.exists()
    assert destination_file.read_text() == "test"


def test_source_file_to_destination_directory_create_false(source_file):
    destination_directory = pathlib.Path(DESTINATION_PATH)
    assert not destination_directory.exists()

    with pytest.raises(pyconfman.DestinationDoesNotExistError) as exc_info:
        pyconfman.copy(source_file, destination_directory, create=False)

    assert exc_info.type == pyconfman.DestinationDoesNotExistError
    assert (
        exc_info.value.args[0]
        == "destination does not exist, and create has not been chosen"
    )


def test_source_file_to_destination_directory_with_overwrite(
    source_file, destination_directory
):
    pyconfman.copy(source_file, destination_directory, overwrite=True)

    assert destination_directory.exists()
    assert destination_directory.is_file()
    assert destination_directory.read_text() == "test"


def test_source_directory_to_destination_file(source_directory, destination_file):
    with pytest.raises(pyconfman.DestinationExistsError) as exc_info:
        pyconfman.copy(source_directory, destination_file)

    assert exc_info.type == pyconfman.DestinationExistsError
    assert (
        exc_info.value.args[0]
        == "destination already exists, and overwrite has not been chosen"
    )


def test_source_directory_to_destination_file_with_overwrite(
    source_directory, destination_file
):
    pyconfman.copy(source_directory, destination_file, overwrite=True)

    assert destination_file.is_dir()
    assert (destination_file / source_directory.name).exists()
    assert (destination_file / source_directory.name).read_text() == "test"
