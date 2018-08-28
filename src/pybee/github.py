# -*- coding: utf-8 -*-

from pybee import download

release_compress_file_fmts = ['tar.gz', 'zip']

class NotSupportFileFormat(Exception):
	pass

def download_by_release_version(out_put_path, url, release_version, file_fmt='tar.gz'):
	if not file_fmt in release_compress_file_fmts: raise NotSupportFileFormat()

	download_url = '%s/archive/%s.%s' % (url, release_version, filt_fmt)
	download.download(download_url, out_put_path)


def download_by_commit_id(out_put_path, url, commid_id):
	
	download_url = '%s/archive/%s.zip' % (url, commid_id)
	download.download(download_url, out_put_path)

