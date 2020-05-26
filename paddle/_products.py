import logging
from urllib.parse import urljoin

log = logging.getLogger(__name__)


def list_products(self) -> dict:
    url = urljoin(self.vendors_v2, 'product/get_products')
    return self.post(url=url)
