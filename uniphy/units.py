import numpy as np
from enum import Enum
from collections import Counter


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
    LENGTH = 0
    MASS = 1
    TIME = 2
    ELECTRIC_CURRENT = 3
    THERMODYNAMIC_TEMPERATURE = 4
    AMOUNT_OF_SUBSTANCE = 5
    LUMINOUS_INTENSITY = 6
    DIMENSIONLESS = 7


class _SIUnit():
    __slots__ = (
        '_unit_name',
        '_dimension',
        '_conversion',
        '_multiplier'
        )

    def __init__(self, unit_name, dimension, multiplier=1, conversion=1):
        self._multiplier = multiplier
        self._conversion = conversion

        assert isinstance(unit_name, str)
        self._unit_name = unit_name

        assert isinstance(dimension, dict)
        self._dimension = dimension


    @property
    def unit_name(self):
        return self._unit_name

    @property
    def dimension(self):
        return self._dimension



    def __str__(self):
        return '{} {}'.format(self._multiplier, self.unit_name)

    def __repr__(self):
        return type(self)(self.unit_name, self.dimension, self._multiplier)
#class units():
#        BaseUnit('m', Dimensions.LENGTH),
#        BaseUnit('kg', Dimensions.MASS),
#        BaseUnit('s', Dimensions.TIME),
#        BaseUnit('A', Dimensions.ELECTRIC_CURRENT),
#        BaseUnit('K', Dimensions.THERMODYNAMIC_TEMPERATURE),
#        BaseUnit('mol', Dimensions.AMOUNT_OF_SUBSTANCE),
#        BaseUnit('cd', Dimensions.LUMINOUS_INTENSITY)


class DimensionError(Exception):
    def __init__(self, message):
        # Call the base class constructor with the parameters it needs
        super(DimensionError, self).__init__(message)






