# -*- coding: utf-8 -*-

import importlib
from importlib import machinery

def import_module_from_src(name, src_path):
    loader = machinery.SourceFileLoader(name, src_path)
    spec = importlib.util.spec_from_loader(loader.name, loader)
    mod = importlib.util.module_from_spec(spec)
    return loader.exec_module(mod)
