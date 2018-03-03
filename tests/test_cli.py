from pytest import raises
from click import BadParameter
from uberfare.cli import validate_coordinate


class TestValidateCoordinate:

    def test_no_spaces(self):
        """It should handle input separated with a comma with no whitespace."""

        value = '123.1,123.1'
        assert validate_coordinate(None, None, value) == value

    def test_space_before_comma(self):
        """It should handle input that has a whitespace before the comma."""

        value = '123.1 ,123.1'
        assert validate_coordinate(None, None, value) == value

    def test_space_after_comma(self):
        """It should handle input that has a whitespace after the comma."""

        value = '123.1, 123.1'
        assert validate_coordinate(None, None, value) == value

    def test_no_decimal_points(self):
        """It should handle input without decimal points in the values"""

        value = '123,123'
        assert validate_coordinate(None, None, value) == value

    def test_invalid_input(self):
        """It should raise a BadParameter exception on an invalid value."""

        value = 'abc,123'

        with raises(BadParameter):
            validate_coordinate(None, None, value)
