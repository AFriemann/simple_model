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

from simple_model import Attribute, list_type

class AttributeTestCase(unittest.TestCase):
    """Tests for the Attribute class"""

    def test_attribute_should_not_be_nullifiable_by_default(self):
        with self.assertRaises(ValueError):
            Attribute(str)(None)

    def test_attribute_should_be_nullifiable_if_specified(self):
        uut = Attribute(str, optional=True)

        try:
            self.assertIsNone(uut(None).value)
        except ValueError as e:
            self.fail('creation of attribute failed in spite of "optional" set to True: ' + str(e))

    def test_attribute_should_use_fallback_if_specified(self):
        uut = Attribute(str, fallback='test')

        try:
            self.assertEqual(uut(None).value, 'test')
        except ValueError as e:
            self.fail('creation of attribute failed in spite of fallback being given: ' + str(e))

    def test_attribute_should_call_fallback_if_function(self):
        def test_function():
            return 'test'

        uut = Attribute(str, fallback=test_function)

        try:
            self.assertEqual(uut(None).value, 'test')
        except ValueError as e:
            self.fail('creation of attribute failed in spite of fallback function being given: ' + str(e))

    def test_attribute_should_cast_value_to_given_type(self):
        try:
            uut = Attribute(str, fallback='test')
            self.assertEqual(uut(12).value, '12')

            uut = Attribute(int, fallback='test')
            self.assertEqual(uut(12).value, 12)
        except ValueError as e:
            self.fail('creation of attribute failed in spite of "fallback" set: ' + str(e))

    def test_named_attributes(self):
        uut = Attribute(str, name='@foobar')
        self.assertEqual(uut('def').name, '@foobar')

    def test_attribute_should_raise_when_type_is_none(self):
        with self.assertRaises(ValueError):
            Attribute(None)

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 fenc=utf-8
