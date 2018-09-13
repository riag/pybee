# -*- coding: utf-8 -*-

import io

import pybee

def check_or_add_hosts(fpath, ip, domain, *arg):
    
    l = [ip, domain]
    if arg:
        l.extend(*arg)
    pattern = '\s+'.join(l)

    match = pybee.sed.find_by_pattern(fpath, pattern)
    if match: return False

    with io.open(fpath, 'a', encoding='UTF-8') as f:
        f.write("")
        f.write(' '.join(l))

    return True


def remove_hosts(fpath, ip, domain, *arg):
    l = [ip, domain]
    if arg:
        l.extend(*arg)
    pattern = '\s+'.join(l)
    pybee.sed.delete_by_pattern(fpath, pattern)

def remove_hosts_by_ip(fpath, ip):
    pattern = '%s\s+.*' % ip
    pybee.sed.delete_by_pattern(fpath, pattern)


def disable_selinux(fpath):

    match = pybee.sed.find_by_pattern(fpath,
            'SELINUX\s*=\s*(.*)'
            )
    selinux = match.group(1)
    if selinux == 'disabled': return False

    pybee.sed.replace_by_pattern(fpath,
            '(SELINUX)\s*=\s*.*',
            '\g<1>=disabled'
            )
    return True
