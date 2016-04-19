#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
.. module:: TODO
   :platform: Unix
   :synopsis: TODO.

.. moduleauthor:: Aljosha Friemann aljosha.friemann@gmail.com

"""

import warnings, functools

def deprecated(msg):
    """This is a decorator which can be used to mark functions
    as deprecated. It will result in a warning being emmitted
    when the function is used.
    """
    def function_with_warning(f):
        def new_function(*args, **kwargs):
            warnings.warn(msg, category=DeprecationWarning)
            return f(*args, **kwargs)
        new_function.__name__ = f.__name__
        new_function.__doc__ = f.__doc__
        new_function.__dict__.update(f.__dict__)
        return new_function
    return function_with_warning

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 fenc=utf-8
