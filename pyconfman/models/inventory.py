"""
Everything that makes up an inventory of hosts and groups of hosts.
The inventory is you central point to manage your stock.
"""
from __future__ import annotations
import importlib
import types

from dataclasses import dataclass
from typing import Union


@dataclass(init=True)
class Host:
    """
    Class representing a host this can be a physical box a VM or a container
    """

    name: str

    def __hash__(self):
        return self.name.__hash__()


class Group(set):
    """
    Class representing a group of hosts. Groups can be nested.
    """

    name: str

    def __init__(self, name, elements: set[Union[Group, Host]]):
        self.name = name
        super().__init__(elements)

    def hosts(self):
        """
        Unroll the group and its nested groups and hosts, into a flat listing of hosts.
        :return: all hosts that are in the group and nested groups.
        """
        hosts = set()
        for element in self:
            if isinstance(element, Host):
                hosts.add(element)
            else:
                hosts.update(element.hosts())
        return hosts

    def __hash__(self):
        return sum(element.__hash__() for element in self)


class Inventory(dict):
    """
    Class representing inventory of your stock: hosts and groups of hosts
    """

    name: str

    def __init__(self, name: str):
        self.name = name
        super().__init__(Inventory.import_module(name))

    @staticmethod
    def import_module(name: str) -> dict[str, Group | Host]:
        """
        Import an inventories module by its name to read its contents into the current
        interpreter
        :param name: the module's name
        :return: An Inventory in the style of a dictionary with
                 "hostname" | "groupname": Host | Group
        """
        module = importlib.import_module(name)
        return Inventory._filter_module_dict(module)

    @staticmethod
    def _filter_module_dict(module: types.ModuleType):
        """
        filter a module from its ModuleDict into a dict
        :param module: the imported module
        :return: filtered dict in the style of
                 "hostname" | "groupname": Host | Group
        """
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
