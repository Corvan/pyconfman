from __future__ import annotations
import importlib
import types

from dataclasses import dataclass
from typing import Union


@dataclass(init=True)
class Host:
    name: str
    ip: str = "0.0.0.0"

    def __hash__(self):
        return self.name.__hash__()


class Group(set):

    name: str

    def __init__(self, name, elements: set[Union[Group, Host]]):
        self.name = name
        super().__init__(elements)

    def hosts(self):
        hosts = set()
        for element in self:
            if isinstance(element, Host):
                hosts.add(element)
            else:
                hosts.update(element.hosts())
        return hosts

    def __hash__(self):
        return sum(element.__hash__() for element in self)


def filter_module_dict(module: types.ModuleType):
    return {
        key: value
        for key, value in module.__dict__.items()
        if not any(
            (
                key.startswith("__") and key.endswith("__"),  # builtins
                isinstance(value, type),  # classes
                isinstance(value, types.ModuleType),  # modules
            )
        )
    }


def import_module(name: str) -> dict[str, Group | Host]:

    module = importlib.import_module(name)
    return filter_module_dict(module)
