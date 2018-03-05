# -*- coding: utf-8 -*-

import copy


Unset = Ellipsis


class ModelError(RuntimeError):
    def __str__(self):
        def format_arg(arg):
            return '- attribute: {}\n  value: "{}"\n  exception: {}'.format(
                arg[0].name if arg[0] else None, arg[1], arg[2]
            ).strip()

        return '{name}\n{errors}'.format(
            name=self.args[0],
            errors='\n'.join(
                format_arg(arg.args) for arg in self.args[1]
            )
        )


class Model(object):
    def __init__(self, mutable=True, hide_unset=False, drop_unknown=False, ignore_unknown=True):
        self.mutable = mutable
        self.hide_unset = hide_unset
        self.drop_unknown = drop_unknown
        self.ignore_unknown = ignore_unknown

    def __call__(self, model):
        old_init = getattr(model, '__init__', None)

        def new_init(cls, *args, **kwargs):
            exceptions = []

            for attribute in cls.__attributes__:
                if hasattr(cls, attribute.name):
                    if getattr(cls, attribute.name) is not Unset:
                        continue

                value = kwargs.pop(attribute.name,
                        kwargs.pop(attribute.alias, Unset))  # noqa: E128

                try:
                    attribute.fset(cls, value)
                except (AttributeError, ValueError) as e:
                    exception = AttributeError(attribute, value, e)
                    exception.__cause__ = None
                    exceptions.append(exception)

                if not self.mutable:
                    setattr(model, attribute.name,
                            property(fget=getattr(model, attribute.name).fget)
                            )

            if kwargs:
                if self.drop_unknown:
                    kwargs = {}
                elif not self.ignore_unknown:
                    exceptions.extend(
                        (AttributeError(None, v, 'Unknown attribute "%s"' % k) for k, v in kwargs.items())
                    )

            if exceptions:
                raise ModelError(cls.__class__.__name__, exceptions)

            if old_init:
                old_init(cls, *args, **kwargs)

        if old_init:
            new_init.__doc__ = old_init.__doc__

        def getitem(cls, key):
            for a in cls.__attributes__:
                if a.name == key or a.alias == key:
                    try:
                        return dict(getattr(cls, a.name))
                    except (ValueError, TypeError):
                        return getattr(cls, a.name)

            raise KeyError(key)

        model.__init__ = new_init
        model.__getitem__ = getitem

        model.__str__ = lambda cls: str(dict(cls))
        model.__repr__ = lambda cls: str(dict(cls))
        model.__ne__ = lambda cls, o: not cls.__eq__(o)
        model.__eq__ = lambda cls, o: (issubclass(o.__class__, cls.__class__) and dict(cls) == dict(o))
        model.__contains__ = lambda cls, key: getattr(cls, key) not in [None, Unset]
        model.keys = lambda cls: sorted(
            [a.alias or a.name for a in cls.__attributes__ if (
                getattr(cls, a.name) not in [None, Unset] or not self.hide_unset)]
        )

        return model


class Attribute(object):
    def __init__(self, name, type, optional=False, nullable=False, mutable=True, default=None, fdefault=None, alias=None, help=None, value_by_reference=False):
        self.name = name
        self.type = type
        self.default = default
        self.fdefault = fdefault
        self.optional = optional
        self.nullable = nullable
        self.mutable = mutable
        self.alias = alias
        self.help = help
        self.value_by_reference = value_by_reference

    def __repr__(self):
        return str(vars(self))

    def __call__(self, model):
        if not hasattr(model, '__attributes__'):
            model.__attributes__ = set()

        try:
            model.__attributes__.remove(next((a for a in model.__attributes__ if a.name == self.name)))
        except StopIteration:
            pass
        finally:
            model.__attributes__.add(self)

        setattr(model, self.value_name, Unset)

        prop = property(
            fget=self.fget,
            fset=self.fset if self.mutable else None,
            fdel=self.fdel if self.mutable else None,
            doc=self.help
        )

        setattr(model, self.name, prop)

        return model

    def fget(self, cls):
        return getattr(cls, self.value_name)

    def fset(self, cls, value):
        if value is Unset:
            if self.default is not None:
                value = self.default
            elif self.fdefault is not None:
                value = self.fdefault()

        setattr(cls, self.value_name, self.parse(value))

    def fdel(self, cls):
        setattr(cls, self.value_name, Unset)

    def get_default(self):
        if self.default is not None:
            return self.default
        elif self.fdefault is not None:
            return self.fdefault()
        else:
            raise AttributeError(self, "Attribute has not default")

    @property
    def value_name(self):
        return '_%s' % self.name

    def parse(self, value):
        if value is Unset:
            if self.optional:
                return value
            else:
                raise AttributeError(self, value, "Attribute is not optional")
        elif value is None:
            if self.nullable:
                return None
            else:
                value = self.get_default()

        if not self.value_by_reference:
            value = copy.deepcopy(value)

        if self.type is None:
            return value

        try:
            return self.type(**value)
        except TypeError:
            return self.type(value)

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 fenc=utf-8
