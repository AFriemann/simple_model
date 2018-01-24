# -*- coding: utf-8 -*-
"""
.. module:: simple_model.helpers
   :platform: Unix
   :synopsis: Helper functions and classes for simple_model.

.. moduleauthor:: Aljosha Friemann a.friemann@automate.wtf

"""


class list_type():
    def __init__(self, t):
        self.__type__ = t

    def __call__(self, lst):
        try:
            return [ self.__type__(**e) for e in lst ]
        except TypeError:
            return [ self.__type__(e) for e in lst ]

    def __repr__(self):
        return str({ 'list_type': self.__type__ })

    def __str__(self):
        return self.__repr__()


def one_of(*args):
    def f(value):
        if value not in args:
            raise ValueError('must be one of {} but was \'{}\''.format(args, value))
        return value
    return f

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 fenc=utf-8
