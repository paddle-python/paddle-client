import logging
from urllib.parse import urljoin

log = logging.getLogger(__name__)


def get_order_details(self, checkout_id: str) -> dict:
    url = urljoin(self.checkout_v1, 'order')
    params = {'checkout_id': checkout_id}
    return self.get(url=url, params=params)
