#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
.. module:: TODO
   :platform: Unix
   :synopsis: TODO.

.. moduleauthor:: Aljosha Friemann aljosha.friemann@gmail.com

"""

__version__ = '0.1.6'

import abc, logging

from simple_model.decorators import deprecated

__logger__ = logging.getLogger(__name__)

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
        elif type(value) is self._type:
            return value
        else:
            try: return self._type(**value)
            except: return self._type(value)

    def __iter__(self):
        yield 'class', self.__class__.__name__
        yield 'type', self._type
        yield 'optional', self._optional
        yield 'fallback', self._fallback

    def __str__(self):
        return str(dict(self))

class AttributeList(Attribute):
    def __call__(self, lst):
        if lst is None:
            if self._fallback is not None:
                try: lst = self._fallback()
                except TypeError: lst = self._fallback
            elif self._optional:
                lst = []
            else:
                raise ValueError('attribute list must not be None')

        result = []
        for value in lst:
            result.append(Attribute.__call__(self, value))
        return result

class Model(object):
    __metaclass__ = abc.ABCMeta

    @deprecated('__attributes__ is deprecated, please use cast to dict instead')
    def __attributes__(self):
        return dict(self)

    def __iter__(self):
        for key in dir(self):
            if not key.startswith('_'):
                value = getattr(self, key)
                if isinstance(value, list): value = [ dict(v) if isinstance(v, Model) else v for v in value ]
                if isinstance(value, Model): value = dict(value)
                yield key, value

    def __eq__(self, other):
        return (isinstance(other, self.__class__)
            and vars(self) == vars(other))

    def __ne__(self, other):
        return not self.__eq__(other)

    def __init__(self, **kwargs):
        failed_values = []
        for name, attribute in dict(self).items():
            value = kwargs.get(name)
            __logger__.debug('parsing attribute %s %s with value "%s"' % (name, attribute, value))
            try:
                setattr(self, name, attribute(value))
            except Exception as e:
                __logger__.debug('failed to parse value "%s" with %s' % (value, attribute))
                failed_values.append({ 'key': str(name), 'attribute': str(attribute), 'value': str(value), 'exception': '%s: %s' % (e.__class__.__name__, str(e)) })
        assert len(failed_values) == 0, "failed to parse data: %s" % failed_values

    def __str__(self):
        return str(vars(self))

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 fenc=utf-8
