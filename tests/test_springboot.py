# -*- coding: utf-8 -*-

import pybee
import pytest
import re
import os


def test_systemd_script(capsys):
    s = pybee.springboot.make_systemd_script(
            desc='test start',
            depend=['syslog.target', 'network.target'],
            start_cmd='java -jar test.jar',
            stop_cmd='curl -X POST http://127.0.0.1:9000/shutdown',
            cwd='/opt'
            )
    with capsys.disabled():
        print("")
        print("systemd script content is: ")
        print(s)


def test_port_re(capsys):
    sv_port_re = r'\s*(server.port)\s*=\s*\d+'
    m = re.search(sv_port_re, 'server.port = 8080')
    assert m is not None

    s = re.sub(sv_port_re, r'\g<1> = 9000', 'server.port =8080')
    assert s == 'server.port = 9000'


def test_change_port(capsys):
    text = '''
        server.port = 8080
    '''
    path = './tmp/springboot/'
    pybee.path.mkdir(path, True)
    back_suffix = 'back'
    config_file = os.path.join(path, 'config')
    pybee.path.save_text_file(
            config_file, text
            )
    pybee.springboot.change_port(
            config_file, 9000
            )
    text = pybee.path.read_first_line_from_file(
            config_file
            )
    assert os.path.isfile(config_file + '.' + back_suffix)
    assert text == 'server.port = 9000'
