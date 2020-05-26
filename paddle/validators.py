from datetime import date, datetime


def validate_date(value, field_name):
    date_format = '%Y-%m-%d'
    if isinstance(value, str):
        error_message = '{0} must be a datetime/data object or string in format YYYY-MM-DD'.format(field_name)  # NOQA: E501
        try:
            datetime.strptime(value, date_format)
        except ValueError:
            raise ValueError(error_message)
        else:
            return value
    elif type(value) in [datetime, date]:
        return value.strftime(date_format)

    raise ValueError(error_message)