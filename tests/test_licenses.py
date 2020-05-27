import os
from datetime import datetime

import pytest

from .test_paddle import paddle_client  # NOQA: F401


@pytest.mark.manual_cleanup
def test_generate_license(paddle_client):  # NOQA: F811
    generate_license = getattr(paddle_client, 'generate_license', None)
    if not generate_license or not callable(generate_license):
        pytest.skip('paddle.generate_license does not exist')

    # ToDo: Create product when API exists for it here
    product_id = int(os.environ['PADDLE_TEST_DEFAULT_PRODUCT_ID'])
    allowed_uses = 1
    expires_at = datetime.now().strftime('%Y-%m-%d')

    response = paddle_client.generate_license(
        product_id=product_id,
        allowed_uses=allowed_uses,
        expires_at=expires_at,
    )
    assert 'license_code' in response
    assert response['expires_at'] == expires_at


def test_generate_license_mocked(mocker, paddle_client):  # NOQA: F811
    """
    Mock test as the above test is not run by tox due to manual_cleanup mark
    """
    generate_license = getattr(paddle_client, 'generate_license', None)
    if not generate_license or not callable(generate_license):
        pytest.skip('paddle.generate_license does not exist')

    request = mocker.patch('paddle.paddle.requests.request')

    product_id = int(os.environ['PADDLE_TEST_DEFAULT_PRODUCT_ID'])
    allowed_uses = 1
    expires_at = datetime.now()
    json = {
        'product_id': product_id,
        'allowed_uses': allowed_uses,
        'expires_at': expires_at.strftime('%Y-%m-%d'),
        'vendor_id': int(os.environ['PADDLE_VENDOR_ID']),
        'vendor_auth_code': os.environ['PADDLE_API_KEY'],

    }
    url = 'https://vendors.paddle.com/api/2.0/product/generate_license'
    method = 'POST'

    paddle_client.generate_license(
        product_id=product_id,
        allowed_uses=allowed_uses,
        expires_at=expires_at,
    )
    request.assert_called_once_with(
        url=url,
        json=json,
        method=method,
    )
