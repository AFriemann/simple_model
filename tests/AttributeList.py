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

from simple_model import Model, Attribute, AttributeList

class AttributeListTestCase(unittest.TestCase):
    uut = AttributeList(int)

    def test_attribute_list_should_cast_all_values(self):
        try:
            self.assertEqual(self.uut([1, 2, "3"]), [1,2,3])
        except Exception as e:
            self.fail('failed to validate list with AttributeList class: ' + str(e))

    def test_attribute_list_should_raise_value_errors(self):
        with self.assertRaises(ValueError):
            self.uut([1, "abc", 3])

    def test_encapsulated_validation(self):
        class Data1(Model):
            value = Attribute(str)
        class Data2(Model):
            list_value = AttributeList(Data1, optional=True)

        try:
            data2 = Data2()
            self.assertEqual(data2.list_value, [])

            data2 = Data2(list_value = [{'value': 'a'}, {'value': 'b'}])
            self.assertEqual(data2.list_value[0].value, 'a')
        except Exception as e:
            self.fail("data validation with encapsulated Models in AttributeLists failed: " + str(e))

    def test_encapsulated_serialization(self):
        class Data1(Model):
            value = Attribute(str)
        class Data2(Model):
            list_value = AttributeList(Data1, optional=True)

        try:
            data2 = Data2()
            self.assertEqual(dict(data2), {'list_value': []})

            data2 = Data2(list_value = [{'value': 'a'}, {'value': 'b'}])
            self.assertDictEqual(dict(data2), {'list_value': [{'value': 'a'},{'value': 'b'}]})
        except Exception as e:
            self.fail("serialization with encapsulated Models in AttributeLists failed: " + str(e))

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 fenc=utf-8
