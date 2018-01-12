# -*- coding: utf-8 -*-
"""
.. module: TODO
    :platform: TODO
    :synopsis: TODO

.. moduleauthor:: Aljosha Friemann a.friemann@automate.wtf
"""

import abc
import logging
import copy

from simple_model.v1.attribute import Attribute


class Model(object):
    __metaclass__ = abc.ABCMeta

    __hide_unset__ = False
    __ignore_unknown__ = True
    __mutable__ = True

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

    def __contains__(self, item):
        for key, _ in self.attributes:
            if key == item:
                return True
        return False

    def __eq__(self, other):
        return (isinstance(other, self.__class__) and dict(self) == dict(other))

    def __ne__(self, other):
        return not self.__eq__(other)

    def __init__(self, **kwargs):
        logger = logging.getLogger(__package__ + '.' + self.__class__.__name__)

        failed_values = []

        for key, attribute in self.attributes:
            name = attribute.name or key
            value = kwargs.get(name, kwargs.get(key, kwargs.get(attribute.alias)))

            logger.debug('[{}] parsing attribute {} with value "{}"'.format(name, attribute, value))

            try:
                attribute.value = value
                object.__setattr__(self, key, attribute)
            except Exception as e:
                logger.warning('[{}] failed to parse value "{}" with {}'.format(name, value, attribute))

                failed_values.append(
                    {
                        'key': str(name),
                        'attribute': str(attribute),
                        'value': str(value),
                        'exception': '{0}: {1}'.format(e.__class__.__name__, str(e))
                    }
                )

        if not self.__ignore_unknown__:
            failed_values.extend([
                'Unknown key "{}" with value "{}"'.format(key, value)
                for key, value in kwargs.items() if key not in self
            ])

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

    def __setattr__(self, name, value):
        try:
            obj = object.__getattribute__(self, name)
        except AttributeError:
            obj = None

        if issubclass(type(obj), Attribute):
            if obj.value == value:
                return
            elif not self.__mutable__:
                raise AttributeError('Model is immutable')

            obj.value = value
            value = obj

        object.__setattr__(self, name, value)


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 fenc=utf-8
