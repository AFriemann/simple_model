#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
.. module:: simple_model
   :platform: Unix
   :synopsis: Simple models for easy data (de-)serialization and validation.

.. moduleauthor:: Aljosha Friemann a.friemann@automate.wtf

"""

import abc, logging, copy

__version__ = '<VERSION>'


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

    def get(self):
        return self.value

    def set(self, value):
        self.value = value

class Property(object):
    def __new__(self, ptype, name=None, alias=None, optional=False, fallback=None):
        backend = Attribute(ptype, name, alias, optional, fallback)

        def get_value(cls):
            return backend.value

        def set_value(cls, new_value):
            backend.value = new_value

        def del_value():
            del backend

        return property(get_value, set_value, del_value, "TODO: some property")

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
            if not self.mutable:
                raise AttributeError(
                    "can't set attribute '{}', {} is immutable".format(
                        name, self.__class__))

            return cls.properties.get(name).set(value)

        def pdel(cls):
            del self.properties[name]

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


# class Model(object):
#     __metaclass__  = abc.ABCMeta
#
#     __hide_unset__     = False
#     __ignore_unknown__ = True
#     __mutable__        = True
#
#     @property
#     def attributes(self):
#         for key in dir(self):
#             if key != 'attributes' and not key.startswith('_'):
#                 value = object.__getattribute__(self, key)
#
#                 if issubclass(type(value), Attribute):
#                     yield key, copy.deepcopy(value)
#
#     def __iter__(self):
#         for key, attribute in self.attributes:
#             name = attribute.name or key
#
#             if attribute.value is None and self.__hide_unset__:
#                 continue
#             elif isinstance(attribute.value, list):
#                 value = [ dict(v) if isinstance(v, Model) else v for v in attribute.value ]
#             elif isinstance(attribute.value, Model):
#                 value = dict(attribute.value)
#             else:
#                 value = attribute.value
#
#             yield name, value
#
#     def __contains__(self, item):
#         for key, _ in self.attributes:
#             if key == item:
#                 return True
#         return False
#
#     def __eq__(self, other):
#         return (isinstance(other, self.__class__) and dict(self) == dict(other))
#
#     def __ne__(self, other):
#         return not self.__eq__(other)
#
#     def __init__(self, **kwargs):
#         logger = logging.getLogger(__package__ + '.' + self.__class__.__name__)
#
#         failed_values = []
#
#         for key, attribute in self.attributes:
#             name = attribute.name or key
#             value = kwargs.get(name, kwargs.get(key, kwargs.get(attribute.alias)))
#
#             logger.debug('[{}] parsing attribute {} with value "{}"'.format(name, attribute, value))
#
#             try:
#                 attribute.value = value
#                 object.__setattr__(self, key, attribute)
#             except Exception as e:
#                 logger.warning('[{}] failed to parse value "{}" with {}'.format(name, value, attribute))
#
#                 failed_values.append(
#                     {
#                         'key': str(name),
#                         'attribute': str(attribute),
#                         'value': str(value),
#                         'exception': '{0}: {1}'.format(e.__class__.__name__, str(e))
#                     }
#                 )
#
#         if not self.__ignore_unknown__:
#             failed_values.extend([
#                 'Unknown key "{}" with value "{}"'.format(key, value)
#                 for key, value in kwargs.items() if key not in self
#             ])
#
#         if len(failed_values) != 0:
#             raise ValueError(*failed_values)
#
#     def __repr__(self):
#         return str(dict(self))
#
#     def __str__(self):
#         return str(dict(self))
#
#     def __getattribute__(self, name):
#         attr = object.__getattribute__(self, name)
#         if issubclass(type(attr), Attribute):
#             return attr.value
#         else:
#             return attr
#
#     def __setattr__(self, name, value):
#         try:
#             obj = object.__getattribute__(self, name)
#         except AttributeError:
#             obj = None
#
#         if issubclass(type(obj), Attribute):
#             if obj.value == value:
#                 return
#             elif not self.__mutable__:
#                 raise AttributeError('Model is immutable')
#
#             obj.value = value
#             value = obj
#
#         object.__setattr__(self, name, value)


from simple_model.helpers import list_type, one_of

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 fenc=utf-8
