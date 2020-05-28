import logging
from typing import List
from urllib.parse import urljoin

from .constants import countries_requiring_postcode, supported_countries
from .types import DatetimeType, PaddleJsonType
from .validators import validate_date

log = logging.getLogger(__name__)


def create_pay_link(
    self,
    product_id: int = None,
    title: str = None,
    webhook_url: str = None,
    prices: List[str] = None,
    recurring_prices: List[str] = None,
    trial_days: int = None,
    custom_message: str = None,
    coupon_code: str = None,
    discountable: bool = None,
    image_url: str = None,
    return_url: str = None,
    quantity_variable: bool = None,
    quantity: int = None,
    expires: DatetimeType = None,
    affiliates: List[str] = None,
    recurring_affiliate_limit: int = None,
    marketing_consent: str = None,
    customer_email: str = None,
    customer_country: str = None,
    customer_postcode: str = None,
    passthrough: str = None,
    vat_number: str = None,
    vat_company_name: str = None,
    vat_street: str = None,
    vat_city: str = None,
    vat_state: str = None,
    vat_country: str = None,
    vat_postcode: str = None,
) -> dict:
    """
    https://developer.paddle.com/api-reference/product-api/pay-links/createpaylink

    product_id appears to be required:
        Paddle error 108 - Unable to find requested product
    Even though the docs states:
        "If no product_id is set, custom non-subscription product checkouts
        can be generated instead by specifying title, webhook_url and prices."
    https://developer.paddle.com/api-reference/product-api/coupons/createcoupon  # NOQA: E501
    """

    url = urljoin(self.vendors_v2, 'product/generate_license')

    if not product_id:
        if not title:
            raise ValueError('title must be set if product_id is not set')
        if not webhook_url:
            raise ValueError('webhook_url must be set if product_id is not set')  # NOQA: E501
        if recurring_prices:
            raise ValueError('recurring_prices can only be set if product_id is set to a subsciption')  # NOQA: E501
    if customer_country:
        if customer_country not in supported_countries.keys():
            error = 'Country code "{0}" is not valid'.format(customer_country)
            raise ValueError(error)
        if customer_country in countries_requiring_postcode and not customer_postcode:  # NOQA: E501
            error = ('customer_postcode must be set for {0} when '
                     'customer_country is set'.format(vat_country))
            raise ValueError(error)

    if vat_number:
        if not vat_company_name:
            raise ValueError('vat_company_name must be set if vat_number is set')  # NOQA: E501
        if not vat_street:
            raise ValueError('vat_street must be set if vat_number is set')
        if not vat_city:
            raise ValueError('vat_city must be set if vat_number is set')
        if not vat_state:
            raise ValueError('vat_state must be set if vat_number is set')
        if not vat_country:
            raise ValueError('vat_country must be set if vat_number is set')
        if vat_country in countries_requiring_postcode and not vat_postcode:  # NOQA: E501
            error = ('vat_postcode must be set for {0} when '
                     'vat_country is set'.format(vat_country))
            raise ValueError(error)

    json = {
        'product_id': product_id,
        'title': title,
        'webhook_url': webhook_url,
        'prices': prices,
        'recurring_prices': recurring_prices,
        'trial_days': trial_days,
        'custom_message': custom_message,
        'coupon_code': coupon_code,
        'discountable': 1 if discountable is True else 0,
        'image_url': image_url,
        'return_url': return_url,
        'quantity_variable': 1 if quantity_variable is True else 0,
        'quantity': quantity,
        'affiliates': affiliates,
        'recurring_affiliate_limit': recurring_affiliate_limit,
        'marketing_consent': marketing_consent,
        'customer_email': customer_email,
        'customer_country': customer_country,
        'customer_postcode': customer_postcode,
        'passthrough': passthrough,
        'vat_number': vat_number,
        'vat_company_name': vat_company_name,
        'vat_street': vat_street,
        'vat_city': vat_city,
        'vat_state': vat_state,
        'vat_country': vat_country,
        'vat_postcode': vat_postcode,
    }  # type: PaddleJsonType
    if expires:
        json['expires'] = validate_date(expires, 'expires')

    return self.post(url=url, json=json)
