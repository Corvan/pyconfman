import pathlib
import shutil

import pyconfman.modules
import pytest

from pyconfman.modules.copy.tests.fixtures import (
    SOURCE_PATH,
    DESTINATION_PATH,
    prefix,
    source_file,
    source_directory,
    destination_file,
    destination_directory,
)


class TestPaths:
    def test_source_file_to_destination_file(self, source_file):
        destination_file = pathlib.Path(DESTINATION_PATH)
        assert not destination_file.exists()

        pyconfman.modules.copy.local_copy(source_file, destination_file)

        assert destination_file.exists()
        assert destination_file.read_text() == "test"
        destination_file.unlink()

    def test_source_file_to_destination_file_create_false(
        self, source_file, destination_file
    ):
        with pytest.raises(pyconfman.modules.copy.DestinationExistsError) as exc_info:
            pyconfman.modules.copy.local_copy(
                source_file, destination_file, create=False
            )

        assert exc_info.type == pyconfman.modules.copy.DestinationExistsError
        assert (
            exc_info.value.args[0]
            == "destination already exists, and overwrite has not been chosen"
        )

    def test_source_file_to_destination_file_with_overwrite(
        self, source_file, destination_file
    ):
        pyconfman.modules.copy.local_copy(source_file, destination_file, overwrite=True)

        assert destination_file.exists()
        assert source_file.is_file()

        assert destination_file.read_text() == "test"

    def test_source_not_existing(self, destination_file):
        source_file = pathlib.Path(SOURCE_PATH)

        assert not source_file.exists()

        with pytest.raises(pyconfman.modules.copy.SourceDoesNotExistError) as exc_info:
            pyconfman.modules.copy.local_copy(source_file, destination_file)

        assert exc_info.type == pyconfman.modules.copy.SourceDoesNotExistError
        assert exc_info.value.args[0] == "source does not exist"

    def test_source_file_to_destination_directory(
        self, source_file, destination_directory
    ):
        pyconfman.modules.copy.local_copy(source_file, destination_directory)

        assert destination_directory.exists()
        assert destination_directory.is_dir()

        destination_file = destination_directory / source_file.name
        assert destination_file.exists()
        assert destination_file.read_text() == "test"

    def test_source_file_to_destination_directory_create_false(self, source_file):
        destination_directory = pathlib.Path(DESTINATION_PATH)
        assert not destination_directory.exists()

        with pytest.raises(
            pyconfman.modules.copy.DestinationDoesNotExistError
        ) as exc_info:
            pyconfman.modules.copy.local_copy(
                source_file, destination_directory, create=False
            )

        assert exc_info.type == pyconfman.modules.copy.DestinationDoesNotExistError
        assert (
            exc_info.value.args[0]
            == "destination does not exist, and create has not been chosen"
        )

    def test_source_file_to_destination_directory_with_overwrite(
        self, source_file, destination_directory
    ):
        pyconfman.modules.copy.local_copy(
            source_file, destination_directory, overwrite=True
        )

        assert destination_directory.exists()
        assert destination_directory.is_file()
        assert destination_directory.read_text() == "test"

    def test_source_directory_to_destination_file(
        self, source_directory, destination_file
    ):
        with pytest.raises(pyconfman.modules.copy.DestinationExistsError) as exc_info:
            pyconfman.modules.copy.local_copy(source_directory, destination_file)

        assert exc_info.type == pyconfman.modules.copy.DestinationExistsError
        assert (
            exc_info.value.args[0]
            == "destination already exists, and overwrite has not been chosen"
        )

    def test_source_directory_to_destination_file_with_overwrite(
        self, source_directory, destination_file
    ):
        pyconfman.modules.copy.local_copy(
            source_directory, destination_file, overwrite=True
        )

        assert destination_file.is_dir()
        assert (destination_file / source_directory.name).exists()
        assert (destination_file / source_directory.name).read_text() == "test"

    def test_source_not_directory_or_file(self):
        source_file = pathlib.Path("/dev/loop0")
        destination_file = pathlib.Path(DESTINATION_PATH)

        assert source_file.exists()
        assert source_file.is_block_device()

        with pytest.raises(
            pyconfman.modules.copy.SourceMustBeDirectoryOrFileError
        ) as exc_info:
            pyconfman.modules.copy.local_copy(source_file, destination_file)

        assert exc_info.type == pyconfman.modules.copy.SourceMustBeDirectoryOrFileError
        assert (
            exc_info.value.args[0] == "source must be either regular file or directory"
        )

    def test_source_and_destination_are_same_file(self, source_file):
        with pytest.raises(shutil.SameFileError) as exc_info:
            pyconfman.modules.copy.local_copy(
                source_file, source_file, same_file_ok=False
            )
        assert exc_info.type == shutil.SameFileError
        assert (
            exc_info.value.args[0]
            == f"PosixPath('{source_file}') and PosixPath('{source_file}') "
            f"are the same file"
        )


