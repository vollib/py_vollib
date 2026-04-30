# -*- coding: utf-8 -*-
"""Compatibility namespace for the historical ``py_vollib`` import path.

The canonical package name is now ``vollib``.  This module keeps existing
``py_vollib.*`` imports working during the transition.
"""

from importlib import import_module
import pkgutil
import sys
import warnings

import vollib as _vollib


warnings.warn(
    "py_vollib is deprecated and will be removed in a future release; "
    "please import from vollib instead.",
    DeprecationWarning,
    stacklevel=2,
)

__path__ = _vollib.__path__
__doc__ = _vollib.__doc__


def _alias_vollib_modules():
    prefix = _vollib.__name__ + "."
    for module_info in pkgutil.walk_packages(_vollib.__path__, prefix):
        module = import_module(module_info.name)
        compat_name = __name__ + module_info.name[len(_vollib.__name__) :]
        sys.modules[compat_name] = module


_alias_vollib_modules()

for _name, _value in _vollib.__dict__.items():
    if _name not in {"__name__", "__package__", "__path__", "__spec__"}:
        globals()[_name] = _value
