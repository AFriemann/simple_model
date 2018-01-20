# -*- coding: utf-8 -*-
"""
.. module:: simple_model.v2
   :platform: Unix
   :synopsis: Simple decorator based models for easy data (de-)serialization and validation.

.. moduleauthor:: Aljosha Friemann a.friemann@automate.wtf

"""

import copy


Unset = Ellipsis


class ModelError(RuntimeError):
    def __str__(self):
        def format_arg(arg):
            return '- attribute: {}\n  value: "{}"\n  exception: {}'.format(*arg).strip()

        return '{name}\n{errors}'.format(
            name=self.args[0],
            errors='\n'.join(
                format_arg(arg) for arg in self.args[1]
            )
        )


class Model:
    def __init__(self, mutable=False, hide_unset=False, drop_unknown=False, ignore_unknown=True):
        self.mutable = mutable
        self.hide_unset = hide_unset
        self.drop_unknown = drop_unknown
        self.ignore_unknown = ignore_unknown

    def __call__(self, model):
        custom_init = getattr(model, '__init__', None)

        def __init__(cls, *args, **kwargs):
            # make this instance memory independent from it's class.
            cls.__attributes__ = copy.deepcopy(cls.__attributes__)

            errors = []

            for attribute in cls.__attributes__:
                if attribute.is_set():
                    # skip attributes that have already been set.
                    continue

                value = kwargs.pop(attribute.name, kwargs.pop(
                                   attribute.alias,
                                   Unset))

                try:
                    attribute.set(value=value)
                except (AttributeError, ValueError) as e:
                    errors.append((attribute, value, e))

                mutable = attribute.mutable or (self.mutable and attribute.mutable is None)

                prop = property(
                    fget=attribute.get,
                    fset=attribute.set if mutable else None,
                    fdel=attribute.unset if mutable else None,
                    doc=attribute.help
                )

                setattr(model, attribute.name, prop)

            if kwargs:
                if self.drop_unknown:
                    kwargs = {}
                elif not self.ignore_unknown:
                    errors.extend(
                        (None, v, AttributeError('Unknown attribute "%s"' % k)) for k, v in kwargs.items()
                    )

            if errors:
                raise ModelError(cls.__class__.__name__, errors)

            if custom_init:
                custom_init(cls, *args, **kwargs)

        if custom_init is not None:
            __init__.__doc__ = custom_init.__doc__

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
        model.__repr__ = lambda cls: str(dict(cls))
        model.__ne__ = lambda cls, o: not cls.__eq__(o)
        model.__eq__ = lambda cls, o: (isinstance(o, cls.__class__) and dict(cls) == dict(o))
        model.__contains__ = lambda cls, key: next((a for a in cls.__attributes__ if a.name == key and (a.is_set() or not self.hide_unset)), Unset) is not Unset
        model.keys = lambda cls: sorted([ a.alias or a.name for a in cls.__attributes__ if (a.is_set() or not self.hide_unset)])

        return model


class Attribute:
    def __init__(self, name, type, optional=False, nullable=False, default=None, fdefault=None, mutable=None, alias=None, help=None):
        self.name = name
        self.type = type
        self.default = default
        self.fdefault = fdefault
        self.optional = optional
        self.nullable = nullable
        self.mutable = mutable
        self.alias = alias
        self.help = help

        try:
            if self.default is not None:
                self.parse(self.default)
            elif self.fdefault is not None:
                self.parse(self.fdefault())
        except Exception as e:
            raise ValueError("Invalid default value(s) (%s/%s) for type %s" % (self.default, self.fdefault, self.type), e)

    def __call__(self, model):
        if not hasattr(model, '__attributes__'):
            model.__attributes__ = set()

        try:
            model.__attributes__.remove(next((a for a in model.__attributes__ if a.name == self.name)))
        except StopIteration:
            pass
        finally:
            model.__attributes__.add(self)

        return model

    def __repr__(self):
        return str(vars(self))

    def set(self, model=None, value=Unset):
        if value is Unset:
            try:
                value = self.get_default()
            except AttributeError as e:
                pass

        try:
            self.value = self.parse(value)
        except NotImplementedError as e:
            raise e
        except Exception as e:
            raise ValueError("Invalid value for Attribute: %s" % value, e)

    def get(self, model=None):
        try:
            return self.value
        except AttributeError as e:
            if not self.optional:
                raise e

    def unset(self, model=None):
        del self.value

    def parse(self, value):
        if value is Unset:
            if self.optional:
                return value
            else:
                raise ValueError("Non-optional attribute set with non-value.")
        elif value is None:
            if self.nullable:
                return None
            else:
                value = self.get_default()

        value = copy.deepcopy(value)

        if self.type is None:
            return value

        try:
            return self.type(**value)
        except TypeError:
            return self.type(value)

    def is_set(self):
        try:
            return self.value is not Unset
        except AttributeError:
            return False

    def get_default(self):
        if self.default is not None:
            return self.default
        elif self.fdefault is not None:
            return self.fdefault()
        else:
            raise AttributeError("Attribute has no default")

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 fenc=utf-8
