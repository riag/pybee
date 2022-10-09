# -*- coding: utf-8 -*-

import zipfile
import tarfile
import os
from datetime import datetime


def zip(zipname, pathname, path_prefix=None, filterfunc=None, password=None):
    with zipfile.ZipFile(zipname, 'w') as z:
        if password:
            z.setpassword(password)

        for root, dirs, files in os.walk(pathname):

            for name in sorted(dirs):
                p = os.path.join(root, name)
                if filterfunc and filterfunc(p):
                    print("ignore dir %s" % p)
                    continue

                fixp = p[len(pathname)+1:]
                if path_prefix:
                    fixp = path_prefix + '/' + fixp
                z.write(p, fixp)

            for f in files:
                p = os.path.join(root, f)
                if filterfunc and not filterfunc(p):
                    print("ignore file %s" % p)
                    continue

                fixp = p[len(pathname)+1:]
                if path_prefix:
                    fixp = path_prefix + '/' + fixp
                z.write(p, fixp)


def list_zip(zipname):
    with zipfile.ZipFile(zipname, 'r') as z:
        return z.infolist()


def print_zip(zipname):

    fmt = '%d-%d-%d %d:%d:%d'
    with zipfile.ZipFile(zipname, 'r') as z:
        print("Length\t\t Date     Time\t\t\tName")
        for m in z.infolist():
            s = fmt % m.date_time
            print("%d\t\t%s\t\t%s" % (m.file_size, s, m.filename))


def unzip(zipname, dest_dir, password=None):
    with zipfile.ZipFile(zipname, 'r') as z:
        z.extractall(dest_dir, pwd=password)


def tar_gz(tarname, pathname, path_prefix=None, filterfunc=None):
    with tarfile.open(tarname, 'w:gz') as t:

        for root, dirs, files in os.walk(pathname):
            for name in sorted(dirs):
                p = os.path.join(root, name)
                if filterfunc and filterfunc(p):
                    print('ignore dir %s' % p)
                    continue

                fixp = p[len(pathname)+1:]
                if path_prefix:
                    fixp = path_prefix + '/' + fixp
                info = tarfile.TarInfo(fixp)
                info.type = tarfile.DIRTYPE
                t.addfile(info)

            for f in files:
                p = os.path.join(root, f)
                if filterfunc and filterfunc(p):
                    print("ignore file %s" % p)
                    continue

                fixp = p[len(pathname)+1:]
                if path_prefix:
                    fixp = path_prefix + '/' + fixp
                t.add(p, fixp)


def print_tar(tarname):
    with tarfile.open(tarname) as t:
        fmt = '%d-%d-%d %d:%d:%d'
        info_list = t.getmembers()
        fmt = '%Y-%m-%d %H:%M:%S'
        for info in info_list:
            t = datetime.fromtimestamp(info.mtime)
            m = t.strftime(fmt)
            print("%d\t\t%s\t\t%s" % (info.size, m, info.name))


def untar(tarname, dest_dir):
    with tarfile.open(tarname) as t:
        def is_within_directory(directory, target):
            
            abs_directory = os.path.abspath(directory)
            abs_target = os.path.abspath(target)
        
            prefix = os.path.commonprefix([abs_directory, abs_target])
            
            return prefix == abs_directory
        
        def safe_extract(tar, path=".", members=None, *, numeric_owner=False):
        
            for member in tar.getmembers():
                member_path = os.path.join(path, member.name)
                if not is_within_directory(path, member_path):
                    raise Exception("Attempted Path Traversal in Tar File")
        
            tar.extractall(path, members, numeric_owner=numeric_owner) 
            
        
        safe_extract(t, dest_dir)
