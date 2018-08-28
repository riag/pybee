# -*- coding: utf-8 -*-

from urllib.request import urlopen
import os

from hfilesize import FileSize
from tqdm import tqdm

class DownloadFileException(Exception):
    pass

def download(url, out_put_path, chunk_size=1024, user=None, password=None):
    tmp_path = out_put_path + '.tmp'
    u = urlopen(url)
    meta = u.info()

    file_name = os.path.basename(out_put_path)
    
    file_size = int(meta['Content-Length'])
    human_file_size = '{:.03Hc}'.format(FileSize(file_size))
    content_type = meta['Content-Type']

    print("url is %s" % u.geturl())
    print("Length is %d (%s) [%s]" % (file_size, human_file_size, content_type))
    print("Saveing to: %s" % out_put_path)


    download_size = 0
    with open(tmp_path, 'wb') as f:
        pbar = tqdm(total=file_size, unit='B', unit_scale=True, unit_divisor=1024, miniters=1)
        pbar.set_description('%s ' % file_name)
        while True:
            chunk = u.read(chunk_size)
            if not chunk:
                break
            download_size += len(chunk)
            pbar.update(len(chunk))
            f.write(chunk)

        pbar.close()

    if download_size != file_size:
        raise DownloadFileException() 

    os.rename(tmp_path, out_put_path)
