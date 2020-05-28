import logging
from typing import Dict
from urllib.parse import urljoin

from .constants import supported_countries

log = logging.getLogger(__name__)


def get_prices(
    self,
    product_ids: list,
    customer_country: str = None,
    customer_ip: str = None,
    coupons: list = None,
) -> dict:
    """
    https://developer.paddle.com/api-reference/checkout-api/prices/getprices
    """
    url = urljoin(self.checkout_v2, 'prices')

    params = {}  # type: Dict[str, str]
    if product_ids:
        products = ','.join([str(int(product)) for product in product_ids])
        params['product_ids'] = products
    if customer_country:
        if customer_country not in supported_countries.keys():
            raise ValueError('Country code "{0}" is not valid'.format(customer_country))  # NOQA: E501
        params['customer_country'] = customer_country
    if customer_ip:
        params['customer_ip'] = customer_ip
    if coupons:
        params['coupons'] = ','.join(coupons)

    return self.get(url=url, params=params)
