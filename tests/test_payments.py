import pytest
import os
import contextlib

from paddle.paddle import requests

from .test_paddle import paddle_client  # NOQA: F401


@pytest.mark.mocked
def test_refund_payment(mocker, paddle_client):  # NOQA: F811
    """
    This test is mocked as creating a refund is not something you want to
    happen against a live system.

    If the below test fails it means a change has been made which has affected
    the refund payment endpoint.

    The code now needs to be run directly against Paddle's API at least once to
    ensure the new code is working as expected.

    Please uncomment the `refund_payment_no_mock` function call to run the
    refund_payment code against the PAddle API to check the changes work.

    Once the `refund_payment_no_mock` function / test passes please update
    the mock below and comment out the function again.
    """
    order_id = 123
    amount = 0.1
    reason = 'paddle-python-test_refund_payment'
    json = {
        'order_id': order_id,
        'amount': amount,
        'reason': reason,
        'vendor_id': int(os.environ['PADDLE_VENDOR_ID']),
        'vendor_auth_code': os.environ['PADDLE_API_KEY'],
    }
    url = 'https://vendors.paddle.com/api/2.0/payment/refund'
    method = 'POST'
    with contextlib.ExitStack() as stack:
        stack.enter_context(mocker.patch('paddle.paddle.requests.request'))
        paddle_client.refund_payment(
            order_id=order_id,
            amount=amount,
            reason=reason
        )
        requests.request.assert_called_once_with(
            url=url,
            json=json,
            method=method,
        )

    # Uncomment the next line to ensure refund_payment is working as expected
    # refund_payment_no_mock(paddle_client)


def refund_payment_no_mock(paddle_client):  # NOQA: F811
    """
    If you get the error:
        "Paddle error 172 - The transaction can no longer be refunded.""
    You may need to manually find an order_id to run this test against.
    (this is why it's mocked in the first place, it's a pain sorry)
    """
    checkout_id = os.environ['PADDLE_TEST_DEFAULT_CHECKOUT_ID']
    checkout_list = paddle_client.list_transactions(
        entity='checkout',
        entity_id=checkout_id,
        page=1,
    )
    order_id = checkout_list[0]['order_id']
    response = paddle_client.refund_payment(
        order_id=order_id,
        amount=0.1,
        reason='paddle-python-test_refund_payment'
    )
    assert isinstance(response['refund_request_id'], int)
