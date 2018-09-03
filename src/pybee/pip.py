# -*- coding: utf-8 -*-

import pybee

def download_source_packages(
        download_dir, package_list, 
        format_control=':all:', pip_bin='pip3',
        repo_url=None
        ):
    cmd_list = [pip_bin, 'download', 
            '-d', download_dir, 
            '--no-binary', format_control]
    if repo_url:
        cmd_list.append('--index-url')
        cmd_list.append(repo_url)

    cmd_list.extend(package_list)
    pybee.shell.exec(cmd_list)

def download_binary_packages(
        download_dir, package_list, 
        format_control=':all:', pip_bin='pip3',
        repo_url=None
        ):
    cmd_list = [pip_bin, 'download', 
            '-d', download_dir, 
            '--only-binary', format_control,
            ]
    if repo_url:
        cmd_list.append('--index-url')
        cmd_list.append(repo_url)

    cmd_list.extend(package_list)
    pybee.shell.exec(cmd_list)

