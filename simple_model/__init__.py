#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
.. module:: TODO
   :platform: Unix
   :synopsis: TODO.

.. moduleauthor:: Aljosha Friemann aljosha.friemann@gmail.com

"""

from simple_model.decorators import deprecated

import abc

class Attribute:
    def __init__(self, t, optional=False, fallback=None):
        assert t is not None, "attribute type can not be None"

        self._type = t
        self._optional = optional
        self._fallback = fallback

    def __call__(self, value):
        if value is None:
            if self._fallback is not None:
                try: return self._type(self._fallback())
                except TypeError: return self._type(self._fallback)
            elif self._optional:
                return None
            else:
                raise ValueError('attribute value must not be None')
        return self._type(value)

class AttributeList(Attribute):
    def __call__(self, *lst):
        result = []
        for value in lst:
            result.append(super(AttributeList, self).__call__(value))
        return result

class Model(object):
    __metaclass__ = abc.ABCMeta

    _allow_missing = False

    @deprecated('__attributes__ is deprecated, please use cast to dict instead')
    def __attributes__(self):
        return dict(self)

    def __iter__(self):
        for key in dir(self):
            if not key.startswith('_'): yield key, getattr(self, key)

    def __eq__(self, other):
        return (isinstance(other, self.__class__)
            and vars(self) == vars(other))

    def __ne__(self, other):
        return not self.__eq__(other)

    def __init__(self, **kwargs):
        allow_missing = kwargs.get('allow_missing', self._allow_missing)

        for key, value in dict(self).items():
            if key not in kwargs:
                assert allow_missing, "%s not found in %s" % (key, kwargs)

            setattr(self, key, value(kwargs.get(key)))

    def __str__(self):
        return str(vars(self))

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 fenc=utf-8
