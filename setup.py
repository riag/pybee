# -*- coding: utf-8 -*-

import io
import re

from setuptools import setup

with io.open('src/pybee/__init__.py', 'rt', encoding='utf8') as f:
    version = re.search(r'__version__ = \'(.*?)\'', f.read()).group(1)


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
        packages=['src/pybee'],
        include_package_data=True,
        zip_safe=False,
        platforms='any',
        python_requires='>=3.4',
        install_requires=[
            'PyFunctional==1.1.3',
            'hfilesize==0.1.0',
            'tqdm==4.25.0',
            'jinja2==2.10',
            'click==6.7',
            ],
        extras_require={
            'dev':[
                'pytest>=3',
                ]
            },
        classifiers=[
            'License :: OSI Approved :: BSD License',
            'Programming Language :: Python :: 3',
            'Topic :: Software Development :: Libraries :: Python Modules',
        ]
)

