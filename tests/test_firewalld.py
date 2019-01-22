# -*- coding: utf-8 -*-

import os
import io
import pytest

import pybee


@pytest.fixture
def firewalld_service_file():
    p = './tmp/firewalld'
    pybee.path.mkdir(p)
    p = os.path.join(p, 'firewalld-service')
    with io.open(p, 'w') as f:
        f.write("")
    return p


def test_add_service_file(firewalld_service_file):
    pybee.firewalld.add_service_file(
            firewalld_service_file,
            'tcp', '80', 'http',
            'HTTP is the protocol used to serve Web pages.'
            )
    s = pybee.path.read_text_file(firewalld_service_file)
    assert len(s) != 0
