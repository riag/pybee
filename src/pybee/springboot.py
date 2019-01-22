# -*- coding: utf-8 -*-

import re
import pybee


def make_systemd_script(
        desc='', depend=[],
        start_cmd='', stop_cmd=None,
        reload_cmd=None,
        user=None, group=None,
        cwd=None,
        restart_sec='42s'
        ):
    '''
    生成 systemd 的启动脚本内容
    '''
    text_list = ['[Unit]']
    text_list.append('Description=%s' % desc)
    if depend:
        text_list.append('After=%s' % ' '.join(depend))

    text_list.append('')
    text_list.append('[Install]')
    text_list.append('WantedBy=multi-user.target')
    text_list.append('')

    text_list.append('[Service]')
    if user:
        text_list.append('User=%s' % user)
    if group:
        text_list.append('Group=%s' % group)

    text_list.append('ExecStart=%s' % start_cmd)
    if stop_cmd:
        text_list.append('ExecStop=%s' % stop_cmd)

    if reload_cmd:
        text_list.append('ExecReload=%s' % reload_cmd)

    if cwd:
        text_list.append('WorkingDirectory=%s' % cwd)

    text_list.append('SuccessExitStatus=143')
    text_list.append('KillMode=process')
    text_list.append('Restart=on-failure')
    text_list.append('RestartSec=%s' % restart_sec)

    return '\n'.join(text_list)


sv_port_pattern = re.compile(r'\s*(server.port)\s*=\s*\d+')
mgr_port_pattern = re.compile(r'\s*(management.server.port)\s*=\s*\d+')
livereload_port_pattern = re.compile(
    r'\s*(spring.devtools.livereload.port)\s*=\s*\d+'
    )


def change_port(
        config_file,
        sv_port=None, mgr_port=None,
        livereload_port=None, back_suffix='back'):

    replace_pattern_list = []
    if sv_port:
        replace_pattern_list.append(
            (sv_port_pattern, r'\g<1> = %d' % sv_port)
            )
    if mgr_port:
        replace_pattern_list.append(
            (mgr_port_pattern, r'\g<1> = %d' % mgr_port)
            )
    if livereload_port:
        replace_pattern_list.append(
                (livereload_port_pattern, r'\g<1> = %d' % livereload_port)
            )

    pybee.sed.replace_by_pattern_list(
            config_file,
            replace_pattern_list,
            back_suffix=back_suffix
            )
