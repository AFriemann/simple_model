# -*- coding: utf-8 -*-
"""
.. module: TODO
    :platform: TODO
    :synopsis: TODO

.. moduleauthor:: Aljosha Friemann a.friemann@automate.wtf
"""

import copy
import logging

from simple_model import Attribute


def fgetattr(obj, key, otype=None):
    try:
        attr = getattr(obj, key)
    except AttributeError:
        return None

    if otype is not None:
        if type(attr) is not otype:
            return None

    return attr

class Model(object):
    def __init__(self, **kwargs):
        mutable = self.mutable
        self.mutable = True

        self.__class__ = type(
            self.__class__.__name__ + 'Dyn',
            (self.__class__,),
            { key: self.__create_property__(key) for key in self.attributes }
        )

        self._logger = logging.getLogger(__package__ + '.' + self.__class__.__name__)

        errors = []
        for key, attr in self.attributes.items():
            value = kwargs.get(key, kwargs.get(attr.alias))
            try:
                setattr(self, key, value)
            except Exception as e:
                errors.append('Failed attribute `{}` {} with value {}: {}'.format(key, attr, value, e))

        if not self.ignore_unknown:
            for key, value in kwargs.items():
                if key not in self:
                    errors.append(
                        "Unknown key `{}` with value `{}`".format(key, value)
                    )

        if errors:
            raise ValueError(*errors)

        self.mutable = mutable

    @property
    def ignore_unknown(self):
        try:
            return self.__ignore_unknown__
        except AttributeError:
            self.__ignore_unknown__ = True
            return self.__ignore_unknown__

    @ignore_unknown.setter
    def ignore_unknown(self, value):
        self.__ignore_unknown__ = value

    @property
    def mutable(self):
        try:
            return self.__mutable__
        except AttributeError:
            self.__mutable__ = True
            return self.__mutable__

    @mutable.setter
    def mutable(self, value):
        self.__mutable__ = value

    @property
    def hide_unset(self):
        try:
            return self.__hide_unset__
        except AttributeError:
            self.__hide_unset__ = False
            return self.__hide_unset__

    @hide_unset.setter
    def hide_unset(self, value):
        self.__hide_unset__ = value

    def __iter__(self):
        for key in self.attributes:
            value = getattr(self, key)
            if value is None and self.hide_unset:
                continue
            elif issubclass(type(value), Model):
                value = dict(value)
            yield key, value

    def __contains__(self, key):
        return key in self.attributes

    def __eq__(self, other):
        try:
            return (dict(self) == dict(other))
        except TypeError:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    @property
    def attributes(self):
        try:
            return self.__attributes
        except AttributeError:
            self.__attributes = self.__copy_attributes__()
            return self.__attributes

    def __copy_attributes__(self):
        attributes = copy.deepcopy({
            key: fgetattr(self, key, Attribute) for key in dir(self)
            if (not key.startswith('__') and key != 'attributes' and
                fgetattr(self, key, Attribute) is not None)
        })
        return attributes

    def __create_property__(self, name):
        def pget(cls):
            return cls.attributes.get(name).value

        def pset(cls, value):
            if not cls.mutable:
                raise AttributeError(
                    "can't set attribute '{}', {} is immutable".format(
                        name, self.__class__))

            cls.attributes.get(name).value = value

        def pdel(cls):
            del cls.attributes[name]

        return property(pget, pset if self.mutable else None, pdel)


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 fenc=utf-8
