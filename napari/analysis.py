"""
Analysis registry and control hub.
"""
from napari.core.registry import FuncInfoRegistry


analysis_registry = FuncInfoRegistry('Analysis')
register = analysis_registry.register

del FuncInfoRegistry
