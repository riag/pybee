# -*- coding: utf-8 -*-

import os
import io
import contextlib
import shutil
from shutil import copy2, copystat, Error

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

def read_first_line_from_file(path, encoding='UTF-8'):
    with io.open(path, 'r',encoding=encoding) as f:
        while True:
            line = f.readline()
            if not line: return None
            line = line.strip()
            if not line: continue
            return line

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

# 如果目标目录已经存在了，就不再创建目录
# 可以覆盖复制
def copytree(src, dst, symlinks=False, ignore=None, copy_function=copy2,
             ignore_dangling_symlinks=False):
    """Recursively copy a directory tree.

    The destination directory must not already exist.
    If exception(s) occur, an Error is raised with a list of reasons.

    If the optional symlinks flag is true, symbolic links in the
    source tree result in symbolic links in the destination tree; if
    it is false, the contents of the files pointed to by symbolic
    links are copied. If the file pointed by the symlink doesn't
    exist, an exception will be added in the list of errors raised in
    an Error exception at the end of the copy process.

    You can set the optional ignore_dangling_symlinks flag to true if you
    want to silence this exception. Notice that this has no effect on
    platforms that don't support os.symlink.

    The optional ignore argument is a callable. If given, it
    is called with the `src` parameter, which is the directory
    being visited by copytree(), and `names` which is the list of
    `src` contents, as returned by os.listdir():

        callable(src, names) -> ignored_names

    Since copytree() is called recursively, the callable will be
    called once for each directory that is copied. It returns a
    list of names relative to the `src` directory that should
    not be copied.

    The optional copy_function argument is a callable that will be used
    to copy each file. It will be called with the source path and the
    destination path as arguments. By default, copy2() is used, but any
    function that supports the same signature (like copy()) can be used.

    """
    names = os.listdir(src)
    if ignore is not None:
        ignored_names = ignore(src, names)
    else:
        ignored_names = set()

    mkdir(dst)
    errors = []
    for name in names:
        if name in ignored_names:
            continue
        srcname = os.path.join(src, name)
        dstname = os.path.join(dst, name)
        try:
            if os.path.islink(srcname):
                linkto = os.readlink(srcname)
                if symlinks:
                    # We can't just leave it to `copy_function` because legacy
                    # code with a custom `copy_function` may rely on copytree
                    # doing the right thing.
                    os.symlink(linkto, dstname)
                    copystat(srcname, dstname, follow_symlinks=not symlinks)
                else:
                    # ignore dangling symlink if the flag is on
                    if not os.path.exists(linkto) and ignore_dangling_symlinks:
                        continue
                    # otherwise let the copy occurs. copy2 will raise an error
                    if os.path.isdir(srcname):
                        copytree(srcname, dstname, symlinks, ignore,
                                 copy_function)
                    else:
                        copy_function(srcname, dstname)
            elif os.path.isdir(srcname):
                copytree(srcname, dstname, symlinks, ignore, copy_function)
            else:
                # Will raise a SpecialFileError for unsupported file types
                copy_function(srcname, dstname)
        # catch the Error from the recursive copytree so that we can
        # continue with other files
        except Error as err:
            errors.extend(err.args[0])
        except OSError as why:
            errors.append((srcname, dstname, str(why)))
    try:
        copystat(src, dst)
    except OSError as why:
        # Copying file access times may fail on Windows
        if getattr(why, 'winerror', None) is None:
            errors.append((src, dst, str(why)))
    if errors:
        raise Error(errors)
    return dst

@contextlib.contextmanager
def working_dir(path):
	prev_cwd = os.getcwd()
	os.chdir(path)
	try:
		yield
	finally:
		os.chdir(prev_cwd)
