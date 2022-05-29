=====
pyconfman - Python Configuration Management
=====
About
--------
Pure Python configuration management.
While having worked for several years with Ansible, There where some things I did not like so much, like the combination of the following tools:

- Python
- YAML
- Jinja

Every one of them has got a different kind of Syntax, for example booleans:

- Python: True/False
- Jinja: true/false
- YAML: yes/no

Additionally, while idempotency a high goal, subjecting everything to it often can lead to problems.
But this is by far not meant to roast Ansible.
It is rather the attempt to do things differently.

Motivation
---------
Everything should be written in pure Python and offer Python objects to be used in Python scripts.
The scripts are meant to be declarative, but with a clear and easy way of using Python's syntax to do one task at a time and per line or block of code.

Getting Started
---------------
The only thing existing yet is a function to copy files locally.
Have a look at `copy.py <https://github.com/Corvan/pyconfman/blob/main/pyconfman/modules/copy/src/module.py>`_ or how it is used in its `tests <https://github.com/Corvan/pyconfman/blob/main/pyconfman/modules/copy/tests/test_copy.py>`_