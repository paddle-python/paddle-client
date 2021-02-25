import os
import warnings
from datetime import datetime, timedelta

import pytest

from paddle import PaddleException

from .test_paddle import BadPaddleDataWarning, paddle_client  # NOQA: F401


def test_list_subscription_payments(paddle_client):  # NOQA: F811
    response = paddle_client.list_subscription_payments()

    if not response:
        warning = ('No subscription payments returned by '
                   'list_subscription_payments in test_list_subscription_payments')  # NOQA: E501
        warnings.warn(warning, BadPaddleDataWarning)
        skip_message = ('list_subscription_payments did not return any subscription payments')  # NOQA: E501
        pytest.skip(skip_message)

    for payment in response:
        assert isinstance(payment['id'], int)
        assert isinstance(payment['subscription_id'], int)
        assert isinstance(payment['amount'], int)
        assert isinstance(payment['currency'], str)
        assert isinstance(payment['payout_date'], str)
        datetime.strptime(payment['payout_date'], '%Y-%m-%d')
        assert isinstance(payment['is_paid'], int)
        assert isinstance(payment['is_one_off_charge'], int)
        if 'receipt_url' in payment:
            assert isinstance(payment['receipt_url'], str)


def test_list_subscription_payments_with_subscription_id(paddle_client):  # NOQA: F811,E501
    subscription_id = int(os.environ['PADDLE_TEST_DEFAULT_SUBSCRIPTION_ID'])
    response = paddle_client.list_subscription_payments(
        subscription_id=subscription_id
    )

    if not response:
        warning = ('No subscription payments returned by '
                   'list_subscription_payments in test_list_subscription_payments_with_subscription_id')  # NOQA: E501
        warnings.warn(warning, BadPaddleDataWarning)
        skip_message = ('list_subscription_payments did not return any subscription payments')  # NOQA: E501
        pytest.skip(skip_message)

    for payment in response:
        assert payment['subscription_id'] == subscription_id


def test_list_subscription_payments_with_plan_id(paddle_client):  # NOQA: F811
    plan_id = int(os.environ['PADDLE_TEST_DEFAULT_PLAN_ID'])
    response = paddle_client.list_subscription_payments(plan=plan_id)

    if not response:
        warning = ('No subscription payments returned by '
                   'list_subscription_payments in test_list_subscription_payments_with_plan_id')  # NOQA: E501
        warnings.warn(warning, BadPaddleDataWarning)
        skip_message = ('list_subscription_payments did not return any subscription payments')  # NOQA: E501
        pytest.skip(skip_message)


def test_list_subscription_payments_with_from_to(paddle_client):  # NOQA: F811
    all_payments = paddle_client.list_subscription_payments()
    if not all_payments:
        warning = ('No subscription payments returned by '
                   'list_subscription_payments in test_list_subscription_payments_with_from_to')  # NOQA: E501
        warnings.warn(warning, BadPaddleDataWarning)
        skip_message = ('list_subscription_payments did not return any subscription payments')  # NOQA: E501
        pytest.skip(skip_message)

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


def test_list_subscription_payments_with_is_paid(paddle_client):  # NOQA: F811,E501
    response = paddle_client.list_subscription_payments(
        is_paid=False
    )

    if not response:
        warning = ('No subscription payments returned by '
                   'list_subscription_payments in test_list_subscription_payments_with_is_paid')  # NOQA: E501
        warnings.warn(warning, BadPaddleDataWarning)
        skip_message = ('list_subscription_payments did not return any subscription payments')  # NOQA: E501
        pytest.skip(skip_message)

    for payment in response:
        assert payment['is_paid'] == 0


# ToDo: Fix this
@pytest.mark.xfail(raises=PaddleException, reason='Date issue, unsure why')
def test_reschedule_subscription_payment(paddle_client):  # NOQA: F811
    all_payments = paddle_client.list_subscription_payments(
        is_paid=False,
        is_one_off_charge=False,
    )
    if not all_payments:
        warning = ('No subscription payments returned by '
                   'list_subscription_payments in test_refund_product_payments')  # NOQA
        warnings.warn(warning, BadPaddleDataWarning)
        skip_message = ('list_subscription_payments did not return any subscription payments')  # NOQA: E501
        pytest.skip(skip_message)

    payment = all_payments[0]
    single_payout_date = datetime.strptime(payment['payout_date'], '%Y-%m-%d')

    response = paddle_client.reschedule_subscription_payment(
        payment_id=payment['id'],
        date=single_payout_date,
    )
    assert response is True
