# -*- coding: utf-8 -*-

import os
import sys

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages

from simple_model import __version__


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname), 'r').read()


if 'upload' in sys.argv or 'register' in sys.argv:
    if not __version__ or __version__ == '<VERSION>':
        raise RuntimeError("Package version not set!")
    elif '.rc' in __version__:
        raise RuntimeError("Not deploying release candidate to PyPi!")

setup(
    name="simple_model",
    version=__version__,
    author="Aljosha Friemann",
    author_email="a.friemann@automate.wtf",
    description="very simple model framework",
    long_description=open('README.rst').read(),
    url="https://github.com/afriemann/simple_model",
    download_url="https://github.com/afriemann/simple_model/archive/{}.tar.gz".format(__version__),
    packages=find_packages(exclude=('test*', 'assets')),
    install_requires=[],
    platforms=['linux'],
    keywords=['model', 'serialization', 'validation', 'dataclass'],
    classifiers=[
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Operating System :: POSIX :: Linux",
        "Topic :: Software Development :: Libraries",
        "License :: OSI Approved :: BSD License",
    ],
)

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 fenc=utf-8
