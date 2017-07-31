#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 29 00:15:42 2017

@author: johannes
"""

import unittest
import decorators


@decorators.type_checked
def test_func1(a: int, b: "nonsene", c: 1*1=list()) -> (1, 'hala'):
    pass


@decorators.type_checked
def test_func2(a, b: str, c=None, d: list=None):
    pass


correct1 = (1, "hello", [], [])
failures1 = [
        (1, 1, [], []),  # first annotation wrong
        (1, "hello", [], 1),  # second annotation wrong
        (1, 1, 1, 1)  # both annoations wrong
        ]

correct2 = {'a': 1, 'b': "hello", 'c': [], 'd': []}
failures2 = [
        {'a': 1, 'b': 1, 'c': [], 'd': []},  # first annotation wrong
        {'a': 1, 'b': 'hello', 'c': [], 'd': 1},  # second annotation wrong
        {'a': 1, 'b': 1, 'c': 1, 'd': 1},  # both annotations wrong
        ]


class TestTypeChecked(unittest.TestCase):

    def test_return_correct(self):
        """Raise no exception when return type is correct."""
        @decorators.type_checked
        def a() -> int:
            return 1
        a()

    def test_return_incorrect(self):
        '''Raise Type when return type incorrect.'''
        @decorators.type_checked
        def a() -> int:
            return "hello"
        with self.assertRaises(TypeError):
            a()

    def test_not_type_annotation(self):
        """Test that annotations that are not a type are beeing ignored."""
        test_func1(1, b=1)

    def test_only_positional_no_defaults_correct_arguments(self):
        test_func2(*correct1)

    def test_only_positional_no_defaults_wrong_arguments(self):
        for failure in failures1:
            with self.assertRaises(TypeError):
                test_func2(*failure)

    def test_only_positional_with_defaults_correct_arguments(self):
        test_func2(*correct1[:2])

    def test_only_positional_with_defaults_wrong_arguments(self):
        with self.assertRaises(TypeError):
            test_func2(1, 1)

    def test_only_kwarg_no_defaults_correct_arguments(self):
        test_func2(**correct2)

    def test_only_kwarg_no_defaults_wrong_arguments(self):
        for failure in failures2:
            with self.assertRaises(TypeError):
                test_func2(**failure)

    def test_only_kwarg_with_defaults_correct_arguments(self):
        correct = correct2.copy()
        del correct['c']
        del correct['d']
        test_func2(**correct2)

    def test_only_kwarg_with_defaults_wrong_arguments(self):
        with self.assertRaises(TypeError):
            test_func2(a=1, b=1)

    def test_keep_annotation_metadata(self):
        """Test that annotation metadata is not influenced."""
        def a(a: int=2):
            pass
        b = decorators.type_checked(a)
        self.assertEqual(a.__annotations__, b.__annotations__)

    def test_wrong_default_arguments(self):
        '''Test if wrong default arguments raise TypeError at function definition.'''
        with self.assertRaises(TypeError):
            @decorators.type_checked
            def test_func(a: int="hello"):
                pass

    def test_works_with_args_kwargs(self):
        '''TODO: Define behaviour when *args and **kwargs are beeing used.'''
        @decorators.type_checked
        def test_func(*args: int, **kwargs: int):
            pass
        test_func(1, 2, 3, b=4)


if __name__ == '__main__':
    unittest.main()
