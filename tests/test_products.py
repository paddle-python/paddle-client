from .test_paddle import paddle_client  # NOQA: F401


def test_list_products(paddle_client):  # NOQA: F811
    # ToDo: Create product when API exists for it here
    response = paddle_client.list_products()
    assert 'count' in response
    assert 'total' in response
    for product in response['products']:
        assert 'id' in product
        assert 'name' in product
        assert 'description' in product
        assert 'base_price' in product
        assert 'sale_price' in product
        assert 'screenshots' in product
        assert 'icon' in product
