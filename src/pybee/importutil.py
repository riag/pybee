# -*- coding: utf-8 -*-

import importlib
from importlib import machinery
import sys
import types

def import_module_from_src(name, src_path):
    loader = machinery.SourceFileLoader(name, src_path)
    spec = importlib.util.spec_from_loader(loader.name, loader)
    if sys.version_info >=(3,5,0):
            mod = importlib.util.module_from_spec(spec)
    else:
            mod = types.ModuleType(loader.name)	
    mod.__file__ = src_path
    loader.exec_module(mod)
    return mod
