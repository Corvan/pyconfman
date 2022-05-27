import os.path
import shutil

import pyconf
import pytest

PREFIX = "/tmp/pyconf"
SOURCE_PATH = f"{PREFIX}/source"
DESTINATION_PATH = f"{PREFIX}/destination"


@pytest.fixture
def prefix():
    if not os.path.exists(PREFIX):
        os.mkdir(PREFIX)
    yield
    if os.path.exists(PREFIX):
        shutil.rmtree(PREFIX)


@pytest.fixture
def source_file(prefix):
    with open(SOURCE_PATH, "w") as source:
        source.writelines(["test"])
    yield
    if os.path.exists(SOURCE_PATH):
        os.remove(SOURCE_PATH)


@pytest.fixture
def source_directory(prefix):
    pass


@pytest.fixture
def destination_file(prefix):
    yield
    os.remove(DESTINATION_PATH)


@pytest.fixture
def destination_directory(prefix):
    os.mkdir(DESTINATION_PATH)
    yield
    for dirpath, dirnames, filenames in os.walk(DESTINATION_PATH):
        for filename in filenames:
            os.remove(f"{DESTINATION_PATH}/{filename}")
    os.rmdir(DESTINATION_PATH)


def test_source_file_to_destination_file(source_file, destination_file):
    pyconf.copy(SOURCE_PATH, DESTINATION_PATH)

    assert os.path.exists(DESTINATION_PATH)
    assert os.path.isfile(SOURCE_PATH)

    with open(DESTINATION_PATH, "r") as destination:
        assert destination.readlines()[0] == "test"


def test_source_file_to_destination_directory(source_file, destination_directory):
    pyconf.copy(SOURCE_PATH, DESTINATION_PATH)

    assert os.path.exists(DESTINATION_PATH)
    assert os.path.isdir(DESTINATION_PATH)
    assert os.path.exists(f"{DESTINATION_PATH}/{os.path.split(SOURCE_PATH)[-1]}")

    with open(f"{DESTINATION_PATH}/{os.path.split(SOURCE_PATH)[-1]}") as destination:
        destination.readlines()[0] = "test"
