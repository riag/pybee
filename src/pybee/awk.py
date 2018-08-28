# -*- coding: utf-8 -*-

import os
import io

from functional import seq

import pybee

def create_file_seq(fpath, encoding='UTF-8', fs=' '):
    lines = pybee.path.read_lines_with_encoding(fpath, encoding)
    file_seq = seq(lines)
    return file_seq.enumerate().map(lambda x: (x[0], x[1].split(fs)))

def create_str_seq(text, fs=' '):
    f = io.StringIO(text)
    file_seq = seq(f.readlines())
    f.close()
    return file_seq.enumerate().map(lambda x: (x[0], x[1].split(fs)))
