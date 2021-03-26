from datetime import datetime

from .fixtures import get_product, paddle_client  # NOQA: F401


def test_generate_license(paddle_client, get_product):  # NOQA: F811
    """
    The product used must have the Fulfillment Method: `Paddle License`
    or his test will fail.
    The  list_products endpoint / get_product fixture does not include the
    fulfillment method, it can only be checked manually at:
        https://sandbox-vendors.paddle.com/products
    """
    # ToDo: Create product when API exists for it here

    # Note: This product must be a
    product_id = get_product['id']
    allowed_uses = 999
    expires_at = datetime.now().strftime('%Y-%m-%d')

    response = paddle_client.generate_license(
        product_id=product_id,
        allowed_uses=allowed_uses,
        expires_at=expires_at,
    )
    assert isinstance(response['license_code'], str)
    assert response['expires_at'] == expires_at
