from datetime import datetime

from .test_paddle import paddle_client  # NOQA: F401


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
    first_subscription = response[0]
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
    first_subscription = response[0]
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
    first_subscription = response[0]
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
    list_two = paddle_client.list_subscription_users(
        results_per_page=1, page=2,
    )
    assert list_one != list_two


def test_list_subscription_users_with_results_per_page(paddle_client):  # NOQA: F811,E501
    # ToDo: Create plan when API exists for it here
    list_one = paddle_client.list_subscription_users(
        results_per_page=1, page=1,
    )
    assert len(list_one) == 1

# def test_cancel_subscription(paddle_client):  # NOQA: F811
#     # ToDo: Create plan when API exists for it here
#     plan_id = int(os.environ['PADDLE_TEST_DEFAULT_PLAN_ID'])
#     plan_list = paddle_client.list_plans(plan=plan_id)
