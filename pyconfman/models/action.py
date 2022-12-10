"""
containing everything regarding actions
"""
import abc
from pyconfman.models.model import Model


class Action(Model):
    """
    Action class that is the Base class for all kinds of Actions
    """

    __metaclass__ = abc.ABCMeta

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
