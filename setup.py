# -*- coding: utf-8 -*-

import io
import os
import re

from setuptools import setup, find_packages

from pipenv.vendor.requirementslib import Lockfile

with io.open('src/pybee/__init__.py', 'rt', encoding='utf8') as f:
    version = re.search(r'__version__ = \'(.*?)\'', f.read()).group(1)

lockfile = Lockfile.create(os.path.abspath(os.path.dirname(__file__)))
install_requires = lockfile.as_requirements(dev=False)

setup(
        name='pybee',
        version = version,
        url='https://github.com/riag/pybee',
        license='BSD',
        author='riag',
        author_email='riag@163.com',
        maintainer='riag',
        maintainer_email='riag@163.com',
        description='util function for write python script, instead of bash script',
        package_dir={'': 'src'},
        packages=find_packages(where='src'),
        include_package_data=True,
        zip_safe=False,
        platforms='any',
        python_requires='>=3.4',
        install_requires=install_requires,
        setup_requires=[
            'pytest-runner',
        ],
        classifiers=[
            'License :: OSI Approved :: BSD License',
            'Programming Language :: Python :: 3',
            'Topic :: Software Development :: Libraries :: Python Modules',
        ]
)

