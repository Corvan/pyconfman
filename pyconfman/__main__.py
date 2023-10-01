"""
main module of pyconftest
made to be run like `python -m pyconftest`
"""
from pathlib import Path
from pyconfman.models.inventory import Inventory
import pyconfman.models.playbook

try:
    import tomllib as toml  # type: ignore
except (ImportError, ModuleNotFoundError):
    import tomli as toml  # type: ignore


if __name__ in ("__main__", "pyconfman.__main__"):
    config = {}
    config_path = Path("config.toml")
    if config_path.exists():
        with open(config_path, "rb") as fd:
            config = toml.load(fd)["pyconfman"]["main"]
    config.setdefault("inventory", "inventory")
    config.setdefault("playbook", "playbook")
    inventory = Inventory.import_module(config["inventory"])
    pyconfman.models.playbook.run(config["playbook"], inventory)
    if __name__ == "pyconfman.__main__":  # we are in the testing environment
        globals()["test"] = inventory
