# -*- coding: utf-8 -*-

# linux 下 iptables 的常见更新配置的操作

import re
from string import Template

import pybee

reject_pattern = re.compile(
            '\s+'.join([
            '-A', 'INPUT', '-j' ,'REJECT', '--reject-with', 'icmp-host-prohibited'
            ])
        )

port_pattern_list = [
            '-A', 'INPUT', '-m', 'state', '--state', 'NEW',
            '-m', '$pro', '-p', '$pro', '--dport', '$port',
            '-j', 'ACCEPT'
            ]
port_pattern_tpl =  '\s+'.join(port_pattern_list)        
port_text_tpl = ' '.join(port_pattern_list)

def check_by_pattern(fpath, pattern):
    match = pybee.sed.find_by_pattern(fpath,
            pattern
            )
    if match: return True

    return False

def check_or_add_by_pattern(fpath, search_pattern, insert_text, back_suffix='back'):
    '''
 根据 search pattern 来检查是否已存在
 存在，就返回 False
 不存在，就把 insert_text 插入到 fpath 文件里的 reject_pattern 之前
 然后返回 True
 返回值表示是否有插入数据
    '''
    
    match = pybee.sed.find_by_pattern(fpath, 
            search_pattern
            )
    if match: return False

    pybee.sed.insert_text_by_pattern(fpath, 
            reject_pattern, insert_text, False,
            back_suffix = back_suffix
            )
    return True


def remove_by_pattern(fpath, pattern):
    pybee.sed.delete_by_pattern(
            fpath, pattern
            )

def add_port(fpath, pro, port):
    m = {
            'pro': pro,
            'port': '%d' % port
            }
    t = Template(port_text_tpl)
    s = t.substitute(m)

    t = Template(port_pattern_tpl)
    pattern = t.substitute(m)

    check_or_add_by_pattern(
            fpath, pattern, s
            )
    

def remove_port(fpath, pro, port):
    
    m = {
            'pro': pro,
            'port': '%d' % port
            }
    t = Template(port_pattern_tpl)
    pattern = t.substitute(m)

    print(pattern)
    remove_by_pattern(fpath, pattern)

