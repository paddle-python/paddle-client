import pytest

from .fixtures import get_product, paddle_client  # NOQA: F401


def test_create_pay_link(paddle_client, get_product):  # NOQA: F811
    response = paddle_client.create_pay_link(
        product_id=get_product['id'],
        title='paddle-python-test_create_pay_link',
        prices=['USD:19.99'],
        recurring_prices=['USD:19.99'],
        trial_days=1,
        custom_message='custom_message',
        discountable=False,
        image_url='https://example.com/image_url',
        return_url='https://example.com/return_url',
        quantity_variable=1,
        quantity=1,
        recurring_affiliate_limit=1,
        marketing_consent=True,
        customer_email='test@example.com',
        customer_country='US',
        customer_postcode='00000',
        passthrough='passthrough data',
        vat_number="vat_number",
        vat_company_name="vat_company_name",
        vat_street="vat_street",
        vat_city="vat_city",
        vat_state="vat_state",
        vat_country="vat_country",
        vat_postcode="vat_postcode",
        # affiliates=['12345:0.25'],
        # coupon_code='paddle-python-coupon_code',
        # webhook_url='https://example.com/paddle-python',
    )
    assert isinstance(response['url'], str)
    assert response['url'].startswith('https://sandbox-checkout.paddle.com/checkout/custom/')  # NOQA: E501


def test_create_pay_link_no_product_or_title(paddle_client):  # NOQA: F811
    with pytest.raises(ValueError) as error:
        paddle_client.create_pay_link()
    error.match('title must be set if product_id is not set')


def test_create_pay_link_no_product_or_webhook(paddle_client):  # NOQA: F811
    with pytest.raises(ValueError) as error:
        paddle_client.create_pay_link(title='test')
    error.match('webhook_url must be set if product_id is not set')


def test_create_pay_link_no_product_and_recurring_prices(paddle_client):  # NOQA: F811,E501
    with pytest.raises(ValueError) as error:
        paddle_client.create_pay_link(
            title='test', webhook_url='test', recurring_prices=['USD:19.99'],
        )
    error.match('recurring_prices can only be set if product_id is set to a subsciption')  # NOQA: F811,E501


def test_create_pay_link_no_product_reccuring(paddle_client):  # NOQA: F811
    with pytest.raises(ValueError) as error:
        paddle_client.create_pay_link(
            title='test',
            recurring_prices=['USD:19.99']
        )
    error.match('webhook_url must be set if product_id is not set')


def test_create_pay_link_product_and_webhook(paddle_client, get_product):  # NOQA: F811,E501
    with pytest.raises(ValueError) as error:
        paddle_client.create_pay_link(
            product_id=get_product['id'],
            webhook_url='https://example.com/paddle-python',
        )
    error.match('product_id and webhook_url cannot both be set')


def test_create_pay_link_invalid_country(paddle_client):  # NOQA: F811
    country = 'FAKE'
    with pytest.raises(ValueError) as error:
        paddle_client.create_pay_link(
            title='test',
            webhook_url='https://example.com/paddle-python',
            customer_country=country,
        )
    error.match('Country code "{0}" is not valid'.format(country))


def test_create_pay_link_country_without_postcode(paddle_client):  # NOQA: F811
    country = 'US'
    with pytest.raises(ValueError) as error:
        paddle_client.create_pay_link(
            title='test',
            webhook_url='https://example.com/paddle-python',
            customer_country=country,
        )

    message = (
        'customer_postcode must be set for {0} when customer_country is set'
    )
    error.match(message.format(country))


def test_create_pay_link_vat_number(paddle_client):  # NOQA: F811
    with pytest.raises(ValueError) as error:
        paddle_client.create_pay_link(
            title='test', webhook_url='fake', vat_number='1234',
        )
    error.match('vat_company_name must be set if vat_number is set')

    with pytest.raises(ValueError) as error:
        paddle_client.create_pay_link(
            title='test', webhook_url='fake', vat_number='1234',
            vat_company_name='name',
        )
    error.match('vat_street must be set if vat_number is set')

    with pytest.raises(ValueError) as error:
        paddle_client.create_pay_link(
            title='test', webhook_url='fake', vat_number='1234',
            vat_company_name='name', vat_street='street',
        )
    error.match('vat_city must be set if vat_number is set')

    with pytest.raises(ValueError) as error:
        paddle_client.create_pay_link(
            title='test', webhook_url='fake', vat_number='1234',
            vat_company_name='name', vat_street='street',
            vat_city='city', vat_state='state',
        )
    error.match('vat_country must be set if vat_number is set')

    with pytest.raises(ValueError) as error:
        country = 'US'
        paddle_client.create_pay_link(
            title='test', webhook_url='fake', vat_number='1234',
            vat_company_name='name', vat_street='street',
            vat_city='city', vat_state='state', vat_country=country,
        )
    message = 'vat_postcode must be set for {0} when vat_country is set'
    error.match(message.format(country))


def test_create_pay_link_invalid_date(paddle_client):  # NOQA: F811
    with pytest.raises(ValueError) as error:
        paddle_client.create_pay_link(
            title='test',
            webhook_url='https://example.com/paddle-python',
            expires='test'
        )
    error.match('expires must be a datetime/date object or string in format YYYY-MM-DD')  # NOQA: E501
