from datetime import datetime

import pytest

from .fixtures import (  # NOQA: F401
    create_plan, get_checkout, get_product, get_subscription, paddle_client
)


def test_list_transactions_subscription(paddle_client, get_subscription):  # NOQA: F811,E501
    subscription_id = get_subscription['subscription_id']
    subscription_list = paddle_client.list_transactions(
        entity='subscription',
        entity_id=subscription_id,
    )
    for plan in subscription_list:
        assert isinstance(plan['order_id'], str)
        assert isinstance(plan['checkout_id'], str)
        assert isinstance(plan['amount'], str)
        assert isinstance(plan['currency'], str)
        assert isinstance(plan['status'], str)
        assert isinstance(plan['created_at'], str)
        datetime.strptime(plan['created_at'], '%Y-%m-%d %H:%M:%S')
        if plan['passthrough']:
            assert isinstance(plan['passthrough'], str)
        assert isinstance(plan['product_id'], int)
        assert plan['is_subscription'] is True
        assert isinstance(plan['is_one_off'], bool)
        assert isinstance(plan['subscription']['subscription_id'], int)
        assert isinstance(plan['subscription']['status'], str)
        assert isinstance(plan['user']['user_id'], int)
        assert isinstance(plan['user']['email'], str)
        assert isinstance(plan['user']['marketing_consent'], bool)
        assert isinstance(plan['receipt_url'], str)


def test_list_transactions_product(paddle_client, get_product):  # NOQA: F811
    product_id = get_product['id']
    product_list = paddle_client.list_transactions(
        entity='product',
        entity_id=product_id,
    )
    for product in product_list:
        assert isinstance(product['order_id'], str)
        assert isinstance(product['checkout_id'], str)
        assert isinstance(product['amount'], str)
        assert isinstance(product['currency'], str)
        assert isinstance(product['status'], str)
        assert isinstance(product['created_at'], str)
        datetime.strptime(product['created_at'], '%Y-%m-%d %H:%M:%S')
        if product['passthrough']:
            assert isinstance(product['passthrough'], str)
        assert isinstance(product['product_id'], int)
        assert product['is_subscription'] is False
        assert isinstance(product['is_one_off'], bool)
        # assert isinstance(product['product']['product_id'], int)
        # assert isinstance(product['product']['status'], str)
        assert isinstance(product['user']['user_id'], int)
        assert isinstance(product['user']['email'], str)
        assert isinstance(product['user']['marketing_consent'], bool)
        assert isinstance(product['receipt_url'], str)


def test_list_transactions_checkout(paddle_client, get_checkout):  # NOQA: F811
    checkout_id = get_checkout
    checkout_list = paddle_client.list_transactions(
        entity='checkout',
        entity_id=checkout_id,
        page=1,
    )
    for checkout in checkout_list:
        assert isinstance(checkout['order_id'], str)
        assert isinstance(checkout['checkout_id'], str)
        assert isinstance(checkout['amount'], str)
        assert isinstance(checkout['currency'], str)
        assert isinstance(checkout['status'], str)
        assert isinstance(checkout['created_at'], str)
        datetime.strptime(checkout['created_at'], '%Y-%m-%d %H:%M:%S')
        if checkout['passthrough']:
            assert isinstance(checkout['passthrough'], str)
        assert isinstance(checkout['product_id'], int)
        assert isinstance(checkout['is_subscription'], bool)
        assert isinstance(checkout['is_one_off'], bool)
        assert isinstance(checkout['user']['user_id'], int)
        assert isinstance(checkout['user']['email'], str)
        assert isinstance(checkout['user']['marketing_consent'], bool)
        assert isinstance(checkout['receipt_url'], str)


def test_list_transactions_bad_entity(paddle_client):  # NOQA: F811
    entity = 'test'
    with pytest.raises(ValueError) as error:
        paddle_client.list_transactions(entity=entity, entity_id=1)
    msg = 'entity "{0}" must be one of user, subscription, order, checkout, product'  # NOQA: E501
    error.match(msg.format(entity))

# ToDo: Check order entity
# ToDo: Check user entity
