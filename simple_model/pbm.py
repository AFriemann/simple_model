# -*- coding: utf-8 -*-
"""
.. module: TODO
    :platform: TODO
    :synopsis: TODO

.. moduleauthor:: Aljosha Friemann a.friemann@automate.wtf
"""

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
    def attach_dyn_prop(instance, prop_name, prop):
        """
        Attach prop_fn to instance with name prop_name.
        Assumes that prop_fn takes self as an argument.
        Reference: https://stackoverflow.com/a/1355444/509706
        """
        class_name = instance.__class__.__name__ + 'Dynamic'
        child_class = type(class_name, (instance.__class__,), {prop_name: prop})

        instance.__class__ = child_class

    def __init__(self, **kwargs):
        mutable = self.mutable
        self.mutable = True

        self.__build_properties__()

        self._logger = logging.getLogger(__package__ + '.' + self.__class__.__name__)

        for key, attr in self.properties.items():
            setattr(self, key, kwargs.get(key))

        self.mutable = mutable

    def __build_properties__(self):
        for key in dir(self):
            attribute = fgetattr(self, key, Attribute)
            if attribute is not None:
                self.properties.update({key: attribute})
                self.attach_dyn_prop(key, self.__create_property__(key))

    def __create_property__(self, name):
        def pget(cls):
            return cls.properties.get(name).value

        def pset(cls, value):
            if not cls.mutable:
                raise AttributeError(
                    "can't set attribute '{}', {} is immutable".format(
                        name, self.__class__))

            cls.properties.get(name).value = value

        def pdel(cls):
            del cls.properties[name]

        return property(pget, pset if self.mutable else None, pdel)

    @property
    def properties(self):
        try:
            return self._properties
        except AttributeError:
            self._properties = dict()
            return self._properties

    @property
    def mutable(self):
        try:
            return self.__mutable__
        except AttributeError:
            self.__mutable__ = False
            return self.__mutable__

    @mutable.setter
    def mutable(self, value):
        self.__mutable__ = value

    def __valid_key__(self, key):
        return not (
            key.startswith('_') or key.endswith('_')
        )

    def __contains__(self, key):
        return key in self.properties


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 fenc=utf-8
