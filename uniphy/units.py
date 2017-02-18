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


class Dimension():
    def __init__(self, numerator=Dimensions.DIMENSIONLESS,
                 denominator=Dimensions.DIMENSIONLESS):

        def test_input(argument):
            msg = """arguments must be of type enum Dimensions or tuple of
            enum Dimensions."""
            try:
                for element in argument:
                    assert isinstance(element, Dimensions), msg \
                    + ' Found ' + str(type(element)) + ': ' + str(element)
            except TypeError:
                assert isinstance(argument, Dimensions), msg
                return (argument, )
            else:
                assert isinstance(argument, tuple), msg
                return argument

        self._numerator = test_input(numerator)
        self._denominator = test_input(denominator)
        self._sort()

    def __mul__(self, other):
        if not isinstance(other, type(self)):
            #to be replaced by correct implementation
            raise TypeError
        numerator = self._numerator+other._numerator
        denominator = self._denominator+other._denominator
        return Dimension(numerator, denominator)

    def __truediv__(self, other):
        if not isinstance(other, type(self)):
            #to be replaced by correct implementation
            raise TypeError
        numerator = self._numerator+other._denominator
        denominator = self._denominator+other._numerator
        return Dimension(numerator, denominator)

    def _sort(self):
        num_counter = Counter(self._numerator)
        den_counter = Counter(self._denominator)

        num_count = num_counter.get(Dimensions.DIMENSIONLESS)
        den_count = den_counter.get(Dimensions.DIMENSIONLESS)

        numerator = sorted(self._numerator)
        denominator = sorted(self._denominator)

        if num_count:
            for i in range(num_count-1):
                numerator.remove(Dimensions.DIMENSIONLESS)
        if den_count:
            for i in range(den_count-1):
                denominator.remove(Dimensions.DIMENSIONLESS)

        self._numerator = tuple(numerator)
        self._denominator = tuple(denominator)

    def __str__(self):
        numerator_str = '*'.join([e.name for e in self._numerator])
        denominator_str = '*'.join([e.name for e in self._denominator])
        return '<{}, {}>'.format(numerator_str, denominator_str)



class BaseUnit():
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

        assert isinstance(dimension, Dimension)
        self._dimension = dimension


    @property
    def unit_name(self):
        return self._unit_name

    @property
    def dimension(self):
        return self._dimension

    def __add__(self, other):
        if not isinstance(other, type(self)):
            raise TypeError("Units may only be added to units.")
        if not self.dimension == other.dimension:
            raise DimensionError("Cannot broadcast " + str(self.dimension)
                + ' ' + str(other.dimension) + '.')
        multiplier = self._multiplier + other._multiplier
        return type(self)(self.unit_name, self.dimension, multiplier)

    def __sub__(self, other):
        return self + -other

    def __neg__(self):
        return type(self)(self.unit_name, self.dimension, -self._multiplier)

    def __mul__(self, other):
        try:
            multiplier = self._multiplier * other._multiplier
        except AttributeError:
            multiplier = self._multiplier * other
            return type(self)(self.unit_name, self.dimension, multiplier)
        else:
            unit_name = self.unit_name + '*' + other.unit_name
            dimension = self.dimension * other.dimension
            return type(self)(unit_name, dimension)

    def __rmul__(self, other):
        return self * other

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






