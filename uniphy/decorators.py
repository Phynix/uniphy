#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 25 23:05:04 2017

@author: Johannes Lade, Jonas Eschle 'Mayou36'
"""

import inspect
from functools import wraps, lru_cache
from inspect import Parameter


# noinspection PyPep8Naming,PyRedundantParentheses
class type_checked():
    """Decorator for dynamic type checking with annotations.

    - Decorates functions, static methods and bound methods.
    - Each Parameter and the return value can be annotated with one expression of <class 'type'>.
    - Other expressions or missing annotations are ignored.
    - Default values are type checked once when the function is decorated.
    - All other annotations are checked once per function call.
    - Type checking of arguments, default values or the return value can be turned off separately.
    - Annotations for *args and **kwargs are ignored.
    - The effect of this decorator is turned of if __debug__ == False i.e. if python is run with the
    option -O.
    - Can be used as class Decorator to decorate each method of the class.

    Examples
    --------
    >>> @type_checked
    ... def foo(a : int, b : int = 3) -> int:
    ...     return a + b
    >>> @type_checked(check_defaults=False)
    ... def bar(a : int = 3.2):
    ...     pass
    >>> @type_checked()
    ... def knu(a : int = 3.2):
    ...     pass
    Traceback (most recent call last):
        ...
    TypeError: default argument a = 3.2 is not instance of <class 'int'>
    """

    # *args, **kwargs are ignored.
    ALLOWED_PARAMETER_KINDS = (
        Parameter.POSITIONAL_ONLY,
        Parameter.KEYWORD_ONLY,
        Parameter.POSITIONAL_OR_KEYWORD
    )

    def __new__(cls, *args, **kwargs):
        """Allows for usage of different syntax: @type_checked or @type_checked(...)

        Returns
        -------
        callable or type_checked
            Depending on how __new__ was called the wrapped function or an instance of type_checked is
            returned.

        Raises
        ------
        TypeError
            If illegal decorator argument was used.
        """
        self = super().__new__(cls)

        if (not args and not kwargs) \
                or (args and all(isinstance(value, bool) for value in args)) \
                or (kwargs and all(isinstance(value, bool) for value in kwargs.values())):
            # Called as @type_checked(...)
            return self
        elif args and callable(args[0]):
            # Called as @type_checked
            self.__init__()
            return self(args[0])
        else:
            raise TypeError("Illegal decorator arguments: args={}, kwargs={}".format(args, kwargs))

    def __init__(self, check_arguments=True, check_defaults=True, check_return=True):
        """Set decorator arguments.

        Parameters
        ----------
        check_arguments : bool
            Decides whether arguments should be checked at execution time.
        check_defaults : bool
            Decides whether default values should be checked at declaration.
        check_return : bool
            Decides whether the return value should be checked at execution time.
        """
        self.check_arguments = check_arguments
        self.check_defaults = check_defaults
        self.check_return = check_return

    def __call__(self, arg):
        """Decorates class or function.
        Parameters
        ----------
        arg : type or callable
            Class or function to decorate.

        Returns
        -------
        type or callable
            Decorated class or function.
        """
        if inspect.isclass(arg):
            # Called to decorate a class.
            return self.decorate_class(arg)
        else:
            # Called to decorate a function.
            return self.decorate_function(arg)

    def decorate_class(self, Cls):
        """Decorates a class.

        Parameters
        ----------
        Cls : type
            A class to be decorated

        Returns
        -------
        Decorated : type
            Decorated class.
        """
        class Decorated(Cls):
            @type_checked
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)

            @lru_cache(maxsize=None)
            def __getattribute__(self, item):
                """Checks if something is a method in an attribute lookup and decorates it with type_checked
                if this is the case.
                """
                item = super().__getattribute__(item)
                if inspect.ismethod(item):
                    return type_checked(item)
                else:
                    return item
        return Decorated

    def decorate_function(self, func):
        """Decorates a function or method.

        This is the core function of this class. All decorations are done with this class one way or another.

        Parameters
        ----------
        func : callable
            Function to be type checked.

        Returns
        -------
        decorated : callable
            Decorated function.

        Raises
        ------
        TypeError
            If default value does not match annotation.
        """
        # Turn off decorator when run in optimized mode. python -O
        if not __debug__:
            return func

        signature = inspect.signature(func)
        parameters = signature.parameters

        # Check type of default values.
        if self.check_defaults:
            for parameter in parameters.values():
                if parameter.default is not Parameter.empty \
                        and parameter.default is not None \
                        and self.__is_suitable_annotation(parameter.annotation) \
                        and not isinstance(parameter.default, parameter.annotation):
                    msg = 'default argument {} = {} is not instance of {}'
                    raise TypeError(msg.format(parameter.name, parameter.default,
                                               parameter.annotation))

        @wraps(func)
        def decorated(*args, **kwargs):
            bound_arguments = signature.bind(*args, **kwargs)
            all_args = bound_arguments.arguments

            # Check type of positional and keyword arguments.
            if self.check_arguments:
                for arg_name, value in all_args.items():
                    parameter = parameters[arg_name]
                    annotation = parameter.annotation
                    if parameter.kind in self.ALLOWED_PARAMETER_KINDS \
                            and self.__is_suitable_annotation(annotation) \
                            and not isinstance(value, annotation):
                        msg = 'argument {} = {} is not instance of {}'
                        raise TypeError(msg.format(arg_name, value, annotation))

            # Check type of return value.
            result = func(*args, **kwargs)
            if self.check_return:
                annotation = signature.return_annotation
                if self.__is_suitable_annotation(annotation) and not isinstance(result, annotation):
                    raise TypeError('expected {}, returned {}'.format(annotation, type(result)))
            return result

        return decorated


    @staticmethod
    def __is_suitable_annotation(annotation):
        """Checks whether annotation is specified and is a type.

        This checks if annotations is relevant for this decorator.
        """
        # Used for testing Parameter and Signature annotations. Might fail in the future due to
        # Parameter.empty != Signature.empty.
        return annotation is not Parameter.empty and isinstance(annotation, type)
