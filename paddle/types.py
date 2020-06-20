from datetime import date, datetime
from typing import Dict, List, Union

PaddleJsonType = Dict[str, Union[str, int, float, List, None]]
DatetimeType = Union[str, datetime]
DateType = Union[str, date]
