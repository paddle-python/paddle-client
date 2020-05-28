import warnings
import contextlib
import os
from datetime import datetime

import pytest
import requests

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
        assert isinstance(subscription['next_payment'], dict)
        assert isinstance(subscription['payment_information'], dict)
        assert isinstance(subscription['linked_subscriptions'], list)


def test_list_subscription_users_with_subscription_id(paddle_client):  # NOQA: F811,E501
    # ToDo: Create plan when API exists for it here
    response = paddle_client.list_subscription_users(
        results_per_page=1
    )
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
    response = paddle_client.list_subscription_users(
        results_per_page=1
    )
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
    response = paddle_client.list_subscription_users(
        results_per_page=1
    )
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
    This test is mocked as creating a refund is not something you want to
    happen against a live system.

    If the below test fails it means a change has been made which has affected
    the refund payment endpoint.

    The code now needs to be run directly against Paddle's API at least once to
    ensure the new code is working as expected.

    Please uncomment the '@pytest.mark.skip()' line for the
    'cancel_subscription_no_mock' test to run the the cancel_subscription code
    against the PAddle API to check the changes work.

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
    with contextlib.ExitStack() as stack:
        stack.enter_context(mocker.patch('paddle.paddle.requests.request'))
        paddle_client.cancel_subscription(
            subscription_id=subscription_id,
        )
        requests.request.assert_called_once_with(
            url=url,
            json=json,
            method=method,
        )


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
