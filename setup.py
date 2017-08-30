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

def sh(*args):
    return Popen(args, stdout=PIPE).communicate()[0].strip().decode()

def current_commit():
    return sh('git', 'rev-parse', '--short', 'HEAD')

def git_tag_for(commit):
    return sh('git', 'tag', '--points-at', commit)

def latest_tag():
    return sh('git', 'describe', '--abbrev=0', '--tags')

def get_version():
    commit = current_commit()
    tag = git_tag_for(commit)

    return tag or '{}-{}'.format(latest_tag(), commit)

def set_version(version):
    template = read('simple_model/__init__.py')

    with open('simple_model/__init__.py', 'w') as output:
        for line in template.split('\n'):
            if 'VERSION' in line:
                line = line.replace('<VERSION>', version)
            output.write(line + os.linesep)

VERSION = get_version()

if 'upload' in sys.argv or 'register' in sys.argv:
    set_version(VERSION)

setup(name             = "simple_model",
      author           = "Aljosha Friemann",
      author_email     = "aljosha.friemann@gmail.com",
      description      = "very simple model framework",
      url              = "https://www.github.com/afriemann/simple_model.git",
      download_url     = "https://github.com/AFriemann/simple_model/archive/{}.tar.gz".format(VERSION),
      keywords         = ['model','serialization','validation'],
      version          = VERSION,
      license          = read('LICENSE.txt'),
      long_description = read('README.rst'),
      install_requires = [],
      classifiers      = [],
      packages         = ["simple_model"],
      platforms        = 'linux'
)

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 fenc=utf-8
