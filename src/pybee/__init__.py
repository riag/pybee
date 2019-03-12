# -*- coding: utf-8 -*-

from pybee import path
from pybee import compress
from pybee import shell
from pybee import download
from pybee import sed
from pybee import awk
from pybee import git
from pybee import pip
from pybee import importutil
from pybee import netstat
from pybee import springboot
from pybee import iptables
from pybee import network
from pybee import ask
from pybee import datetime

import sys
import io

if sys.platform.startswith('win32'):
    pass
else:
    from pybee import firewalld
    from pybee import user

net = netstat

__version__ = '0.2.2'


get_date_time = datetime.to_str


def get_curr_date_time(fmt='%Y-%m-%d %H:%M:%S'):
    d = datetime.now()
    return get_date_time(d, fmt)


def source(filepath, globals=None, locals=None):
    with io.open(filepath, 'r', encoding='utf-8') as f:
        exec(f.read(), globals, locals)


def source_str(s, globals=None, locals=None):
    exec(s, globals, locals)
