# -*- coding: utf-8 -*-
"""
.. module:: simple_model
   :platform: Unix
   :synopsis: Simple models for easy data (de-)serialization and validation.

.. moduleauthor:: Aljosha Friemann a.friemann@automate.wtf
"""

__version__ = '1.2.4'

from simple_model.helpers import list_type, one_of  # noqa: F401
from simple_model.v1 import Model, Attribute  # noqa: F401

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 fenc=utf-8
