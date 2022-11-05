import pyconfman.inventory
import pyconfman.playbook

if __name__ == "__main__":
    inventory = pyconfman.inventory.import_module("inventory")
    pyconfman.playbook.run("playbook", inventory)
