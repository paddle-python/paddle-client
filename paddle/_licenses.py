import logging
from urllib.parse import urljoin

from .types import DatetimeType, PaddleJsonType
from .validators import validate_date

log = logging.getLogger(__name__)


def generate_license(
    self,
    product_id: int,
    allowed_uses: int,
    expires_at: DatetimeType = None,
) -> dict:
    """
    https://developer.paddle.com/api-reference/product-api/licenses/createlicense
    """
    url = urljoin(self.vendors_v2, 'product/generate_license')
    json = {
        'product_id': product_id,
        'allowed_uses': allowed_uses,
    }  # type: PaddleJsonType
    if expires_at:
        json['expires_at'] = validate_date(expires_at, 'expires_at')
    return self.post(url=url, json=json)
