# -*- coding: utf-8 -*-

import pybee

def get_current_branch():
    return pybee.shell.call(
            ['git', 'rev-parse', '--abbrev-ref', 'HEAD']
            )

def get_last_commit_id(short=True):
    cmd_list = ['git', 'rev-parse']
    if short: cmd_list.append('--short')
    cmd_list.append('HEAD')
    return pybee.shell.call(cmd_list)

