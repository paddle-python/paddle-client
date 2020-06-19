import os

import pytest

from paddle import PaddleException

from .test_paddle import paddle_client  # NOQA: F401


@pytest.fixture()
def create_modifier(paddle_client):  # NOQA: F811
    subscription_id = int(os.environ['PADDLE_TEST_DEFAULT_SUBSCRIPTION_ID'])
    response = paddle_client.add_modifier(
        subscription_id=subscription_id,
        modifier_amount=0.01,
        modifier_recurring=True,
        modifier_description='test_modifier_fixture_modifier_description',
    )
    modifier_id = response['modifier_id']
    subscription_id = response['subscription_id']

    yield modifier_id, subscription_id

    try:
        paddle_client.delete_modifier(modifier_id=modifier_id)
    except PaddleException as error:
        valid_error = 'Paddle error 123 - Unable to find requested modifier'
        if str(error) != valid_error:
            raise


def test_add_modifier(paddle_client):  # NOQA: F811
    subscription_id = int(os.environ['PADDLE_TEST_DEFAULT_SUBSCRIPTION_ID'])
    response = paddle_client.add_modifier(
        subscription_id=subscription_id,
        modifier_amount=0.01,
        modifier_recurring=True,
        modifier_description='test_add_modifier_modifier_description',
    )
    assert response['subscription_id'] == subscription_id
    assert isinstance(response['modifier_id'], int)
    paddle_client.delete_modifier(modifier_id=response['modifier_id'])


def test_delete_modifier(paddle_client, create_modifier):  # NOQA: F811
    modifier_id, __ = create_modifier
    response = paddle_client.delete_modifier(modifier_id=modifier_id)
    assert response is True


def test_list_modifiers(paddle_client, create_modifier):  # NOQA: F811
    response = paddle_client.list_modifiers()
    for modifier in response:
        assert isinstance(modifier['modifier_id'], int)
        assert isinstance(modifier['subscription_id'], int)
        assert isinstance(modifier['amount'], str)
        assert isinstance(modifier['currency'], str)
        assert isinstance(modifier['is_recurring'], int)  # Returns 0 or 1
        assert isinstance(modifier['description'], str)


def test_list_modifiers_with_subscription_id(paddle_client, create_modifier):  # NOQA: F811,E501
    __, subscription_id = create_modifier
    response = paddle_client.list_modifiers(subscription_id=subscription_id)
    for modifier in response:
        assert modifier['subscription_id'] == subscription_id
        assert isinstance(modifier['modifier_id'], int)
        assert isinstance(modifier['amount'], str)
        assert isinstance(modifier['currency'], str)
        assert isinstance(modifier['is_recurring'], int)  # Returns 0 or 1
        assert isinstance(modifier['description'], str)
