#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
.. module:: TODO
   :platform: Unix
   :synopsis: TODO.

.. moduleauthor:: Aljosha Friemann aljosha.friemann@gmail.com

"""

import abc

class Attribute:
    def __init__(self, t, nullable=False, fallback=None):
        if t is None:
            raise ValueError('attribute type can not be None')

        self.__type = t
        self.__nullable__ = nullable
        self.__fallback__ = fallback

    def __call__(self, value):
        if value is None:
            if self.__fallback__ is not None:
                try: return self.__type(self.__fallback__())
                except TypeError: return self.__type(self.__fallback__)
            elif self.__nullable__:
                return None
            else:
                raise ValueError('attribute value must not be None')
        return self.__type(value)

class Model(object):
    __metaclass__ = abc.ABCMeta
    __allow_unknown__ = False
    __allow_missing__ = False

    def __attributes__(self):
        return { k: getattr(self, k) for k in dir(self) if not k.startswith('_') }

    def __eq__(self, other):
        return (isinstance(other, self.__class__)
            and self.__attributes__() == other.__attributes__())

    def __ne__(self, other):
        return not self.__eq__(other)

    def __init__(self, **kwargs):
        allow_unknown = kwargs.get('_allow_unknown', self.__allow_unknown__)
        allow_missing = kwargs.get('_allow_missing', self.__allow_missing__)

        for key, value in kwargs.items():
            if key.startswith('_'): continue

            if key not in dir(self) or not isinstance(getattr(self, key), Attribute):
                if allow_unknown: continue
                else: raise TypeError("not part of model: %s" % key)

            try:
                setattr(self, key, getattr(self, key)(value))
            except ValueError as e:
                raise ValueError('%s: %s' % (key, e))

        uninitialized = { k:v for k,v in self.__attributes__().items() if isinstance(v, Attribute) }
        if len(uninitialized) != 0:
            if allow_missing:
                for key, value in uninitialized.items():
                    setattr(self, key, value(None))
            else:
                raise TypeError('missing attributes: %s' % uninitialized)

    def __str__(self):
        return str(self.__dict__)

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 fenc=utf-8
