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

def read_version():
    with open(os.path.join(os.path.dirname(__file__), 'simple_model/__init__.py')) as f:
        for line in f:
            if 'VERSION' in line:
                version = line.split('=')[1].replace("\"", "").strip()
                return version

install_reqs = pip.req.parse_requirements('requirements.txt', session=pip.download.PipSession())
print(install_reqs)

requirements = [str(ir.req) for ir in install_reqs if ir is not None]

setup(name             = "simple_model",
      author           = "Aljosha Friemann",
      author_email     = "aljosha.friemann@gmail.com",
      license          = "",
      version          = read_version(),
      description      = "very simple model framework",
      url              = "www.bitbucket.org/afriemann/simple_model.git",
      keywords         = [],
      # download_url     = "",
      install_requires = requirements,
      long_description = read('README'),
      classifiers      = [],
      packages         = ["simple_model"]
)

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 fenc=utf-8
