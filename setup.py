# -*- coding: utf-8 -*-
"""
.. module:: TODO
   :platform: Unix
   :synopsis: TODO.

.. moduleauthor:: Aljosha Friemann aljosha.friemann@gmail.com

"""

import os, sys
from subprocess import Popen, PIPE

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname), 'r').read()

def git(*args):
    cmd = ['git']
    cmd.extend(args)
    return Popen(cmd, stdout=PIPE).communicate()[0].strip().decode()

def current_commit():
    return git('rev-parse', '--short', 'HEAD')

def git_tag_for(commit):
    return git('tag', '--points-at', commit)

def latest_tag():
    return git('describe', '--abbrev=0', '--tags')

def get_version_from_git():
    commit = current_commit()
    tag = git_tag_for(commit)

    return tag or '{}-{}'.format(latest_tag(), commit)

from simple_model import __version__

if 'upload' in sys.argv or 'register' in sys.argv:
    VERSION = get_version_from_git()

    if VERSION != __version__:
        raise RuntimeError(
            "Package version ({}) and git version ({}) are not the same".format(
                __version__, VERSION))

if not __version__ or __version__ == '<VERSION>':
    raise RuntimeError("Package version not set!")

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
      install_requires = [],
      classifiers      = [],
      packages         = ["simple_model"],
      platforms        = 'linux'
)

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 fenc=utf-8
