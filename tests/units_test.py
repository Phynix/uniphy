import unittest
from units import BaseUnit, Dimension, Dimensions, DimensionError


class TestBaseUnit(unittest.TestCase):

    def setUp(self):
        dimension = Dimension(Dimensions.LENGTH)
        self.test_unit = BaseUnit('test_unit', dimension)

    def test_constructor(self):
        BaseUnit('test_unit', Dimension(Dimensions.LENGTH))

    def test_set_unit_name(self):
        with self.assertRaises(AttributeError):
            self.test_unit.unit_name = None

    def test_del_unit_name(self):
        with self.assertRaises(AttributeError):
            del self.test_unit.unit_name

    def test_set_dimension(self):
        with self.assertRaises(AttributeError):
            self.test_unit.dimension = None

    def test_del_dimension(self):
        with self.assertRaises(AttributeError):
            del self.test_unit.dimension

    def test_add_with_BaseUnit_same_dimension_same_unit(self):
        other = BaseUnit('test_unit', self.test_unit.dimension)
        result = self.test_unit + other
        expected_multiplier = self.test_unit._multiplier + other._multiplier
        self.assertEqual(result._multiplier, expected_multiplier)

    def test_add_with_BaseUnit_different_dimension(self):
        different_dimension = Dimension(Dimensions.AMOUNT_OF_SUBSTANCE)
        self.assertIsNot(self.test_unit.dimension, different_dimension)
        other = BaseUnit('some_unit', different_dimension)
        with self.assertRaises(DimensionError):
            self.test_unit + other

    def test_radd_with_BaseUnit_same_dimension_same_unit(self):
        other = BaseUnit('test_unit', self.test_unit.dimension)
        result = other + self.test_unit
        expected_multiplier = self.test_unit._multiplier + other._multiplier
        self.assertEqual(result._multiplier, expected_multiplier)

    def test_radd_with_BaseUnit_different_dimension(self):
        different_dimension = Dimension(Dimensions.AMOUNT_OF_SUBSTANCE)
        self.assertIsNot(self.test_unit.dimension, different_dimension)
        other = BaseUnit('some_unit', different_dimension)
        with self.assertRaises(DimensionError):
            other + self.test_unit

    def test_sub_same_dimension_same_unit(self):
        other = BaseUnit('test_unit', self.test_unit.dimension)
        result = self.test_unit - other
        expected_multiplier = self.test_unit._multiplier - other._multiplier
        self.assertEqual(result._multiplier, expected_multiplier)

    def test_mul_unit(self):
        other = BaseUnit('some_unit', self.test_unit.dimension)
        result = self.test_unit * other
        expected_multiplier = self.test_unit._multiplier * other._multiplier
        expected_unit_name = self.test_unit.unit_name + '*' + other.unit_name
        self.assertEqual(result._multiplier, expected_multiplier)
        self.assertEqual(result._unit_name, expected_unit_name)

    def test_mul_numerical(self):
        other = 3.2
        result = self.test_unit * other
        expected_multiplier = self.test_unit._multiplier * other
        self.assertEqual(result._multiplier, expected_multiplier)
        self.assertEqual(result._unit_name, self.test_unit.unit_name)

    def test_rmul_numerical(self):
        other = 3.2
        result = other * self.test_unit
        expected_multiplier = self.test_unit._multiplier * other
        self.assertEqual(result._multiplier, expected_multiplier)
        self.assertEqual(result._unit_name, self.test_unit.unit_name)


if __name__ == '__main__':
    unittest.main()

