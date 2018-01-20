# -*- coding: utf-8 -*-
"""
.. module: TODO
    :platform: TODO
    :synopsis: TODO

.. moduleauthor:: Aljosha Friemann a.friemann@automate.wtf
"""


class Attribute(object):
    __type__ = None
    __name__ = None
    __alias__ = None
    __default__ = None
    __value__ = None
    __optional__ = False

    def __init__(self, t, name=None, alias=None, optional=False, fallback=None):
        if t is None:
            raise ValueError('attribute type can not be None')

        self.__type__ = t
        self.__name__ = name
        self.__alias__ = alias
        self.__default__ = fallback
        self.__optional__ = optional

    def __iter__(self):
        yield 'class', self.__class__.__name__
        yield 'name', self.__name__
        yield 'type', self.__type__
        yield 'default', self.__default__
        yield 'optional', self.__optional__
        yield 'alias', self.__alias__
        yield 'value', self.__value__

    def __str__(self):
        return str(dict(self))

    def __call__(self, value):
        self.value = value
        return self

    @property
    def alias(self):
        return self.__alias__

    @property
    def name(self):
        return self.__name__

    @property
    def value(self):
        return self.__value__

    @value.setter
    def value(self, value):
        if value is None:
            if self.__default__ is not None:
                try:
                    self.__value__ = self.__type__(self.__default__())
                except TypeError:
                    self.__value__ = self.__type__(self.__default__)
            elif self.__optional__:
                self.__value__ = None
            else:
                raise ValueError('attribute value must not be None')
        elif type(value) is self.__type__:
            self.__value__ = value
        else:
            try:
                self.__value__ = self.__type__(**value)
            except TypeError:
                self.__value__ = self.__type__(value)

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 fenc=utf-8
