import os

import pytest

from paddle import PaddleException

from .test_paddle import paddle_client  # NOQA: F401


def test_get_order_details(paddle_client):  # NOQA: F811
    # ToDo: Create / get a list of orders instead of hardcoding ID here
    checkout_id = os.environ['PADDLE_TEST_DEFAULT_CHECKOUT_ID']
    response = paddle_client.get_order_details(checkout_id=checkout_id)
    assert len(response.keys()) == 4
    assert response['checkout']['checkout_id'] == checkout_id
    assert 'state' in response
    assert 'order' in response
    assert 'lockers' in response


def test_get_order_details_invalid_id(paddle_client):  # NOQA: F811
    with pytest.raises(PaddleException) as error:
        paddle_client.get_order_details(checkout_id='fake-id')

    msg = 'Paddle error 101 - Could not find a checkout matching this ID'
    error.match(msg)
