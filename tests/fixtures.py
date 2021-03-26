from datetime import datetime

import pytest

from paddle import PaddleClient, PaddleException


@pytest.fixture(scope='session')
def paddle_client():
    """
    Paddle client details are for the paddle-client@pkgdeploy.com sandbox
    account. If these details do not work or you require access to this
    account please raise a GitHub issue.
    """
    paddle = PaddleClient(
        vendor_id=1468,
        api_key="2ab9a716510da54fefa9b708b0e5b94f8145dcd8ba983bfab3",
        sandbox=True,
    )
    return paddle


@pytest.fixture(scope='session')
def create_plan(paddle_client):
    """
    https://sandbox-vendors.paddle.com/subscriptions/plans

    Returns the plan ID
    """
    plan_name = 'paddle-python-fixture-create_plan'

    plans = paddle_client.list_plans()
    if plans:
        for plan in plans:
            if plan['name'] == plan_name:
                return plan

    response = paddle_client.create_plan(
        plan_name=plan_name,
        plan_trial_days=0,
        plan_length=1,
        plan_type='day',
        main_currency_code='USD',
        initial_price_usd=1.00,
        initial_price_gbp=1.00,
        initial_price_eur=1.00,
        recurring_price_usd=1.00,
        recurring_price_gbp=1.00,
        recurring_price_eur=1.00,
    )
    return response


@pytest.fixture(scope='session')
def get_product(paddle_client):
    """
    https://sandbox-vendors.paddle.com/products

    Returns a dict of product info
    """
    response = paddle_client.list_products()
    found_product = None
    for product in response.get('products', []):
        if product['name'] == 'test-product':
            found_product = product

    if not found_product:
        message = (
            'No product found with name "test-product". As there is no Paddle '
            'API endpoint to create products please create a GitHub issue to '
            'let the maintainers of this package aware that no products exist '
            'in the sandbox account'
        )
        pytest.fail(message)
        return

    return found_product


@pytest.fixture(scope='session')
def get_subscription(paddle_client, create_plan):
    """
    https://sandbox-vendors.paddle.com/subscriptions/customers

    A subscription is record of a plan being purchase by a customer.
    This can only be done via the Paddle Checkout JS, it is not possible to
    create a subscirption via the Paddle API.

    Returns a dict with subscription info
    """
    subscriptions = paddle_client.list_subscription_users()
    if subscriptions:
        return subscriptions[-1]

    fail_message = (
        'It was not possible to find a checkout in the paddle sandbox account '
        'which is required for this test. Please follow the instructions under'
        ' `Creating subscription` in CONTRIBUTING.md using the plan ID: {0}'
    )
    plan_id = create_plan['id']
    pytest.fail(fail_message.format(plan_id))
    return


@pytest.fixture(scope='session')
def get_checkout(paddle_client, get_subscription):
    """
    https://sandbox-vendors.paddle.com/orders

    A checkout is a record of a single payment by a customer.
    This can only be done via the Paddle Checkout JS, it is not possible to
    create a checkout via the Paddle API.

    Returns a checkout ID
    """
    subscription_list = paddle_client.list_transactions(
        entity='subscription',
        entity_id=get_subscription['subscription_id'],
    )
    for subscription in subscription_list:
        return subscription['checkout_id']

    fail_message = (
        'It was not possible to find a checkout in the paddle sandbox account '
        'which is required for this test. Please follow the instructions under'
        ' `Creating a subscription` in CONTRIBUTING.md using the plan ID: {0}'
    )
    pytest.fail(fail_message.format(get_subscription['plan_id']))
    return


@pytest.fixture()
def create_coupon(paddle_client, get_product):
    product_id = get_product['id']
    currency = 'USD'
    now = datetime.now().isoformat()
    response = paddle_client.create_coupon(
        coupon_type='product',
        discount_type='percentage',
        discount_amount=1,
        allowed_uses=1,
        recurring=False,
        currency=currency,
        product_ids=[product_id],
        coupon_code='paddle-python-create_coupon_fixture-{0}'.format(now),
        description='Test coupon created by paddle-python create_coupon_fixture',  # NOQA: E501
        expires=datetime.today(),
        minimum_threshold=9999,
        group='paddle-python',
    )
    coupon_code = response['coupon_codes'][0]
    yield coupon_code, product_id

    try:
        paddle_client.delete_coupon(
            coupon_code=coupon_code, product_id=product_id
        )
    except PaddleException as error:
        valid_error = 'Paddle error 135 - Unable to find requested coupon'
        if str(error) != valid_error:
            raise


@pytest.fixture()
def create_modifier(paddle_client, get_subscription):  # NOQA: F811
    subscription_id = get_subscription['subscription_id']
    response = paddle_client.add_modifier(
        subscription_id=subscription_id,
        modifier_amount=0.01,
        modifier_recurring=True,
        modifier_description='test_modifier_fixture_modifier_description',
    )
    modifier_id = response['modifier_id']
    subscription_id = response['subscription_id']

    yield modifier_id, subscription_id

    try:
        paddle_client.delete_modifier(modifier_id=modifier_id)
    except PaddleException as error:
        valid_error = 'Paddle error 123 - Unable to find requested modifier'
        if str(error) != valid_error:
            raise
