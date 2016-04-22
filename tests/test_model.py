#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
.. module:: TODO
   :platform: Unix
   :synopsis: TODO.

.. moduleauthor:: Aljosha Friemann aljosha.friemann@gmail.com

"""

import unittest

from simple_model import Model, Attribute, AttributeList

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

class AttributeTestCase(unittest.TestCase):
    """Tests for the Attribute class"""

    def test_attribute_should_not_be_nullifiable_by_default(self):
        with self.assertRaises(ValueError):
            Attribute(str)(None)

    def test_attribute_should_be_nullifiable_if_specified(self):
        uut = Attribute(str, optional=True)
        try:
            self.assertIsNone(uut(None))
        except ValueError as e:
            self.fail('creation of attribute failed in spite of "optional" set to True: ' + str(e))

    def test_attribute_should_use_fallback_if_specified(self):
        uut = Attribute(str, fallback='test')
        try:
            self.assertEqual(uut(None), 'test')
        except ValueError as e:
            self.fail('creation of attribute failed in spite of fallback being given: ' + str(e))

    def test_attribute_should_call_fallback_if_function(self):
        def test_function():
            return 'test'

        uut = Attribute(str, fallback=test_function)
        try:
            self.assertEqual(uut(None), 'test')
        except ValueError as e:
            self.fail('creation of attribute failed in spite of fallback function being given: ' + str(e))

    def test_attribute_should_cast_value_to_given_type(self):
        try:
            uut = Attribute(str, fallback='test')
            self.assertEqual(uut(12), '12')
            uut = Attribute(int, fallback='test')
            self.assertEqual(uut(12), 12)
        except ValueError as e:
            self.fail('creation of attribute failed in spite of "fallback" set: ' + str(e))


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

class ExampleTestCase(unittest.TestCase):
    """Tests for the examples"""

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

if __name__ == '__main__':
    unittest.main()

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 fenc=utf-8
