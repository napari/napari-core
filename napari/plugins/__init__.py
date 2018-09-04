"""User sourced plugins."""
import sys
import os.path as osp
from .machinery import plugin_manager, _load as _l, _config as _c


class NapariPluginImporter:
    """MetaPathFinder for Napari plugin imports."""
    @classmethod
    def find_spec(cls, fullname, path=None, target=None):
        if not fullname.startswith(_l.get_plugin_namespace('')):
            return None

        for install_spec in plugin_manager.install_specs:
            napari_spec = _c.napari_spec_from_install_spec(install_spec)
            package_spec = _c.package_spec_from_napari_spec(napari_spec)

            plugin_name = package_spec['plugin_name']
            base_namespace = _l.get_plugin_namespace(plugin_name)

            if not fullname.startswith(base_namespace):
                continue

            base_path = osp.join(_c.entry_points.plugins_path,
                                 _c.get_abs_plugin_path(install_spec))

            path = package_spec.get('path')
            if path:
                path = _c.normalize_crossplatform_path(path)
                return _l.get_plugin_spec(plugin_name,
                                          osp.join(base_path, path))

            paths = package_spec['paths']

            if fullname == base_namespace:
                return _l.make_namespace_spec(plugin_name)

            for _path in paths:
                path = _c.normalize_crossplatform_path(_path)
                module_name = osp.splitext(osp.basename(path))[0]
                module_name = plugin_name + '.' + module_name

                if fullname == _l.get_plugin_namespace(module_name):
                    return _l.get_plugin_spec(module_name,
                                              osp.join(base_path, path))


sys.meta_path.append(NapariPluginImporter)
