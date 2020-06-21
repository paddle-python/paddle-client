import os
import warnings
from datetime import datetime

import pytest

from .test_paddle import BadPaddleDataWarning, paddle_client  # NOQA: F401


def test_list_subscription_users(paddle_client):  # NOQA: F811
    # ToDo: Create plan when API exists for it here
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


def test_list_subscription_users_with_subscription_id(paddle_client):  # NOQA: F811,E501
    # ToDo: Create plan when API exists for it here
    response = paddle_client.list_subscription_users(results_per_page=1)
    try:
        first_subscription = response[0]
    except IndexError:
        warning = ('No subscriptions returned by list_subscription_users() in '
                   'test_list_subscription_users_with_subscription_id')
        warnings.warn(warning, BadPaddleDataWarning)
        skip_message = ('list_subscription_users did not return any user subscription')  # NOQA: E501
        pytest.skip(skip_message)

    subscription_id = first_subscription['subscription_id']
    subscription_users = paddle_client.list_subscription_users(
        subscription_id=first_subscription['subscription_id'],
    )
    for subscription in subscription_users:
        assert subscription['subscription_id'] == subscription_id


def test_list_subscription_users_with_plan_id(paddle_client):  # NOQA: F811
    # ToDo: Create plan when API exists for it here
    response = paddle_client.list_subscription_users(results_per_page=1)
    try:
        first_subscription = response[0]
    except IndexError:
        warning = ('No subscriptions returned by list_subscription_users() in '
                   'test_list_subscription_users_with_plan_id')
        warnings.warn(warning, BadPaddleDataWarning)
        skip_message = ('list_subscription_users did not return any user subscription')  # NOQA: E501
        pytest.skip(skip_message)
    subscription_users = paddle_client.list_subscription_users(
        plan_id=first_subscription['plan_id'],
    )
    for subscription in subscription_users:
        assert subscription['plan_id'] == first_subscription['plan_id']


def test_list_subscription_users_with_state(paddle_client):  # NOQA: F811
    # ToDo: Create plan when API exists for it here
    response = paddle_client.list_subscription_users(results_per_page=1)
    try:
        first_subscription = response[0]
    except IndexError:
        warning = ('No subscriptions returned by list_subscription_users() in '
                   'test_list_subscription_users_with_state')
        warnings.warn(warning, BadPaddleDataWarning)
        skip_message = ('list_subscription_users did not return any user subscription')  # NOQA: E501
        pytest.skip(skip_message)
    subscription_users = paddle_client.list_subscription_users(
        state=first_subscription['state'],
    )
    for subscription in subscription_users:
        assert subscription['state'] == first_subscription['state']


def test_list_subscription_users_with_page(paddle_client):  # NOQA: F811
    # ToDo: Create plan when API exists for it here
    list_one = paddle_client.list_subscription_users(
        results_per_page=1, page=1,
    )
    if not list_one:
        warning = ('No subscriptions returned by list_subscription_users() in '
                   'test_list_subscription_users_with_page')
        warnings.warn(warning, BadPaddleDataWarning)
        skip_message = ('list_subscription_users did not return any user subscription')  # NOQA: E501
        pytest.skip(skip_message)
    list_two = paddle_client.list_subscription_users(
        results_per_page=1, page=2,
    )
    assert list_one != list_two


def test_list_subscription_users_with_results_per_page(paddle_client):  # NOQA: F811,E501
    # ToDo: Create plan when API exists for it here
    list_one = paddle_client.list_subscription_users(
        results_per_page=1, page=1,
    )
    if not list_one:
        warning = ('No subscriptions returned by list_subscription_users() in '
                   'test_list_subscription_users_with_page')
        warnings.warn(warning, BadPaddleDataWarning)
        skip_message = ('list_subscription_users did not return any user subscription')  # NOQA: E501
        pytest.skip(skip_message)
    assert len(list_one) == 1


