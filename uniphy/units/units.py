# -*- coding: utf-8 -*-

from dimensions import Dimensions


class _SIUnit():
    __slots__ = (
        '_unit_name',
        '_dimension',
    )

    def __init__(self, unit_name, dimension):

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

    def __repr__(self):
        return type(self)(self.unit_name, self.dimension)

class units():
        BaseUnit('m', Dimensions.LENGTH),
        BaseUnit('kg', Dimensions.MASS),
        BaseUnit('s', Dimensions.TIME),
        BaseUnit('A', Dimensions.ELECTRIC_CURRENT),
        BaseUnit('K', Dimensions.THERMODYNAMIC_TEMPERATURE),
        BaseUnit('mol', Dimensions.AMOUNT_OF_SUBSTANCE),
        BaseUnit('cd', Dimensions.LUMINOUS_INTENSITY)


class DimensionError(Exception):
    def __init__(self, message):
        # Call the base class constructor with the parameters it needs
        super(DimensionError, self).__init__(message)






