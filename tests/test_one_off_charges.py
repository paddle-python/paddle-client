import os
from datetime import datetime

import pytest

from paddle import PaddleException

from .test_paddle import paddle_client  # NOQA: F401


@pytest.mark.mocked
def test_create_one_off_charge(mocker, paddle_client):  # NOQA: F811
    """
    This test is mocked as creating a one off charge against Paddle will
    actually create a one of charge

    If this test fails it means a change has been made which has affected
    the one-off charge endpoint.

    The code now needs to be run directly against Paddle's API at least once to
    ensure the new code is working as expected.

    Please uncomment the '@pytest.mark.skip()' line for the
    'test_create_one_off_charge_no_mock' test to run the create_one_off_charge
    code against the Paddle API to check the changes work.

    Once the `test_create_one_off_charge_no_mock` test passes please update
    the mock below and comment out the function again.
    """
    subscription_id = int(os.environ['PADDLE_TEST_DEFAULT_SUBSCRIPTION_ID'])
    amount = 0.01
    charge_name = 'test_create_one_off_charge'
    data = {
        'amount': amount,
        'charge_name': charge_name,
        'vendor_id': int(os.environ['PADDLE_VENDOR_ID']),
        'vendor_auth_code': os.environ['PADDLE_API_KEY'],
    }
    url = 'https://vendors.paddle.com/api/2.0/subscription/{0}/charge'.format(
        subscription_id
    )
    url = paddle_client.get_environment_url(url)
    method = 'POST'
    request = mocker.patch('paddle.paddle.requests.request')
    paddle_client.create_one_off_charge(
        subscription_id=subscription_id,
        amount=amount,
        charge_name=charge_name
    )
    request.assert_called_once_with(url=url, data=data, method=method)


# Comment out '@pytest.mark.skip()' to ensure the create_one_off_charge code
# is working as expected
@pytest.mark.skip()
def test_create_one_off_charge_no_mock(mocker, paddle_client):  # NOQA: F811
    subscription_id = int(os.environ['PADDLE_TEST_DEFAULT_SUBSCRIPTION_ID'])
    amount = 1.00
    response = paddle_client.create_one_off_charge(
        subscription_id=subscription_id,
        amount=amount,
        charge_name="test_create_one_off_charge"
    )
    assert isinstance(response['invoice_id'], int)
    assert isinstance(response['currency'], str)
    assert isinstance(response['receipt_url'], str)
    assert response['subscription_id'] == subscription_id
    assert response['amount'] == '%.2f' % round(amount, 2)
    assert isinstance(response['payment_date'], str)
    datetime.strptime(response['payment_date'], '%Y-%m-%d')


def test_create_one_off_charge_zero_ammount(paddle_client):  # NOQA: F811
    subscription_id = int(os.environ['PADDLE_TEST_DEFAULT_SUBSCRIPTION_ID'])

    with pytest.raises(PaddleException) as error:
        paddle_client.create_one_off_charge(
            subscription_id=subscription_id,
            amount=0.0,
            charge_name="test_create_one_off_charge"
        )

    msg = 'Paddle error 183 - Charges cannot be made with a negative amount'
    error.match(msg)
