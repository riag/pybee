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
	if sys.version_info >=(3,5,0):
		return subprocess.run(args,shell=shell, check=check, cwd=cwd, **kwargs)
	else:
		if check:
			return subprocess.check_call(args, shell=shell, cwd=cwd, **kwargs)
		else:
			return subprocess.call(args, shell=shell, cwd=cwd,**kwargs)

def call(args, shell=False, check=True, cwd=None, encoding=sys.stdout.encoding, **kwargs):
	'''
		调用命令行工具，获取 stdin 和 stderr 的输出
		使用 encoding 编码解码，返回 string 数据
	'''
	kwargs.pop('stdout', None)
	kwargs.pop('stderr', None)
	m = subprocess.run(args,shell=shell, \
		check=check, stdout=PIPE, stderr=PIPE, cwd=cwd, **kwargs).stdout
	return m.decode(encoding).rstrip('\n')
