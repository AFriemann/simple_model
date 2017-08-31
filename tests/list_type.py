# -*- coding: utf-8 -*-
"""
.. module:: TODO
   :platform: Unix
   :synopsis: TODO.

.. moduleauthor:: Aljosha Friemann aljosha.friemann@gmail.com

"""

import unittest

from simple_model import Model, Attribute
from simple_model.helpers import list_type

class ListType(unittest.TestCase):
    def test_with_simple_types(self):
        self.assertEqual(list_type(str)([1, 'b']), ['1', 'b'])

    def test_with_model(self):
        class Foo(Model):
            attribute = Attribute(str)

        result = list_type(Foo)([{'attribute': 1}, {'attribute': '2'}])

        for element in result:
            self.assertIsInstance(element, Foo)

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 fenc=utf-8
