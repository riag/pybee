# -*- coding: utf-8 -*-

import pybee


def get_current_branch(cwd=None):
    return pybee.shell.call(
            ['git', 'rev-parse', '--abbrev-ref', 'HEAD'], cwd=cwd
            )


def get_last_commit_id(short=True, cwd=None):
    cmd_list = ['git', 'rev-parse']
    if short:
        cmd_list.append('--short')
    cmd_list.append('HEAD')
    return pybee.shell.call(cmd_list, cwd=cwd)
