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

class Examples(unittest.TestCase):
    class Data(Model):
        name = Attribute(str)
        some_value = Attribute(str, optional=True)
        another_value = Attribute(int, fallback=0)

    def test_examples(self):
        actual = dict(self.Data(name = 'test', some_value = None, another_value = 12))
        expected = { 'name': 'test', 'some_value': None, 'another_value': 12 }
        self.assertEqual(actual, expected)

        actual = dict(self.Data(name = 'test'))
        expected = { 'name': 'test', 'some_value': None, 'another_value': 0 }
        self.assertEqual(actual, expected)

        actual = dict(self.Data(name = 'test', unknown_value = True))
        expected = { 'name': 'test', 'some_value': None, 'another_value': 0 }
        self.assertEqual(actual, expected)

        init_dict = {'name': 'test', 'some_value': 'val', 'another_value': 3}
        actual = dict(self.Data(**init_dict))
        expected = { 'name': 'test', 'some_value': 'val', 'another_value': 3 }
        self.assertEqual(actual, expected)

    def test_serialization(self):
        import json

        def serialize(model):
            return json.dumps(dict(model))

        def deserialize(string):
            return self.Data(**json.loads(string))

        data = self.Data(name = 'test', some_value = 'val', another_value = 3)

        serialized = serialize(data)
        deserialized = deserialize(serialized)

        self.assertEquals(data, deserialized)

    def test_complex_types(self):
        from datetime import datetime

        def parse_date(string):
            return datetime.strptime(string, '%Y-%m-%d')

        class Data(Model):
            date = Attribute(parse_date)

        expected = { 'date': datetime(2015, 11, 20, 0, 0) }
        actual = dict(Data(date = '2015-11-20'))

        self.assertEquals(actual, expected)

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 fenc=utf-8
