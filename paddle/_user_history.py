import logging
from urllib.parse import urljoin

log = logging.getLogger(__name__)


def get_user_history(
    self,
    email: str,
    vendor_id: int = None,
    product_id: int = None
) -> dict:
    url = urljoin(self.checkout_v2, 'user/history')

    params = {'email': email}
    if product_id:
        params['product_id'] = product_id

    if vendor_id:
        params['vendor_id'] = vendor_id
    else:
        params['vendor_id'] = self.vendor_id

    return self.get(url=url, params=params)
