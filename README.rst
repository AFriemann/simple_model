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

    >>> dict(Data(name = 'test'))
    { 'name': 'test', 'some_value': None, 'another_value': 0 }

    >>> init_dict = {'name': 'test', 'some_value': 'val', 'another_value': 3}
    >>> Data(**init_dict)
    { 'name': 'test', 'some_value': 'val', 'another_value': 3 }

Initializing with missing attributes while not specifying them as optional or providing a fallback value
will result in an *ValueError*.
Note that *fallback* takes precedence over *optional*, specifying both is unnecessary.

Unknown values will be ignored::

    >>> dict(Data(name = 'test', unknown_value = True))
    { 'name': 'test', 'some_value': None, 'another_value': 0 }


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

    >>> dict(Data())
    { 'point': 'foo' }

If you need to verify Lists of objects, use the provided *AttributeList* class::

     >>> class Data(Model):
     ...     point = AttributeList(str)

     >>> dict(Data(point=['abc', 'def', 'ghi']))
     { 'point': ['abc', 'def', 'ghi'] }

For more complex data, use Models to verify::

     >>> class SubData(Model):
     ...     some_value = AttributeList(str)

     >>> class Data(Model):
     ...     point = Attribute(SubData)

     >>> dict(Data(point={'some_value': ['abc', 'def', 'ghi']}))
     { 'point': ['abc', 'def', 'ghi'] }
        
Tests
-----

To run the tests use tox::

    $ tox

Or run py.test manually (not recommended, needs simple_module installed)::

    $ py.test .