class TestStrings:
    def test_source_file_to_destination_file(self, source_file):
        destination_file = pathlib.Path(DESTINATION_PATH)
        assert not destination_file.exists()

        pyconfman.modules.copy.local_copy(str(source_file), str(destination_file))

        assert destination_file.exists()
        assert destination_file.read_text() == "test"
        destination_file.unlink()

    def test_source_file_to_destination_file_create_false(
        self, source_file, destination_file
    ):
        with pytest.raises(pyconfman.modules.copy.DestinationExistsError) as exc_info:
            pyconfman.modules.copy.local_copy(
                str(source_file), str(destination_file), create=False
            )

        assert exc_info.type == pyconfman.modules.copy.DestinationExistsError
        assert (
            exc_info.value.args[0]
            == "destination already exists, and overwrite has not been chosen"
        )

    def test_source_file_to_destination_file_with_overwrite(
        self, source_file, destination_file
    ):
        pyconfman.modules.copy.local_copy(
            str(source_file), str(destination_file), overwrite=True
        )

        assert destination_file.exists()
        assert source_file.is_file()

        assert destination_file.read_text() == "test"

    def test_source_not_existing(self, destination_file):
        source_file = pathlib.Path(SOURCE_PATH)

        assert not source_file.exists()

        with pytest.raises(pyconfman.modules.copy.SourceDoesNotExistError) as exc_info:
            pyconfman.modules.copy.local_copy(str(source_file), str(destination_file))

        assert exc_info.type == pyconfman.modules.copy.SourceDoesNotExistError
        assert exc_info.value.args[0] == "source does not exist"

    def test_source_file_to_destination_directory(
        self, source_file, destination_directory
    ):
        pyconfman.modules.copy.local_copy(str(source_file), f"{destination_directory}/")

        assert destination_directory.exists()
        assert destination_directory.is_dir()

        destination_file = destination_directory / source_file.name
        assert destination_file.exists()
        assert destination_file.read_text() == "test"

    def test_source_file_to_destination_directory_create_false(self, source_file):
        destination_directory = pathlib.Path(DESTINATION_PATH)
        assert not destination_directory.exists()

        with pytest.raises(
            pyconfman.modules.copy.DestinationDoesNotExistError
        ) as exc_info:
            pyconfman.modules.copy.local_copy(
                str(source_file), f"{destination_directory}/", create=False
            )

        assert exc_info.type == pyconfman.modules.copy.DestinationDoesNotExistError
        assert (
            exc_info.value.args[0]
            == "destination does not exist, and create has not been chosen"
        )

    def test_source_file_to_destination_directory_with_overwrite(
        self, source_file, destination_directory
    ):
        pyconfman.modules.copy.local_copy(
            str(source_file), f"{destination_directory}/", overwrite=True
        )

        assert destination_directory.exists()
        assert destination_directory.is_file()
        assert destination_directory.read_text() == "test"

    def test_source_directory_to_destination_file(
        self, source_directory, destination_file
    ):
        with pytest.raises(pyconfman.modules.copy.DestinationExistsError) as exc_info:
            pyconfman.modules.copy.local_copy(
                f"{source_directory}", str(destination_file)
            )

        assert exc_info.type == pyconfman.modules.copy.DestinationExistsError
        assert (
            exc_info.value.args[0]
            == "destination already exists, and overwrite has not been chosen"
        )

    def test_source_directory_to_destination_file_with_overwrite(
        self, source_directory, destination_file
    ):
        pyconfman.modules.copy.local_copy(
            f"{source_directory}/", str(destination_file), overwrite=True
        )

        assert destination_file.is_dir()
        assert (destination_file / source_directory.name).exists()
        assert (destination_file / source_directory.name).read_text() == "test"

    def test_source_not_directory_or_file(self):
        source_file = "/dev/loop0"
        destination_file = DESTINATION_PATH

        source_path = pathlib.Path(source_file)
        assert source_path.exists()
        assert source_path.is_block_device()

        with pytest.raises(
            pyconfman.modules.copy.SourceMustBeDirectoryOrFileError
        ) as exc_info:
            pyconfman.modules.copy.local_copy(source_file, destination_file)

        assert exc_info.type == pyconfman.modules.copy.SourceMustBeDirectoryOrFileError
        assert (
            exc_info.value.args[0] == "source must be either regular file or directory"
        )
