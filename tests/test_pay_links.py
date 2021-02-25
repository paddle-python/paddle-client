import os

import pytest

from .test_paddle import paddle_client  # NOQA: F401


@pytest.mark.manual_cleanup
def test_create_pay_link(paddle_client):  # NOQA: F811
    create_pay_link = getattr(paddle_client, 'create_pay_link', None)
    if not create_pay_link or not callable(create_pay_link):
        pytest.skip('paddle.create_pay_link does not exist')

    # ToDo: Create product when API exists for it here
    response = paddle_client.create_pay_link(
        # product_id=int(os.environ['PADDLE_TEST_DEFAULT_PRODUCT_ID']),
        title='paddle-python-test_create_pay_link',
        webhook_url='https://example.com/paddle-python',
        prices=['USD:19.99'],
        # recurring_prices=['USD:19.99'],
        trial_days=1,
        custom_message='custom_message',
        coupon_code='paddle-python-coupon_code',
        discountable=False,
        image_url='https://example.com/image_url',
        return_url='https://example.com/return_url',
        quantity_variable=1,
        quantity=1,
        affiliates=['12345:0.25'],
        recurring_affiliate_limit=1,
        # marketing_consent='0',
        customer_email='test@example.com',
        customer_country='GB',
        customer_postcode='SW1A 1AA',
        passthrough='passthrough data',
    )
    assert 'url' in response


def test_create_pay_link_mock(mocker, paddle_client):  # NOQA: F811
    """
    Mock test as the above test is not run by tox due to manual_cleanup mark
    """
    create_pay_link = getattr(paddle_client, 'create_pay_link', None)
    if not create_pay_link or not callable(create_pay_link):
        pytest.skip('paddle.create_pay_link does not exist')

    request = mocker.patch('paddle.paddle.requests.request')

    # product_id = int(os.environ['PADDLE_TEST_DEFAULT_PRODUCT_ID'])
    title = 'paddle-python-test_create_pay_link'
    webhook_url = 'https://example.com/paddle-python'
    prices = ['USD:19.99']
    trial_days = 1
    custom_message = 'custom_message'
    coupon_code = 'paddle-python-coupon_code'
    discountable = False
    image_url = 'https://example.com/image_url'
    return_url = 'https://example.com/return_url'
    quantity_variable = 0
    quantity = 1
    affiliates = ['12345:0.25']
    recurring_affiliate_limit = 1
    # marketing_consent = False
    customer_email = 'test@example.com'
    customer_country = 'GB'
    customer_postcode = 'SW1A 1AA'
    passthrough = 'passthrough data'

    json = {
        # 'product_id': product_id,
        'title': title,
        'webhook_url': webhook_url,
        'prices': prices,
        # recurring_prices=prices,
        'trial_days': trial_days,
        'custom_message': custom_message,
        'coupon_code': coupon_code,
        'discountable': 1 if discountable else 0,
        'image_url': image_url,
        'return_url': return_url,
        'quantity_variable': quantity_variable,
        'quantity': quantity,
        'affiliates': affiliates,
        'recurring_affiliate_limit': recurring_affiliate_limit,
        # 'marketing_consent': '1' if marketing_consent else '0',
        'customer_email': customer_email,
        'customer_country': customer_country,
        'customer_postcode': customer_postcode,
        'passthrough': passthrough,
        'vendor_id': int(os.environ['PADDLE_VENDOR_ID']),
        'vendor_auth_code': os.environ['PADDLE_API_KEY'],
    }
    url = 'https://vendors.paddle.com/api/2.0/product/generate_license'
    url = paddle_client.get_environment_url(url)
    method = 'POST'

    paddle_client.create_pay_link(
        # product_id=int(os.environ['PADDLE_TEST_DEFAULT_PRODUCT_ID']),
        title=title,
        webhook_url=webhook_url,
        prices=prices,
        # recurring_prices=prices,
        trial_days=trial_days,
        custom_message=custom_message,
        coupon_code=coupon_code,
        discountable=discountable,
        image_url=image_url,
        return_url=return_url,
        quantity_variable=quantity_variable,
        quantity=quantity,
        affiliates=affiliates,
        recurring_affiliate_limit=recurring_affiliate_limit,
        # marketing_consent=marketing_consent,
        customer_email=customer_email,
        customer_country=customer_country,
        customer_postcode=customer_postcode,
        passthrough=passthrough,
    )
    request.assert_called_once_with(
        url=url,
        json=json,
        method=method,
    )
