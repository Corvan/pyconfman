from __future__ import annotations

import abc
import hashlib
import pathlib

from .model import Model


class Resource(Model):
    __metaclass__ = abc.ABCMeta
    _path: pathlib.Path | None = None

    def __init__(
        self,
        path: pathlib.Path | str,
        hashing_algorithm: str = "sha3_512",
        hashing_block_size: int = 65536,
    ):
        self.path = path
        self.directory = False
        self.hashing_algorithm: str = hashing_algorithm
        self.hashing_block_size: int = hashing_block_size
        self.__hash: str | None = None

    @property
    def path(self) -> pathlib.Path:
        return self._path

    @path.setter
    def path(self, path: pathlib.Path | str):
        if isinstance(path, str):
            if path[-1] == "/":
                self.directory = True
            self.path = pathlib.Path(path)
        else:
            self._path = path

    @property
    def hash(self) -> str:
        if not self.__hash:
            self.__hash = Resource.calculate_hash(
                self.path,
                self.hashing_algorithm,
                self.hashing_block_size,
            )
        return self.__hash

    @staticmethod
    def calculate_hash(
        path: pathlib.Path | str,
        hashing_algorithm: str = "sha3_512",
        hashing_block_size: int = 65536,
    ):
        hasher = hashlib.new(hashing_algorithm)
        if isinstance(path, str):
            path = pathlib.Path(path)
        if not path.exists() or not path.is_file():
            return ""

        with open(path, "rb") as fd:
            buffer = fd.read(hashing_block_size)
            while len(buffer) > 0:
                buffer = fd.read(hashing_block_size)
                hasher.update(buffer)
        return hasher.hexdigest()
