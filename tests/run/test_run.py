import importlib
import os
from pyconfman.models.inventory import Host, Group
import shutil
import subprocess


def test_run_module():
    module = importlib.import_module("pyconfman.__main__")
    glob = {"test": "test"}
    loc = {"test": "test"}
    assert exec(open(module.__file__).read(), glob, loc) is None
    assert module.test == (
        {
            "host1": Host(name="host1.example.com", ip="0.0.0.0"),
            "host2": Host(name="host2.example.com", ip="1.2.3.4"),
            "group1": Group(
                "group1",
                {
                    Host(name="host1.example.com", ip="0.0.0.0"),
                    Host(name="host2.example.com", ip="1.2.3.4"),
                },
            ),
            "group2": Group(
                "group2",
                {
                    Host(name="host1.example.com", ip="0.0.0.0"),
                    Group(
                        "group1",
                        {
                            Host(name="host1.example.com", ip="0.0.0.0"),
                            Host(name="host2.example.com", ip="1.2.3.4"),
                        },
                    ),
                },
            ),
            "host3": Host(name="Test", ip="0.0.0.0"),
        }
    )


def test_run_from_commandline():
    poetry_path = shutil.which("poetry")
    poetry_process = subprocess.run(
        f"{poetry_path} env info -p",
        shell=True,
        stdout=subprocess.PIPE,
        check=True,
    )
    python_process = subprocess.run(
        f"{poetry_process.stdout.decode().strip()}/bin/python -m pyconfman",
        cwd=f"{os.getcwd()}/tests/run",
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True,
    )
    assert python_process.stderr.decode().strip() == ""
    assert python_process.stdout.decode().strip() == "host1.example.com"
