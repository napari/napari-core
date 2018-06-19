"""Handles plugin configuration."""
import os.path as osp

from .._internal import paths


plugins_path = paths.create_config_path('plugins')
plugins_index = osp.join(plugins_path, 'index.yml')
