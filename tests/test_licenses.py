from datetime import datetime
import os

from .test_paddle import paddle_client  # NOQA: F401


def test_generate_license(paddle_client):  # NOQA: F811
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
