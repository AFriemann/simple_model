simple_model
============

.. image:: https://travis-ci.org/AFriemann/simple_model.svg?branch=master
    :target: https://travis-ci.org/AFriemann/simple_model
.. image:: https://badge.fury.io/py/simple_model.svg
    :target: https://badge.fury.io/py/simple_model

As the name suggests, this is a very simple model framework. It can be used for data
validation and (de-)serialization.

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

*Note*: casting Data to a dict as it is done here is unnecessary as well. However pprint does not sort models in
Python 2 without the cast for some reason.

Examples:

.. code:: python

    >>> from simple_model.v2 import Model, Attribute, ModelError

    >>> @Model(drop_unknown=True)
    ... @Attribute('name', type=str)
    ... @Attribute('some_value', type=str, optional=True, nullable=True)
    ... @Attribute('another_value', type=int, default=0)
    ... class Data(object):
    ...     pass

    >>> pprint(dict(Data(name = 'test', some_value = None, another_value = 12)))
    {'another_value': 12, 'name': 'test', 'some_value': None}

    >>> pprint(dict(Data(name = 'test')))
    {'another_value': 0, 'name': 'test', 'some_value': Ellipsis}

    >>> init_dict = {'name': 'test', 'some_value': 'val', 'another_value': 3}
    >>> pprint(dict(Data(**init_dict)))
    {'another_value': 3, 'name': 'test', 'some_value': 'val'}

Initializing with missing attributes while not specifying them as optional or providing a fallback value
will result in a *ValueError* containing all failed attributes.
Note that *fallback* takes precedence over *optional*, specifying both is unnecessary.

Unknown values will be ignored for Models with *drop_unknown* set to True

.. code:: python

    >>> pprint(dict(Data(name = 'test', unknown_value = True)))
    {'another_value': 0, 'name': 'test', 'some_value': Ellipsis}


Serialization can be achieved easily, for example

.. code:: python

    >>> import json
    >>> def serialize(model):
    ...     return json.dumps(model)

    >>> def deserialize(string):
    ...     return Data(**json.loads(string))

Since the Model class simply calls the Attribute class for each parameter and the Attribute class in turn calls the
given 'type', one could easily use functions instead of types to achieve more complex results and value parsing

.. code:: python

    >>> from datetime import datetime
    >>> def parse_date(string):
    ...     return datetime.strptime(string, '%Y-%m-%d')

    >>> @Model()
    ... @Attribute('date', type=parse_date)
    ... class Data(object):
    ...     pass

    >>> Data(date='2015-11-20')
    {'date': datetime.datetime(2015, 11, 20, 0, 0)}

Fallback values can also be given as functions

.. code:: python

    >>> def fun():
    ...     return "foo"

    >>> @Model()
    ... @Attribute('point', type=str, fdefault=fun)
    ... class Data(object):
    ...     pass

    >>> Data()
    {'point': 'foo'}

If you need to verify Lists of objects, use functions

.. code:: python

    >>> @Model()
    ... @Attribute('points', type=lambda l: list(map(str, l)))
    ... class Data(object):
    ...     pass

    >>> Data(points=['abc', 'def', 'ghi'])
    {'points': ['abc', 'def', 'ghi']}

Or the included *list_type* helper class

.. code:: python

    >>> from simple_model.helpers import list_type

    >>> @Model()
    ... @Attribute('points', type=list_type(str))
    ... class Data(object):
    ...     pass

    >>> Data(points=['abc', 'def', 'ghi'])
    {'points': ['abc', 'def', 'ghi']}

For more complex data, use Models to verify

.. code:: python

    >>> @Model()
    ... @Attribute('some_value', type=str)
    ... @Attribute('some_other_value', type=int)
    ... class SubData(object):
    ...     pass

    >>> @Model()
    ... @Attribute('point', type=SubData)
    ... class Data(object):
    ...     pass

    >>> pprint(dict(Data(point={'some_value': 'abc', 'some_other_value': 12})))
    {'point': {'some_other_value': 12, 'some_value': 'abc'}}

    >>> sub_data = SubData(some_value='abc', some_other_value=12)
    >>> pprint(dict(Data(point=sub_data)))
    {'point': {'some_other_value': 12, 'some_value': 'abc'}}

To allow uncommon names, use the Attribute name keyword

.. code:: python

    >>> @Model()
    ... @Attribute('point', type=str, alias='@point')
    ... class Data(object):
    ...     pass

    >>> Data(point='something')
    {'@point': 'something'}

    >>> Data(**{ '@point': 'something' })
    {'@point': 'something'}

To easily check against expected values you can use the helper function *one_of*

.. code:: python

    >>> from simple_model.helpers import one_of

    >>> @Model()
    ... @Attribute('foo', type=one_of('bar', 'foobar'))
    ... class Data(object):
    ...     pass

    >>> Data(foo='bar')
    {'foo': 'bar'}

    >>> Data(foo='foo') # doctest: +ELLIPSIS +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
        ...
    simple_model.v2.ModelError: Data
    - attribute: foo
      value: "foo"
      exception: must be one of ('bar', 'foobar') but was 'foo'

If you want to disallow unknown values, set the *ignore_unknown* attribute to False

.. code:: python

    >>> @Model(ignore_unknown=False)
    ... @Attribute('point', type=str)
    ... class Data(object):
    ...     pass

    >>> Data(point = 'abc', other = 'def') # doctest: +ELLIPSIS +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
        ...
    simple_model.v2.ModelError: Data
    - attribute: None
      value: "def"
      exception: Unknown attribute "other"

Models are mutable by default

.. code:: python

    >>> @Model()
    ... @Attribute('point', type=int)
    ... class Data(object):
    ...     pass

    >>> d = Data(point = 1)
    >>> d.point
    1
    >>> d.point = 2
    >>> d.point
    2

.. fix vim syntax issues: '

You can set Models to be immutable

.. code:: python

    >>> @Model(mutable=False)
    ... @Attribute('point', type=int)
    ... class Data(object):
    ...     pass

    >>> d = Data(point = 1)
    >>> d.point
    1
    >>> d.point = 2
    Traceback (most recent call last):
        ...
    AttributeError: can't set attribute

.. fix syntax: '

This can also be done on a per Attribute basis

.. code:: python

    >>> @Model()
    ... @Attribute('point', type=int, mutable=True)
    ... class Data(object):
    ...     pass

    >>> d = Data(point=12)
    >>> d.point
    12
    >>> d.point = 2
    >>> d.point
    2

Attributes can take a transformation function to execute when setting the value

.. code:: python

    >>> import hashlib

    >>> @Model()
    ... @Attribute('username', type=str)
    ... @Attribute('password', type=str, transformation=lambda s: hashlib.md5(s.encode()).hexdigest())
    ... class User(object):
    ...     pass

    >>> u = User(username='foobar', password='foobaz')
    >>> u.password
    '80338e79d2ca9b9c090ebaaa2ef293c7'

**Note**: This only works with new-style python classes, so make sure to inherit *object* if you're using python 2.

Tests
-----

To run the tests use tox::

    $ tox

Issues
------

Please submit any issues on `GitHub`_.

Changelog
---------

see `CHANGELOG`_

.. _CHANGELOG: CHANGELOG.rst
.. _GitHub: https://github.com/afriemann/simple_model/issues
