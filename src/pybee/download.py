# -*- coding: utf-8 -*-

from urllib.request import urlopen
import os

from hfilesize import FileSize
from tqdm import tqdm


class DownloadFileException(Exception):
    pass


def download(url, out_put_path, chunk_size=1024, user=None, password=None):
    '''
        out_put_path 可以是一个目录
        也可以是文件路径
    '''
    u = urlopen(url)
    meta = u.info()

    dest_file = out_put_path
    if os.path.isdir(out_put_path):
        name = meta.get_filename()
        if name is None:
            name = url.split('/')[-1]

        dest_file = os.path.join(out_put_path, name)

    tmp_path = dest_file + '.tmp'

    file_name = os.path.basename(dest_file)

    size_str = meta['Content-Length']
    file_size = -1
    if size_str:
        file_size = int(size_str)

    if file_size > 0:
        human_file_size = '{:.03Hc}'.format(FileSize(file_size))
    content_type = meta['Content-Type']

    print("url is %s" % u.geturl())
    if file_size > 0:
        print("Length is %d (%s) [%s]" % (file_size, human_file_size, content_type))
    else:
        print("Length unspecified [%s]" % (content_type))

    print("Saveing to: %s" % dest_file)

    download_size = 0
    with open(tmp_path, 'wb') as f:
        pbar = tqdm(
            total=file_size, unit='B',
            unit_scale=True, unit_divisor=1024,
            miniters=1)
        pbar.set_description('%s ' % file_name)
        while True:
            chunk = u.read(chunk_size)
            if not chunk:
                break
            download_size += len(chunk)
            pbar.update(len(chunk))
            f.write(chunk)

        pbar.close()

    if file_size > 0 and download_size != file_size:
        raise DownloadFileException()

    os.rename(tmp_path, dest_file)
    return dest_file
