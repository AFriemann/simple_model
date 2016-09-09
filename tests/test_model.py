#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
.. module:: TODO
   :platform: Unix
   :synopsis: TODO.

.. moduleauthor:: Aljosha Friemann aljosha.friemann@gmail.com

"""

import logging
logging.basicConfig(level=logging.DEBUG)

import unittest

from simple_model import Model, Attribute

class ModelTestCase(unittest.TestCase):
    """Tests for the Model class"""

    def create_uut(self):
        class UUT(Model):
            name = Attribute(str)
            number = Attribute(int)
            null = Attribute(str, optional=True)
            default_false = Attribute(bool, fallback=False)
        return UUT

    def setUp(self):
        self.uut = self.create_uut()

    def test_model_should_nullify_missing_optional_arguments(self):
        try:
            uut = self.uut(name = 'test', number = 3)
            self.assertIsNone(uut.null)
            self.assertIsNotNone(uut.default_false)
            self.assertFalse(uut.default_false)
        except Exception as e:
            self.fail('creation with missing argument failed in spite of optional/fallback set to True: ' + str(e))

        with self.assertRaises(AssertionError):
            self.uut(name = 'test')

    def test_model_should_allow_unknown_arguments_by_default(self):
        try:
            self.uut(name = 'test', number = 3, null = None, default_false = True, unknown = 2)
        except Exception as e:
            self.fail('creation with unknown argument failed: ' + str(e))

    def test_model_should_not_store_unknown_argument(self):
        with self.assertRaises(AttributeError):
            self.uut(name = 'test', number = 3, null = None, default_false = True, unknown = 2).unkown

    def test_model_should_be_comparable_to_others(self):
        uut1 = self.uut(name = 'test', number = 3)
        uut2 = self.uut(name = 'test', number = 3)

        self.assertEquals(uut1, uut2)

        uut3 = self.uut(name = 'test', number = 1)

        self.assertNotEquals(uut1, uut3)

    def test_model_should_provide_legacy_attributes_method(self):
        uut = self.uut(name = 'test', number = 3)

        self.assertEquals(uut.__attributes__(), dict(uut))

class ModelCastTestCase(unittest.TestCase):
    def setUp(self):
        class Data1(Model):
            value = Attribute(str)
        class Data2(Model):
            model_value = Attribute(Data1)

        self.Data2 = Data2

    def test_model_casting(self):
        try:
            data2 = self.Data2(model_value = { 'value': 'abc' })
            self.assertEqual(data2.model_value.value, "abc")
        except Exception as e:
            self.fail("using model classes as Attributes did not work: " + str(e))

    def test_serialization(self):
        data2 = self.Data2(model_value = { 'value': 'abc' })
        self.assertDictEqual(dict(data2), {'model_value': {'value': 'abc'}})

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 fenc=utf-8
