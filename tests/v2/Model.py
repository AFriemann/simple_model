# -*- coding: utf-8 -*-

import sys

from simple_model.v2 import Model, Attribute, Unset
from simple_model.helpers import list_type


@Model(hide_unset=True)
@Attribute('foo', type=str, help='foo is a str')
@Attribute('bar', type=int, optional=True, mutable=False)
@Attribute('baz', type=int, default=12)
class TestModel(object):
    pass


def test_creation():
    m = TestModel(foo='abc')

    assert m is not None

    assert m.foo == 'abc'
    assert m.baz == 12
    assert m.bar is Unset

    assert 'bar' not in m


def test_attribute_uses_default_when_not_nullable():
    m = TestModel(foo='def', baz=None)

    assert m.foo == 'def'
    assert m.baz is 12
    assert m.bar is Unset


def test_memory_independence():
    m1 = TestModel(foo='abc', baz=33)

    assert m1.foo == 'abc', 'expected "abc" but got "%s"' % (m1.foo)
    assert m1.baz == 33, 'expected 33 but got %s' % m1.baz

    m2 = TestModel(foo='def')

    assert m2.foo == 'def', 'expected "def" but got "%s"' % (m2.foo)
    assert m2.baz == 12, 'expected default 12 but got %s' % m2.baz

    assert m1.foo == 'abc', 'expected "abc" but got "%s"' % (m1.foo)
    assert m1.baz == 33, 'expected 33 but got %s' % m1.baz


def test_mutability():
    m = TestModel(foo='abc')

    assert m.foo == 'abc'

    m.foo = 'fofo'

    assert m.foo == 'fofo'

    try:
        m.bar = 'abc'
        assert False, 'Attribute is mutable'
    except AttributeError:
        pass

    @Model()
    @Attribute('foobar', type=int, mutable=True)
    class TestModel2(object):
        pass

    m2 = TestModel2(foobar=12)

    assert m2.foobar == 12

    m2.foobar = 3

    assert m2.foobar == 3


def test_global_immutability():
    @Model(mutable=False)
    @Attribute('foobar', type=str)
    class TestModel:
        pass

    m = TestModel(foobar='abc')

    try:
        m.foobar = 'def'

        if sys.version_info.major > 2:
            assert False, 'Attribute is mutable'
        else:
            assert m.foobar == 'def', 'Attribute is mutable'
    except AttributeError:
        pass


def test_attribute_aliasing():
    @Model()
    @Attribute('foobar', type=str, alias='@foobar')
    class AliasModel(object):
        pass

    m = AliasModel(**{'@foobar': 'abc'})

    assert m.foobar == 'abc'

    del m

    m = AliasModel(foobar='abc')

    assert m.foobar == 'abc'


def test_model_stacking():
    @Model()
    @Attribute('foobar', type=TestModel)
    class StackedModel(object):
        pass

    s = StackedModel(foobar={'foo': 'abc'})

    assert s is not None
    assert isinstance(s.foobar, TestModel)

    del s

    m = TestModel(foo='abc')

    s = StackedModel(foobar=m)

    assert s is not None
    assert isinstance(s.foobar, TestModel)

    assert m == s.foobar
    assert m is not s.foobar

    assert StackedModel(**s) == s


def test_list_model_stacking():
    @Model()
    @Attribute('foobar', type=list_type(TestModel))
    class StackedModel:
        pass

    m1 = TestModel(foo='abc')
    m2 = TestModel(foo='def')

    s = StackedModel(foobar=[m1, m2])

    assert s is not None

    for unit in s.foobar:
        assert isinstance(unit, TestModel)


def test_model_with_custom_init():
    @Model()
    @Attribute('foobar', type=str)
    class InitModel:
        def __init__(self, arg, omg=None):
            """foobar"""
            self.arg = arg
            self.omg = omg

    m = InitModel(123, foobar='abcdef', omg=456)

    assert m.foobar == 'abcdef'
    assert m.arg == 123
    assert m.omg == 456


def test_model_inheritance():
    def not_implemented(*args, **kwargs):
        raise NotImplementedError

    @Model()
    @Attribute('encode', type=not_implemented)
    class Super(object):
        def decode(self):
            raise NotImplementedError

    try:
        Super(encode='hjkl')
        assert False, 'Could initialize un-initializable Model'
    except NotImplementedError:
        pass

    @Model()
    @Attribute('encode', type=lambda s: s.encode())
    class Child(Super):
        def decode(self):
            return self.encode.decode()

    m = Child(encode='abcdef')

    assert m.encode == b'abcdef'
    assert m.decode() == 'abcdef'


def test_model_hides_unset_attributes_if_specified():
    @Model(hide_unset=True)
    @Attribute('foo', type=str, optional=True)
    @Attribute('bar', type=str, optional=True)
    class MyModel(object):
        pass

    m = MyModel(foo='abc')

    assert 'bar' not in dict(m)
    assert 'bar' not in m


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 fenc=utf-8
