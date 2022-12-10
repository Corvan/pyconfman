"""
everything about playbooks, playbooks are the pieces that define with modules are to be run
"""
import importlib


def run(name: str, inventory):
    """
    run a playbook by its name
    :param name: the playbook's name
    :param inventory: the inventory to use the playbook on
    """
    playbook = importlib.import_module(name)
    playbook.run(inventory)
