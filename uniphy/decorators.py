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

    + Each Parameter and the return value can be annotated with one expression of <class 'type'>.
    + Other expressions or missing annotations are ignored.
    + Default values are type checked once the decorator is used for the first time.
    + All other annotations are checked once per function call.
    + Type checking of arguments, default values or the return value can be turned off separately.
    + Annotations for *args and **kwargs are ignored.
    """

    # *args, **kwargs are ignored.
    ALLOWED_PARAMETER_KINDS = (
        Parameter.POSITIONAL_ONLY,
        Parameter.KEYWORD_ONLY,
        Parameter.POSITIONAL_OR_KEYWORD
    )

    def __new__(cls, *args, **kwargs):
        self = super().__new__(cls)

        if not args or isinstance(args[0], bool):
            # Called as @type_checked(...)
            return self
        elif callable(args[0]):
            # Called as @type_checked
            msg = "type_checked must be called with brackets like this type_checked() and can only accept booleans."
            raise SyntaxError(msg)
        else:
            raise TypeError("Illegal decorator argument: {}".format(args[0]))

    def __init__(self, check_arguments=True, check_defaults=True, check_return=True):
        """
        Parameters
        ----------
        check_arguments : bool
            Decided wheter arguments should be checked at execution time.
        check_defaults : bool
            Decides whether default values should be checked at declaration.
        check_return : bool
            Decides whether the return value should be checked at execution time.
        """
        self.check_arguments = check_arguments
        self.check_defaults = check_defaults
        self.check_return = check_return

    def __call__(self, func):
        """
        Parameters
        ----------
        func : callable
            Function to be type checked.

        Returns
        -------
        wrapper : callable
            Decorated function.
        """
        signature = inspect.signature(func)
        parameters = signature.parameters

        # Check type of default values.
        if self.check_defaults:
            for parameter in parameters.values():
                if (parameter.default is not Parameter.empty
                    and parameter.default is not None
                    and self.__is_suitable_annotation(parameter.annotation)
                    and not isinstance(parameter.default, parameter.annotation)):
                    msg = 'default argument {}={} is not instance of {}'
                    raise TypeError(msg.format(parameter.name, parameter.default,
                                               parameter.annotation))

        @wraps(func)
        def wrapper(*args, **kwargs):
            bound_arguments = signature.bind(*args, **kwargs)
            all_args = bound_arguments.arguments

            # Check type of positional and keyword arguments.
            if self.check_arguments:
                for arg_name, value in all_args.items():
                    parameter = parameters[arg_name]
                    annotation = parameter.annotation
                    if (parameter.kind in self.ALLOWED_PARAMETER_KINDS
                        and self.__is_suitable_annotation(annotation)
                        and not isinstance(value, annotation)):
                        msg = 'argument {}={} is not instance of {}'
                        raise TypeError(msg.format(arg_name, value, annotation))

            # Check type of return value.
            result = func(*args, **kwargs)
            if self.check_return:
                annotation = signature.return_annotation
                if self.__is_suitable_annotation(annotation) and not isinstance(result, annotation):
                    raise TypeError('expected {}, returned {}'.format(annotation, type(result)))
            return result

        return wrapper

    @staticmethod
    def __is_suitable_annotation(annotation):
        """Checks wether annotation is specified and is a type.

        This is supposed to prevent other python expressions in annotations
        from crashing this decorator.
        """
        return annotation is not Parameter.empty and isinstance(annotation, type)
