import os
from datetime import datetime

from .test_paddle import paddle_client  # NOQA: F401


def test_list_transactions_subscription(paddle_client):  # NOQA: F811
    # ToDo: Create plan when API exists for it here
    subscription_id = int(os.environ['PADDLE_TEST_DEFAULT_PLAN_ID'])
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
        assert isinstance(plan['passthrough'], str)
        assert isinstance(plan['product_id'], int)
        assert plan['is_subscription'] is True
        assert plan['is_one_off'] is False
        assert isinstance(plan['subscription']['subscription_id'], int)
        assert isinstance(plan['subscription']['status'], str)
        assert isinstance(plan['user']['user_id'], int)
        assert isinstance(plan['user']['email'], str)
        assert isinstance(plan['user']['marketing_consent'], bool)
        assert isinstance(plan['receipt_url'], str)


def test_list_transactions_product(paddle_client):  # NOQA: F811
    # ToDo: Create product when API exists for it here
    product_id = int(os.environ['PADDLE_TEST_DEFAULT_PRODUCT_ID'])
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
        assert isinstance(product['passthrough'], str)
        assert isinstance(product['product_id'], int)
        assert product['is_subscription'] is False
        assert product['is_one_off'] is True
        # assert isinstance(product['product']['product_id'], int)
        # assert isinstance(product['product']['status'], str)
        assert isinstance(product['user']['user_id'], int)
        assert isinstance(product['user']['email'], str)
        assert isinstance(product['user']['marketing_consent'], bool)
        assert isinstance(product['receipt_url'], str)


def test_list_transactions_checkout(paddle_client):  # NOQA: F811
    checkout_id = os.environ['PADDLE_TEST_DEFAULT_CHECKOUT_ID']
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
        assert isinstance(checkout['passthrough'], str)
        assert isinstance(checkout['product_id'], int)
        assert isinstance(checkout['is_subscription'], bool)
        assert isinstance(checkout['is_one_off'], bool)
        assert isinstance(checkout['user']['user_id'], int)
        assert isinstance(checkout['user']['email'], str)
        assert isinstance(checkout['user']['marketing_consent'], bool)
        assert isinstance(checkout['receipt_url'], str)


# ToDo: Check order entity
# ToDo: Check user entity
