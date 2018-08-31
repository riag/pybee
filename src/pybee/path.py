# -*- coding: utf-8 -*-

import os
import io
import contextlib
import shutil

def get_work_path():
	'''
		获取当前工作路径
	'''
	return os.path.abspath(os.getcwd())

def get_script_path(script_path):
	'''
		获取脚本的路径
		用法 get_script_path(__file__)
	'''
	return os.path.abspath(os.path.dirname(script_path))

def read_file_with_encoding(path, encoding='UTF-8'):
	with io.open(path, 'r',encoding=encoding) as f:
	    return f.read()

def read_lines_with_encoding(path, encoding='UTF-8'):
    with io.open(path, 'r', encoding=encoding) as f:
        return f.readlines()

def write_file_with_encoding(path, text, encoding='UTF-8'):
	with io.open(path, 'w',encoding=encoding) as f:
		f.write(text)

def mkdir(path, recursive=False, **kwargs):
    if recursive:
        os.makedirs(path, exist_ok=True, **kwargs)
    else:
        if os.path.isdir(path): return
        os.mkdir(path, **kwargs)

# 这里只删除目录下的文件和目录
# 不删除根目录
def rmtree(path):
    p_list = os.listdir(path)
    for p in p_list:
        m = os.path.join(path, p)
        if os.path.isfile(m):
            os.unlink(m)	
        else:
            shutil.rmtree(m)

def copyfiles(src_list, dest_dir):
    if not os.path.isdir(dest_dir):
        raise OSError('Not a directory: %s' % dest_dir)
    for src in src_list:
        shutil.copy(src, dest_dir)

@contextlib.contextmanager
def working_dir(path):
	prev_cwd = os.getcwd()
	os.chdir(path)
	try:
		yield
	finally:
		os.chdir(prev_cwd)
