simple_model
============

.. image:: https://travis-ci.org/AFriemann/simple_model.svg?branch=master
    :target: https://travis-ci.org/AFriemann/simple_model
.. image:: https://badge.fury.io/py/simple_model.svg
    :target: https://badge.fury.io/py/simple_model

As the name suggests, this is a very simple model framework. It can be used for data
validation and (de-)serialization.

**New** Head over to `v2 <https://github.com/AFriemann/simple_model/blob/master/README.v2.rst>`_ now!

Installation
------------

Install with pip::

    $ pip install --user simple_model

Usage
-----

This allows me to test the examples by taking care of sorting the dictionaries, it is not required for simple_model
to work:

.. code:: python

    >>> from pprint import pprint

Examples:

.. code:: python

    >>> from simple_model import Model, Attribute

    >>> class Data(Model):
    ...     name = Attribute(str)
    ...     some_value = Attribute(str, optional=True)
    ...     another_value = Attribute(int, fallback=0)

    >>> pprint(dict(Data(name = 'test', some_value = None, another_value = 12)))
    {'another_value': 12, 'name': 'test', 'some_value': None}

    >>> pprint(dict(Data(name = 'test')))
    {'another_value': 0, 'name': 'test', 'some_value': None}

    >>> init_dict = {'name': 'test', 'some_value': 'val', 'another_value': 3}
    >>> pprint(dict(Data(**init_dict)))
    {'another_value': 3, 'name': 'test', 'some_value': 'val'}

Initializing with missing attributes while not specifying them as optional or providing a fallback value
will result in a *ValueError* containing all failed attributes.
Note that *fallback* takes precedence over *optional*, specifying both is unnecessary.

Unknown values will be ignored

.. code:: python

    >>> pprint(dict(Data(name = 'test', unknown_value = True)))
    {'another_value': 0, 'name': 'test', 'some_value': None}


Serialization can be achieved easily, for example

.. code:: python

    >>> import json
    >>> def serialize(model):
    ...     return json.dumps(dict(model))

    >>> def deserialize(string):
    ...     return Data(**json.loads(string))

Since the Model class simply calls the Attribute class for each parameter and the Attribute class in turn calls the
given 'type', one could easily use functions instead of types to achieve more complex results and value parsing

.. code:: python

    >>> from datetime import datetime
    >>> def parse_date(string):
    ...     return datetime.strptime(string, '%Y-%m-%d')

    >>> class Data(Model):
    ...     date = Attribute(parse_date)

    >>> dict(Data(date='2015-11-20'))
    {'date': datetime.datetime(2015, 11, 20, 0, 0)}

Fallback values can also be given as functions

.. code:: python

    >>> def fun():
    ...     return "foo"

    >>> class Data(Model):
    ...     point = Attribute(str, fallback=fun)

    >>> dict(Data())
    {'point': 'foo'}

If you need to verify Lists of objects, use functions

.. code:: python

    >>> class Data(Model):
    ...     points = Attribute(lambda l: list(map(str, l)))

    >>> dict(Data(points=['abc', 'def', 'ghi']))
    {'points': ['abc', 'def', 'ghi']}

Or the included *list_type* helper class

.. code:: python

    >>> from simple_model.helpers import list_type
    >>> class Data(Model):
    ...     points = Attribute(list_type(str))

    >>> dict(Data(points=['abc', 'def', 'ghi']))
    {'points': ['abc', 'def', 'ghi']}

For more complex data, use Models to verify

.. code:: python

     >>> class SubData(Model):
     ...     some_value = Attribute(str)
     ...     some_other_value = Attribute(int)

     >>> class Data(Model):
     ...     point = Attribute(SubData)

     >>> pprint(dict(Data(point={'some_value': 'abc', 'some_other_value': 12})))
     {'point': {'some_other_value': 12, 'some_value': 'abc'}}

To allow uncommon names, use the Attribute name keyword

.. code:: python

    >>> class Data(Model):
    ...     point = Attribute(str, name='@point')

    >>> dict(Data(point='something'))
    {'@point': 'something'}

    >>> dict(Data(**{ '@point': 'something' }))
    {'@point': 'something'}

To easily check against expected values you can use the helper function *one_of*

.. code:: python

    >>> from simple_model.helpers import one_of
    >>> class Data(Model):
    ...     foo = Attribute(one_of('bar', 'foobar'))

    >>> dict(Data(foo='bar'))
    {'foo': 'bar'}

    >>> dict(Data(foo='foo')) # doctest: +ELLIPSIS
    Traceback (most recent call last):
        ...
    ValueError: {...'exception': "ValueError: must be one of ('bar', 'foobar') but was 'foo'"...}

If you want to disallow unknown values, set the __ignore_unknown__ attribute to False

.. code:: python

    >>> class Data(Model):
    ...     __ignore_unknown__ = False
    ...
    ...     point = Attribute(str)

    >>> Data(point = 'abc', other = 'def')
    Traceback (most recent call last):
        ...
    ValueError: Unknown key "other" with value "def"

You can now set Models to be mutable and change Attribute values after creation

.. code:: python

    >>> class Data(Model):
    ...     point = Attribute(int)

    >>> d = Data(point = 1)
    >>> d.point
    1
    >>> d.point = 2
    >>> d.point
    2
    >>> d.__mutable__ = False
    >>> d.point = 3
    Traceback (most recent call last):
        ...
    AttributeError: Model is immutable

Tests
-----

To run the tests use tox::

    $ tox

Issues
------

Please submit any issues on `GitHub <https://github.com/afriemann/simple_model/issues>`_.

Changelog
---------

see `CHANGELOG <https://github.com/AFriemann/simple_model/blob/master/CHANGELOG.rst>`_

License
-------

see `LICENSE <https://github.com/AFriemann/simple_model/blob/master/LICENSE.txt>`_
