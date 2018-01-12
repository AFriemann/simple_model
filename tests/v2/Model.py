# -*- coding: utf-8 -*-
"""
.. module: TODO
    :platform: TODO
    :synopsis: TODO

.. moduleauthor:: Aljosha Friemann a.friemann@automate.wtf
"""

import unittest


from simple_model.v2 import Model, Attribute


@Model(mutable=True)
@Attribute('foo', type=str, help='foo is a str')
@Attribute('bar', type=int, optional=True, mutable=False)
@Attribute('baz', type=int, default=12)
class TestModel:
    pass


class ModelV2Test(unittest.TestCase):
    def test_creation(self):
        m = TestModel(foo='abc')

        self.assertIsNotNone(m)

        self.assertEqual(m.foo, 'abc')
        self.assertEqual(m.baz, 12)
        self.assertIsNone(m.bar)

        self.assertEqual(m['foo'], 'abc')

        with self.assertRaises(KeyError):
            m['fooo']

    def test_mutability(self):
        m = TestModel(foo='abc')

        m.foo = 'fofo'

        self.assertEqual(m.foo, 'fofo')

        with self.assertRaises(AttributeError):
            m.bar = 'abc'

    def test_attribute_aliasing(self):
        @Model()
        @Attribute('foobar', type=str, alias='@foobar')
        class AliasModel:
            pass

        m = AliasModel(**{'@foobar': 'abc'})

        self.assertEqual(m.foobar, 'abc')
        self.assertEqual(m['@foobar'], 'abc')

        del m

        m = AliasModel(foobar='abc')

        self.assertEqual(m.foobar, 'abc')
        self.assertEqual(m['@foobar'], 'abc')

    def test_model_stacking(self):
        @Model()
        @Attribute('foobar', type=TestModel)
        class StackedModel:
            pass

        s = StackedModel(foobar={'foo': 'abc'})

        self.assertIsNotNone(s)
        self.assertIsInstance(s.foobar, TestModel)

        del s

        m = TestModel(foo='abc')

        s = StackedModel(foobar=m)
        self.assertIsNotNone(s)
        self.assertIsInstance(s.foobar, TestModel)

        self.assertEqual(m, s.foobar)

        self.assertEqual(StackedModel(**s), s)


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 fenc=utf-8
