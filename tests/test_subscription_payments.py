import warnings
from datetime import datetime, timedelta

from .fixtures import (  # NOQA: F401
    create_plan, get_subscription, paddle_client
)
from .test_paddle import BadPaddleDataWarning


def test_list_subscription_payments(paddle_client, get_subscription):  # NOQA: F811,E501
    response = paddle_client.list_subscription_payments()
    for payment in response:
        assert isinstance(payment['id'], int)
        assert isinstance(payment['subscription_id'], int)
        assert type(payment['amount']) in [int, float]
        assert isinstance(payment['currency'], str)
        assert isinstance(payment['payout_date'], str)
        datetime.strptime(payment['payout_date'], '%Y-%m-%d')
        assert isinstance(payment['is_paid'], int)
        assert isinstance(payment['is_one_off_charge'], int)
        if 'receipt_url' in payment:
            assert isinstance(payment['receipt_url'], str)


def test_list_subscription_payments_with_subscription_id(paddle_client, get_subscription):  # NOQA: F811,E501
    subscription_id = get_subscription['subscription_id']
    response = paddle_client.list_subscription_payments(
        subscription_id=subscription_id
    )
    for payment in response:
        assert payment['subscription_id'] == subscription_id


def test_list_subscription_payments_with_plan_id(paddle_client, create_plan):  # NOQA: F811,E501
    plan_id = create_plan['id']
    response = paddle_client.list_subscription_payments(plan=plan_id)
    for payment in response:
        assert 'id' in payment
        assert 'amount' in payment
        assert 'currency' in payment


def test_list_subscription_payments_with_from_to(paddle_client, get_subscription):  # NOQA: F811,E501
    all_payments = paddle_client.list_subscription_payments()
    single_payment = all_payments[0]
    single_payout_date = datetime.strptime(single_payment['payout_date'], '%Y-%m-%d')  # NOQA: E501

    _from = single_payout_date - timedelta(minutes=30)
    to = single_payout_date + timedelta(minutes=30)
    time_payments = paddle_client.list_subscription_payments(
        _from=_from.strftime('%Y-%m-%d'),
        to=to,
    )
    for payment in time_payments:
        payout_date = datetime.strptime(payment['payout_date'], '%Y-%m-%d')
        assert payout_date > _from
        assert payout_date < to


def test_list_subscription_payments_with_is_paid(paddle_client, get_subscription):  # NOQA: F811,E501
    response = paddle_client.list_subscription_payments(is_paid=False)
    if not response:
        subscription_payments = paddle_client.list_subscription_payments()
        assert len(subscription_payments) != len(response)

        warning = ('No subscription payments returned by '
                   'list_subscription_payments in test_list_subscription_payments_with_is_paid')  # NOQA: E501
        warnings.warn(warning, BadPaddleDataWarning)

    for payment in response:
        assert payment['is_paid'] == 0


def test_reschedule_subscription_payment(paddle_client):  # NOQA: F811
    all_payments = paddle_client.list_subscription_payments(
        is_paid=False,
        is_one_off_charge=False,
    )
    if not all_payments:
        subscription_payments = paddle_client.list_subscription_payments()
        assert len(subscription_payments) != len(all_payments)
        warning = (
            'No subscription payments returned by list_subscription_payments '
            'in test_refund_product_payments'
        )
        warnings.warn(warning, BadPaddleDataWarning)

    payment = all_payments[0]
    single_payout_date = datetime.strptime(payment['payout_date'], '%Y-%m-%d')

    response = paddle_client.reschedule_subscription_payment(
        payment_id=payment['id'],
        date=single_payout_date,
    )
    assert response is True
