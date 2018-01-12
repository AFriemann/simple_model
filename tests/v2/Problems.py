# -*- coding: utf-8 -*-

import sys

from simple_model.v2 import Model, Attribute


@Model(mutable=False)
@Attribute('foo', type=str, help='foo is a str')
@Attribute('bar', type=int, optional=True, mutable=True)
@Attribute('baz', type=int, default=12)
class TestModel:
    pass


def test_immutability_fails_with_oldstyle_class():
    m = TestModel(foo='abc')

    if sys.version_info.major > 2:
        try:
            m.foo = 'def'
            assert False, 'immutable attribute is mutable'
        except AttributeError:
            pass
    else:
        m.foo = 'def'


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 fenc=utf-8
