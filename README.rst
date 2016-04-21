simple_model
============

As the name says, this is a very simple model framework. It can be used for data
validation and (de-)serialization.

Installation
------------

Install with pip::

    $ pip install --user simple_model

Usage
-----

Examples::

    >>> from simple_model import Model, Attribute

    >>> class Data(Model):
    ...     name = Attribute(str)
    ...     some_value = Attribute(str, optional=True)
    ...     another_value = Attribute(int, fallback=0)

    >>> dict(Data(name = 'test', some_value = None, another_value = 12))
    { 'name': 'test', 'some_value': None, 'another_value': 12 }

    >>> dict(Data(name = 'test', allow_missing=True))
    { 'name': 'test', 'some_value': None, 'another_value': 0 }

    >>> dict(Data(name = 'test', unknown_value = True, allow_missing=True))
    { 'name': 'test', 'some_value': None, 'another_value': 0 }

    >>> init_dict = {'name': 'test', 'some_value': 'val', 'another_value': 3}
    >>> Data(**init_dict)
    { 'name': 'test', 'some_value': 'val', 'another_value': 3 }

Initializing with missing attributes while not specifying to allow
them will result in an *AssertionError*.

The default behaviour for missing attributes can be changed::

    >>> class Data(Model):
    ...     _allow_missing = True

Serialization can be achieved easily, for example::

    >>> import json
    >>> def serialize(model):
    ...     return json.dumps(dict(model))

    >>> def deserialize(string):
    ...     return Data(**json.loads(string))

Since the Model class simply calls the Attribute class for each parameter and the Attribute class in turn calls the
given 'type', one could easily use functions instead of types to achieve more complex results and value parsing::

    >>> from datetime import datetime
    >>> def parse_date(string):
    ...     return datetime.strptime(string, '%Y-%m-%d')

    >>> class Data(Model):
    ...     date = Attribute(parse_date)

    >>> dict(Data('2015-11-20'))
    { 'date': datetime.datetime(2015, 11, 20, 0, 0) }

Fallback values can also be given as functions ::

    >>> def fun():
    ...     return "foo"

    >>> class Data(Model):
    ...     point = Attribute(str, fallback=fun)

    >>> dict(Data(allow_missing=True))
    { 'point': 'foo' }

Tests
-----

To run the tests use tox::

    $ tox

Or run py.test manually (not recommended, needs simple_module installed)::

    $ py.test .
