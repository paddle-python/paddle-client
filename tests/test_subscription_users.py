from datetime import datetime

import pytest

from .fixtures import create_plan, get_subscription  # NOQA: F401
from .test_paddle import BadPaddleDataWarning, paddle_client  # NOQA: F401


def test_list_subscription_users(paddle_client, get_subscription):  # NOQA: F811,E501
    subscription_users = paddle_client.list_subscription_users()
    for subscription in subscription_users:
        assert isinstance(subscription['subscription_id'], int)
        assert isinstance(subscription['plan_id'], int)
        assert isinstance(subscription['user_id'], int)
        assert isinstance(subscription['user_email'], str)
        assert isinstance(subscription['marketing_consent'], bool)
        assert isinstance(subscription['update_url'], str)
        assert isinstance(subscription['update_url'], str)
        assert isinstance(subscription['state'], str)
        assert isinstance(subscription['cancel_url'], str)
        assert isinstance(subscription['signup_date'], str)
        datetime.strptime(subscription['signup_date'], '%Y-%m-%d %H:%M:%S')
        assert isinstance(subscription['last_payment'], dict)
        assert isinstance(subscription['payment_information'], dict)
        assert isinstance(subscription['linked_subscriptions'], list)


def test_list_subscription_users_with_subscription_id(paddle_client, get_subscription):  # NOQA: F811,E501
    subscription_id = get_subscription['subscription_id']
    subscription_users = paddle_client.list_subscription_users(
        subscription_id=subscription_id,
    )
    for subscription in subscription_users:
        assert subscription['subscription_id'] == subscription_id


def test_list_subscription_users_with_plan_id(paddle_client, get_subscription):  # NOQA: F811,E501
    plan_id = get_subscription['plan_id']
    subscription_users = paddle_client.list_subscription_users(plan_id=plan_id)
    for subscription in subscription_users:
        assert subscription['plan_id'] == plan_id


def test_list_subscription_users_with_state(paddle_client, get_subscription):  # NOQA: F811,E501
    state = get_subscription['state']
    subscription_users = paddle_client.list_subscription_users(state=state)
    for subscription in subscription_users:
        assert subscription['state'] == state


def test_list_subscription_users_with_page(paddle_client, get_subscription):  # NOQA: F811,E501
    list_one = paddle_client.list_subscription_users(
        results_per_page=1, page=1,
    )
    list_two = paddle_client.list_subscription_users(
        results_per_page=1, page=2,
    )
    assert list_one != list_two


def test_list_subscription_users_with_results_per_page(paddle_client, get_subscription):  # NOQA: F811,E501
    list_one = paddle_client.list_subscription_users(
        results_per_page=1, page=1,
    )
    assert len(list_one) == 1


def test_list_subscription_users_invalid_state(paddle_client):  # NOQA: F811
    with pytest.raises(ValueError) as error:
        paddle_client.list_subscription_users(state='test')
    error.match('state must be one of active, past due, trialling, paused')


def test_update_subscription(paddle_client, get_subscription):  # NOQA: F811
    """
    If you get the error:
        Unable to find subscription with id 1
    You will need to manually enter a subscription_id below.
    (this is why it's mocked in the first place, it's a pain sorry)
    """
    subscription_id = get_subscription['subscription_id']

    # Can't udate passthrough (least destructive) as 'list_subscription_users'
    # does not return it in the response
    started_at_paused = 'paused_at' in get_subscription
    pause = not started_at_paused
    response = paddle_client.update_subscription(
        subscription_id=subscription_id,
        pause=pause,
    )
    assert response['subscription_id'] == subscription_id
    assert isinstance(response['user_id'], int)
    assert isinstance(response['plan_id'], int)
    assert isinstance(response['next_payment'], dict)

    new_subscription_data = paddle_client.list_subscription_users(
        subscription_id=subscription_id,
    )
    new_subscription_data = new_subscription_data[0]

    if started_at_paused:
        assert 'paused_at' not in new_subscription_data
        assert 'paused_from' not in new_subscription_data
        assert 'paused_reason' not in new_subscription_data
    else:
        assert isinstance(new_subscription_data['paused_at'], str)
        datetime.strptime(new_subscription_data['paused_at'], '%Y-%m-%d %H:%M:%S')  # NOQA: E501
        assert isinstance(new_subscription_data['paused_from'], str)
        datetime.strptime(new_subscription_data['paused_from'], '%Y-%m-%d %H:%M:%S')  # NOQA: E501
        assert new_subscription_data['paused_reason'] == 'voluntary'

    # Set the pause state back to what is was before the test ran
    paddle_client.update_subscription(
        subscription_id=subscription_id,
        pause=not pause,
    )

    # Test the change back worked
    new_subscription_data = paddle_client.list_subscription_users(
        subscription_id=subscription_id,
    )
    new_subscription_data = new_subscription_data[0]
    if started_at_paused:
        assert isinstance(new_subscription_data['paused_at'], str)
        datetime.strptime(new_subscription_data['paused_at'], '%Y-%m-%d %H:%M:%S')  # NOQA: E501
        assert isinstance(new_subscription_data['paused_from'], str)
        datetime.strptime(new_subscription_data['paused_from'], '%Y-%m-%d %H:%M:%S')  # NOQA: E501
        assert new_subscription_data['paused_reason'] == 'voluntary'
    else:
        assert 'paused_at' not in new_subscription_data
        assert 'paused_from' not in new_subscription_data
        assert 'paused_reason' not in new_subscription_data


def test_update_subscription_invalid_currency(paddle_client):  # NOQA: F811
    with pytest.raises(ValueError) as error:
        paddle_client.update_subscription(
            subscription_id=1, currency='test'
        )
    error.match('currency must be one of USD, GBP, EUR')


@pytest.mark.mocked
def test_cancel_subscription(mocker, paddle_client):  # NOQA: F811
    """
    This test is mocked as subscriptions must be created manually (see
    `Creating a subscription` in CONTRIBUTING.md) as there is no API
    to do so

    If this test fails it means a change has been made which has affected
    the cancel subscription endpoint.

    The code now needs to be run directly against Paddle's API at least once to
    ensure the new code is working as expected.

    Please uncomment the '@pytest.mark.skip()' line for the
    'cancel_subscription_no_mock' test to run the the cancel_subscription code
    against the Paddle API to check the changes work.

    Once the `cancel_subscription_no_mock` test passes please update
    the mock below and comment out the function again.
    """
    subscription_id = 123
    json = {
        'subscription_id': subscription_id,
        'vendor_id': paddle_client.vendor_id,
        'vendor_auth_code': paddle_client.api_key,
    }
    url = 'https://sandbox-vendors.paddle.com/api/2.0/subscription/users_cancel'  # NOQA: E501
    method = 'POST'
    request = mocker.patch('paddle.paddle.requests.request')
    paddle_client.cancel_subscription(
        subscription_id=subscription_id,
    )
    request.assert_called_once_with(url=url, json=json, method=method)


# Comment out '@pytest.mark.skip()' to ensure the cancel_subscription
# code is working as expected
@pytest.mark.skip()
def test_cancel_subscription_no_mock(paddle_client, get_subscription):  # NOQA: F811,E501
    subscription_id = get_subscription
    response = paddle_client.cancel_subscription(
        subscription_id=subscription_id,
    )
    assert response is True
