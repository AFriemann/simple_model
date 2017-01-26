#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
.. module:: TODO
   :platform: Unix
   :synopsis: TODO.

.. moduleauthor:: Aljosha Friemann aljosha.friemann@gmail.com

"""

import abc, logging, copy

__version__ = '1.0.2'

class Attribute(object):
    __type__     = None
    __name__     = None
    __alias__    = None
    __default__  = None
    __value__    = None
    __optional__ = False

    def __init__(self, t, name=None, alias=None, optional=False, fallback=None):
        if t is None:
            raise ValueError('attribute type can not be None')

        self.__type__     = t
        self.__name__     = name
        self.__alias__    = alias
        self.__default__  = fallback
        self.__optional__ = optional

    def __iter__(self):
        yield 'class', self.__class__.__name__
        yield 'name', self.__name__
        yield 'type', self.__type__
        yield 'default', self.__default__
        yield 'optional', self.__optional__
        yield 'alias', self.__alias__

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

class Model(object):
    __metaclass__  = abc.ABCMeta
    __hide_unset__ = False

    @property
    def attributes(self):
        for key in dir(self):
            if key != 'attributes' and not key.startswith('_'):
                value = object.__getattribute__(self, key)

                if issubclass(type(value), Attribute):
                    yield key, copy.deepcopy(value)

    def __iter__(self):
        for key, attribute in self.attributes:
            name = attribute.name or key

            if attribute.value is None and self.__hide_unset__:
                continue
            elif isinstance(attribute.value, list):
                value = [ dict(v) if isinstance(v, Model) else v for v in attribute.value ]
            elif isinstance(attribute.value, Model):
                value = dict(attribute.value)
            else:
                value = attribute.value

            yield name, value

    def __eq__(self, other):
        return (isinstance(other, self.__class__) and dict(self) == dict(other))

    def __ne__(self, other):
        return not self.__eq__(other)

    def __init__(self, **kwargs):
        logger = logging.getLogger(self.__class__.__name__)

        failed_values = []

        for key, attribute in self.attributes:
            name = attribute.name or key
            value = kwargs.get(name) or kwargs.get(key) or kwargs.get(attribute.alias)

            logger.debug('parsing attribute {0} {1} with value "{2}"'.format(name, attribute, value))

            try:
                setattr(self, key, attribute(value))
            except Exception as e:
                logger.warning('failed to parse value "{0}" with {1}'.format(value, attribute))

                failed_values.append(
                    {
                        'key': str(name),
                        'attribute': str(attribute),
                        'value': str(value),
                        'exception': '{0}: {1}'.format(e.__class__.__name__, str(e))
                    }
                )

        if len(failed_values) != 0:
            raise ValueError(*failed_values)

    def __repr__(self):
        return str(dict(self))

    def __str__(self):
        return str(dict(self))

    def __getattribute__(self, name):
        attr = object.__getattribute__(self, name)
        if issubclass(type(attr), Attribute):
            return attr.value
        else:
            return attr

from simple_model.helpers import list_type

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 fenc=utf-8
