from .fixtures import create_modifier, create_plan, get_subscription, paddle_client  # NOQA: F401, E501


def test_add_modifier(paddle_client, get_subscription):  # NOQA: F811
    subscription_id = get_subscription['subscription_id']
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
