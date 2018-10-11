"""User sourced plugins."""
import sys
import os.path as _osp
from .machinery import plugin_manager as _ep, _load as _l, _config as _c


class NapariPluginImporter:
    """MetaPathFinder for Napari plugin imports."""
    @classmethod
    def find_spec(cls, fullname, path=None, target=None):
        if not fullname.startswith(_l.get_plugin_namespace('')):
            return None

        for install_spec in _ep.install_specs:
            napari_spec = _c.napari_spec_from_install_spec(install_spec)
            package_spec = _c.package_spec_from_napari_spec(napari_spec)

            plugin_name = package_spec['plugin_name']
            base_namespace = _l.get_plugin_namespace(plugin_name)

            if not fullname.startswith(base_namespace):
                continue

            base_path = _osp.join(_c.entry_points.plugins_path,
                                  _c.get_abs_plugin_path(install_spec))

            path = package_spec.get('path')
            if path:
                if fullname != base_namespace:
                    continue
                path = _c.normalize_crossplatform_path(path)
                return _l.get_plugin_spec(plugin_name,
                                          _osp.join(base_path, path))

            paths = package_spec['paths']

            if fullname == base_namespace:
                return _l.make_namespace_spec(plugin_name)

            for _path in paths:
                path = _c.normalize_crossplatform_path(_path)
                module_name = _l.module_name_from_filepath(path)
                module_name = plugin_name + '.' + module_name

                if fullname == _l.get_plugin_namespace(module_name):
                    return _l.get_plugin_spec(module_name,
                                              _osp.join(base_path, path))


sys.meta_path.append(NapariPluginImporter)
del sys