@pytest.mark.mocked
def test_cancel_subscription(mocker, paddle_client):  # NOQA: F811
    """
    This test is mocked as canceling a subscription is not something you want
    to do against a live system.

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
        'vendor_id': int(os.environ['PADDLE_VENDOR_ID']),
        'vendor_auth_code': os.environ['PADDLE_API_KEY'],
    }
    url = 'https://vendors.paddle.com/api/2.0/subscription/users_cancel'
    method = 'POST'
    request = mocker.patch('paddle.paddle.requests.request')
    paddle_client.cancel_subscription(
        subscription_id=subscription_id,
    )
    request.assert_called_once_with(url=url, json=json, method=method)


# Comment out '@pytest.mark.skip()' to ensure the cancel_subscription
# code is working as expected
@pytest.mark.skip()
def test_cancel_subscription_no_mock(paddle_client):  # NOQA: F811
    """
    If you get the error:
        "Paddle error 119 - Unable to find requested subscription""
    You will need to manually enter a subscription_id below.
    (this is why it's mocked in the first place, it's a pain sorry)
    """
    subscription_id = 1  # This will need to be manually entered
    response = paddle_client.cancel_subscription(
        subscription_id=subscription_id,
    )
    assert response is True


@pytest.mark.mocked
def test_update_subscription(mocker, paddle_client):  # NOQA: F811
    """
    This test is mocked as updating a subscription is probably not  something
    you want to do on a live system.

    If this test fails it means a change has been made which has affected
    the update subscription endpoint.

    The code now needs to be run directly against Paddle's API at least once to
    ensure the new code is working as expected.

    Please uncomment the '@pytest.mark.skip()' line for the
    'update_subscription_no_mock' test to run the the update_subscription code
    against the Paddle API to check the changes work.

    Once the `update_subscription_no_mock` test passes please update
    the mock below and comment out the function again.
    """
    subscription_id = 123
    quantity = 0.1
    currency = 'GBP'
    recurring_price = 0.1
    bill_immediately = False
    plan_id = int(os.environ['PADDLE_TEST_DEFAULT_PLAN_ID'])
    prorate = False
    keep_modifiers = True
    passthrough = 'passthrough-update-test_update_subscription'
    json = {
        'subscription_id': subscription_id,
        'quantity': quantity,
        'currency': currency,
        'recurring_price': recurring_price,
        'bill_immediately': bill_immediately,
        'plan_id': plan_id,
        'prorate': prorate,
        'keep_modifiers': keep_modifiers,
        'passthrough': passthrough,
        'vendor_id': int(os.environ['PADDLE_VENDOR_ID']),
        'vendor_auth_code': os.environ['PADDLE_API_KEY'],
    }
    url = 'https://vendors.paddle.com/api/2.0/subscription/users/update'
    method = 'POST'
    request = mocker.patch('paddle.paddle.requests.request')
    paddle_client.update_subscription(
        subscription_id=subscription_id,
        quantity=quantity,
        currency=currency,
        recurring_price=recurring_price,
        bill_immediately=bill_immediately,
        plan_id=plan_id,
        prorate=prorate,
        keep_modifiers=keep_modifiers,
        passthrough=passthrough,
    )
    request.assert_called_once_with(url=url, json=json, method=method)


# Comment out '@pytest.mark.skip()' to ensure the update_subscription
# code is working as expected
@pytest.mark.skip()
def test_update_subscription_no_mock(paddle_client):  # NOQA: F811
    """
    If you get the error:
        Unable to find subscription with id 1
    You will need to manually enter a subscription_id below.
    (this is why it's mocked in the first place, it's a pain sorry)
    """
    subscription_id = 1  # This will need to be manually entered
    subscription_data = get_subscription(paddle_client, subscription_id)

    # Can't udate passthrough (least destructive) as 'list_subscription_users'
    # does not return it in the response
    started_at_paused = 'paused_at' in subscription_data
    pause = not started_at_paused
    response = paddle_client.update_subscription(
        subscription_id=subscription_id,
        pause=pause,
    )
    assert response['subscription_id'] == subscription_id
    assert isinstance(response['user_id'], int)
    assert isinstance(response['plan_id'], int)
    assert isinstance(response['next_payment'], dict)
    new_subscription_data = get_subscription(paddle_client, subscription_id)

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


def get_subscription(paddle_client, subscription_id):  # NOQA: F811
    subscription_users = paddle_client.list_subscription_users()
    for subscription in subscription_users:
        if subscription['subscription_id'] == subscription_id:
            return subscription
    raise ValueError('Unable to find subscription with id {0}'.format(subscription_id))  # NOQA: E501


@pytest.mark.mocked
def test_pause_subscription(mocker, paddle_client):  # NOQA: F811
    """
    This test is mocked as pausing a subscription is probably not something
    you want to do on a live system.

    If this test fails it means a change has been made which has affected
    the update subscription endpoint. Please see test_update_subscription
    one what to do now.
    """
    subscription_id = 123
    json = {
        'subscription_id': subscription_id,
        'pause': True,
        'vendor_id': int(os.environ['PADDLE_VENDOR_ID']),
        'vendor_auth_code': os.environ['PADDLE_API_KEY'],
    }
    url = 'https://vendors.paddle.com/api/2.0/subscription/users/update'
    method = 'POST'
    request = mocker.patch('paddle.paddle.requests.request')
    paddle_client.pause_subscription(subscription_id=subscription_id)
    request.assert_called_once_with(url=url, json=json, method=method)


@pytest.mark.mocked
def test_resume_subscription(mocker, paddle_client):  # NOQA: F811
    """
    This test is mocked as pausing a subscription is probably not something
    you want to do on a live system.

    If this test fails it means a change has been made which has affected
    the update subscription endpoint. Please see test_update_subscription
    one what to do now.
    """
    subscription_id = 123
    json = {
        'subscription_id': subscription_id,
        'pause': False,
        'vendor_id': int(os.environ['PADDLE_VENDOR_ID']),
        'vendor_auth_code': os.environ['PADDLE_API_KEY'],
    }
    url = 'https://vendors.paddle.com/api/2.0/subscription/users/update'
    method = 'POST'
    request = mocker.patch('paddle.paddle.requests.request')
    paddle_client.resume_subscription(subscription_id=subscription_id)
    request.assert_called_once_with(url=url, json=json, method=method)


def test_preview_subscription_update(mocker, paddle_client):  # NOQA: F811
    subscription_data = {}
    subscription_users = paddle_client.list_subscription_users()
    for subscription in subscription_users:
        if 'paused_at' not in subscription and subscription['state'] == 'active':  # NOQA: E501
            subscription_data = subscription
    if not subscription_data:
        warning = ('No subscriptions returned by list_subscription_users() in '
                   'test_list_subscription_users_with_subscription_id')
        warnings.warn(warning, BadPaddleDataWarning)
        skip_message = ('list_subscription_users did not return any user subscription')  # NOQA: E501
        pytest.skip(skip_message)

    subscription_id = subscription_data['subscription_id']
    amount = subscription_data['next_payment']['amount']
    currency = subscription_data['next_payment']['currency']
    new_quantity = amount + 1
    response = paddle_client.preview_update_subscription(
        subscription_id=subscription_id,
        bill_immediately=True,
        quantity=new_quantity,
    )
    assert response['subscription_id'] == subscription_id
    assert isinstance(response['plan_id'], int)
    assert isinstance(response['user_id'], int)
    assert type(response['immediate_payment']['amount']) in [int, float]
    assert response['immediate_payment']['currency'] == currency
    assert isinstance(response['immediate_payment']['date'], str)
    datetime.strptime(response['immediate_payment']['date'], '%Y-%m-%d')

    assert response['next_payment']['amount'] == amount
    assert response['next_payment']['currency'] == currency
    assert isinstance(response['next_payment']['date'], str)
    datetime.strptime(response['next_payment']['date'], '%Y-%m-%d')
