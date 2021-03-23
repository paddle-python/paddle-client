import pytest

from paddle.validators import validate_date, validate_datetime


def test_validate_date_not_string_or_date():
    field_name = 'test'
    with pytest.raises(ValueError) as error:
        validate_date(value=123, field_name=field_name)
    msg = '{0} must be a datetime/date object or string in format YYYY-MM-DD'
    error.match(msg.format(field_name))


def test_validate_datetime_not_string_or_datetime():
    field_name = 'test'
    with pytest.raises(ValueError) as error:
        validate_datetime(value=123, field_name=field_name)
    msg = '{0} must be a datetime object or string in format YYYY-MM-DD'
    error.match(msg.format(field_name))


def test_validate_datetime_not_valid_string():
    field_name = 'test'
    with pytest.raises(ValueError) as error:
        validate_datetime(value='123', field_name=field_name)
    msg = '{0} must be a datetime object or string in format YYYY-MM-DD'
    error.match(msg.format(field_name))
