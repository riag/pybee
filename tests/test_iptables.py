# -*- coding: utf-8 -*-

import os
import pytest
import io
from string import Template

import pybee

iptables_txt = '''
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

def check_port(fpath, pro, port):
    
    m = {
            'pro': pro,
            'port': '%d' % port
            }
    t = Template(pybee.iptables.port_pattern_tpl)
    pattern = t.substitute(m)

    return pybee.iptables.check_by_pattern(
            fpath, pattern
            )


@pytest.fixture
def iptables_file():
    p = './tmp/iptables'
    pybee.path.mkdir(p)
    p = os.path.join(p, 'iptables.txt')
    with io.open(p, 'w') as f:
        f.write(iptables_txt)
    return p

def test_add_port(iptables_file):
    pro = 'tcp'
    port = 456
    pybee.iptables.add_port(
            iptables_file,
            pro, port
            )

    result = check_port(iptables_file, pro, port)
    assert result == True

def test_remove_port(iptables_file):
    
    pro = 'udp'
    port = 897
    pybee.iptables.add_port(
            iptables_file,
            pro, port
            )
    result = check_port(iptables_file, pro, port)
    assert result == True

    pybee.iptables.remove_port(
            iptables_file, pro, port
            )
    result = check_port(iptables_file, pro, port)
    assert result == False


