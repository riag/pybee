# -*- coding: utf-8 -*-

# centos 7 改为使用 firewalld  模块来做防火墙
# 该模块就是提供相关函数 firewalld
# firewalld 主页 https://firewalld.org/
# 或者这里可以查看相关文档 https://fedoraproject.org/wiki/FirewallD/zh-cn

from string import Template
import io

import pybee

service_file_tpl = '''<?xml version="1.0" encoding="utf-8"?>
<service>
  <short>$short_desc</short>
  <description>$desc</description>
  <port protocol="$pro" port="$port"/>
</service>
'''


def add_service_file(fpath, pro, port, short_desc, desc):
    '''
    添加或者替换原有的 service 文件
    CentOS 7 下的路径是 /usr/lib/firewalld/services/
    文档格式可以使用 man firewalld.service 来查看格式
    或者 https://firewalld.org/documentation/service/options.html
    '''
    m = {
            'short_desc': short_desc,
            'pro': pro,
            'port': port,
            'desc': desc
            }
    t = Template(service_file_tpl)
    s = t.substitute(m)

    with io.open(fpath, 'w', encoding='UTF-8') as f:
        f.write(s)


def enable_service(svr_name, zone='public'):

    cmd_list = ['firewall-cmd', '--permanent', '--zone=%s' % zone]
    cmd_list.append('--add-service=%s' % svr_name)

    pybee.shell.exec(cmd_list)


def disable_service(svr_name, zone='public'):

    cmd_list = ['firewall-cmd', '--permanent', '--zone=%' % zone]
    cmd_list.append('--remove-service=%s' % svr_name)

    pybee.shell.exec(cmd_list)


def add_port(pro, port, zone='public'):
    cmd_list = ['firewall-cmd', '--permanent', '--zone=%' % zone]
    cmd_list.append('--add-port=%d/%s' % (port, pro))

    pybee.shell.exec(cmd_list)


def remove_port(pro, port, zone='public'):
    cmd_list = ['firewall-cmd', '--permanent', '--zone=%' % zone]
    cmd_list.append('--remove-port=%d/%s' % (port, pro))

    pybee.shell.exec(cmd_list)

    
def reload():
    pybee.shell.exec(
            ['firewall-cmd', '--reload']
            )
