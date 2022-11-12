from pathlib import Path
from pyconfman.inventory import Inventory
import pyconfman.playbook

try:
    import tomllib as toml
except (ImportError, ModuleNotFoundError):
    import tomli as toml

config: dict
config_path = Path("config.toml")

if __name__ == "__main__":
    if config_path.exists():
        with open("config.toml", "rb") as fd:
            config = toml.load(fd)["pyconfman"]["main"]
    config.setdefault("inventory", "inventory")
    config.setdefault("playbook", "playbook")
    inventory = Inventory.import_module(config["inventory"])
    pyconfman.playbook.run(config["playbook"], inventory)
