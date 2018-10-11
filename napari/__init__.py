from ._version import get_versions
__version__ = get_versions()['version']
del get_versions


try:
    __IPYTHON__
    from .plugins.machinery import plugin_manager as _pm
    _pm.setup()
    _pm.activate()
except NameError:
    pass
