"""
module for the base of all provided concepts
"""
from __future__ import annotations

import abc


class Model(abc.ABC):
    """
    Abstract Base Class representing the base for all provided concepts
    """

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        super().__init__()
