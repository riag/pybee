# -*- coding: utf-8 -*-

import subprocess
from subprocess import PIPE
import sys
import logging

logger = logging.getLogger(__file__)


def exec(args, shell=False, check=True, cwd=None, **kwargs):
    '''
       直接调用命令
    '''
    if sys.version_info >= (3, 5, 0):
        return subprocess.run(
            args, shell=shell, check=check, cwd=cwd,
            **kwargs
        ).returncode
    else:
        if check:
            return subprocess.check_call(
                args, shell=shell, cwd=cwd, **kwargs
            )
        else:
            return subprocess.call(
                args, shell=shell, cwd=cwd, **kwargs
                )


def call(
        args, shell=False, check=True, cwd=None,
        encoding=sys.stdout.encoding, **kwargs):
    '''
    调用命令行工具，获取 stdin 和 stderr 的输出
    使用 encoding 编码解码，返回 string 数据
    这个接口改为使用 get_output
    '''
    kwargs.pop('stdout', None)
    kwargs.pop('stderr', None)
    if sys.version_info >= (3, 5, 0):
        m = subprocess.run(
            args, shell=shell,
            check=check, stdout=PIPE, stderr=PIPE,
            cwd=cwd, **kwargs
            ).stdout
    else:
        kwargs['shell'] = shell
        kwargs['cwd'] = cwd
        kwargs['stdout'] = PIPE
        kwargs['stderr'] = PIPE
        timeout = kwargs.get('timeout', None)
        input = kwargs.get('input', None)
        with subprocess.Popen(args, **kwargs) as p:
            try:
                stdout, stderr = p.communicate(input, timeout=timeout)
                m = stdout
            except subprocess.TimeoutExpired:
                p.kill()
                stdout, stderr = p.communicate()
                raise subprocess.TimeoutExpired(p.args, timeout)
            except Exception:
                p.kill()
                p.wait()
                raise

        retcode = p.poll()
        if check and retcode:
            raise subprocess.CalledProcessError(retcode, p.args)

    return m.decode(encoding).rstrip('\n')


def get_output(
        args, shell=False, check=True, cwd=None,
        encoding=sys.stdout.encoding, **kwargs):
    '''
    调用命令行工具，获取 stdin 和 stderr 的输出
    使用 encoding 编码解码，返回 string 数据
    '''
    kwargs.pop('stdout', None)
    kwargs.pop('stderr', None)
    if sys.version_info >= (3, 5, 0):
        m = subprocess.run(
            args, shell=shell,
            check=check, stdout=PIPE, stderr=PIPE,
            cwd=cwd, **kwargs
            ).stdout
    else:
        kwargs['shell'] = shell
        kwargs['cwd'] = cwd
        kwargs['stdout'] = PIPE
        kwargs['stderr'] = PIPE
        timeout = kwargs.get('timeout', None)
        input = kwargs.get('input', None)
        with subprocess.Popen(args, **kwargs) as p:
            try:
                stdout, stderr = p.communicate(input, timeout=timeout)
                m = stdout
            except subprocess.TimeoutExpired:
                p.kill()
                stdout, stderr = p.communicate()
                raise subprocess.TimeoutExpired(p.args, timeout)
            except Exception:
                p.kill()
                p.wait()
                raise

        retcode = p.poll()
        if check and retcode:
            raise subprocess.CalledProcessError(retcode, p.args)

    return m.decode(encoding).rstrip('\n')


def pipe_call_shell_command(pipe_cmd_list):
    pre_stdout = subprocess.PIPE
    last_p = None
    for item in pipe_cmd_list:
        cmd = item[0]
        if len(item) > 1:
            kw = item[1]
        else:
            kw = {}
        assert isinstance(kw, dict)

        shell = False
        if isinstance(cmd, str):
            shell = True

        kw['stdin'] = pre_stdout
        kw['stdout'] = subprocess.PIPE
        kw['shell'] = shell
        p = subprocess.Popen(
            cmd, **kw
        )
        pre_stdout = p.stdout
        last_p = p

    last_p.wait()
