# -*- coding: utf-8 -*-

import os

import pybee

test_dir = './tmp/sed/'

def test_find_by_pattern():
    pybee.path.mkdir(test_dir, True)

    p = os.path.join(test_dir, 'net_dev')

    s = '''
DEVICE=eth1
HWADDR=00:0C:29:B5:24:43
TYPE=Ethernet
UUID=9837a1c3-6001-459d-95b3-ea04fe5ee9ab
ONBOOT=true
    '''

    pybee.path.save_text_file(p, s)
    match = pybee.sed.find_by_pattern(p, 'DEVICE=(.*)')
    assert match != None
    assert match.group(1) == 'eth1'

    match = pybee.sed.find_by_pattern(p, 'HWADDR=(.*)')
    assert match != None
    assert match.group(1) == '00:0C:29:B5:24:43'

    match = pybee.sed.find_by_pattern(p, 'UUID=(.*)')
    assert match != None
    assert match.group(1) == '9837a1c3-6001-459d-95b3-ea04fe5ee9ab'


def test_find_by_pattern_list():
    pybee.path.mkdir(test_dir, True)

    p = os.path.join(test_dir, 'net_dev')

    s = '''
DEVICE=eth1
HWADDR=00:0C:29:B5:24:43
TYPE=Ethernet
UUID=9837a1c3-6001-459d-95b3-ea04fe5ee9ab
ONBOOT=true
    '''

    pattern_list = (
            'DEVICE=(.*)', 
            'HWADDR=(.*)',
            'UUID=(.*)'
            )
    pybee.path.save_text_file(p, s)
    match_list = pybee.sed.find_by_pattern_list(p, 
            pattern_list
            )
    assert match_list != None

    assert match_list[0].group(1) == 'eth1' 
    assert match_list[1].group(1) == '00:0C:29:B5:24:43' 
    assert match_list[2].group(1) == '9837a1c3-6001-459d-95b3-ea04fe5ee9ab' 

def test_replace_by_pattern(capsys):
    
    pybee.path.mkdir(test_dir, True)

    p = os.path.join(test_dir, 'replace')
    s = '''
NETWORKING=yes
HOSTNAME=test
    '''
    pybee.path.save_text_file(p, s)

    pybee.sed.replace_by_pattern(p, 
            r'(HOSTNAME)\s*=\s*.+', '\g<1>=mytest'
            )
    match = pybee.sed.find_by_pattern(
            p, 'HOSTNAME\s*=\s*(.*)'
            )
    assert match != None
    assert match.group(1) == 'mytest'
