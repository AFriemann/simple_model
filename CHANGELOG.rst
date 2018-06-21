Changelog
=========

1.3.0
-----
* transformation function attribute added to Attribute class

1.2.0
-----
* added decorator based v2 version

1.1.4
-----
* It should now be possible to set Model attributes after initialization

1.1.3
-----
* changed Model logger so simple_model logs can be turned off easily

1.1.2
-----
* can now change model attributes correctly after initialization
* added Model class attribute __mutable__ to allow locking Attributes

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
