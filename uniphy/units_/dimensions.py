# -*- coding: utf-8 -*-

from enum import Enum


class OrderedEnum(Enum):
    def __ge__(self, other):
        if self.__class__ is other.__class__:
            return self.value >= other.value
        return NotImplemented

    def __gt__(self, other):
        if self.__class__ is other.__class__:
            return self.value > other.value
        return NotImplemented

    def __le__(self, other):
        if self.__class__ is other.__class__:
            return self.value <= other.value
        return NotImplemented

    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.value < other.value
        return NotImplemented


class Dimensions(OrderedEnum):
    '''OrderedEnum of allowed physical dimensions.'''
    LENGTH = 0
    MASS = 1
    TIME = 2
    ELECTRIC_CURRENT = 3
    THERMODYNAMIC_TEMPERATURE = 4
    AMOUNT_OF_SUBSTANCE = 5
    LUMINOUS_INTENSITY = 6


class DimensionError(Exception):
    '''ErrorClass for operations that make physically no sense because of the
    dimensions.'''
    def __init__(self, message):
        # Call the base class constructor with the parameters it needs
        super(DimensionError, self).__init__(message)
