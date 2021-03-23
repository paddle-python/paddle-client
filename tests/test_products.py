from .fixtures import get_product, paddle_client  # NOQA: F401


def test_list_products(paddle_client, get_product):  # NOQA: F811
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
