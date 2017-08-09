#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 25 23:05:04 2017

@author: Johannes Lade, Jonas Eschle 'Mayou36'
"""

import inspect
from functools import wraps
from inspect import Parameter


class type_checked():
    """Decorator for dynamic type checking with annotations.

    - Decorates functions, static methods and bound methods.
    - Each Parameter and the return value can be annotated with one expression of <class 'type'>.
    - Other expressions or missing annotations are ignored.
    - Default values are type checked once when the function is decorated.
    - All other annotations are checked once per function call.
    - Type checking of arguments, default values or the return value can be turned off separately.
    - Annotations for *args and **kwargs are ignored.

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
            return self.__call__(args[0])
        else:
            raise TypeError("Illegal decorator arguments: args={}, kwargs={}".format(args, kwargs))

    def __init__(self, check_arguments=True, check_defaults=True, check_return=True):
        """Sets decorator arguments.

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

    def __call__(self, func):
        """Decorates the function.

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
        """Checks wether annotation is specified and is a type.

        This is supposed to prevent other python expressions in annotations
        from crashing this decorator.
        """
        # Used for testing Parameter and Signature annotations. Might fail in the future due to
        # Parameter.empty != Signature.empty.
        return annotation is not Parameter.empty and isinstance(annotation, type)
