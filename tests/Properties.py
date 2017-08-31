# -*- coding: utf-8 -*-
"""
.. module: TODO
    :platform: TODO
    :synopsis: TODO

.. moduleauthor:: Aljosha Friemann a.friemann@automate.wtf
"""

import unittest

from simple_model import Attribute
from simple_model.pbm import Model

class PropertyBasedModels(unittest.TestCase):
    def test_model(self):
        class TestModel(Model):
            prop = Attribute(int)

        print('creating without prop')
        with self.assertRaises(ValueError):
            m = TestModel()

        print('creating with prop')
        m = TestModel(prop=66)

        self.assertEqual(m.prop, 66)

        with self.assertRaises(AttributeError):
            m.prop = 100

        self.assertEqual(m.prop, 66)

        m.mutable = True

        m.prop = 100
        self.assertEqual(m.prop, 100)

    def test_unusual_models(self):
        class TestModel(Model):
            _a = Attribute(int, optional=True)

            @property
            def blub(self):
                try:
                    return self.__cache
                except AttributeError:
                    self.__cache = {}
                    return self.__cache

        m = TestModel()

        self.assertIsNone(m._a)

        self.assertIn('_a', m)
        self.assertNotIn('blub', m)

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 fenc=utf-8
