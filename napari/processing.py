"""
Processing registry and control hub.
"""
from napari.core.registry import FuncInfoRegistry


processing_registry = FuncInfoRegistry('Processing')
register = processing_registry.register

del FuncInfoRegistry
