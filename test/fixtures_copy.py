import os
import shutil

import pytest

PREFIX = "/tmp/pyconf"
SOURCE_PATH = f"{PREFIX}/source"
DESTINATION_PATH = f"{PREFIX}/destination"


@pytest.fixture
def prefix():
    if not os.path.exists(PREFIX):
        os.mkdir(PREFIX)
    yield prefix
    if os.path.exists(PREFIX):
        shutil.rmtree(PREFIX)


@pytest.fixture
def source_file(prefix):
    with open(SOURCE_PATH, "w") as source:
        source.writelines(["test"])
    yield SOURCE_PATH
    if os.path.exists(SOURCE_PATH):
        os.remove(SOURCE_PATH)


@pytest.fixture
def source_directory(prefix):
    os.mkdir(SOURCE_PATH)
    with open(f"{SOURCE_PATH}/source", "w") as source:
        source.writelines(["test"])
    yield SOURCE_PATH
    for dir_path, dir_names, file_names in os.walk(SOURCE_PATH):
        for filename in file_names:
            os.remove(f"{SOURCE_PATH}/{filename}")
    os.rmdir(f"{SOURCE_PATH}")


@pytest.fixture
def destination_file(prefix):
    with open(DESTINATION_PATH, "w") as destination:
        destination.writelines(["test"])
    yield DESTINATION_PATH
    os.remove(DESTINATION_PATH)


@pytest.fixture
def destination_directory(prefix):
    os.mkdir(DESTINATION_PATH)
    yield DESTINATION_PATH
    for dir_path, dir_names, file_names in os.walk(DESTINATION_PATH):
        for filename in file_names:
            os.remove(f"{DESTINATION_PATH}/{filename}")
    os.rmdir(DESTINATION_PATH)
