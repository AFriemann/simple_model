#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
.. module:: TODO
   :platform: Unix
   :synopsis: TODO.

.. moduleauthor:: Aljosha Friemann aljosha.friemann@gmail.com

"""

import os, pip

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

install_reqs = pip.req.parse_requirements('requirements.txt', session=pip.download.PipSession())

requirements = [str(ir.req) for ir in install_reqs if ir is not None]

setup(name             = "simple_model",
      author           = "Aljosha Friemann",
      author_email     = "aljosha.friemann@gmail.com",
      description      = "very simple model framework",
      url              = "www.bitbucket.org/afriemann/simple_model.git",
      keywords         = ['model','serialization','validation'],
      version          = open('simple_model/VERSION').read().strip(),
      license          = open('LICENSE.txt').read(),
      long_description = open('README.rst').read(),
      install_requires = requirements,
      classifiers      = [],
      packages         = ["simple_model"],
      package_data     = { 'simple_model': ['VERSION'] },
      platforms        = 'linux'
)

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 fenc=utf-8
