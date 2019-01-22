# -*- coding: utf-8 -*-

import pytest
import io
import os

import pybee


@pytest.fixture
def network_file():
    p = './tmp/network'
    pybee.path.mkdir(p)
    p = os.path.join(p, 'hosts')
    with io.open(p, 'w') as f:
        f.write("")
    return p


selinux_text = '''
# This file controls the state of SELinux on the system.
# SELINUX= can take one of these three values:
#     enforcing - SELinux security policy is enforced.
#     permissive - SELinux prints warnings instead of enforcing.
#     disabled - No SELinux policy is loaded.
SELINUX=enforcing
# SELINUXTYPE= can take one of three two values:
#     targeted - Targeted processes are protected,
#     minimum - Modification of targeted policy. Only selected processes are protected.
#     mls - Multi Level Security protection.
SELINUXTYPE=targeted
'''


@pytest.fixture
def selinux_file():

    p = './tmp/network'
    pybee.path.mkdir(p)
    p = os.path.join(p, 'selinux')
    with io.open(p, 'w') as f:
        f.write(selinux_text)
    return p


def test_add_hosts(network_file):
    ip = '192.168.0.5'
    domain = 'node1.pybee.com'
    domain2 = 'node2.pybee.com'
    result = pybee.network.check_or_add_hosts(
            network_file, ip,
            domain, domain2
            )
    assert result
    result = pybee.network.check_or_add_hosts(
            network_file, ip,
            domain, domain2
            )
    assert not result


def test_remove_hosts(network_file):

    ip = '192.168.0.10'
    domain = 'node5.pybee.com'
    domain2 = 'node6.pybee.com'

    domain3 = 'node10.pybee.com'
    domain4 = 'node11.pybee.com'
    result = pybee.network.check_or_add_hosts(
            network_file, ip,
            domain, domain2
            )
    assert result

    result = pybee.network.check_or_add_hosts(
            network_file, ip,
            domain3, domain4
            )
    assert result

    pybee.network.remove_hosts(
            network_file, ip,
            domain, domain2)

    result = pybee.network.check_or_add_hosts(
            network_file, ip,
            domain, domain2
            )
    assert result

    pybee.network.remove_hosts_by_ip(
            network_file, ip
            )
    s = pybee.path.read_text_file(network_file).strip()
    assert len(s) == 0


def test_disable_selinux(selinux_file):
    result = pybee.network.disable_selinux(
            selinux_file
            )
    assert result

    result = pybee.network.disable_selinux(
            selinux_file
            )
    assert result is False
