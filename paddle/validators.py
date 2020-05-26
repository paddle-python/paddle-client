from datetime import date, datetime


def validate_date(value):
    if isinstance(value, str):
        error_message = 'expires_at must be a data, datetime or string in format YYYY-MM-DD'  # NOQA: E501
        try:
            datetime.strptime(value, '%Y-%m-%d')
        except ValueError:
            raise ValueError(error_message)
        else:
            return value
    elif type(value) in [datetime, date]:
        return value.strftime('%Y-%m-%d')

    raise ValueError(error_message)
