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
    author="Aljosha Friemann",
    author_email="a.friemann@automate.wtf",
    description="very simple model framework",
    url="https://github.com/afriemann/simple_model",
    download_url="https://github.com/afriemann/simple_model/archive/{}.tar.gz".format(__version__),
    keywords=['model', 'serialization', 'validation'],
    version=__version__,
    license=read('LICENSE.txt'),
    long_description=read('README.rst'),
    install_requires=[],
    classifiers=[],
    packages=find_packages(exclude=('test*', 'assets')),
    platforms=['linux']
)

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 fenc=utf-8
