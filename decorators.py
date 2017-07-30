#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 25 23:05:04 2017

@author: johannes
"""

import inspect
from inspect import Parameter
from functools import wraps


def type_checked(func):

    def is_suitable_annotation(annotation):
        '''Checks wether annotation is specified and is a type.

        This is supposed to prevent other python expressions in annotations
        from crashing this decorator.'''
        return annotation is not Parameter.empty and type(annotation) is type

    signature = inspect.signature(func)
    parameters = signature.parameters

    # Check type of default values.
    for parameter in parameters.values():
        if (parameter.default is not Parameter.empty
            and parameter.default is not None
            and is_suitable_annotation(parameter.annotation)
            and not isinstance(parameter.default, parameter.annotation)):
            msg = 'default argument {}={} is not instance of {}'
            raise TypeError(msg.format(parameter.name, parameter.default,
                                        parameter.annotation))

    @wraps(func)
    def wrapper(*args, **kwargs):
        bound_arguments = signature.bind(*args, **kwargs)
        all_args = bound_arguments.arguments

        # Check type of positional and keyword arguments.
        for arg_name, value in all_args.items():
            annotation = parameters[arg_name].annotation
            if is_suitable_annotation(annotation) and not isinstance(value, annotation):
                msg = 'argument {}={} is not instance of {}'
                raise TypeError(msg.format(arg_name, value, annotation))

        # Check type of return value.
        result = func(*args, **kwargs)
        annotation = signature.return_annotation
        if is_suitable_annotation(annotation) and not isinstance(result, annotation):
            raise TypeError('expected {}, returned {}'.format(annotation, type(result)))
        return result

    return wrapper


if __name__ == '__main__':
    import unittest
    from decorators_test import type_checked_test
    unittest.main()