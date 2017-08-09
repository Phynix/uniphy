#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 29 00:15:42 2017

@author: Johannes Lade
"""

import unittest

from uniphy import decorators


@decorators.type_checked
def test_func1(a: int, b: "nonsene", c: 1*1 = "hello") -> (1, 'hala'):
    pass


@decorators.type_checked
def test_func2(a, b: str, c=None, d: list = None):
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
    @staticmethod
    def test_return_correct():
        """Raise no exception when return type is correct."""

        @decorators.type_checked
        def a() -> int:
            return 1

        a()

    def test_return_incorrect(self):
        """Raise Type when return type incorrect."""

        @decorators.type_checked
        def a() -> int:
            return "hello"

        with self.assertRaises(TypeError):
            a()

    @staticmethod
    def test_not_type_annotation():
        """Test that annotations that are not a type are beeing ignored."""
        test_func1(1, b=1)

    @staticmethod
    def test_only_positional_no_defaults_correct_arguments():
        test_func2(*correct1)

    def test_only_positional_no_defaults_wrong_arguments(self):
        for failure in failures1:
            with self.assertRaises(TypeError):
                test_func2(*failure)

    @staticmethod
    def test_only_positional_with_defaults_correct_arguments():
        test_func2(*correct1[:2])

    def test_only_positional_with_defaults_wrong_arguments(self):
        with self.assertRaises(TypeError):
            test_func2(1, 1)

    @staticmethod
    def test_only_kwarg_no_defaults_correct_arguments():
        test_func2(**correct2)

    def test_only_kwarg_no_defaults_wrong_arguments(self):
        for failure in failures2:
            with self.assertRaises(TypeError):
                test_func2(**failure)

    @staticmethod
    def test_only_kwarg_with_defaults_correct_arguments():
        correct = correct2.copy()
        del correct['c']
        del correct['d']
        test_func2(**correct2)

    def test_only_kwarg_with_defaults_wrong_arguments(self):
        with self.assertRaises(TypeError):
            test_func2(a=1, b=1)

    def test_keep_annotation_metadata(self):
        """Test that annotation metadata is not influenced."""

        def a(a: int = 2):
            pass

        b = decorators.type_checked(a)
        self.assertEqual(a.__annotations__, b.__annotations__)

    def test_wrong_default_arguments(self):
        """Test if wrong default arguments raise TypeError at function definition."""
        with self.assertRaises(TypeError):
            @decorators.type_checked
            def test_func(a: int = "hello"):
                pass

    @staticmethod
    def test_works_with_args_kwargs():
        """Test that *args and **kwargs are ignored."""

        @decorators.type_checked
        def test_func(*args: int, **kwargs: int):
            pass

        test_func(1, 2, 3, b=4)

    def test_bound_method_correct_annotation(self):
        """Test correct annotations for bound methods."""

        class CorrectAnnotation():
            @decorators.type_checked
            def bar(self, a: int):
                pass

        foo = CorrectAnnotation()
        # Call with correct argument.
        foo.bar(2)
        # Call with wrong argument.
        with self.assertRaises(TypeError):
            foo.bar("hello")

    def test_bound_method_wrong_return_value(self):
        """Test bound method with wrong return value."""

        class WrongReturnValue():
            @decorators.type_checked
            def bar(self) -> int:
                return "hello"

        foo = WrongReturnValue()
        with self.assertRaises(TypeError):
            foo.bar()

    def test_bound_method_wrong_default_values(self):
        """Test bound methods with a wrong default value."""
        with self.assertRaises(TypeError):
            class WrongDefaultValue():
                @decorators.type_checked
                def bar(self, a: int = "hello"):
                    pass

    def test_class_method_correct_annotation(self):
        """Test correct annotations for class methods."""

        class CorrectAnnotation():
            @classmethod
            @decorators.type_checked
            def bar(cls, a: int):
                pass

        # Call with correct argument.
        CorrectAnnotation.bar(2)
        # Call with wrong argument.
        with self.assertRaises(TypeError):
            CorrectAnnotation.bar("hello")

    def test_class_method_wrong_return_value(self):
        """Test clas method with wrong return value."""

        class WrongReturnValue():
            @classmethod
            @decorators.type_checked
            def bar(cls) -> int:
                return "hello"

        with self.assertRaises(TypeError):
            WrongReturnValue.bar()

    def test_class_method_wrong_default_values(self):
        """Test class methods with a wrong default value."""
        with self.assertRaises(TypeError):
            class WrongDefaultValue():
                @classmethod
                @decorators.type_checked
                def bar(cls, a: int = "hello"):
                    pass

    # def test_static_method(self):
    #     # Not tested yet because in principle equivalent to normal function.

    def test_decorator_arguments_no_arguments(self):
        """Test whether @type_checked is the same as @type_checked()"""

        def foo():
            pass

        # @type_checked
        decorated_without_brackets = decorators.type_checked(foo)
        # @type_checked()
        decorated_with_brackets = decorators.type_checked()(foo)
        # Test that same
        self.assertEqual(decorated_without_brackets.__wrapped__, decorated_with_brackets.__wrapped__)

    def test_decorator_arguments_positional_only(self):
        """"Test whether positional arguments work for decorator"""

        @decorators.type_checked(False, False, False)
        def foo(a: int, b: int = 2.3) -> int:
            return "hello"

        # Check all functionality turned off.
        foo(2.3)

        # Check only some functionality turned off.
        with self.assertRaises(TypeError):
            decorators.type_checked(False, True, False)(foo)

    def test_decorator_arguments_keyword_only(self):
        """"Test whether keyword arguments work for decorator"""

        @decorators.type_checked(check_arguments=False, check_defaults=False, check_return=False)
        def foo(a: int, b: int = 2.3) -> int:
            return "hello"

        # Check all functionality turned off.
        foo(2.3)

        # Check only some functionality turned off.
        with self.assertRaises(TypeError):
            decorators.type_checked(check_arguments=False, check_defaults=True, check_return=False)(foo)

    def test_decorator_arguements_positional_and_keyword(self):
        """"Test whether positional and keyword arguments mixed work for decorator"""

        @decorators.type_checked(False, check_defaults=False, check_return=False)
        def foo(a: int, b: int = 2.3) -> int:
            return "hello"

        # Check all functionality turned off.
        foo(2.3)

        # Check only some functionality turned off.
        with self.assertRaises(TypeError):
            decorators.type_checked(False, check_defaults=True, check_return=False)(foo)

    def test_decorator_arguments_wrong_arguments(self):
        def foo():
            pass

        with self.assertRaises(TypeError):
            decorators.type_checked(2)(foo)
        with self.assertRaises(TypeError):
            decorators.type_checked(check_arguments=2)

    def test_decorating_class_method_raises_type_error(self):
        @classmethod
        def foo():
            pass

        with self.assertRaises(TypeError):
            decorators.type_checked(foo)

    def test_decorating_static_method_raises_type_error(self):
        @staticmethod
        def foo():
            pass

        with self.assertRaises(TypeError):
            decorators.type_checked(foo)


if __name__ == '__main__':
    unittest.main()
