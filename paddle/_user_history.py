import logging
from typing import Dict, Union
from urllib.parse import urljoin

log = logging.getLogger(__name__)


def get_user_history(
    self,
    email: str,
    vendor_id: int = None,
    product_id: int = None
) -> dict:
    """
    https://developer.paddle.com/api-reference/checkout-api/user-history/getuserhistory
    """
    url = urljoin(self.checkout_v2, 'user/history')

    params = {'email': email}   # type: Dict[str, Union[str, int]]
    if product_id:
        params['product_id'] = product_id

    if vendor_id:
        params['vendor_id'] = str(vendor_id)
    else:
        params['vendor_id'] = str(self.vendor_id)

    return self.get(url=url, params=params)
