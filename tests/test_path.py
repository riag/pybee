# -*- coding: utf-8 -*-

import pybee

def test_mkdir():
    p = './tmp/test'
    pybee.path.mkdir(p, True)
    pybee.path.mkdir(p, True)


def test_copytree():
    p_list = ['./tmp/test/test1', './tmp/test/test2']
    for p in p_list:
        pybee.path.mkdir(p, True)

    pybee.path.copytree('./tmp/test', './tmp/test_copy')
    pybee.path.copytree('./tmp/test', './tmp/test_copy')
