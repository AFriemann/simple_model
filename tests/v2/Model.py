# -*- coding: utf-8 -*-

from simple_model.v2 import Model, Attribute


@Model(mutable=True)
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
    assert m.bar is None

    assert m['foo'] == 'abc'

    try:
        m['fooo']
        assert False, 'did not raise KeyError for unknown attribute'
    except KeyError:
        pass


def test_mutability():
    m = TestModel(foo='abc')

    assert m.foo == 'abc'

    print('mutating foo')
    m.foo = 'fofo'

    assert m.foo == 'fofo'

    try:
        m.bar = 'abc'
        assert False, 'Attribute is mutable'
    except AttributeError:
        pass


def test_attribute_aliasing():
    @Model()
    @Attribute('foobar', type=str, alias='@foobar')
    class AliasModel:
        pass

    m = AliasModel(**{'@foobar': 'abc'})

    assert m.foobar == 'abc'
    assert m['@foobar'] == 'abc'
    assert m.foobar is m['@foobar']

    del m

    m = AliasModel(foobar='abc')

    assert m.foobar == 'abc'
    assert m['@foobar'] == 'abc'
    assert m.foobar is m['@foobar']


def test_model_stacking():
    @Model()
    @Attribute('foobar', type=TestModel)
    class StackedModel:
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

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 fenc=utf-8
