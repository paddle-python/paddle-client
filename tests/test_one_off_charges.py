from datetime import datetime

import pytest

from paddle import PaddleException

from .fixtures import (  # NOQA: F401
    create_plan, get_subscription, paddle_client
)


def test_create_one_off_charge(paddle_client, get_subscription):  # NOQA: F811,E501
    subscription_id = get_subscription['subscription_id']
    amount = 5.00
    response = paddle_client.create_one_off_charge(
        subscription_id=subscription_id,
        amount=amount,
        charge_name="test_create_one_off_charge"
    )
    assert isinstance(response['invoice_id'], int)
    assert isinstance(response['currency'], str)
    assert isinstance(response['receipt_url'], str)
    assert response['subscription_id'] == subscription_id
    # There is a bug with the sandbox API where the ammount is returned
    # with 3 decimal places.
    if len(str(response['amount'])) == 5:
        assert response['amount'] == '%.3f' % round(amount, 3)
    else:
        assert response['amount'] == '%.2f' % round(amount, 2)
    assert isinstance(response['payment_date'], str)
    datetime.strptime(response['payment_date'], '%Y-%m-%d')


def test_create_one_off_charge_zero_ammount(paddle_client, get_subscription):  # NOQA: F811,E501
    subscription_id = get_subscription['subscription_id']

    with pytest.raises(PaddleException) as error:
        paddle_client.create_one_off_charge(
            subscription_id=subscription_id,
            amount=0.0,
            charge_name="test_create_one_off_charge"
        )

    msg = 'Paddle error 183 - Charges cannot be made with a negative amount'
    error.match(msg)
