# -*- coding: utf-8 -*-
"""
.. module:: simple_model.v2
   :platform: Unix
   :synopsis: Simple decorator based models for easy data (de-)serialization and validation.

.. moduleauthor:: Aljosha Friemann a.friemann@automate.wtf

"""


class ModelError(RuntimeError):
    def __str__(self):
        def format_arg(arg):
            return '''
            - attribute: {}
              value: {}
              exception: {}
            '''.format(*arg)

        return '{name}:\n{errors}'.format(
            name=self.args[0],
            errors='\n'.join(
                format_arg(arg) for arg in self.args[1]
            )
        )


class Model:
    def __call__(self, model):
        model.__slots__ = set((a.name for a in model.__attributes__))

        def __init__(cls, **kwargs):
            errors = []

            for attribute in cls.__attributes__:
                value = kwargs.get(attribute.name, None)

                if value is None and attribute.alias is not None:
                    value = kwargs.get(attribute.alias, None)

                try:
                    attribute.set(value=value)

                    prop = property(
                        fget=attribute.get,
                        fset=attribute.set if self.mutable and attribute.mutable else None,
                        fdel=attribute.unset if self.mutable and attribute.mutable else None,
                        doc=attribute.help
                    )

                    setattr(model, attribute.name, prop)
                except (AttributeError, ValueError) as e:
                    errors.append((attribute, value, e))

            if errors:
                raise ModelError(cls.__class__.__name__, errors)

        def __getitem__(cls, key):
            for attribute in cls.__attributes__:
                if attribute.name == key or attribute.alias == key:
                    try:
                        return dict(attribute.get())
                    except (ValueError, TypeError):
                        return attribute.get()

            raise KeyError(key)

        model.__init__ = __init__
        model.__getitem__ = __getitem__
        model.__str__ = lambda cls: str(dict(cls))
        model.__ne__ = lambda cls, o: not cls.__eq__(o)
        model.__eq__ = lambda cls, o: (isinstance(o, cls.__class__) and dict(cls) == dict(o))
        model.__contains__ = lambda cls, key: bool([a for a in cls.__attributes__ if a.name == key])
        model.keys = lambda cls: [ a.name for a in cls.__attributes__]

        return model

    def __init__(self, mutable=False, hide_unset=False):
        self.mutable = mutable
        self.hide_unset = hide_unset


class Attribute:
    def __call__(self, model):
        if not hasattr(model, '__attributes__'):
            model.__attributes__ = []

        model.__attributes__.append(self)

        return model

    def __init__(self, name, type, default=None, optional=False, mutable=True, alias=None, help=None):
        self.name = name
        self.type = type
        self.default = default
        self.optional = optional
        self.mutable = mutable
        self.alias = alias
        self.help = help

    def __repr__(self):
        return str(vars(self))

    def set(self, model=None, value=None):
        if self.type is None:
            self.value = value
        elif value is None:
            if self.optional:
                self.value = None
            elif self.default is not None:
                self.value = self.type(self.default)
            else:
                raise ValueError("Missing value for required Attribute")
        else:
            try:
                if hasattr(self.type, '__attributes__'):
                    self.value = self.type(**value)
                else:
                    self.value = self.type(value)
            except (ValueError, TypeError) as e:
                raise ValueError("Invalid value for Attribute: %s" % value, e)

    def get(self, model=None):
        try:
            return self.value
        except AttributeError:
            pass

    def unset(self, model=None):
        self.value = None

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 fenc=utf-8
