Changelog
=========

1.1.1
-----
* fixed problem with falsy attribute values

1.1.0
-----
* can now disallow unkown fields

1.0.2
-----
* moved list_type class to helpers module
* added one_of helper function

1.0.1
-----
* Model will now raise ValueError for failed attributes with a list instead of a string.
* Attributes now allow an alias as keyword argument.

1.0.0
-----
* removed the AttributeList class, use functions instead.
* Model Attributes can now be named. To allow this we keep the Attribute object and store the value.
