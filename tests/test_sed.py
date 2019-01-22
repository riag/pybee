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
    assert match is not None
    assert match.group(1) == 'eth1'

    match = pybee.sed.find_by_pattern(p, 'HWADDR=(.*)')
    assert match is not None
    assert match.group(1) == '00:0C:29:B5:24:43'

    match = pybee.sed.find_by_pattern(p, 'UUID=(.*)')
    assert match is not None
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
    match_list = pybee.sed.find_by_pattern_list(
                p, pattern_list
            )
    assert match_list is not None

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

    pybee.sed.replace_by_pattern(
                p,
                r'(HOSTNAME)\s*=\s*.+', r'\g<1>=mytest'
            )
    match = pybee.sed.find_by_pattern(
                p, r'HOSTNAME\s*=\s*(.*)'
            )
    assert match is not None
    assert match.group(1) == 'mytest'


def test_insert_by_pattern():

    pybee.path.mkdir(test_dir, True)

    p = os.path.join(test_dir, 'insert')
    s = '''
*filter
:INPUT ACCEPT [0:0]
:FORWARD ACCEPT [0:0]
:OUTPUT ACCEPT [0:0]
-A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT
-A INPUT -p icmp -j ACCEPT
-A INPUT -i lo -j ACCEPT
-A INPUT -m state --state NEW -m tcp -p tcp --dport 22 -j ACCEPT
-A INPUT -j REJECT --reject-with icmp-host-prohibited
-A FORWARD -j REJECT --reject-with icmp-host-prohibited
    '''

    pybee.path.save_text_file(p, s)

    reject_list = [
        '-A', 'INPUT', '-j',  'REJECT',  '--reject-with', 'icmp-host-prohibited'
        ]
    insert_list = [
        '-A', 'INPUT', '-m', 'state', '--state', 'NEW',
        '-m', 'udp', '-p', 'udp', '--dport',  '694', '-j', 'ACCEPT'
            ]
    pybee.sed.insert_text_by_pattern(p,
            r'\s+'.join(reject_list), ' '.join(insert_list), False
            )
    match = pybee.sed.find_by_pattern(p,
            r'\s+'.join(insert_list)
            )
    assert match is not None
