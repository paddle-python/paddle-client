from .test_paddle import paddle_client  # NOQA: F401


def test_create_pay_link(paddle_client):  # NOQA: F811
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
        marketing_consent='Unsure?',
        customer_email='test@example.com',
        customer_country='GB',
        customer_postcode='SW1A 1AA',
        passthrough='passthrough data',
    )
    assert 'url' in response
