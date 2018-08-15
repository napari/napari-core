"""
Provides functionality for defining and registering States.

States are the main objects that Napari passes around.
"""
from ._class import State, DynamicState
from ._register import state_registry, register_state
from .types import IncompatibilityError


__all__ = ['DynamicState',
           'IncompatibilityError',
           'register_state',
           'State',
           'state_registry']
