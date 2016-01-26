#!/usr/bin/env python

from setuptools import setup
from pip.req import parse_requirements
from pip.download import PipSession

VERSION = "0.2.7"


install_reqs = parse_requirements("./requirements.txt", session=PipSession())
reqs = [str(ir.req) for ir in install_reqs]

setup(
    name             = 'intmaniac',
    packages         = ['intmaniac'],
    version          = VERSION,
    description      = 'A generic integration test tool utilizing docker-compose (for now)',
    author           = 'Axel Bock',
    author_email     = 'mr.axel.bock@gmail.com',
    url              = 'https://github.com/flypenguin/python-intmaniac',
    download_url     = 'https://github.com/flypenguin/python-intmaniac/tarball/{}'.format(VERSION),
    keywords         = 'integrationtest sysadmin devops ci cd',
    install_requires = reqs,
    entry_points     = {
        'console_scripts': [
            'intmaniac=intmaniac:console_entrypoint',
        ],
    },
    classifiers      = [
        "License :: OSI Approved :: MIT License",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Programming Language :: Python :: 3",
        "Operating System :: POSIX",
        "Operating System :: MacOS",
        "Topic :: System :: Systems Administration",
        "Topic :: Software Development :: Testing",
    ],
)
