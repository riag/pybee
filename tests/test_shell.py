# -*- coding: utf-8 -*-

import pybee


def test_get_output():
    m = pybee.shell.get_output(['echo', '"test"'])
    assert len(m) > 0


def test_exec():
    result = pybee.shell.exec(['echo', '"test"'])
    assert result == 0
