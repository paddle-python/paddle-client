import logging
from urllib.parse import urljoin

log = logging.getLogger(__name__)


def get_order_details(self, checkout_id: str) -> dict:
    """
    https://developer.paddle.com/api-reference/checkout-api/order-information/getorder
    """
    url = urljoin(self.checkout_v1, 'order')
    return self.get(url=url, params={'checkout_id': checkout_id})
