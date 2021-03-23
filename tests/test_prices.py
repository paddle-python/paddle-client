import pytest

from .fixtures import get_product, paddle_client  # NOQA: F401


def test_get_prices(paddle_client, get_product):  # NOQA: F811
    product_id = get_product['id']
    response = paddle_client.get_prices(product_ids=[product_id])
    assert len(response.keys()) == 2
    assert 'customer_country' in response
    for product in response['products']:
        assert product['product_id'] == product_id
        assert 'currency' in product
        assert 'list_price' in product
        assert 'price' in product
        assert 'product_title' in product
        assert 'vendor_set_prices_included_tax' in product


def test_get_prices_with_customer_country(paddle_client, get_product):  # NOQA: F811,E501
    product_id = get_product['id']
    country = 'US'
    response = paddle_client.get_prices(
        product_ids=[product_id], customer_country=country
    )
    assert len(response.keys()) == 2
    assert response['customer_country'] == country
    for product in response['products']:
        assert 'product_id' in product


def test_get_prices_invalid_customer_country(paddle_client, get_product):  # NOQA: F811,E501
    product_id = get_product['id']
    bad_country = '00'
    value_error = 'Country code "{0}" is not valid'.format(bad_country)

    with pytest.raises(ValueError) as error:
        paddle_client.get_prices(
            product_ids=[product_id], customer_country=bad_country,
        )

    error.match(value_error)


def test_get_prices_with_customer_ip(paddle_client, get_product):  # NOQA: F811
    product_id = get_product['id']
    ip = '8.47.69.211'  # https://tools.tracemyip.org/search--city/los+angeles  # NOQA: E501
    response = paddle_client.get_prices(
        product_ids=[product_id], customer_ip=ip
    )
    assert len(response.keys()) == 2
    assert response['customer_country'] == 'US'
    for product in response['products']:
        assert product['product_id'] == product_id


def test_get_prices_with_coupons(paddle_client, get_product):  # NOQA: F811
    product_id = get_product['id']
    coupon_code = 'COUPONOFF'
    response = paddle_client.get_prices(
        product_ids=[product_id], coupons=[coupon_code]
    )
    assert len(response.keys()) == 2
    assert 'products' in response
    for product in response['products']:
        assert product['product_id'] == product_id
        # Coupon discounts are for one-time products only
        if 'subscription' not in product and product['applied_coupon']:
            product['applied_coupon']['code'] == coupon_code


def test_get_prices_invalid_product_id(paddle_client):  # NOQA: F811
    response = paddle_client.get_prices(product_ids=[11])
    assert 'customer_country' in response
    assert response['products'] == []
