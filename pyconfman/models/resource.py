"""
everything about filesystem resources
"""
from __future__ import annotations

import abc
import hashlib
import pathlib

from pyconfman.models.model import Model


class Resource(Model):
    """
    class representing a resource. A resource can be a file or a directory.
    """

    __metaclass__ = abc.ABCMeta
    _path: pathlib.Path | None = None

    def __init__(
        self,
        path: pathlib.Path | str,
        hashing_algorithm: str = "sha3_512",
        hashing_block_size: int = 65536,
    ):
        """
        create a resource
        :param path: resource's path
        :param hashing_algorithm: the hashing algorith to use to create a hash over the
               resource to check whether the resource has changed
        :param hashing_block_size: the blocksize for the hashig algorithm
        """
        super().__init__()
        self.path = path  # type: ignore
        self.directory = False
        self.hashing_algorithm: str = hashing_algorithm
        self.hashing_block_size: int = hashing_block_size
        self.__hash: str | None = None

    @property
    def path(self) -> pathlib.Path | None:
        """
        path getter
        :return: the resources path
        """
        return self._path

    @path.setter
    def path(self, path: pathlib.Path | str):
        """
        path setter
        :param path: the path to set the resources path to
        """
        if isinstance(path, str):
            if path[-1] == "/":
                self.directory = True
            self.path = pathlib.Path(path)
        else:
            self._path = path

    @property
    def hash(self) -> str:
        """
        get the hash of a resource
        :return: the resource's hash
        """
        if not self.__hash:
            if self.path is None:
                return ""
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
    ) -> str:
        """
        calculate a resources hash
        :param path: the resource's path
        :param hashing_algorithm: ashing_algorithm: the hashing algorith to use to
               create a hash over the resource to check whether the resource has changed
        :param hashing_block_size:
        :return: the calculated hash
        """
        hasher = hashlib.new(hashing_algorithm)
        if isinstance(path, str):
            path = pathlib.Path(path)
        if not path.exists() or not path.is_file():
            return ""

        with open(path, "rb") as file_descriptor:
            buffer = file_descriptor.read(hashing_block_size)
            while len(buffer) > 0:
                buffer = file_descriptor.read(hashing_block_size)
                hasher.update(buffer)
        return hasher.hexdigest()
