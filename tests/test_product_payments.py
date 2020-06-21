import os

import pytest

from .test_paddle import paddle_client  # NOQA: F401


@pytest.mark.mocked
def test_refund_product_payment(mocker, paddle_client):  # NOQA: F811
    """
    This test is mocked as creating a refund is not something you want to
    happen against a live system.

    If this test fails it means a change has been made which has affected
    the refund product payment endpoint.

    The code now needs to be run directly against Paddle's API at least once to
    ensure the new code is working as expected.

    Please uncomment the '@pytest.mark.skip()' line for the
    'test_refund_product_payment_no_mock' test to run the the
    refund_product_payment code against the Paddle API to check the changes
    work.

    Once the `test_refund_product_payment_no_mock` test passes please update
    the mock below and comment out the function again.
    """
    order_id = 123
    amount = 0.1
    reason = 'paddle-python-test_refund_product_payment'
    json = {
        'order_id': order_id,
        'amount': amount,
        'reason': reason,
        'vendor_id': int(os.environ['PADDLE_VENDOR_ID']),
        'vendor_auth_code': os.environ['PADDLE_API_KEY'],
    }
    url = 'https://vendors.paddle.com/api/2.0/payment/refund'
    method = 'POST'
    request = mocker.patch('paddle.paddle.requests.request')
    paddle_client.refund_product_payment(
        order_id=order_id,
        amount=amount,
        reason=reason
    )
    request.assert_called_once_with(url=url, json=json, method=method)


# Comment out '@pytest.mark.skip()' to ensure the refund_product_payment code
# is working as expected
@pytest.mark.skip()
def test_refund_product_payment_no_mock(paddle_client):  # NOQA: F811
    """
    If you get the error:
        "Paddle error 172 - The transaction can no longer be refunded.""
    You will need to manually enter a subscription_id below.
    (this is why it's mocked in the first place, it's a pain sorry)
    """
    order_id = 1  # This will need to be manually entered
    response = paddle_client.refund_product_payment(
        order_id=order_id,
        amount=0.1,
        reason='paddle-python-test_refund_product_payment'
    )
    assert isinstance(response['refund_request_id'], int)
