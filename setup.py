#!/usr/bin/env python

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import os
import sys

if sys.version < '3':
    execfile(os.path.join('icebergsdk', 'version.py'))
else:
    exec(open("icebergsdk/version.py").read())

install_requires = []
install_requires.append('requests >= 2.3.0')
install_requires.append('algoliasearch>=1.7.1')
install_requires.append('python-dateutil>=2.4.0')
install_requires.append('pytz')

setup(
    name='icebergsdk',
    version=VERSION,
    description='Iceberg Marketplace API Client for Python',
    author='Iceberg',
    author_email='florian@izberg-marketplace.com',
    url='https://github.com/Iceberg-Marketplace/Iceberg-API-PYTHON',
    packages=["icebergsdk", 'icebergsdk.resources', 'icebergsdk.mixins', 'icebergsdk.utils'],
    install_requires=install_requires,
    keywords=['iceberg', 'modizy', 'marketplace', 'saas'],
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        'Intended Audience :: Developers',
        "License :: OSI Approved :: MIT License",
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
