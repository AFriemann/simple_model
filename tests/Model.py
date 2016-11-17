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

from simple_model import Model, Attribute, list_type

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

    def tearDown(self):
        del self.uut

    def test_model_should_nullify_missing_optional_arguments(self):
        try:
            uut = self.uut(name = 'test', number = 3)
            self.assertIsNone(uut.null)
            self.assertIsNotNone(uut.default_false)
            self.assertFalse(uut.default_false)
        except Exception as e:
            self.fail('creation with missing argument failed in spite of optional/fallback set to True: ' + str(e))

        with self.assertRaises(ValueError):
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

class ModelCastTestCase(unittest.TestCase):
    def setUp(self):
        class Data1(Model):
            value = Attribute(str)
        class Data2(Model):
            model_value = Attribute(Data1)
        class Data3(Model):
            data1 = Attribute(list_type(Data1))
            data2 = Attribute(Data2)

        self.Data1 = Data1
        self.Data2 = Data2
        self.Data3 = Data3

    def tearDown(self):
        del self.Data1
        del self.Data2
        del self.Data3

    def test_model_casting(self):
        try:
            data2 = self.Data2(model_value = { 'value': 'abc' })
            self.assertEqual(data2.model_value.value, "abc")
        except Exception as e:
            self.fail("using model classes as Attributes did not work: " + str(e))

    def test_serialization(self):
        data2 = self.Data2(model_value = { 'value': 'abc' })
        self.assertDictEqual(dict(data2), {'model_value': {'value': 'abc'}})

    def test_model_should_serialize_all_contained_models(self):
        input_data = {
            'data1': [
                {
                    'value': 'abc',
                }
            ],
            'data2': {
                'model_value': {
                    'value': 'def',
                }
            }
        }

        uut = self.Data3(**input_data)

        self.assertDictEqual(dict(uut), input_data)

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 fenc=utf-8
