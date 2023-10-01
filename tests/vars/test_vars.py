import importlib
import os
from ipaddress import ip_interface

import pytest
from pyconfman.models.inventory import Group
import shutil
import subprocess

import deepdiff

from tests.vars.vars_inventory import TestHost


@pytest.mark.integration
def test_run_vars_module():
    module = importlib.import_module("pyconfman.__main__")
    glob = {"test": "test"}
    loc = {"test": "test"}
    assert exec(open(module.__file__).read(), glob, loc) is None
    actual: dict = module.test
    expected = {
        "host1": TestHost(
            name="host1.example.com", ip_interface=ip_interface("0.0.0.0/32")
        ),
        "host2": TestHost(
            name="host2.example.com", ip_interface=ip_interface("fd01:0:0:1::1/64")
        ),
        "group1": Group(
            "group1",
            {
                TestHost(
                    name="host1.example.com",
                    ip_interface=ip_interface("0.0.0.0/32"),
                ),
                TestHost(
                    name="host2.example.com",
                    ip_interface=ip_interface("fd01:0:0:1::1/64"),
                ),
            },
        ),
        "group2": Group(
            "group2",
            {
                TestHost(
                    name="host1.example.com",
                    ip_interface=ip_interface("0.0.0.0/32"),
                ),
                Group(
                    "group1",
                    {
                        TestHost(
                            name="host1.example.com",
                            ip_interface=ip_interface("0.0.0.0/32"),
                        ),
                        TestHost(
                            name="host2.example.com",
                            ip_interface=ip_interface("fd01:0:0:1::1/64"),
                        ),
                    },
                ),
            },
        ),
        "host3": TestHost(name="Test", ip_interface=None),
    }
    assert deepdiff.DeepDiff(
        actual, expected, ignore_order=True, report_repetition=True
    )


@pytest.mark.integration
def test_run_vars_from_commandline():
    poetry_path = shutil.which("poetry")
    poetry_process = subprocess.run(
        f"{poetry_path} env info -p",
        shell=True,
        stdout=subprocess.PIPE,
        check=True,
    )
    python_process = subprocess.run(
        f"{poetry_process.stdout.decode().strip()}/bin/python -m pyconfman",
        cwd=f"{os.getcwd()}/tests/vars",
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True,
    )
    assert python_process.stderr.decode().strip() == ""
    assert python_process.stdout.decode().strip() == "host1.example.com"
