import pytest

from paddle import PaddleClient, PaddleException

from .test_paddle import paddle_client, unset_vendor_id  # NOQA: F401


def test_get_user_history_with_vendor_id(unset_vendor_id):  # NOQA: F811
    email = 'test@example.com'
    vendor_id = 11  # This will need to be manually entered
    paddle = PaddleClient(vendor_id=vendor_id)
    response = paddle.get_user_history(email=email, vendor_id=vendor_id)
    assert response == 'We\'ve sent details of your past transactions, licenses and downloads to you via email.'  # NOQA: E501


def test_get_user_history_with_vendor_id_env_var(paddle_client):  # NOQA: F811
    email = 'test@example.com'
    response = paddle_client.get_user_history(email=email)
    assert response == 'We\'ve sent details of your past transactions, licenses and downloads to you via email.'  # NOQA: E501


def test_get_user_history_with_product_id(paddle_client):  # NOQA: F811
    email = 'test@example.com'
    product_id = 1
    with pytest.raises(PaddleException):
        paddle_client.get_user_history(email=email, product_id=product_id)
    try:
        paddle_client.get_user_history(email=email, product_id=product_id)
    except PaddleException as error:
        assert str(error) == 'Paddle error 110 - We were unable to find any past transactions, licenses or downloads matching that email address.'  # NOQA: E501


def test_get_user_history_missing_vendoer_id_and_product_id(unset_vendor_id):  # NOQA: F811, E501
    email = 'test@example.com'
    vendor_id = 11  # This will need to be manually entered
    paddle = PaddleClient(vendor_id=vendor_id)
    response = paddle.get_user_history(email=email)
    assert response == 'We\'ve sent details of your past transactions, licenses and downloads to you via email.'  # NOQA: E501
