#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 29 00:15:42 2017

@author: Johannes Lade
"""

import unittest
from collections import OrderedDict

from uniphy import decorators


class TestTypeChecked(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.decorator_arg_type_err_regex = r'^Illegal decorator arguments: args=\(.{0,}?\), kwargs={.{0,}?}$'
        cls.default_type_error_regex = r'^default argument .{1,}? is not instance of .{2,}?$'
        cls.argument_type_error_regex = r'^argument .{1,}? is not instance of .{2,}?$'
        cls.return_type_error_regex = r'^expected .{2,}?, returned .{2,}?$'
        cls.correct_args = (1, "hello", [], [])
        cls.correct_kwargs = OrderedDict(a=1, b="hello", c=[], d=[])

    @staticmethod
    @decorators.type_checked
    def generic_testing_function(a, b: str, c=None, d: list = None):
        """Generic testing function for type_checked decorator."""
        pass

    @staticmethod
    def test_return_correct():
        """Raise no exception when return type is correct."""

        # noinspection PyMissingOrEmptyDocstring
        @decorators.type_checked
        def a() -> int:
            return 1

        a()

    def test_return_incorrect(self):
        """Raise TypeError when return type incorrect."""

        # noinspection PyMissingOrEmptyDocstring
        @decorators.type_checked
        def a() -> int:
            return "hello"

        with self.assertRaisesRegex(TypeError, self.return_type_error_regex):
            a()

    @staticmethod
    def test_not_type_annotation():
        """Test that annotations that are not a type are being ignored."""
        # noinspection PyMissingOrEmptyDocstring
        @decorators.type_checked
        def nonsense_annotation(a: int, b: "nonsense", c: 1*1 = "hello") -> (1, 'more_nonsense'):
            pass
        nonsense_annotation(1, b=1)

    def test_only_positional_no_defaults_correct_arguments(self):
        self.generic_testing_function(*self.correct_args)

    def test_only_positional_no_defaults_wrong_arguments(self):
        faulty_args = [
            (1, 1, [], []),  # first annotation wrong
            (1, "hello", [], 1),  # second annotation wrong
            (1, 1, 1, 1)  # both annotations wrong
        ]
        for failure in faulty_args:
            with self.subTest(failure=failure), self.assertRaisesRegex(TypeError,
                                                                       self.argument_type_error_regex):
                self.generic_testing_function(*failure)

    def test_only_positional_with_defaults_correct_arguments(self):
        self.generic_testing_function(*self.correct_args[:2])

    def test_only_positional_with_defaults_wrong_arguments(self):
        with self.assertRaisesRegex(TypeError, self.argument_type_error_regex):
            self.generic_testing_function(1, 1)

    def test_only_kwarg_no_defaults_correct_arguments(self):
        self.generic_testing_function(**self.correct_kwargs)

    def test_only_kwarg_no_defaults_wrong_arguments(self):
        faulty_kwargs = [
            OrderedDict(a=1, b=1, c=[], d=[]),  # first annotation wrong
            OrderedDict(a=1, b='hello', c=[], d=1),  # second annotation wrong
            OrderedDict(a=1, b=1, c=1, d=1),  # both annotations wrong
        ]
        for failure in faulty_kwargs:
            with self.subTest(failure=failure), \
                 self.assertRaisesRegex(TypeError, self.argument_type_error_regex):
                self.generic_testing_function(**failure)

    def test_only_kwarg_with_defaults_correct_arguments(self):
        correct = self.correct_kwargs.copy()
        del correct['c']
        del correct['d']
        self.generic_testing_function(**correct)

    def test_only_kwarg_with_defaults_wrong_arguments(self):
        with self.assertRaisesRegex(TypeError, self.argument_type_error_regex):
            self.generic_testing_function(a=1, b=1)

    def test_keep_annotation_metadata(self):
        """Test that annotation metadata is not influenced."""

        # noinspection PyMissingOrEmptyDocstring
        def naked_function(a: int = 2):
            pass

        decorated_function = decorators.type_checked(naked_function)
        self.assertEqual(naked_function.__annotations__, decorated_function.__annotations__)

    def test_wrong_default_arguments(self):
        """Test if wrong default arguments raise TypeError at function definition."""
        with self.assertRaisesRegex(TypeError, self.default_type_error_regex):
            # noinspection PyMissingOrEmptyDocstring
            @decorators.type_checked
            def wrong_default(a: int = "hello"):
                pass

    @staticmethod
    def test_works_with_args_kwargs():
        """Test that *args and **kwargs are ignored."""

        # noinspection PyMissingOrEmptyDocstring
        @decorators.type_checked
        def ignore_args_kwargs(*args: int, **kwargs: int):
            pass

        ignore_args_kwargs(1, 2, 3, b=4)

    # noinspection PyMissingOrEmptyDocstring
    def test_bound_method_correct_annotation(self):
        """Test correct annotations for bound methods."""

        # noinspection PyRedundantParentheses
        class CorrectAnnotation():
            # noinspection PyMissingOrEmptyDocstring
            @decorators.type_checked
            def bar(self, a: int):
                pass

        foo = CorrectAnnotation()
        # Call with correct argument.
        foo.bar(2)
        # Call with wrong argument.
        with self.assertRaisesRegex(TypeError, self.argument_type_error_regex):
            foo.bar("hello")

    # noinspection PyMissingOrEmptyDocstring
    def test_bound_method_wrong_return_value(self):
        """Test bound method with wrong return value."""

        # noinspection PyRedundantParentheses
        class WrongReturnValue():
            # noinspection PyMissingOrEmptyDocstring
            @decorators.type_checked
            def bar(self) -> int:
                return "hello"

        foo = WrongReturnValue()
        with self.assertRaisesRegex(TypeError, self.return_type_error_regex):
            foo.bar()

    # noinspection PyMissingOrEmptyDocstring
    def test_bound_method_wrong_default_values(self):
        """Test bound methods with a wrong default value."""
        with self.assertRaisesRegex(TypeError, self.default_type_error_regex):
            # noinspection PyRedundantParentheses
            class WrongDefaultValue():
                # noinspection PyMissingOrEmptyDocstring
                @decorators.type_checked
                def bar(self, a: int = "hello"):
                    pass

    # noinspection PyMissingOrEmptyDocstring
    def test_class_method_correct_annotation(self):
        """Test correct annotations for class methods."""

        # noinspection PyRedundantParentheses
        class CorrectAnnotation():
            # noinspection PyMissingOrEmptyDocstring
            @classmethod
            @decorators.type_checked
            def bar(cls, a: int):
                pass

        # Call with correct argument.
        CorrectAnnotation.bar(2)
        # Call with wrong argument.
        with self.assertRaisesRegex(TypeError, self.argument_type_error_regex):
            CorrectAnnotation.bar("hello")

    # noinspection PyMissingOrEmptyDocstring
    def test_class_method_wrong_return_value(self):
        """Test class method with wrong return value."""

        # noinspection PyRedundantParentheses
        class WrongReturnValue():
            # noinspection PyMissingOrEmptyDocstring
            @classmethod
            @decorators.type_checked
            def bar(cls) -> int:
                return "hello"

        with self.assertRaisesRegex(TypeError, self.return_type_error_regex):
            WrongReturnValue.bar()

    # noinspection PyMissingOrEmptyDocstring
    def test_class_method_wrong_default_values(self):
        """Test class methods with a wrong default value."""
        with self.assertRaisesRegex(TypeError, self.default_type_error_regex):
            # noinspection PyRedundantParentheses
            class WrongDefaultValue():
                # noinspection PyMissingOrEmptyDocstring
                @classmethod
                @decorators.type_checked
                def bar(cls, a: int = "hello"):
                    pass

    # def test_static_method(self):
    #     # Not tested yet because in principle equivalent to normal function.

    def test_decorator_arguments_no_arguments(self):
        """Test whether @type_checked is the same as @type_checked()"""

        # noinspection PyMissingOrEmptyDocstring
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

        # noinspection PyMissingOrEmptyDocstring
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

        # noinspection PyMissingOrEmptyDocstring
        @decorators.type_checked(check_arguments=False, check_defaults=False, check_return=False)
        def foo(a: int, b: int = 2.3) -> int:
            return "hello"

        # Check all functionality turned off.
        foo(2.3)

        # Check only some functionality turned off.
        with self.assertRaises(TypeError):
            decorators.type_checked(check_arguments=False, check_defaults=True, check_return=False)(foo)

    def test_decorator_arguments_positional_and_keyword(self):
        """"Test whether positional and keyword arguments mixed work for decorator"""

        # noinspection PyMissingOrEmptyDocstring
        @decorators.type_checked(False, check_defaults=False, check_return=False)
        def foo(a: int, b: int = 2.3) -> int:
            return "hello"

        # Check all functionality turned off.
        foo(2.3)

        # Check only some functionality turned off.
        with self.assertRaises(TypeError):
            decorators.type_checked(False, check_defaults=True, check_return=False)(foo)

    def test_decorator_arguments_wrong_arguments(self):
        # noinspection PyMissingOrEmptyDocstring
        def foo():
            pass

        with self.assertRaisesRegex(TypeError, self.decorator_arg_type_err_regex):
            decorators.type_checked(2)(foo)
        with self.assertRaises(TypeError):
            decorators.type_checked(check_arguments=2)

    def test_decorating_class_method_raises_type_error(self):
        # noinspection PyMissingOrEmptyDocstring
        @classmethod
        def foo():
            pass

        with self.assertRaisesRegex(TypeError, self.decorator_arg_type_err_regex):
            decorators.type_checked(foo)

    def test_decorating_static_method_raises_type_error(self):
        # noinspection PyMissingOrEmptyDocstring
        @staticmethod
        def foo():
            pass

        with self.assertRaisesRegex(TypeError,
                                    self.decorator_arg_type_err_regex):
            decorators.type_checked(foo)


if __name__ == '__main__':
    unittest.main()
