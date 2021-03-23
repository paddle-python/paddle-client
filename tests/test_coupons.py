from datetime import datetime, timedelta

import pytest

from paddle import PaddleException

from .fixtures import create_coupon, get_product, paddle_client  # NOQA: F401


def test_list_coupons(paddle_client, create_coupon):  # NOQA: F811
    # ToDo: Create coupon with fixture
    coupon_code, product_id = create_coupon
    response = paddle_client.list_coupons(product_id=product_id)
    for coupon in response:
        assert 'allowed_uses' in coupon
        assert 'coupon' in coupon
        assert 'description' in coupon
        assert 'discount_amount' in coupon
        assert 'discount_currency' in coupon
        assert 'discount_type' in coupon
        assert 'expires' in coupon
        assert 'is_recurring' in coupon
        assert 'times_used' in coupon


def test_list_coupons_invalid_product(paddle_client):  # NOQA: F811
    product_id = 9999999999
    with pytest.raises(PaddleException) as error:
        paddle_client.list_coupons(product_id=product_id)

    error.match('Paddle error 108 - Unable to find requested product')


def test_create_coupon(paddle_client, get_product):  # NOQA: F811
    coupon_type = 'product'
    discount_type = 'percentage'
    discount_amount = 1
    allowed_uses = 1
    recurring = False
    product_id = get_product['id']
    product_ids = [product_id]
    currency = 'USD'
    now = datetime.now().isoformat()
    coupon_code = 'paddle-python-test_create_coupon-{0}'.format(now)
    description = 'Test code created by paddle-python test_create_coupon'
    expires = datetime.today().strftime('%Y-%m-%d')
    minimum_threshold = 100
    group = 'paddle-python'

    response = paddle_client.create_coupon(
        coupon_type=coupon_type,
        discount_type=discount_type,
        discount_amount=discount_amount,
        allowed_uses=allowed_uses,
        recurring=recurring,
        currency=currency,
        product_ids=product_ids,
        coupon_code=coupon_code,
        description=description,
        expires=expires,
        minimum_threshold=minimum_threshold,
        group=group,
    )
    assert response['coupon_codes'] == [coupon_code]

    coupon_list = paddle_client.list_coupons(product_id=product_id)
    paddle_client.delete_coupon(coupon_code=coupon_code, product_id=product_id)

    found = False
    discount_percentage = discount_amount / 100
    expires_time = '{0} 00:00:00'.format(expires)
    for coupon in coupon_list:
        if coupon['coupon'] != coupon_code:
            continue
        found = True
        assert 'times_used' in coupon
        assert coupon['description'] == description
        assert coupon['discount_type'] == discount_type
        assert coupon['allowed_uses'] == allowed_uses
        assert float(coupon['discount_amount']) == discount_percentage
        assert coupon['is_recurring'] == recurring
        assert coupon['expires'] == expires_time
        # Commented out due to a bug in the Paddle list coupons response
        # The discount_currency is returned as None
        # assert coupon['discount_currency'] == currency
    assert found


def test_create_coupon_invalid_coupon_type(paddle_client):  # NOQA: F811
    with pytest.raises(ValueError) as error:
        paddle_client.create_coupon(
            coupon_type='test',
            discount_type='percentage',
            discount_amount=1,
            allowed_uses=1,
            recurring=False,
            currency='USD'
        )
    error.match('coupon_type must be "product" or "checkout"')


def test_create_coupon_missing_product_ids(paddle_client):  # NOQA: F811
    with pytest.raises(ValueError) as error:
        paddle_client.create_coupon(
            coupon_type='product',
            discount_type='percentage',
            discount_amount=1,
            allowed_uses=1,
            recurring=False,
            currency='USD'
        )
    error.match('product_ids must be specified if coupon_type is "product"')


def test_create_coupon_bad_discount_type(paddle_client):  # NOQA: F811
    with pytest.raises(ValueError) as error:
        paddle_client.create_coupon(
            coupon_type='checkout',
            discount_type='test',
            discount_amount=1,
            allowed_uses=1,
            recurring=False,
            currency='USD'
        )
    error.match('coupon_type must be "product" or "checkout"')


