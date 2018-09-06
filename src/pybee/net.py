# -*- coding: utf-8 -*-

import psutil


def net_connections():
    return psutil.net_connections()

def get_in_use_ports():
    sconns = net_connections()
    port_list = []
    for s in sconns:
        p = s.laddr.port
        if p in port_list: continue
        port_list.append(p)

    return port_list

def get_in_use_port_infos():
    sconns = net_connections()
    port_map = {}
    for s in sconns:
        p = s.laddr.port
        if p in port_map: continue
        port_map[p] = s

    return port_map

