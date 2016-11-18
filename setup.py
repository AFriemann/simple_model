#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
.. module:: TODO
   :platform: Unix
   :synopsis: TODO.

.. moduleauthor:: Aljosha Friemann aljosha.friemann@gmail.com

"""

import os, pip
from subprocess import Popen, PIPE

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname), 'r').read()

def sh(*args):
    return Popen(args, stdout=PIPE).communicate()[0].strip().decode()

def git_version():
    commit = sh('git', 'rev-parse', '--short', 'HEAD')
    tag = sh('git', 'tag', '--contains', commit)

    if not tag:
        # this is not PEP440 compatible
        last_tag = sh('git', 'describe', '--abbrev=0', '--tags')
        return '{0}-{1}'.format(last_tag, commit)

    return tag

install_reqs = pip.req.parse_requirements('requirements.txt', session=pip.download.PipSession())

requirements = [str(ir.req) for ir in install_reqs if ir is not None]

version = git_version()

setup(name             = "simple_model",
      author           = "Aljosha Friemann",
      author_email     = "aljosha.friemann@gmail.com",
      description      = "very simple model framework",
      url              = "https://www.github.com/afriemann/simple_model.git",
      download_url     = "https://github.com/AFriemann/simple_model/archive/{}.tar.gz".format(version),
      keywords         = ['model','serialization','validation'],
      version          = version,
      license          = read('LICENSE.txt'),
      long_description = read('README.rst'),
      install_requires = requirements,
      classifiers      = [],
      packages         = ["simple_model"],
      platforms        = 'linux'
)

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 fenc=utf-8
