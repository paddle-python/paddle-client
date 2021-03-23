from datetime import date, datetime

from .types import DatetimeType, DateType


def validate_date(value: DateType, field_name: str) -> str:
    date_format = '%Y-%m-%d'
    error_message = '{0} must be a datetime/date object or string in format YYYY-MM-DD'.format(field_name)  # NOQA: E501
    if isinstance(value, str):
        try:
            datetime.strptime(value, date_format)
        except ValueError:
            raise ValueError(error_message)
        else:
            return value
    elif type(value) in [datetime, date]:
        return value.strftime(date_format)

    raise ValueError(error_message)


def validate_datetime(value: DatetimeType, field_name: str) -> str:
    datetime_format = '%Y-%m-%d %H:%M:%S'
    error_message = '{0} must be a datetime object or string in format YYYY-MM-DD HH:MM:SS'.format(field_name)  # NOQA: E501
    if isinstance(value, str):
        try:
            datetime.strptime(value, datetime_format)
        except ValueError:
            raise ValueError(error_message)
        else:
            return value
    elif type(value) in [datetime, date]:
        return value.strftime(datetime_format)

    raise ValueError(error_message)