def test_create_coupon_code_with_coupon_prefix(paddle_client):  # NOQA: F811
    with pytest.raises(ValueError) as error:
        paddle_client.create_coupon(
            coupon_type='checkout',
            discount_type='percentage',
            discount_amount=1,
            allowed_uses=1,
            recurring=False,
            currency='USD',
            coupon_code='test',
            coupon_prefix='test'
        )
    error.match('coupon_prefix and num_coupons are not valid when coupon_code set')  # NOQA: E501


def test_create_coupon_code_with_num_coupons(paddle_client):  # NOQA: F811
    with pytest.raises(ValueError) as error:
        paddle_client.create_coupon(
            coupon_type='checkout',
            discount_type='percentage',
            discount_amount=1,
            allowed_uses=1,
            recurring=False,
            currency='USD',
            coupon_code='test',
            num_coupons=10,
        )
    error.match('coupon_prefix and num_coupons are not valid when coupon_code set')  # NOQA: E501


def test_create_coupon_invalid_currency(paddle_client):  # NOQA: F811
    with pytest.raises(ValueError) as error:
        paddle_client.create_coupon(
            coupon_type='checkout',
            discount_type='percentage',
            discount_amount=1,
            allowed_uses=1,
            recurring=False,
            currency='TEST',

        )
    error.match('currency must be a 3 letter currency code')


def test_delete_coupon(paddle_client, create_coupon):  # NOQA: F811
    coupon_code, product_id = create_coupon

    paddle_client.delete_coupon(coupon_code=coupon_code, product_id=product_id)
    for coupon in paddle_client.list_coupons(product_id=product_id):
        assert coupon['coupon'] != coupon_code


def test_update_coupon(paddle_client, create_coupon):  # NOQA: F811
    coupon_code, product_id = create_coupon
    now = datetime.now().isoformat()
    new_coupon_code = 'paddle-python-test_update_coupon-{0}'.format(now)
    expires = (datetime.today() + timedelta(days=1)).strftime('%Y-%m-%d')
    currency = 'USD'
    recurring = True
    allowed_uses = 2
    discount_amount = 2
    response = paddle_client.update_coupon(
        coupon_code=coupon_code,
        new_coupon_code=new_coupon_code,
        new_group='paddle-python-test',
        product_ids=[product_id],
        expires=expires,
        allowed_uses=allowed_uses,
        currency=currency,
        minimum_threshold=9998,
        discount_amount=discount_amount,
        recurring=True
    )
    assert response['updated'] == 1

    coupon_list = paddle_client.list_coupons(product_id=product_id)
    paddle_client.delete_coupon(
        coupon_code=new_coupon_code, product_id=product_id
    )
    found = False
    discount_percentage = discount_amount / 100
    expires_time = '{0} 00:00:00'.format(expires)
    for coupon in coupon_list:
        assert coupon['coupon'] != coupon_code
        if coupon['coupon'] == new_coupon_code:
            found = True
            assert 'description' in coupon
            assert 'times_used' in coupon
            assert 'discount_type' in coupon
            assert coupon['allowed_uses'] == allowed_uses
            assert float(coupon['discount_amount']) == discount_percentage
            assert coupon['is_recurring'] == recurring
            assert coupon['expires'] == expires_time
            # Commented out due to a bug in the Paddle list coupons response
            # The discount_currency is returned as None
            # assert coupon['discount_currency'] == currency
    assert found


def test_update_coupon_code_and_group(paddle_client):  # NOQA: F811
    with pytest.raises(ValueError) as error:
        paddle_client.update_coupon(
            coupon_code='coupon_code',
            group='group'

        )
    error.match('You must specify either coupon_code or group, but not both')


def test_update_coupon_invalid_currency(paddle_client):  # NOQA: F811
    with pytest.raises(ValueError) as error:
        paddle_client.update_coupon(
            coupon_code='coupon_code',
            currency='TEST',

        )
    error.match('currency must be a 3 letter currency code')
