import os
from datetime import datetime

import pytest

from .test_paddle import paddle_client  # NOQA: F401


def test_list_plans(paddle_client):  # NOQA: F811
    # ToDo: Create plan when API exists for it here
    plan_list = paddle_client.list_plans()
    for plan in plan_list:
        assert isinstance(plan['id'], int)
        assert isinstance(plan['billing_period'], int)
        assert isinstance(plan['billing_type'], str)
        assert isinstance(plan['initial_price'], dict)
        assert isinstance(plan['name'], str)
        assert isinstance(plan['recurring_price'], dict)
        assert isinstance(plan['trial_days'], int)


def test_list_plans_with_plan(paddle_client):  # NOQA: F811
    # ToDo: Create plan when API exists for it here
    plan_id = int(os.environ['PADDLE_TEST_DEFAULT_PLAN_ID'])
    plan_list = paddle_client.list_plans(plan=plan_id)
    assert len(plan_list) == 1
    plan = plan_list[0]
    assert plan['id'] == plan_id
    assert isinstance(plan['billing_period'], int)
    assert isinstance(plan['billing_type'], str)
    assert isinstance(plan['initial_price'], dict)
    assert isinstance(plan['name'], str)
    assert isinstance(plan['recurring_price'], dict)
    assert isinstance(plan['trial_days'], int)


def test_get_plan(paddle_client):  # NOQA: F811
    # ToDo: Create plan when API exists for it here
    plan_id = int(os.environ['PADDLE_TEST_DEFAULT_PLAN_ID'])
    plan = paddle_client.get_plan(plan=plan_id)
    assert plan['id'] == plan_id
    assert isinstance(plan['billing_period'], int)
    assert isinstance(plan['billing_type'], str)
    assert isinstance(plan['initial_price'], dict)
    assert isinstance(plan['name'], str)
    assert isinstance(plan['recurring_price'], dict)
    assert isinstance(plan['trial_days'], int)


@pytest.mark.manual_cleanup
def test_create_plan(paddle_client):  # NOQA: F811
    now = datetime.now().isoformat()
    plan_name = 'paddle-python-test_create_plan {0}'.format(now)
    plan_trial_days = 999
    plan_length = 999
    plan_type = 'year'
    main_currency_code = 'USD'
    initial_price_usd = 0.0
    initial_price_gbp = 0.0
    initial_price_eur = 0.0
    recurring_price_usd = 0.0
    recurring_price_gbp = 0.0
    recurring_price_eur = 0.0
    response = paddle_client.create_plan(
        plan_name=plan_name,
        plan_trial_days=plan_trial_days,
        plan_length=plan_length,
        plan_type=plan_type,
        main_currency_code=main_currency_code,
        initial_price_usd=initial_price_usd,
        initial_price_gbp=initial_price_gbp,
        initial_price_eur=initial_price_eur,
        recurring_price_usd=recurring_price_usd,
        recurring_price_gbp=recurring_price_gbp,
        recurring_price_eur=recurring_price_eur,
    )
    assert isinstance(response['product_id'], int)
    plan_id = response['product_id']

    plan_list = paddle_client.list_plans(plan=plan_id)
    plan = plan_list[0]
    assert plan['name'] == plan_name
    assert plan['trial_days'] == plan_trial_days
    assert plan['billing_period'] == plan_length
    assert plan['billing_type'] == plan_type

    assert plan['initial_price'] == {
        'USD': '%.2f' % round(initial_price_usd, 2),
        'GBP': '%.2f' % round(initial_price_gbp, 2),
        'EUR': '%.2f' % round(initial_price_eur, 2),
    }
    assert plan['recurring_price'] == {
        'USD': '%.2f' % round(recurring_price_usd, 2),
        'GBP': '%.2f' % round(recurring_price_gbp, 2),
        'EUR': '%.2f' % round(recurring_price_eur, 2),
    }


def test_create_plan_mock(mocker, paddle_client):  # NOQA: F811
    request = mocker.patch('paddle.paddle.requests.request')

    now = datetime.now().isoformat()
    plan_name = 'paddle-python-test_create_plan {0}'.format(now)
    plan_trial_days = 999
    plan_length = 999
    plan_type = 'year'
    main_currency_code = 'USD'
    initial_price_usd = 0.0
    initial_price_gbp = 0.0
    initial_price_eur = 0.0
    recurring_price_usd = 0.0
    recurring_price_gbp = 0.0
    recurring_price_eur = 0.0

    json = {
        'plan_name': plan_name,
        'plan_trial_days': plan_trial_days,
        'plan_length': plan_length,
        'plan_type': plan_type,
        'main_currency_code': main_currency_code,
        'initial_price_usd': initial_price_usd,
        'initial_price_gbp': initial_price_gbp,
        'initial_price_eur': initial_price_eur,
        'recurring_price_usd': recurring_price_usd,
        'recurring_price_gbp': recurring_price_gbp,
        'recurring_price_eur': recurring_price_eur,
        'vendor_id': int(os.environ['PADDLE_VENDOR_ID']),
        'vendor_auth_code': os.environ['PADDLE_API_KEY'],
    }
    url = 'https://vendors.paddle.com/api/2.0/subscription/plans_create'
    method = 'POST'

    paddle_client.create_plan(
        plan_name=plan_name,
        plan_trial_days=plan_trial_days,
        plan_length=plan_length,
        plan_type=plan_type,
        main_currency_code=main_currency_code,
        initial_price_usd=initial_price_usd,
        initial_price_gbp=initial_price_gbp,
        initial_price_eur=initial_price_eur,
        recurring_price_usd=recurring_price_usd,
        recurring_price_gbp=recurring_price_gbp,
        recurring_price_eur=recurring_price_eur,
    )
    request.assert_called_once_with(
        url=url,
        json=json,
        method=method,
    )
