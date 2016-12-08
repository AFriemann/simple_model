# -*- coding: utf-8 -*-
"""
.. module:: TODO
   :platform: Unix
   :synopsis: TODO.

.. moduleauthor:: Aljosha Friemann aljosha.friemann@gmail.com

"""

import os, pip, sys
from subprocess import Popen, PIPE

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

from simple_model import __version__

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname), 'r').read()

def sh(*args):
    return Popen(args, stdout=PIPE).communicate()[0].strip().decode()

def current_commit():
    return sh('git', 'rev-parse', '--short', 'HEAD')

def git_tag_for(commit):
    return sh('git', 'tag', '--points-at', commit)

def check_version_against_tag():
    commit = current_commit()
    tag = git_tag_for(commit)

    if tag and tag != __version__:
        raise Exception('internal version {} is not equal to deployed version {}'.format(__version__, tag))

install_reqs = pip.req.parse_requirements('requirements.txt', session=pip.download.PipSession())

requirements = [str(ir.req) for ir in install_reqs if ir is not None]

if 'upload' in sys.argv or 'register' in sys.argv:
    check_version_against_tag()

setup(name             = "simple_model",
      author           = "Aljosha Friemann",
      author_email     = "aljosha.friemann@gmail.com",
      description      = "very simple model framework",
      url              = "https://www.github.com/afriemann/simple_model.git",
      download_url     = "https://github.com/AFriemann/simple_model/archive/{}.tar.gz".format(__version__),
      keywords         = ['model','serialization','validation'],
      version          = __version__,
      license          = read('LICENSE.txt'),
      long_description = read('README.rst'),
      install_requires = requirements,
      classifiers      = [],
      packages         = ["simple_model"],
      platforms        = 'linux'
)

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 fenc=utf-8
