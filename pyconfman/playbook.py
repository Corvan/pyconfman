import importlib


def run(name: str, inventory):
    playbook = importlib.import_module(name)
    playbook.run(inventory)
