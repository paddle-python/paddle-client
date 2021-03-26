import pytest

from paddle import PaddleException

from .fixtures import (  # NOQA: F401
    create_plan, get_subscription, paddle_client
)


def test_get_user_history_with_vendor_id(paddle_client, get_subscription):  # NOQA: F811,E501
    email = get_subscription['user_email']
    vendor_id = paddle_client.vendor_id
    response = paddle_client.get_user_history(email=email, vendor_id=vendor_id)
    assert response == 'We\'ve sent details of your past transactions, licenses and downloads to you via email.'  # NOQA: E501


def test_get_user_history_with_vendor_id_env_var(paddle_client, get_subscription):  # NOQA: F811,E501
    email = get_subscription['user_email']
    response = paddle_client.get_user_history(email=email)
    assert response == 'We\'ve sent details of your past transactions, licenses and downloads to you via email.'  # NOQA: E501


def test_get_user_history_with_product_id(paddle_client, get_subscription):  # NOQA: F811,E501
    email = get_subscription['user_email']
    product_id = 1
    with pytest.raises(PaddleException) as error:
        paddle_client.get_user_history(email=email, product_id=product_id)

    msg = 'Paddle error 110 - We were unable to find any past transactions, licenses or downloads matching that email address.'  # NOQA: E501
    error.match(msg)


def test_get_user_history_missing_vendor_id_and_product_id(paddle_client, get_subscription):  # NOQA: F811, E501
    email = get_subscription['user_email']
    response = paddle_client.get_user_history(email=email)
    assert response == 'We\'ve sent details of your past transactions, licenses and downloads to you via email.'  # NOQA: E501
