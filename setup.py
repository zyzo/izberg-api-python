#!/usr/bin/env python

from setuptools import setup, find_packages

version = __import__('icebergsdk').__version__


def load_requirements(*filepaths):
    requirements = []
    for filepath in filepaths:
        with open(filepath, 'r') as requirements_file:
            requirements += [
                requirement.split(" #")[0]
                for requirement in requirements_file.read().splitlines()
                if not requirement.startswith('#')
            ]

    return requirements

setup(
    name='izberg-sdk',
    version=version,
    description='IZBERG Marketplace API Client for Python',
    author='IZBERG',
    author_email='florian@izberg-marketplace.com',
    url='https://github.com/izberg-marketplace/izberg-api-python',
    packages=find_packages(),
    install_requires=load_requirements("requirements/base.txt"),
    keywords=['izberg', 'marketplace', 'saas', 'api', 'python'],
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        'Intended Audience :: Developers',
        "License :: OSI Approved :: MIT License",
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    data_files=['requirements/base.txt'],
)
