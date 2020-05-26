import logging
from urllib.parse import urljoin

from .validators import validate_date

log = logging.getLogger(__name__)


def list_coupons(self, product_id: int) -> dict:
    url = urljoin(self.vendors_v2, 'product/list_coupons')
    return self.post(url=url, json={'product_id': product_id})


def create_coupon(
    self,
    coupon_type: str,
    discount_type: str,
    discount_amount: float,
    allowed_uses: int,
    recurring: bool,
    currency: str,
    product_ids: list = None,
    coupon_code: str = None,
    coupon_prefix: str = None,
    num_coupons: int = None,
    description: str = None,
    expires=None,
    minimum_threshold: int = None,
    group: str = None,
) -> dict:
    """
    currency appears to be required:
        Paddle error 134 - The given coupon currency is invalid. The currency must match your balance currency.  # NOQA: E501
    Even though the docs states:
        "Required if discount_amount is flat."
    https://developer.paddle.com/api-reference/product-api/coupons/createcoupon  # NOQA: E501
    """

    url = urljoin(self.checkout_v2_1, 'product/create_coupon')

    if coupon_type not in ['product', 'checkout']:
        raise ValueError('coupon_type must be "product" or "checkout"')
    if coupon_type == 'product' and not product_ids:
        raise ValueError('product_ids must be specified if coupon_type is "product"')  # NOQA: E501
    if discount_type not in ['flat', 'percentage']:
        raise ValueError('coupon_type must be "product" or "checkout"')
    if discount_type == 'flat' and not currency:
        raise ValueError('currency must be specified if discount_type is "flat"')  # NOQA: E501
    if coupon_code and (coupon_prefix or num_coupons):
        raise ValueError('coupon_prefix and num_coupons not valid when coupon_code set')  # NOQA: E501

    json = {
        'coupon_type': coupon_type,
        'discount_type': discount_type,
        'discount_amount': discount_amount,
        'allowed_uses': allowed_uses,
        'recurring': 1 if recurring else 0,
    }
    if product_ids:
        products = ','.join([str(int(product)) for product in product_ids])
        json['product_ids'] = products
    if currency:
        if len(currency) != 3:
            raise ValueError('currency must be a 3 letter currency code')
        json['currency'] = currency

    if expires:
        json['expires'] = validate_date(expires)

    json['coupon_code'] = coupon_code
    json['coupon_prefix'] = coupon_prefix
    json['num_coupons'] = num_coupons
    json['description'] = description
    json['minimum_threshold'] = minimum_threshold
    json['group'] = group
    # Clear None values
    json = {k: v for k, v in json.items() if v}

    return self.post(url=url, json=json)


def delete_coupon(self, coupon_code: str, product_id: int = None) -> dict:
    url = urljoin(self.vendors_v2, 'product/delete_coupon')
    json = {'coupon_code': coupon_code}
    if product_id:
        json['product_id'] = product_id
    return self.post(url=url, json=json)


def update_coupon(
    self,
    coupon_code: str = None,
    new_coupon_code: str = None,
    group: str = None,
    new_group: str = None,
    product_ids: list = None,
    expires=None,
    allowed_uses: int = None,
    currency: str = None,
    minimum_threshold: int = None,
    discount_amount: float = None,
    recurring: bool = None,
) -> dict:
    url = urljoin(self.checkout_v2_1, 'product/update_coupon')

    if coupon_code and group:
        raise ValueError('You must specify either coupon_code or group, but not both')  # NOQA: E501

    json = {
        'coupon_code': coupon_code,
        'new_coupon_code': new_coupon_code,
        'group': group,
        'new_group': new_group,
        'allowed_uses': allowed_uses,
        'minimum_threshold': minimum_threshold,
        'discount_amount': discount_amount,
    }
    if product_ids:
        products = ','.join([str(int(product)) for product in product_ids])
        json['product_ids'] = products

    if currency:
        if len(currency) != 3:
            raise ValueError('currency must be a 3 letter currency code')
        json['currency'] = currency

    if expires:
        json['expires'] = validate_date(expires)

    if recurring:
        json['recurring'] = 1 if recurring else 0

    # Clear None values
    json = {k: v for k, v in json.items() if v}

    return self.post(url=url, json=json)
