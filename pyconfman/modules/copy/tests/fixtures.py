import pathlib
import shutil

import pytest

PREFIX = "/tmp/pyconfman"
SOURCE_PATH = f"{PREFIX}/source"
DESTINATION_PATH = f"{PREFIX}/destination"


@pytest.fixture
def prefix():
    prefix_path = pathlib.Path(PREFIX)
    if not prefix_path.exists():
        prefix_path.mkdir()

    yield prefix_path

    if prefix_path.exists():
        shutil.rmtree(prefix_path)


@pytest.fixture
def source_file(prefix):
    source_path = pathlib.Path(SOURCE_PATH)
    source_path.write_text("test")

    yield source_path

    if source_path.exists():
        source_path.unlink()


@pytest.fixture
def source_directory(prefix):
    source_path = pathlib.Path(SOURCE_PATH)
    source_path.mkdir()
    source_file = source_path / source_path.name
    source_file.write_text("test")

    yield source_path

    for children in source_path.iterdir():
        children.unlink()
    source_path.rmdir()


@pytest.fixture
def destination_file(prefix):
    destination_path = pathlib.Path(DESTINATION_PATH)
    destination_path.write_text("test")

    yield destination_path

    if destination_path.is_dir():
        for child in destination_path.iterdir():
            child.unlink()
        destination_path.rmdir()
    elif destination_path.is_file():
        destination_path.unlink()


@pytest.fixture
def destination_directory(prefix):
    destination_path = pathlib.Path(DESTINATION_PATH)
    destination_path.mkdir()

    yield destination_path

    if destination_path.is_dir():
        for child in destination_path.iterdir():
            child.unlink()
        destination_path.rmdir()
    elif destination_path.is_file():
        destination_path.unlink()
